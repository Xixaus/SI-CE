"""
Configuration for Homogenization Time Study

This configuration file defines all parameters for automated homogenization
timing experiments with the SI-CE system.
"""

from dataclasses import dataclass
from typing import Optional
import logging


@dataclass
class HomogenizationConfig:
    """Configuration for homogenization time study"""

    # ============================================================
    # SIA HARDWARE CONFIGURATION
    # ============================================================
    sia_port: str = "COM7"
    syringe_size: int = 1000  # µL
    valve_positions: int = 8

    # ============================================================
    # VALVE PORTS
    # ============================================================
    meoh_port: int = 5      # Methanol port
    di_port: int = 3        # Deionized water port

    # ============================================================
    # VOLUMES (µL)
    # ============================================================
    meoh_volume: int = 400          # MeOH volume
    di_volume: int = 100            # DI water volume
    homog_volume: int = 290         # Homogenization aspirate volume

    # ============================================================
    # FILLING SPEEDS (µL/min)
    # ============================================================
    meoh_speed: int = 1000          # MeOH filling speed
    di_speed: int = 1200            # DI water filling speed
    homog_speed: int = 1000         # Homogenization speed

    # ============================================================
    # HOMOGENIZATION PARAMETERS
    # ============================================================
    homog_cycles: int = 2           # Number of mixing cycles

    # ============================================================
    # TIMING PARAMETERS (seconds unless noted)
    # ============================================================
    wait_after_meoh: int = 400      # Wait time after MeOH addition (seconds)
    homog_before_analysis_end: float = 2.0  # When to start next homogenization (minutes before analysis end)

    # ============================================================
    # CHEMSTATION PARAMETERS
    # ============================================================
    method_name: str = "Wait"       # CE method name
    vial_number: int = 10           # Vial position for sample

    # ============================================================
    # EXPERIMENT PARAMETERS
    # ============================================================
    num_repetitions: int = 3        # Number of measurements
    sample_start_number: int = 1    # Starting sample number

    # Sample naming
    sample_name_template: str = "{i}_homogenization_test"  # {i} = sample number
    sample_name_prefix: str = ""    # Prefix before number
    sample_name_suffix: str = "_B"  # Suffix after name

    # Standards naming
    standard_vial: int = 11         # Vial position for standards
    standard_name: str = "STD"      # Standard name prefix

    # ============================================================
    # OUTPUT CONFIGURATION
    # ============================================================
    output_file: str = "time_elution.txt"  # Output file for timing data

    # ============================================================
    # LOGGING CONFIGURATION
    # ============================================================
    log_file: str = "homogenization_study.log"
    log_level: str = "INFO"         # DEBUG, INFO, WARNING, ERROR
    log_to_console: bool = True     # Print to console
    verbose: bool = False           # Verbose device output

    # ============================================================
    # OPTIONAL PARAMETERS
    # ============================================================
    comment_file: Optional[str] = None  # Path to comment file (.txt, UTF-8)


def setup_logging(config: HomogenizationConfig) -> logging.Logger:
    """
    Set up logging according to configuration.

    Args:
        config: HomogenizationConfig instance

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("HomogenizationStudy")
    logger.setLevel(getattr(logging, config.log_level))

    # Clear existing handlers
    logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler(config.log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(file_handler)

    # Console handler (if requested)
    if config.log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(console_handler)

    return logger
