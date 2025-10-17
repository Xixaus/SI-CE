"""
Calibration Solution Maker

Automated preparation of calibration solutions using the SI-CE system.
This script reads calibration parameters from an Excel file and prepares
solutions with precise concentrations using volumetric dilution.

Usage:
    python calibration_maker.py

Requirements:
    - Excel file with calibration data (see config.py for format)
    - ChemStation running with communication macro loaded
    - SIA hardware connected and configured
"""

import pandas as pd
import time
from pathlib import Path
from typing import Optional
from tqdm import tqdm
import logging

from config import CalibrationConfig, setup_logging, validate_config


class CalibrationMaker:
    """
    Automated preparation of calibration solutions.

    This class manages the complete workflow for preparing calibration solutions:
    1. Load calibration data from Excel
    2. Calculate required volumes of standard and solvent
    3. Validate calculations and get user confirmation
    4. Prepare solutions using SIA system
    5. Optionally run analysis on ChemStation
    """

    def __init__(self, config: CalibrationConfig, chemstation, sia_methods):
        """
        Initialize CalibrationMaker.

        Args:
            config: CalibrationConfig instance with all parameters
            chemstation: ChemstationAPI instance
            sia_methods: PreparedSIMethods instance
        """
        self.config = config
        self.chemstation = chemstation
        self.sia_methods = sia_methods

        # Set up logger
        self.logger = setup_logging(config)
        self.logger.info("=" * 70)
        self.logger.info("CALIBRATION MAKER - INITIALIZATION")
        self.logger.info("=" * 70)

        # Validate configuration
        validate_config(config)
        self.logger.info("✓ Configuration validated")

        # Load data from Excel
        self.df = self._load_excel_data()

        # Validate DataFrame structure
        self._validate_dataframe()

        self.logger.info(f"✓ Loaded {len(self.df)} calibration points")
        self.logger.info(f"✓ Standard concentration: {config.standard_concentration} mg/L")
        self.logger.info(f"✓ Standard port: {config.standard_port}")
        self.logger.info(f"✓ Solvent port: {config.solvent_port}")

    def _load_excel_data(self) -> pd.DataFrame:
        """
        Load calibration data from Excel file.

        Returns:
            DataFrame with calibration data

        Raises:
            FileNotFoundError: If Excel file doesn't exist
            Exception: If file cannot be read
        """
        try:
            excel_path = Path(self.config.excel_file_path)
            if not excel_path.exists():
                raise FileNotFoundError(f"Excel file not found: {excel_path}")

            self.logger.info(f"📁 Loading data from: {excel_path}")

            # Read Excel file
            df = pd.read_excel(
                excel_path,
                sheet_name=self.config.sheet_name if hasattr(self.config, 'sheet_name') else 0
            )

            self.logger.info(f"✓ Loaded {len(df)} rows from Excel file")
            return df

        except Exception as e:
            self.logger.error(f"❌ Error loading Excel file: {e}")
            raise

    def _validate_dataframe(self):
        """
        Validate that DataFrame contains all required columns.

        Raises:
            ValueError: If required columns are missing
        """
        required_columns = [
            self.config.column_vial,
            self.config.column_concentration,
            self.config.column_volume
        ]

        missing_columns = [col for col in required_columns if col not in self.df.columns]

        if missing_columns:
            error_msg = f"Missing columns in Excel file: {missing_columns}"
            self.logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)

        if self.df.empty:
            raise ValueError("DataFrame with calibration data is empty")

        self.logger.info("✓ DataFrame validation successful - all required columns found")

    def validate_system(self):
        """
        Validate system and vials before preparation.

        Raises:
            ValidationError: If validation fails
        """
        self.logger.info("\n" + "=" * 70)
        self.logger.info("SYSTEM VALIDATION")
        self.logger.info("=" * 70)

        # Validate vial positions
        if self.config.validate_vials:
            self.logger.info("🔍 Validating vial positions...")
            vial_list = self.df[self.config.column_vial].tolist()
            self.chemstation.validation.list_vial_validation(vial_list)
            self.logger.info(f"✓ Vial positions validated: {vial_list}")

        self.logger.info("✓ System validation complete")

    def calculate_volumes(self) -> pd.DataFrame:
        """
        Calculate required volumes of standard and solvent for each calibration point.

        Uses dilution equation: C1*V1 = C2*V2
        Where:
            C1 = stock standard concentration
            V1 = volume of standard needed
            C2 = target concentration
            V2 = total volume

        Returns:
            DataFrame with added 'standard_volume' and 'solvent_volume' columns

        Raises:
            ValueError: If target concentration exceeds stock concentration
        """
        self.logger.info("\n" + "=" * 70)
        self.logger.info("VOLUME CALCULATION")
        self.logger.info("=" * 70)

        # Create copy for results
        results_df = self.df.copy()

        # Calculate volumes
        standard_volumes = []
        solvent_volumes = []

        for idx, row in self.df.iterrows():
            target_concentration = row[self.config.column_concentration]
            total_volume = row[self.config.column_volume]

            # Check if target concentration is valid
            if target_concentration > self.config.standard_concentration:
                raise ValueError(
                    f"Target concentration {target_concentration} exceeds "
                    f"stock concentration {self.config.standard_concentration}"
                )

            # Calculate standard volume: V1 = (C2 * V2) / C1
            if target_concentration == 0:
                standard_volume = 0
            else:
                standard_volume = (target_concentration * total_volume) / self.config.standard_concentration

            # Calculate solvent volume
            solvent_volume = total_volume - standard_volume

            # Validate volumes
            if standard_volume < 0 or solvent_volume < 0:
                raise ValueError(f"Calculated volumes are negative for vial {row[self.config.column_vial]}")

            standard_volumes.append(round(standard_volume, 1))
            solvent_volumes.append(round(solvent_volume, 1))

        # Add calculated volumes to DataFrame
        results_df['standard_volume'] = standard_volumes
        results_df['solvent_volume'] = solvent_volumes

        # Display calculation results
        if self.config.show_calculation_table:
            self.logger.info("\nCalculated volumes for calibration solutions:")
            print("\n" + "=" * 70)
            print("CALIBRATION SOLUTION VOLUMES")
            print("=" * 70)
            display_columns = [
                self.config.column_vial,
                self.config.column_concentration,
                self.config.column_volume,
                'standard_volume',
                'solvent_volume'
            ]
            print(results_df[display_columns].to_string(index=False))
            print("=" * 70 + "\n")

        self.logger.info(f"✓ Volume calculations completed for {len(results_df)} calibration points")

        return results_df

    def prepare_solutions(self, results_df: pd.DataFrame) -> None:
        """
        Prepare calibration solutions using SIA system.

        Args:
            results_df: DataFrame with calculated volumes

        Raises:
            Exception: If solution preparation fails
        """
        self.logger.info("\n" + "=" * 70)
        self.logger.info("SOLUTION PREPARATION")
        self.logger.info("=" * 70)

        # User confirmation
        if self.config.require_user_confirmation:
            response = input("\nProceed with calibration solution preparation? (y/n): ").lower().strip()
            if response not in ['y', 'yes', 'ano', 'a']:
                self.logger.info("❌ Calibration preparation cancelled by user")
                return

        self.logger.info("🚀 Starting calibration solution preparation...")

        # System initialization
        if self.config.perform_system_init:
            self.logger.info("\n🔧 Initializing SIA system...")
            self.sia_methods.system_initialization_and_cleaning()
            self.logger.info("✓ System initialized and cleaned")

        # Prepare batch flow
        self.logger.info("\n💧 Preparing batch flow system...")
        self.sia_methods.prepare_batch_flow(self.config.solvent_port)
        self.logger.info("✓ Batch flow prepared")

        # Prepare each calibration solution
        total_solutions = len(results_df)

        if self.config.show_progress_bars:
            iterator = tqdm(
                results_df.iterrows(),
                total=total_solutions,
                desc="Preparing calibration solutions",
                unit="solution"
            )
        else:
            iterator = results_df.iterrows()

        for idx, row in iterator:
            vial = int(row[self.config.column_vial])
            standard_vol = row['standard_volume']
            solvent_vol = row['solvent_volume']
            target_conc = row[self.config.column_concentration]

            # Get filling speeds from config
            standard_speed = self.config.standard_fill_speed
            solvent_speed = self.config.solvent_fill_speed

            # Log current preparation
            self.logger.info(
                f"\n{'─' * 70}\n"
                f"Preparing vial {vial} - Target: {target_conc} mg/L\n"
                f"  Standard: {standard_vol} µL @ {standard_speed} µL/min\n"
                f"  Solvent:  {solvent_vol} µL @ {solvent_speed} µL/min"
            )

            # Update progress bar postfix
            if self.config.show_progress_bars:
                iterator.set_postfix({
                    'Vial': vial,
                    'Conc': f"{target_conc}",
                    'Std': f"{standard_vol}µL",
                    'Solv': f"{solvent_vol}µL"
                })

            # Determine which solvents to use
            if standard_vol > 0 and solvent_vol > 0:
                # Both standard and solvent
                solvent_ports = [self.config.standard_port, self.config.solvent_port]
                volumes = [standard_vol, solvent_vol]
                speeds = [standard_speed, solvent_speed]
            elif standard_vol > 0:
                # Only standard (100% concentration)
                solvent_ports = [self.config.standard_port]
                volumes = [standard_vol]
                speeds = [standard_speed]
            else:
                # Only solvent (blank - zero concentration)
                solvent_ports = [self.config.solvent_port]
                volumes = [solvent_vol]
                speeds = [solvent_speed]

            # Prepare solution
            try:
                self.sia_methods.batch_fill_multiple_solvents(
                    vial=vial,
                    solvent_ports=solvent_ports,
                    volumes=volumes,
                    solvent_speeds=speeds,
                    transfer_line_volume=self.config.transfer_line_volume,
                    flush_needle=self.config.flush_needle_volume
                )

                self.logger.info(f"  ✓ Vial {vial} prepared successfully")

            except Exception as e:
                self.logger.error(f"  ❌ Error preparing vial {vial}: {e}")
                if self.config.show_progress_bars:
                    iterator.set_postfix({'Vial': vial, 'Status': 'ERROR'})
                raise

        self.logger.info("\n" + "=" * 70)
        self.logger.info(f"✅ ALL {total_solutions} CALIBRATION SOLUTIONS PREPARED SUCCESSFULLY")
        self.logger.info("=" * 70)

    def run(self) -> pd.DataFrame:
        """
        Main workflow: validate system, calculate volumes, and prepare solutions.

        Returns:
            DataFrame with all calculation results

        Raises:
            Exception: If any step fails
        """
        try:
            # Validate system and vials
            self.validate_system()

            # Calculate volumes
            results_df = self.calculate_volumes()

            # Prepare solutions
            self.prepare_solutions(results_df)

            return results_df

        except Exception as e:
            self.logger.error(f"❌ CRITICAL ERROR in calibration preparation: {e}", exc_info=True)
            raise


