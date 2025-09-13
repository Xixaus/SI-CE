# Getting Started with SIA-CE

This guide covers installation and initial system configuration.
## Prerequisites

### Required Hardware
- **Agilent CE7100** or compatible CE system controlled by ChemStation
- **SI Components**: Syringe pump (Cavro XCalibur) and valve selector (VICI)
- **Serial Ports**: COM ports for SI device communication

### Required Software  
- **ChemStation**: OpenLab CDS ChemStation version 
- **Python**: Version 3.7 or higher with pip

---

## Installation

### Step 1: Download and Install
1. Download package from the project repository
2. Extract to desired location (e.g., `C:\SIA-CE\`)
3. Install using pip:

```bash
# Navigate to extracted directory
cd C:\SIA-CE\

# Install package and dependencies
pip install -e .
```

This automatically installs required dependencies: `pyserial`, `tqdm`, `pandas`, and `pywin32`.

### Step 2: Verify Installation
```python
import ChemstationAPI
import SIA_API
print("Installation successful")
```

### Optional: Jupyter Notebook (Recommended for Development)

Jupyter notebooks provide interactive development environment with several advantages for analytical workflows:

| Feature | Benefit |
|---------|---------|
| **Cell-by-cell execution** | Test individual operations without running full scripts |
| **Variable inspection** | Monitor syringe volume, system status in real-time |
| **Result visualization** | Plot data directly in notebook |
| **Documentation** | Combine code, notes, and results in one document |
| **Reproducibility** | Save complete workflow with outputs |

```bash
pip install jupyter notebook
```

Launch with: `jupyter notebook` from your project directory.

---

## ChemStation Setup

### Load Communication Macro
1. **Start ChemStation** and wait for complete loading
2. **Find macro path** - run this Python code to get the exact path:

```python
import os
import ChemstationAPI
macro_path = os.path.join(os.path.dirname(ChemstationAPI.__file__), 
                          "core", "ChemPyConnect.mac")
print(f"Load this macro: {macro_path}")
```

3. **Load macro in ChemStation** - copy the path from above and run:
```chemstation
macro "C:\your\path\to\ChemPyConnect.mac"; Python_Run
```

**Expected output:** `Start Python communication`

### Verify Connection
```python
from ChemstationAPI import ChemstationAPI
ce = ChemstationAPI()
print("ChemStation connected:", ce.system.status())
```

---

## SI Hardware Setup

### Identify COM Ports
```python
import serial.tools.list_ports

for port in serial.tools.list_ports.comports():
    print(f"{port.device}: {port.description}")
```

### Configure Devices
```python
from SIA_API.devices import SyringeController, ValveSelector

# Initialize with your COM ports
syringe = SyringeController(port="COM3", syringe_size=1000)
valve = ValveSelector(port="COM4", num_positions=8)

# Test basic functionality
syringe.initialize()
valve.position(1)
print("SI hardware configured")
```

---

## System Validation

Run this comprehensive test to verify all components:

```python
def validate_system():
    """Test all system components."""
    
    try:
        # Test ChemStation
        from ChemstationAPI import ChemstationAPI
        ce = ChemstationAPI()
        print("✓ ChemStation connection")
        
        # Test SI devices  
        from SIA_API.devices import SyringeController, ValveSelector
        syringe = SyringeController(port="COM3", syringe_size=1000)
        valve = ValveSelector(port="COM4", num_positions=8)
        
        syringe.initialize()
        valve.position(1)
        print("✓ SI hardware ready")
        
        print("✓ System validation complete")
        return True
        
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return False

# Run validation
validate_system()
```

## Quick Troubleshooting

**ChemStation connection fails:**
- Verify ChemStation is running and method is loaded
- Check macro loading: the exact command is shown in error message

**SI device not found:**
- Check COM port in Device Manager
- Verify device power and cable connections

**Import errors:**
- Reinstall package: `pip install -e . --force-reinstall`
- Check Python version: `python --version` (needs 3.7+)
