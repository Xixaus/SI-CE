"""
ChemStation API - Unified interface for Agilent 7100 CE system control.

This package provides comprehensive control of Agilent ChemStation software
and CE instruments through file-based communication protocol.
"""

from .ChemstationAPI import ChemstationAPI
from .core.communication_config import CommunicationConfig
from .exceptions import (
    ChemstationError,
    CommunicationError,
    CommandError,
    FileOperationError,
    SequenceError,
    MethodError,
    VialError,
    ConfigurationError,
    ValidationError,
    TimeoutError
)

__version__ = "0.1.0"
__author__ = "Richard Maršala"
__email__ = "your.email@example.com"

__all__ = [
    # Main API
    'ChemstationAPI',
    'CommunicationConfig',

    # Exceptions
    'ChemstationError',
    'CommunicationError',
    'CommandError',
    'FileOperationError',
    'SequenceError',
    'MethodError',
    'VialError',
    'ConfigurationError',
    'ValidationError',
    'TimeoutError',

    # Configuration
    'configure',
    'get_macro_path',
]

# Convenience function for quick setup
def create_api(port=None, config=None):
    """
    Quick setup function for ChemStation API.

    Args:
        port: COM port for communication
        config: Optional CommunicationConfig instance

    Returns:
        Initialized ChemstationAPI instance
    """
    if config is None:
        config = CommunicationConfig()
    return ChemstationAPI(config)


def configure():
    """
    Configure ChemStation macro with correct installation paths.

    This function updates the ChemPyConnect.mac file to use the correct
    path for communication files based on where the package is installed.

    Run this after installation if the automatic configuration failed.

    Returns:
        bool: True if configuration successful, False otherwise

    Example:
        >>> from ChemstationAPI import configure
        >>> configure()
        ChemStation macro configured successfully!
    """
    import os

    try:
        package_dir = os.path.dirname(__file__)
        macro_path = os.path.join(package_dir, 'core', 'ChemPyConnect.mac')
        comm_files_path = os.path.join(package_dir, 'core', 'communication_files')

        # Ensure communication_files directory exists
        os.makedirs(comm_files_path, exist_ok=True)

        # Read the macro file
        with open(macro_path, 'r') as f:
            lines = f.readlines()

        # Find and update the line containing MonitorFile
        updated = False
        for i, line in enumerate(lines):
            if 'MonitorFile' in line and 'communication_files' in line:
                indent = '    '
                lines[i] = f'{indent}MonitorFile "{comm_files_path}"\n'
                updated = True
                break

        if not updated:
            print("Warning: Could not find MonitorFile line to update")
            return False

        # Write back to file
        with open(macro_path, 'w') as f:
            f.writelines(lines)

        print("\n" + "="*60)
        print("ChemStation macro configured successfully!")
        print("="*60)
        print(f"Macro location: {macro_path}")
        print(f"Communication files: {comm_files_path}")
        print("\nTo use in ChemStation, run:")
        print(f'macro "{macro_path}"; Python_Run')
        print("="*60 + "\n")

        return True

    except PermissionError:
        print("\n" + "!"*60)
        print("ERROR: Permission denied!")
        print("!"*60)
        print("Run Python as Administrator or install in editable mode:")
        print("  pip install -e . --config-settings editable_mode=strict")
        print("!"*60 + "\n")
        return False

    except Exception as e:
        print(f"\nError configuring macro: {e}")
        return False


def get_macro_path():
    """
    Get the full path to the ChemStation communication macro.

    Returns:
        str: Full path to ChemPyConnect.mac file

    Example:
        >>> from ChemstationAPI import get_macro_path
        >>> print(get_macro_path())
        C:\\Python311\\Lib\\site-packages\\ChemstationAPI\\core\\ChemPyConnect.mac
    """
    import os
    package_dir = os.path.dirname(__file__)
    return os.path.join(package_dir, 'core', 'ChemPyConnect.mac')