def main():
    """
    Main function to run calibration preparation.
    """
    # Load configuration
    config = CalibrationConfig()

    # Set up main logger
    logger = logging.getLogger("Main")
    logger.info("=" * 70)
    logger.info("🚀 CALIBRATION MAKER - START")
    logger.info("=" * 70)

    try:
        # Import required modules
        from ChemstationAPI import ChemstationAPI
        from SIA_API.methods import PreparedSIMethods
        from SIA_API.devices import SyringeController, ValveSelector

        # Initialize ChemStation
        logger.info("📡 Initializing ChemStation API...")
        chemstation = ChemstationAPI()
        logger.info("✓ ChemStation connected")

        # Initialize SIA devices
        logger.info("\n🔧 Initializing SIA devices...")
        logger.info(f"   Syringe port: {config.syringe_port}")
        logger.info(f"   Syringe size: {config.syringe_size} µL")
        logger.info(f"   Valve positions: {config.valve_num_positions}")

        syringe = SyringeController(
            port=config.syringe_port,
            syringe_size=config.syringe_size,
            print_info=False
        )
        valve = ValveSelector(
            port=config.syringe_port,
            num_positions=config.valve_num_positions
        )

        sia_methods = PreparedSIMethods(
            chemstation_controller=chemstation,
            syringe_device=syringe,
            valve_device=valve
        )
        logger.info("✓ SIA devices initialized")

        # Create and run calibration maker
        logger.info("\n📊 Creating CalibrationMaker instance...")
        maker = CalibrationMaker(config, chemstation, sia_methods)

        logger.info("\n🚀 Starting calibration preparation workflow...")
        results = maker.run()

        # Save results to Excel if needed
        output_file = Path(config.excel_file_path).parent / "calibration_results.xlsx"
        results.to_excel(output_file, index=False)
        logger.info(f"\n💾 Results saved to: {output_file}")

        logger.info("\n" + "=" * 70)
        logger.info("✅ CALIBRATION MAKER COMPLETED SUCCESSFULLY")
        logger.info("=" * 70)

    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
