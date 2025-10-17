"""
Homogenization Time Study

Automated measurement of homogenization timing for CE sample preparation optimization.
Measures elapsed time from sample preparation to CE injection to determine optimal
homogenization protocols.

Usage:
    python homogenization_study.py
"""

import time
from datetime import datetime
from pathlib import Path
from tqdm import tqdm

from config import HomogenizationConfig, setup_logging


class HomogenizationStudy:
    """
    Automated homogenization timing study.

    This class manages the complete workflow for measuring homogenization timing:
    1. Prepare sample (MeOH + DI water)
    2. Homogenize at specific time points
    3. Run CE analysis
    4. Record timing data
    """

    def __init__(self, config: HomogenizationConfig, chemstation, sia_methods):
        """
        Initialize homogenization study.

        Args:
            config: HomogenizationConfig instance
            chemstation: ChemstationAPI instance
            sia_methods: PreparedSIMethods instance
        """
        self.config = config
        self.chemstation = chemstation
        self.sia = sia_methods

        # Set up logger
        self.logger = setup_logging(config)
        self.logger.info("=" * 70)
        self.logger.info("HOMOGENIZATION TIME STUDY - INITIALIZATION")
        self.logger.info("=" * 70)

        # Time tracking
        self.time_zero = None

        self.logger.info(f"✓ Configured for {config.num_repetitions} repetitions")
        self.logger.info(f"✓ Method: {config.method_name}")
        self.logger.info(f"✓ Vial: {config.vial_number}")

    def wait_for_status(self, target_status: str):
        """
        Wait until ChemStation reaches target status.

        Args:
            target_status: Target status string (e.g., "Run", "Idle")
        """
        while self.chemstation.system.RC_status() != target_status:
            time.sleep(2)

    def save_time_record(self, sample_name: str, elapsed_time: float):
        """
        Save timing record to output file.

        Args:
            sample_name: Name of the sample
            elapsed_time: Elapsed time in seconds
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = f"{timestamp}\t{sample_name}\t{elapsed_time:.2f}\n"

        with open(self.config.output_file, 'a', encoding='utf-8') as f:
            f.write(record)

        self.logger.info(f"📊 Timing recorded: {sample_name} = {elapsed_time:.2f}s")

    def prepare_sample(self):
        """
        Prepare sample: add MeOH, wait, add DI water, start timer.
        """
        self.logger.info("\n" + "=" * 70)
        self.logger.info(f"SAMPLE PREPARATION (Vial {self.config.vial_number})")
        self.logger.info("=" * 70)

        # Prepare batch flow
        self.logger.info("🔧 Preparing batch flow system...")
        self.sia.prepare_batch_flow(
            self.config.meoh_port,
            speed=self.config.meoh_speed
        )

        # Add MeOH
        self.logger.info(f"💧 Adding MeOH: {self.config.meoh_volume} µL @ {self.config.meoh_speed} µL/min")
        self.sia.batch_fill(
            self.config.vial_number,
            self.config.meoh_volume,
            self.config.meoh_port,
            speed=self.config.meoh_speed
        )

        # Wait after MeOH
        self.logger.info(f"⏳ Waiting {self.config.wait_after_meoh}s after MeOH...")
        for _ in tqdm(range(self.config.wait_after_meoh), desc="Wait after MeOH"):
            time.sleep(1)

        # Add DI water
        self.logger.info(f"💧 Adding DI water: {self.config.di_volume} µL @ {self.config.di_speed} µL/min")
        self.sia.batch_fill(
            self.config.vial_number,
            self.config.di_volume,
            self.config.di_port,
            speed=self.config.di_speed
        )

        # Start timer
        self.time_zero = time.time()
        self.logger.info("⏱️  Timer started (T=0)")

        # Prepare for homogenization
        self.logger.info("🔧 Preparing for homogenization...")
        self.sia.prepare_for_liquid_homogenization()
        self.logger.info("✓ Sample preparation complete")

    def homogenize_sample(self, sample_name: str):
        """
        Homogenize sample using liquid mixing.

        Args:
            sample_name: Name of the sample
        """
        elapsed = time.time() - self.time_zero if self.time_zero else 0

        self.logger.info(f"\n🌀 Homogenizing: {sample_name} (T={elapsed:.1f}s)")
        self.logger.info(f"   Volume: {self.config.homog_volume} µL")
        self.logger.info(f"   Cycles: {self.config.homog_cycles}")
        self.logger.info(f"   Speed: {self.config.homog_speed} µL/min")

        self.sia.homogenize_by_liquid_mixing(
            self.config.vial_number,
            volume_aspirate=self.config.homog_volume,
            num_cycles=self.config.homog_cycles,
            aspirate_speed=self.config.homog_speed,
            dispense_speed=self.config.homog_speed,
            clean_after=False
        )

        self.logger.info("✓ Homogenization complete")

    def run_analysis(self, sample_name: str):
        """
        Run CE analysis and record timing.

        Args:
            sample_name: Name of the sample
        """
        self.logger.info(f"\n📊 Starting analysis: {sample_name}")

        # Wait for ready
        self.chemstation.system.ready_to_start_analysis()

        # Start method
        if self.config.comment_file:
            self.chemstation.method.execution_method_with_parameters(
                self.config.vial_number,
                self.config.method_name,
                sample_name,
                comment=self.config.comment_file
            )
        else:
            self.chemstation.method.execution_method_with_parameters(
                self.config.vial_number,
                self.config.method_name,
                sample_name
            )

        time.sleep(5)

        # Wait for injection
        self.logger.info("⏳ Waiting for injection...")
        self.wait_for_status("Injecting")

        # Record timing
        if self.time_zero:
            elapsed = time.time() - self.time_zero
            self.save_time_record(sample_name, elapsed)

        # Wait for run
        self.wait_for_status("Run")
        self.logger.info("✓ Analysis running")

        # Calculate wait time before next homogenization
        analysis_time = self.chemstation.system.get_analysis_time()
        wait_time = max(0, (analysis_time - self.config.homog_before_analysis_end) * 60)

        if wait_time > 0:
            self.logger.info(f"⏳ Waiting {wait_time:.0f}s (next homogenization {self.config.homog_before_analysis_end} min before end)")
            time.sleep(wait_time)

    def run_time_study(self):
        """
        Run the complete time elution experiment.
        """
        self.logger.info("\n" + "=" * 70)
        self.logger.info("STARTING TIME ELUTION STUDY")
        self.logger.info("=" * 70)
        self.logger.info(f"Repetitions: {self.config.num_repetitions}")
        self.logger.info(f"Vial: {self.config.vial_number}")
        self.logger.info(f"Method: {self.config.method_name}")

        # Validate method
        self.chemstation.validation.validate_method(self.config.method_name)
        self.logger.info("✓ Method validated")

        # Prepare sample once
        self.prepare_sample()

        # Run repetitions
        for i in tqdm(range(self.config.num_repetitions), desc="Time study progress"):
            # Generate sample name
            sample_number = self.config.sample_start_number + i

            if "{i}" in self.config.sample_name_template:
                sample_name = self.config.sample_name_template.format(i=sample_number)
            else:
                sample_name = f"{self.config.sample_name_prefix}{sample_number}{self.config.sample_name_suffix}"

            self.logger.info(f"\n{'─' * 70}")
            self.logger.info(f"MEASUREMENT {i+1}/{self.config.num_repetitions}")
            self.logger.info(f"Sample: {sample_name}")
            self.logger.info(f"{'─' * 70}")

            # Homogenize and analyze
            self.homogenize_sample(sample_name)
            self.run_analysis(sample_name)

        self.logger.info("\n" + "=" * 70)
        self.logger.info("✅ TIME STUDY COMPLETED")
        self.logger.info("=" * 70)
        self.logger.info(f"Results saved to: {self.config.output_file}")

    def run_standards(self, count: int = 2):
        """
        Run standard measurements.

        Args:
            count: Number of standards to measure
        """
        self.logger.info("\n" + "=" * 70)
        self.logger.info("RUNNING STANDARDS")
        self.logger.info("=" * 70)

        for i in range(count):
            self.wait_for_status("Idle")

            # Standard name
            standard_name = f"{self.config.standard_name}_{i+1}" if count > 1 else self.config.standard_name

            self.logger.info(f"\n📊 Running standard {i+1}/{count}: {standard_name}")

            if self.config.comment_file:
                self.chemstation.method.execution_method_with_parameters(
                    self.config.standard_vial,
                    self.config.method_name,
                    standard_name,
                    comment=self.config.comment_file
                )
            else:
                self.chemstation.method.execution_method_with_parameters(
                    self.config.standard_vial,
                    self.config.method_name,
                    standard_name
                )

            self.logger.info(f"✓ Standard {i+1}/{count} started")

        self.logger.info("\n✓ All standards completed")


def main():
    """
    Main function to run homogenization study.
    """
    # Load configuration
    config = HomogenizationConfig()

    # Set up logger
    logger = setup_logging(config)
    logger.info("=" * 70)
    logger.info("🚀 HOMOGENIZATION STUDY - START")
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
        logger.info(f"\n🔧 Initializing SIA devices (port: {config.sia_port})...")
        syringe = SyringeController(
            port=config.sia_port,
            syringe_size=config.syringe_size,
            print_info=config.verbose
        )
        valve = ValveSelector(
            port=config.sia_port,
            num_positions=config.valve_positions
        )

        sia_methods = PreparedSIMethods(
            chemstation_controller=chemstation,
            syringe_device=syringe,
            valve_device=valve
        )
        logger.info("✓ SIA devices initialized")

        # Create study instance
        logger.info("\n📊 Creating HomogenizationStudy instance...")
        study = HomogenizationStudy(config, chemstation, sia_methods)

        # Run time study
        study.run_time_study()

        # Optional: Run standards (uncomment to enable)
        # study.run_standards(count=2)

        logger.info("\n" + "=" * 70)
        logger.info("✅ HOMOGENIZATION STUDY COMPLETED SUCCESSFULLY")
        logger.info("=" * 70)

    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
