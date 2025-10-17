import time
import pandas as pd
from pathlib import Path
from typing import Optional
from IPython.display import display
from tqdm import tqdm
import logging
from config import ProcessorConfig, setup_logging


class SampleProcessor:
    """Class for sample processing and analysis"""
    
    def __init__(self, config: ProcessorConfig, chemstation, sia_methods):
        """
        Initialize sample processor
        
        Args:
            config: Processor configuration
            chemstation: ChemStation API instance
            sia_methods: SIA methods instance
        """
        self.config = config
        self.chemstation = chemstation
        self.sia_methods = sia_methods
        
        # Set up logger
        self.logger = setup_logging(config)
        self.logger.info("="*60)
        self.logger.info("SAMPLE PROCESSOR INITIALIZATION")
        self.logger.info("="*60)
        
        # Load data from Excel
        self.df = self._load_excel_data()
        
        # Validate columns
        self._validate_dataframe()
        
        self.logger.info(f"✓ Loaded {len(self.df)} samples for processing")
        self.logger.info(f"✓ MeOH filling speed: {config.batch_fill_speed_meoh} µL/min")
        self.logger.info(f"✓ DI filling speed: {config.batch_fill_speed_di} µL/min")
        
    def _load_excel_data(self) -> pd.DataFrame:
        """Load data from Excel file"""
        try:
            excel_path = Path(self.config.excel_file_path)
            if not excel_path.exists():
                raise FileNotFoundError(f"Excel file not found: {excel_path}")
            
            self.logger.info(f"📁 Loading data from: {excel_path}")
            df = pd.read_excel(
                excel_path,
                #sheet_name=self.config.sheet_name
            )

            display(df)
            #input("OK?")

            self.logger.info(f"✓ Loaded {len(df)} rows from Excel file")
            return df
            
        except Exception as e:
            self.logger.error(f"❌ Error loading Excel file: {e}")
            raise
    
    def _validate_dataframe(self):
        """Validate that DataFrame contains all required columns"""
        required_columns = [
            self.config.column_vial,
            self.config.column_meoh,
            self.config.column_di,
            self.config.column_method,
            self.config.column_name
        ]
        
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        
        if missing_columns:
            error_msg = f"Missing columns in Excel file: {missing_columns}"
            self.logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)
        
        self.logger.info("✓ DataFrame validation successful - all required columns found")
        
    def wait_for_time(self, duration: float, description: str = "Waiting"):
        """
        Wait for specified duration in seconds with progress bar
        
        Args:
            duration: Wait duration in seconds
            description: Description for progress bar
        """
        if self.config.detailed_logging:
            self.logger.debug(f"⏱️ Waiting {duration:.1f} seconds: {description}")
        
        if self.config.show_progress_bars:
            for _ in tqdm(range(int(duration)), desc=description):
                time.sleep(1)
        else:
            time.sleep(duration)
    
    def prepare_initial_batch(self):
        """Prepare initial batch of samples (MeOH and DI) with individual incubation timing"""
        self.logger.info("="*60)
        self.logger.info(f"PREPARING FIRST {self.config.initial_batch_size} SAMPLES")
        self.logger.info("="*60)

        # Prepare batch flow
        self.logger.info("🔧 Preparing batch flow system")
        self.sia_methods.prepare_batch_flow(self.config.meoh_port)
        
        # Dictionary to store MeOH addition times for each sample
        meoh_addition_times = {}
        
        # Add MeOH to first samples
        self.logger.info(f"\n💧 FILLING MeOH - Port {self.config.meoh_port}, Speed: {self.config.batch_fill_speed_meoh} µL/min")
        self.logger.info("-"*40)

        for i in tqdm(range(self.config.initial_batch_size), desc="Filling MeOH"):
            sample = self.df.iloc[i]
            vial = sample[self.config.column_vial]
            meoh_volume = sample[self.config.column_meoh]
            
            self.logger.info(f"  → Vial {vial}: adding {meoh_volume} µL MeOH")
            
            
            self.sia_methods.batch_fill(
                vial, 
                meoh_volume, 
                self.config.meoh_port, 
                speed=self.config.batch_fill_speed_meoh
            )
            
            # Store the time when MeOH addition was completed
            meoh_addition_times[i] = time.time()

        self.logger.info(f"✓ MeOH added to all {self.config.initial_batch_size} vials")

        # Add DI to first samples with individual waiting
        self.logger.info(f"\n💧 FILLING DI WATER - Port {self.config.di_port}, Speed: {self.config.batch_fill_speed_di} µL/min")
        self.logger.info(f"   (with individual MeOH incubation: {self.config.waiting_time_after_meoh}s per sample)")
        self.logger.info("-"*40)

        for i in tqdm(range(self.config.initial_batch_size), desc="Filling DI water"):
            sample = self.df.iloc[i]
            vial = sample[self.config.column_vial]
            di_volume = sample[self.config.column_di]
            
            # Calculate how much time has elapsed since MeOH was added to this specific sample
            elapsed_time = time.time() - meoh_addition_times[i]
            remaining_wait_time = self.config.waiting_time_after_meoh - elapsed_time
            
            if remaining_wait_time > 0:
                self.logger.info(f"  → Vial {vial}: MeOH incubation time {self.config.waiting_time_after_meoh}s, elapsed {elapsed_time:.1f}s, remaining {remaining_wait_time:.1f}s")
                self.wait_for_time(remaining_wait_time, f"MeOH incubation for vial {vial} - {remaining_wait_time:.1f}s remaining")
            else:
                self.logger.info(f"  → Vial {vial}: MeOH incubation time {self.config.waiting_time_after_meoh}s already elapsed (total {elapsed_time:.1f}s)")

            self.logger.info(f"  → Vial {vial}: adding {di_volume} µL DI water")
            
            self.sia_methods.batch_fill(
                vial,
                di_volume,
                self.config.di_port,
                speed=self.config.batch_fill_speed_di
            )
        
        self.logger.info(f"✓ DI water added to all {self.config.initial_batch_size} vials")

        # Prepare for homogenization
        self.logger.info("\n🌀 HOMOGENIZATION OF FIRST SAMPLES")
        self.logger.info("-"*40)
        self.logger.info(f"Homogenization parameters:")
        self.logger.info(f"  - Volume: {self.config.homogenization_volume} µL")
        self.logger.info(f"  - Cycles: {self.config.homogenization_cycles}")
        self.logger.info(f"  - Aspirate speed: {self.config.homogenization_aspirate_speed} µL/min")
        self.logger.info(f"  - Dispense speed: {self.config.homogenization_dispense_speed} µL/min")
        
        self.sia_methods.prepare_for_liquid_homogenization()

        # Homogenize first batch
        for i in tqdm(range(self.config.initial_batch_size), desc="Homogenization"):
            sample = self.df.iloc[i]
            vial = sample[self.config.column_vial]
            name = sample[self.config.column_name]

            self.logger.info(f"  → Homogenizing vial {vial} ({name})")
            
            self.sia_methods.homogenize_by_liquid_mixing(
                vial,
                volume_aspirate=self.config.homogenization_volume,
                num_cycles=self.config.homogenization_cycles,
                dispense_speed=self.config.homogenization_dispense_speed,
                aspirate_speed=self.config.homogenization_aspirate_speed,
                clean_after=self.config.homogenization_clean_after
            )
        
        self.logger.info("✓ First sample preparation completed")
        self.logger.info("="*60)
    
    def wait_for_run(self):
        """Wait until ChemStation starts running"""
        self.logger.debug("⏳ Waiting for ChemStation analysis to start...")

        while self.chemstation.system.RC_status() != "Run":
            time.sleep(2)

        self.logger.debug("▶️ ChemStation analysis running")
    
    def prepare_next_sample(self, current_index: int) -> bool:
        """
        Prepare next sample if it exists
        
        Args:
            current_index: Current sample index
            
        Returns:
            True if next sample was prepared, False otherwise
        """
        next_index = current_index + self.config.initial_batch_size
        
        if next_index < len(self.df):
            next_sample = self.df.iloc[next_index]
            vial = next_sample[self.config.column_vial]
            meoh_volume = next_sample[self.config.column_meoh]
            di_volume = next_sample[self.config.column_di]
            name = next_sample[self.config.column_name]
            
            self.logger.info(f"\n🔄 PREPARING NEXT SAMPLE {next_index + 1}/{len(self.df)}")
            self.logger.info(f"   Vial: {vial}, Name: {name}")

            # Flush transfer line
            self.logger.debug("  🚿 Flushing transfer line")
            self.sia_methods.flush_transfer_line_to_waste()

            # Add MeOH
            self.logger.info(f"  💧 Filling MeOH: {meoh_volume} µL (speed: {self.config.batch_fill_speed_meoh} µL/min)")
            time_start_add_meoh = time.time()
            
            self.sia_methods.batch_fill(
                vial,
                meoh_volume,
                self.config.meoh_port,
                speed=self.config.batch_fill_speed_meoh
            )
            
            # Wait after adding MeOH
            time_wait = self.config.waiting_time_after_meoh - (time.time() - time_start_add_meoh)

            if time_wait > 0:
                self.logger.info(f"  ⏱️ MeOH incubation: {time_wait:.0f} seconds")
                self.wait_for_time(time_wait, f"MeOH incubation (vial {vial})")

            # Add DI
            self.logger.info(f"  💧 Filling DI water: {di_volume} µL (speed: {self.config.batch_fill_speed_di} µL/min)")
            self.sia_methods.batch_fill(
                vial,
                di_volume,
                self.config.di_port,
                speed=self.config.batch_fill_speed_di
            )
            
            # Prepare and homogenize
            self.logger.info(f"  🌀 Homogenizing sample")
            self.sia_methods.prepare_for_liquid_homogenization()

            self.sia_methods.homogenize_by_liquid_mixing(
                vial,
                volume_aspirate=self.config.homogenization_volume,
                num_cycles=self.config.homogenization_cycles,
                dispense_speed=self.config.homogenization_dispense_speed,
                aspirate_speed=self.config.homogenization_aspirate_speed,
                clean_after=self.config.homogenization_clean_after
            )

            self.logger.info(f"  ✓ Sample {next_index + 1} prepared")
            return True

        self.logger.debug("ℹ️ No more samples to prepare")
        return False
    
    def analyze_sample(self, sample_index: int):
        """
        Start sample analysis
        
        Args:
            sample_index: Sample index in DataFrame
        """
        sample = self.df.iloc[sample_index]
        vial = sample[self.config.column_vial]
        method = sample[self.config.column_method]
        name = sample[self.config.column_name]
        
        self.logger.info(f"\n📊 STARTING ANALYSIS")
        self.logger.info(f"   Name: '{name}'")
        self.logger.info(f"   Vial: {vial}")
        self.logger.info(f"   Method: {method}")
        
        self.chemstation.system.ready_to_start_analysis(
            verbose=self.config.verbose_chemstation
        )
        
        self.chemstation.method.execution_method_with_parameters(
            vial,
            method,
            name
        )
        
        self.wait_for_run()
        self.logger.info(f"   ▶️ Analysis of sample '{name}' running")
    
    def wait_for_next_homogenization(self):
        """Wait optimal time before homogenizing next sample"""
        remaining_time = self.chemstation.system.get_remaining_analysis_time()
        wait_time = (remaining_time - self.config.time_prepare_and_homogenization) * 60
        
        if wait_time > 0:
            self.logger.info(f"⏱️ Waiting {wait_time:.0f} seconds before preparing next sample")
            self.wait_for_time(wait_time, "Waiting for optimal homogenization time")
        else:
            self.logger.debug("ℹ️ No wait needed - preparing next sample immediately")
    
    def process_all_samples(self):
        """Main method for processing all samples"""
        self.logger.info("="*70)
        self.logger.info("🚀 STARTING PROCESSING OF ALL SAMPLES")
        self.logger.info(f"   Total number of samples: {len(self.df)}")
        self.logger.info(f"   MeOH incubation time: {self.config.waiting_time_after_meoh/60:.1f} minutes")
        self.logger.info(f"   Initial batch size: {self.config.initial_batch_size}")
        self.logger.info("="*70)
        
        try:
            # Validation and preparation
            self.logger.info("\n📋 SYSTEM VALIDATION AND PREPARATION")
            self.logger.info("-"*40)

            self.logger.info("  🔍 Validating method and vials...")
            self.chemstation.validation.validate_method(
                self.config.default_method_name,
                check_vials=True
            )

            self.chemstation.method.load(self.config.default_method_name)

            # Get vial list for validation
            vial_list = self.df[self.config.column_vial].tolist()
            self.chemstation.validation.list_vial_validation(vial_list)

            self.chemstation.system.ready_to_start_analysis(
                timeout=self.config.ready_timeout,
                verbose=self.config.verbose_chemstation
            )

            self.logger.info("  🔧 Initializing SI system...")
            self.sia_methods.system_initialization_and_cleaning()
            self.logger.info("  ✓ System ready")

            # Prepare initial batch (if needed)
            self.prepare_initial_batch()
            
            # Process all samples
            total_samples = len(self.df)
            
            for index in range(total_samples):
                sample = self.df.iloc[index]
                vial = sample[self.config.column_vial]
                name = sample[self.config.column_name]
                
                self.logger.info(f"\n{'='*60}")
                self.logger.info(f"📌 PROCESSING SAMPLE {index + 1}/{total_samples}")
                self.logger.info(f"   Name: {name}")
                self.logger.info(f"   Vial: {vial}")
                self.logger.info(f"{'='*60}")

                # Homogenize before analysis
                self.logger.info(f"\n🌀 HOMOGENIZATION BEFORE ANALYSIS")
                self.logger.info(f"   Vial {vial}: {self.config.homogenization_cycles} cycles")
                self.logger.info(f"   Volume: {self.config.homogenization_volume} µL")
                
                self.sia_methods.homogenize_by_liquid_mixing(
                    vial,
                    volume_aspirate=self.config.homogenization_volume,
                    num_cycles=self.config.homogenization_cycles,
                    dispense_speed=self.config.homogenization_dispense_speed,
                    aspirate_speed=self.config.homogenization_aspirate_speed,
                    clean_after=self.config.homogenization_clean_after
                )
                
                self.logger.info(f"   ✓ Homogenization completed")

                # Analyze current sample
                self.analyze_sample(index)

                # Prepare next sample during analysis
                if index < total_samples - 1:
                    has_next = self.prepare_next_sample(index)
                    if has_next:
                        self.logger.info(f"   ✓ Next sample prepared during analysis")
                
                # Wait for optimal time
                if index < total_samples - 1:
                    self.wait_for_next_homogenization()
            
            self.logger.info("\n" + "="*70)
            self.logger.info("✅ ALL SAMPLES SUCCESSFULLY PROCESSED")
            self.logger.info(f"   Samples processed: {total_samples}")
            self.logger.info(f"   Completion time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            self.logger.info("="*70)

        except Exception as e:
            self.logger.error(f"❌ CRITICAL ERROR during sample processing: {e}", exc_info=True)
            raise

# Main function
def main(config_file: str = None):
    """
    Main function to run the process
    
    Args:
        config_file: Path to configuration file (optional)
    """
    # Load configuration
    if config_file:
        # Configuration could be loaded from JSON/YAML file here
        pass
    else:
        config = ProcessorConfig()
    
    # Set up logger for main
    logger = logging.getLogger("Main")
    logger.info("="*60)
    logger.info("🚀 STARTING MAIN PROGRAM")
    logger.info("="*60)
    
    try:
        # Import required modules (assuming they are available)
        from ChemstationAPI import ChemstationAPI
        from SIA_API.methods import PreparedSIMethods
        from SIA_API.devices import SyringeController, ValveSelector
        
        # Initialize devices
        logger.info("📡 Initializing ChemStation API")
        chemstation = ChemstationAPI()

        logger.info("🔧 Initializing SIA devices")
        logger.info(f"   Port: COM8")
        logger.info(f"   Syringe size: 1000 µL")
        logger.info(f"   Valve positions: 8")
        
        syringe = SyringeController(port="COM8", syringe_size=1000, print_info=False)
        valve = ValveSelector(port="COM8", num_positions=8)
        
        sia_methods = PreparedSIMethods(
            chemstation_controller=chemstation,
            syringe_device=syringe,
            valve_device=valve
        )
        
        # Create and run processor
        processor = SampleProcessor(config, chemstation, sia_methods)
        processor.process_all_samples()
        
        logger.info("\n" + "="*60)
        logger.info("✅ PROGRAM COMPLETED SUCCESSFULLY")
        logger.info("="*60)

    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR in main program: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()