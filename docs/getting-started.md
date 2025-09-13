# Getting Started with SIA-CE

This comprehensive guide will help you install the SIA-CE package and run your first automated Sequential Injection - Capillary Electrophoresis analysis.

## Prerequisites

Before installing SIA-CE, ensure your system meets these requirements:

### Software Requirements
- **Python 3.7 or higher** with pip package manager
- **Agilent ChemStation** software properly configured and licensed
- **VSCode** (recommended) - Provides enhanced code editing capabilities and debugging tools

### Hardware Requirements
- **Agilent CE7100** or another machine ovládaná chemstationem
- **SI components** (syringe pump, valve selector)
- **Serial communication ports** for device connectivity

---

## Installation Process

### Step 1: Download the SIA-CE Package

1. Navigate to: https://github.com/Xixaus/SIA-CE-code
2. Click "Code" → "Download ZIP"
3. Extract to your desired location (e.g., `C:\SIA-CE\`)
4. Open a terminal/command prompt in the extracted directory

### Step 2: Install the Package

The package includes all necessary dependencies. Install it using pip in development mode:

```bash
# Windows - using the provided batch file
install.bat

# Or manually with pip
python -m pip install -e .
```

!!! info "Development Mode Installation"
    The `-e` flag installs the package in "editable" mode, allowing you to modify the code without reinstalling. This is useful for customizing workflows or debugging.

The installation will automatically install all required dependencies:

- `pyserial` (≥3.5) - Serial communication with SI hardware
- `tqdm` (≥4.60.0) - Progress bars for long-running operations  
- `pandas` (≥1.2.0) - Data manipulation and analysis
- `pywin32` (≥300) - Windows-specific functionality (Windows only)

### Step 3: Install Jupyter notebook

For enhanced script development and testing:

Trochu více popsat, dát sem nějakou tabulku s tím co to je a v čem je to dobré, nějak to dát jako volitelný krok

```bash
# Jupyter for interactive development
python -m pip install jupyter notebook
```

### Step 4: Verify Installation

Test that the package is correctly installed:

```python
# Test import of main modules
import ChemstationAPI
import SIA_API

print("SIA-CE package successfully installed!")
```

---

## ChemStation Configuration

### Step 1: Locate Installation Directory

Find your SIA-CE installation path:

```python
import os
import ChemstationAPI

# Get the absolute path to the ChemstationAPI module
api_path = os.path.dirname(ChemstationAPI.__file__)
macro_path = os.path.join(api_path, "core", "ChemPyConnect.mac")
print(f"Macro location: {macro_path}")
```

### Step 2: Load the Communication Macro

1. **Open ChemStation** and ensure it's fully loaded
2. **Navigate to the command line interface**
3. **Execute the macro loading command** using the path from Step 1:

```chemstation
macro "C:\path\to\SIA-CE\ChemstationAPI\core\ChemPyConnect.mac"; Python_Run
```

!!! success "Successful Macro Loading"
    When the macro loads correctly, ChemStation will display:
    ```
    Start Python communication
    ```
    This confirms the communication bridge is active and ready.


### Step 3: Verify ChemStation Integration

Test the connection between Python and ChemStation:

```python
from ChemstationAPI.ChemstationAPI import ChemstationAPI

# Initialize ChemStation communication
chemstation = ChemstationAPI()

# Test basic communication
response = chemstation.send("response$ = _METHPATH$")
print(f"ChemStation method path: {response}")
print("ChemStation connection established successfully!")
```

!!! tip "Auto-Fix for Connection Errors"
    If initialization fails, the error message will show the EXACT macro command you need to run in ChemStation:
    ```
    ConnectionError: Failed to establish communication with ChemStation.
    Please ensure:
    1. ChemStation is running
    2. Communication macro is loaded: macro "C:\your\actual\path\ChemPyConnect.mac"; Python_Run
    ```
    Simply copy the macro command from the error message and paste it into ChemStation!

---

## SI system Configuration

### Step 1: Identify COM Ports

Discover available serial communication ports on your system:

```python
import serial.tools.list_ports

print("Available COM Ports:")
print("-" * 40)

ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"{port.device}: {port.description}")
    print(f"  Hardware ID: {port.hwid}")
    print()
```

Example output:
```
Available COM Ports:
----------------------------------------
COM3: USB Serial Device (COM3)
  Hardware ID: USB\VID_0403&PID_6001

COM4: Prolific USB-to-Serial Comm Port (COM4)  
  Hardware ID: USB\VID_067B&PID_2303
```

### Step 2: Configure Syringe Controller

Test and configure your syringe pump:

```python
from SIA_API.devices import SyringeController
import time

# Initialize syringe with appropriate parameters
syringe = SyringeController(
    port="COM3",           # Use your identified COM port
    syringe_size=1000,     # Syringe volume in microliters
    baudrate=9600          # Match your device settings
)

# Perform initialization sequence
syringe.initialization()  # Initialize syringe pump
print("Syringe controller ready!")

# Test basic functionality
syringe.print_volume_in_syringe()  # Display current volume status
```

### Step 3: Configure Valve Selector

Test and configure your valve selector:

```python
from SIA_API.devices import ValveSelector
import time

# Initialize valve selector
valve = ValveSelector(
    port="COM4",           # Use your identified COM port  
    num_positions=8,       # Number of valve positions
    baudrate=9600          # Match your device settings
)

# Test valve movement
print("Testing valve positions...")
for position in range(1, 4):  # Test first 3 positions
    valve.position(position)
    print(f"Moved to position {position}")
    time.sleep(1)  # Brief pause between movements

print("Valve selector configured successfully!")
```

---

## Verification and Testing

### Complete System Test

Run this comprehensive test to verify all components:

```python
import time
from ChemstationAPI.ChemstationAPI import ChemstationAPI
from SIA_API.devices import SyringeController, ValveSelector

def system_test():
    """Complete system functionality test"""
    
    print("=== SIA-CE System Test ===")
    
    # Test 1: ChemStation Communication
    print("\n1. Testing ChemStation communication...")
    try:
        chemstation = ChemstationAPI()
        response = chemstation.send("response$ = _METHPATH$")
        print(f"✓ ChemStation connected. Method path: {response}")
    except Exception as e:
        print(f"✗ ChemStation error: {e}")
        return False
    
    # Test 2: Syringe Controller
    print("\n2. Testing syringe controller...")
    try:
        syringe = SyringeController(port="COM3", syringe_size=1000)
        syringe.initialization()
        print("✓ Syringe controller ready")
    except Exception as e:
        print(f"✗ Syringe error: {e}")
        return False
    
    # Test 3: Valve Selector  
    print("\n3. Testing valve selector...")
    try:
        valve = ValveSelector(port="COM4", num_positions=8)
        valve.position(1)
        print("✓ Valve selector operational")
    except Exception as e:
        print(f"✗ Valve error: {e}")
        return False
    
    print("\n🎉 All systems operational!")
    return True

# Run the test
if __name__ == "__main__":
    system_test()
```