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

Choose one of the following installation methods based on your needs:

### Method 1: Direct Installation from GitHub (Recommended)

This is the simplest method - install directly from GitHub with a single command:

```batch
pip install https://github.com/Xixaus/SI-CE/archive/refs/heads/main.zip
```

This command will:

- Download the latest version from GitHub
- Install all required dependencies (`pyserial`, `tqdm`, `pandas`, `pywin32`)
- Make the package available in your Python environment

!!! success "Quick Installation"
    This is the fastest way to get started. Open Command Prompt and run the command above.
    Everything will be installed automatically.

!!! tip "Using Specific Python Version"
    If you have multiple Python versions, use the full path to pip:
    ```batch
    C:\Python311\python.exe -m pip install https://github.com/Xixaus/SI-CE/archive/refs/heads/main.zip
    ```

---

### Method 2: Development Installation

Use this method if you want to:

- Modify the source code
- Contribute to the project
- Test your own changes

#### Step 1: Download the Package

1. **Download** the ZIP file from GitHub: [Download SI-CE](https://github.com/Xixaus/SI-CE/archive/refs/heads/main.zip)
2. The file will be named something like `SI-CE-main.zip`

#### Step 2: Extract and Navigate

1. **Extract the ZIP file** to a location of your choice (e.g., `C:\SI-CE\`)
2. **Open Command Prompt** in that folder:
   - Navigate to the folder in File Explorer
   - Hold **Shift** and **right-click** in empty space
   - Select **"Open PowerShell window here"** or **"Open command window here"**

!!! tip "Choosing Installation Location"
    Choose a simple path without spaces, like `C:\SI-CE\` or `D:\Programs\SI-CE\`.
    Avoid paths with special characters or spaces (like "Program Files").

#### Step 3: Install in Editable Mode

Run this command in the SI-CE folder:

```batch
pip install -e . --config-settings editable_mode=strict
```

The `-e` flag means **editable mode**. This allows you to:

- Modify the source code directly
- See changes immediately without reinstalling
- Keep the package installed while developing

The `--config-settings editable_mode=strict` ensures proper integration with development tools.

!!! example "Installing from a specific path"
    If you're not in the SI-CE folder, you can specify the full path:
    ```batch
    pip install -e C:\SI-CE\SI-CE-main --config-settings editable_mode=strict
    ```
    Replace `C:\SI-CE\SI-CE-main` with the actual path where you extracted the package.

!!! tip "Using Specific Python"
    If you have multiple Python versions, specify which one to use:
    ```batch
    C:\Python311\python.exe -m pip install -e . --config-settings editable_mode=strict
    ```

!!! warning "Important: Keep the Folder in Place"
    **The folder where you extract and install the package must remain in that location.**

    If you move the folder after installation, the package will stop working and you'll need to reinstall it. Choose your installation location carefully!

---

### Verify Installation

After installation (either method), verify it worked:

```batch
python -c "import ChemstationAPI; import SIA_API; print('Installation successful!')"
```

If you see `Installation successful!`, you're ready to go!

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

Before you can control ChemStation from Python, you need to load a special communication macro that allows Python and ChemStation to talk to each other.

!!! info "Automatic Configuration"
    The macro is automatically configured during installation. If the automatic configuration failed, you can manually configure it - see the troubleshooting section below.

### Step 1: Get the Macro Command

The easiest way to get the correct command is to run:

```batch
python -c "from ChemstationAPI import get_macro_path; print(f'macro \"{get_macro_path()}\"; Python_Run')"
```

This will output the complete command ready to paste into ChemStation, for example:

```
macro "C:\Python311\Lib\site-packages\ChemstationAPI\core\ChemPyConnect.mac"; Python_Run
```

**Copy this entire line** - you'll need it in the next step.

!!! note "Using Specific Python"
    If you installed with a specific Python version, use it:
    ```batch
    C:\Python311\python.exe -c "from ChemstationAPI import get_macro_path; print(f'macro \"{get_macro_path()}\"; Python_Run')"
    ```

### Step 2: Load the Macro in ChemStation

1. **Start ChemStation** on your instrument computer and wait for it to fully load
2. **Find the command line** at the bottom of the ChemStation window
3. **Paste the command** from Step 1
4. **Press Enter**

**Expected output:** You should see `Start Python communication` in the ChemStation message area.

!!! success "Communication Established"
    If you see "Start Python communication", the connection is working!
    ChemStation is now ready to receive commands from Python.

!!! tip "Automatic Loading"
    You need to run this macro command every time you start ChemStation.
    To make it automatic, you can add this command to your ChemStation startup macro.

### Troubleshooting: Manual Configuration

If you see errors about file paths or the macro cannot find communication files, run the manual configuration:

```batch
python -c "from ChemstationAPI import configure; configure()"
```

This will update the macro with the correct paths. You should see:

```
============================================================
ChemStation macro configured successfully!
============================================================
Macro location: C:\Python311\Lib\site-packages\ChemstationAPI\core\ChemPyConnect.mac
Communication files: C:\Python311\Lib\site-packages\ChemstationAPI\core\communication_files

To use in ChemStation, run:
macro "C:\Python311\Lib\site-packages\ChemstationAPI\core\ChemPyConnect.mac"; Python_Run
============================================================
```

!!! warning "Permission Errors"
    If you get a "Permission denied" error, run Command Prompt as Administrator:

    1. Right-click on Command Prompt
    2. Select "Run as administrator"
    3. Run the configure command again

---

## Hardware Setup

If you have SIA hardware (syringe pump and valve selector), you need to find out which COM ports they are connected to.

### Step 1: Identify COM Ports

**Option A: Using Python (Recommended)**

1. **Open Command Prompt**
2. **Run this command**:

```batch
python -c "import serial.tools.list_ports; [print(f'{p.device}: {p.description}') for p in serial.tools.list_ports.comports()]"
```

This will show you all connected serial devices, for example:

```
COM3: USB Serial Port (FTDI)
COM4: USB-SERIAL CH340
COM5: Communications Port
```

**Option B: Using Windows Device Manager**

1. Press `Windows + X` and select "Device Manager"
2. Expand "Ports (COM & LPT)"
3. Look for your devices and note their COM port numbers

**Typical device names:**

- Syringe pump: "USB Serial Port", "FTDI USB Serial Device"
- Valve selector: "USB-SERIAL CH340", "Prolific USB-to-Serial"

!!! tip "Write Down COM Ports"
    Note which device is on which COM port. For example:

    - Syringe pump: COM3
    - Valve selector: COM4

    You will need these numbers for your Python scripts.

### Step 2: Test Device Connection

After identifying COM ports, you can test if the devices respond correctly.

**Create a test file** (e.g., `test_hardware.py`) with this content:

```python
from SIA_API.devices import SyringeController, ValveSelector

# Replace COM ports with YOUR ports from Step 1
syringe = SyringeController(port="COM3", syringe_size=1000)  # Your syringe COM port
valve = ValveSelector(port="COM4", num_positions=8)          # Your valve COM port

# Test basic functionality
print("Initializing syringe...")
syringe.initialize()
print("✓ Syringe initialized")

print("Moving valve to position 1...")
valve.position(1)
print("✓ Valve positioned")

print("\n✓ Hardware configured successfully!")
```

**Run the test:**

```batch
python test_hardware.py
```

If you see all checkmarks (✓), your hardware is configured correctly!

---

## Complete System Test

Once you have everything set up (SI-CE installed, ChemStation macro loaded, hardware connected), you can run a full system test to verify everything works together.

**Create a test file** called `test_complete_system.py`:

```python
def validate_system():
    """Test all system components."""
    print("Testing complete SI-CE system...\n")

    try:
        # Test ChemStation connection
        print("[1/3] Testing ChemStation connection...")
        from ChemstationAPI import ChemstationAPI
        ce = ChemstationAPI()
        status = ce.system.status()
        print(f"    ✓ ChemStation connected: {status}")

        # Test SI devices
        print("\n[2/3] Testing SIA hardware...")
        from SIA_API.devices import SyringeController, ValveSelector

        # Replace with YOUR COM ports!
        syringe = SyringeController(port="COM3", syringe_size=1000)
        valve = ValveSelector(port="COM4", num_positions=8)

        syringe.initialize()
        print("    ✓ Syringe initialized")

        valve.position(1)
        print("    ✓ Valve positioned")

        print("\n[3/3] Final check...")
        print("    ✓ System validation complete - ready to use!")
        print("\n" + "="*50)
        print("SUCCESS! Your SI-CE system is fully operational!")
        print("="*50)
        return True

    except Exception as e:
        print(f"\n✗ Validation failed: {e}")
        print("\nPlease check:")
        print("- ChemStation is running with macro loaded")
        print("- COM ports are correct")
        print("- Hardware is powered and connected")
        return False

# Run validation
validate_system()
```

**Run the complete test:**

```batch
python test_complete_system.py
```

If all tests pass, you're ready to start using SI-CE for automated analysis!

---

## What's Next?

Now that your system is set up, you can:

1. **Explore Examples** - Check the `examples/` folder for real-world workflows
2. **Read the API Documentation** - Learn about available functions and modules
3. **Start Your First Automation** - Begin with simple tasks like vial loading or method execution

!!! success "Ready to Go!"
    Your SI-CE system is fully configured. Start with the examples to see how to combine ChemStation and SIA control for automated analysis workflows.

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

- Re-run `python install.py` to reinstall dependencies
- Check Python version: `python --version` (requires 3.7+)
- Make sure you're using the same Python you used for installation
- Restart your command prompt after installation

**"python" is not recognized:**

- Python is not installed or not in PATH
- Try using the full path: `C:\Python311\python.exe` instead of just `python`
- Verify Python installation: open Control Panel → Programs → check if Python is listed
