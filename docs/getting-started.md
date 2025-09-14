# Getting Started with SIA-CE

This guide covers installation and initial system configuration for automated capillary electrophoresis with sequential injection.

## Prerequisites

### Required Hardware
- **Agilent CE7100** or compatible CE system controlled by ChemStation
- **SI Components**: Syringe pump and valve selector with serial communication
- **Serial Ports**: Available COM ports for SI device communication

### Required Software  
- **ChemStation**: OpenLab CDS ChemStation (tested on version C.01.07 SR2)
- **Python**: Version 3.7 or higher

---

## Installation

### Download and Install
1. **Download** the package from the project repository ([download link](https://github.com/Xixaus/SI-CE/archive/refs/heads/main.zip))
2. **Extract** to desired location (e.g., `C:\SIA-CE\`)
3. **Install dependencies** by double-clicking `install.bat`

The install.bat file automatically runs:
```batch
python -m pip install -e .
```

This installs the package and all required dependencies: `pyserial`, `tqdm`, `pandas`, `pywin32`.

### Verify Installation
```python
import ChemstationAPI
import SIA_API
print("Installation successful")
```

---

## Recommended Development Tools

### Code Editor
**[Visual Studio Code](https://code.visualstudio.com/)** - Free, powerful editor with excellent Python support

- Built-in terminal and debugger
- Python extension for syntax highlighting and IntelliSense
- Integrated Git support for version control
- Extensions for Jupyter notebook support

### Interactive Development
**[Jupyter Notebook](https://jupyter.org/)** - Interactive development environment, ideal for analytical workflows

- **Cell-by-cell execution**: Test individual operations without running full scripts
- **Real-time monitoring**: Track syringe volume, system status, and analysis progress
- **Documentation**: Combine code, markdown notes, and results in one document
- **Reproducibility**: Save complete workflows with outputs for later reference

---

## ChemStation Setup

### Load Communication Macro
1. **Start ChemStation** and wait for complete loading
2. **Get macro path** - run this Python code to find the exact path:

```python
import os
import ChemstationAPI
macro_path = os.path.join(os.path.dirname(ChemstationAPI.__file__), 
                          "core", "ChemPyConnect.mac")
print(f"Load this macro: {macro_path}")
```

3. **Load macro in ChemStation** - copy the path from above and execute:
```chemstation
macro "C:\your\path\to\ChemPyConnect.mac"; Python_Run
```

**Expected output:** `Start Python communication`

---

## Hardware Setup

### Identify COM Ports
Before configuring devices, discover which COM ports are available:

```python
import serial.tools.list_ports

print("Available COM ports:")
for port in serial.tools.list_ports.comports():
    print(f"{port.device}: {port.description}")
```

**Typical device descriptions:**

- Syringe pump: "USB Serial Port", "FTDI USB Serial Device"
- Valve selector: "USB-SERIAL CH340", "Prolific USB-to-Serial"

### Configure Devices
```python
from SIA_API.devices import SyringeController, ValveSelector

# Replace COM ports with your actual ports from discovery above
syringe = SyringeController(port="COM3", syringe_size=1000)  # Your syringe port
valve = ValveSelector(port="COM4", num_positions=8)          # Your valve port

# Test basic functionality
syringe.initialize()
valve.position(1)
print("Hardware configured successfully")
```

---

## System Verification

### Complete System Test
Run this comprehensive validation to verify all components:

```python
def validate_system():
    """Test all system components."""
    
    try:
        # Test ChemStation connection
        from ChemstationAPI import ChemstationAPI
        ce = ChemstationAPI()
        status = ce.system.status()
        print(f"✓ ChemStation connected: {status}")
        
        # Test SI devices  
        from SIA_API.devices import SyringeController, ValveSelector
        syringe = SyringeController(port="COM3", syringe_size=1000)  # Use your port
        valve = ValveSelector(port="COM4", num_positions=8)          # Use your port
        
        syringe.initialize()
        print("✓ Syringe initialized")
        
        valve.position(1)
        print("✓ Valve positioned")
        
        print("✓ System validation complete - ready to use!")
        return True
        
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return False

# Run validation
validate_system()
```

---

## Quick Troubleshooting

**ChemStation connection fails:**

- Verify ChemStation is running and responsive
- Check macro loading: `macro "path\ChemPyConnect.mac"; Python_Run`
- Look for "Start Python communication" message

**SI device not found:**

- Check COM ports in Device Manager (Windows)
- Verify device power and USB cable connections
- Try different COM port numbers

**Import errors:**

- Re-run `install.bat` to reinstall dependencies
- Check Python version: `python --version` (requires 3.7+)
- Restart Python environment after installation