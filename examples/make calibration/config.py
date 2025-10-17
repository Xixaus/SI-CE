"""
Configuration for Calibration Solution Preparation

This configuration file defines all parameters for automated preparation
of calibration solutions using the SI-CE system.
"""

from dataclasses import dataclass
import logging
from pathlib import Path


@dataclass
class CalibrationConfig:
    """Configuration for calibration solution preparation"""

    # ============================================================
    # EXCEL FILE CONFIGURATION
    # ============================================================
    excel_file_path: str = "calibration_example.xlsx"
    sheet_name: str = "Sheet1"

    # Column names in Excel file
    column_vial: str = "Vial"                    # Vial position number
    column_concentration: str = "Concentration"  # Target concentration
    column_volume: str = "Volume"                # Total volume (µL)

    # ============================================================
    # SOLUTION PREPARATION PARAMETERS
    # ============================================================
    # Standard solution parameters
    standard_concentration: float = 100.0        # Stock standard concentration (mg/L)
    standard_port: int = 7                       # Valve port for standard solution
    solvent_port: int = 3                        # Valve port for solvent (diluent)

    # Filling speeds (µL/min)
    standard_fill_speed: int = 2000              # Speed for standard solution
    solvent_fill_speed: int = 2000               # Speed for solvent

    # Transfer line parameters
    transfer_line_volume: int = 240              # Transfer line volume (µL)
    flush_needle_volume: int = 10                # Needle flush volume (µL)

    # ============================================================
    # CHEMSTATION PARAMETERS
    # ============================================================
    # Optional: Automatically run analysis after preparation
    run_analysis: bool = False                   # Run analysis after preparation?
    method_name: str = None                      # CE method name for analysis
    sample_name_column: str = None               # Column with sample names

    # ============================================================
    # SYSTEM INITIALIZATION
    # ============================================================
    perform_system_init: bool = True             # Initialize and clean system before start

    # ============================================================
    # VALIDATION OPTIONS
    # ============================================================
    validate_vials: bool = True                  # Validate vial numbers before preparation
    require_user_confirmation: bool = True       # Ask user to confirm before preparation

    # ============================================================
    # LOGGING CONFIGURATION
    # ============================================================
    log_file: str = "calibration_preparation.log"
    log_level: str = "INFO"                      # DEBUG, INFO, WARNING, ERROR
    log_format: str = "%(asctime)s - %(levelname)s - %(message)s"
    log_to_console: bool = True                  # Also print to console

    # ============================================================
    # DISPLAY OPTIONS
    # ============================================================
    show_progress_bars: bool = True              # Show tqdm progress bars
    show_calculation_table: bool = True          # Display volume calculation table
    verbose_output: bool = True                  # Detailed output messages

    # ============================================================
    # DEVICE CONFIGURATION (for main.py)
    # ============================================================
    syringe_port: str = "COM3"                   # Serial port for syringe pump
    syringe_size: int = 1000                     # Syringe volume (µL)
    valve_num_positions: int = 8                 # Number of valve positions


def setup_logging(config: CalibrationConfig) -> logging.Logger:
    """
    Set up logging according to configuration.

    Args:
        config: CalibrationConfig instance

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("CalibrationMaker")
    logger.setLevel(getattr(logging, config.log_level))

    # Clear existing handlers
    logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler(config.log_file, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(config.log_format))
    logger.addHandler(file_handler)

    # Console handler (if requested)
    if config.log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(config.log_format))
        logger.addHandler(console_handler)

    return logger


def validate_config(config: CalibrationConfig) -> None:
    """
    Validate configuration parameters.

    Args:
        config: CalibrationConfig instance

    Raises:
        ValueError: If configuration is invalid
    """
    # Check Excel file exists
    excel_path = Path(config.excel_file_path)
    if not excel_path.exists():
        raise FileNotFoundError(f"Excel file not found: {excel_path}")

    # Validate concentration
    if config.standard_concentration <= 0:
        raise ValueError("Standard concentration must be positive")

    # Validate ports
    if config.standard_port == config.solvent_port:
        raise ValueError("Standard and solvent ports must be different")

    if not (1 <= config.standard_port <= config.valve_num_positions):
        raise ValueError(f"Standard port must be between 1 and {config.valve_num_positions}")

    if not (1 <= config.solvent_port <= config.valve_num_positions):
        raise ValueError(f"Solvent port must be between 1 and {config.valve_num_positions}")

    # Validate speeds
    if config.default_fill_speed <= 0:
        raise ValueError("Fill speed must be positive")
