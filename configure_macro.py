"""
Post-installation configuration script for ChemStation macro.

This script automatically configures the ChemPyConnect.mac file with the correct
installation path for communication files. It runs automatically after pip install,
but can also be run manually if needed.

Usage:
    python configure_macro.py
    or
    python -m configure_macro
"""

import os
import sys


def configure_chemstation_macro():
    """Update ChemPyConnect.mac with correct installation path."""
    try:
        # Find where ChemstationAPI is installed
        import ChemstationAPI
        package_dir = os.path.dirname(ChemstationAPI.__file__)
        macro_path = os.path.join(package_dir, 'core', 'ChemPyConnect.mac')
        comm_files_path = os.path.join(package_dir, 'core', 'communication_files')

        # Ensure communication_files directory exists
        os.makedirs(comm_files_path, exist_ok=True)

        # Read the macro file
        with open(macro_path, 'r') as f:
            lines = f.readlines()

        # Find and update the line containing MonitorFile with communication_files path
        updated = False
        for i, line in enumerate(lines):
            if 'MonitorFile' in line and 'communication_files' in line:
                # Replace the entire line with new path
                indent = '    '  # 4 spaces indentation
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
        print("The macro file cannot be modified (read-only).")
        print("\nSolutions:")
        print("1. Run this script as Administrator:")
        print("   Right-click Command Prompt -> 'Run as administrator'")
        print("   Then run: python configure_macro.py")
        print("\n2. Or install in editable mode (recommended for development):")
        print("   pip install -e . --config-settings editable_mode=strict")
        print("!"*60 + "\n")
        return False

    except ImportError:
        print("\n" + "!"*60)
        print("ERROR: ChemstationAPI not found!")
        print("!"*60)
        print("Please install the package first:")
        print("  pip install -e . --config-settings editable_mode=strict")
        print("or")
        print("  pip install https://github.com/Xixaus/SI-CE/archive/refs/heads/main.zip")
        print("!"*60 + "\n")
        return False

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = configure_chemstation_macro()
    sys.exit(0 if success else 1)
