# SIA-CE Integration Package

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Automated Capillary Electrophoresis with Sequential Injection Analysis**

Complete Python interface for controlling Agilent ChemStation CE systems and Sequential Injection (SI) hardware, enabling fully automated analytical workflows with minimal manual intervention.

## 🔬 Overview

SIA-CE combines two powerful analytical techniques:

- **Capillary Electrophoresis (CE)**: High-resolution separation technique for analyzing charged molecules
- **Sequential Injection (SI)**: Automated sample preparation and liquid handling system

This integration provides:
- ✅ Fully automated sample preparation and analysis
- ✅ Reduced manual intervention and human error  
- ✅ Increased throughput and reproducibility
- ✅ Complex analytical workflows with minimal supervision

## 🚀 Key Features

### ChemStation API
- Direct control of Agilent ChemStation via Command Processor
- Comprehensive method and sequence management
- Real-time instrument status monitoring
- Automated vial handling and positioning
- File-based communication protocol for reliability

### SIA API  
- Precise syringe pump control (Hamilton MVP compatible)
- Multi-position valve automation (VICI compatible)
- Pre-built workflows for common operations
- Volume tracking and safety features
- Flexible port configuration and method development

### Integration Benefits
- Seamless coordination between sample preparation and analysis
- One unified Python interface for complete workflow control
- Parallel operations to reduce total analysis time
- Consistent and reproducible analytical procedures

## 🛠️ System Requirements

### Hardware
- **CE System**: Agilent 7100 Capillary Electrophoresis System (or compatible)
- **SI Components**: 
  - Syringe pump (Hamilton MVP series or compatible)
  - Multi-position valve selector (VICI/Valco or compatible)  
- **Computer**: Windows PC with available COM ports

### Software
- **OS**: Windows 7 or higher
- **ChemStation**: Agilent OpenLab ChemStation Edition (tested on C.01.07 SR2)
- **Python**: 3.7+ with pip package manager

## 📦 Installation

### Quick Install

1. **Clone or Download the Package**
   ```bash
   git clone https://github.com/Xixaus/SIA-CE-code.git
   cd SIA-CE-code
   ```

2. **Install Package**
   ```bash
   # Windows - using provided batch file
   install.bat
   
   # Or manually with pip
   python -m pip install -e .
   ```

3. **Verify Installation**
   ```python
   import ChemstationAPI
   import SIA_API
   print("✅ SIA-CE package successfully installed!")
   ```

### Dependencies
The following packages are automatically installed:
- `pyserial>=3.5` - Serial communication with SIA hardware
- `tqdm>=4.60.0` - Progress bars for long operations
- `pandas>=1.2.0` - Data manipulation and Excel integration
- `pywin32>=300` - Windows-specific functionality

## ⚙️ Setup

### 1. ChemStation Configuration

1. **Load Communication Macro** in ChemStation command line:
   ```chemstation
   macro "C:\path\to\SIA-CE\ChemstationAPI\core\ChemPyConnect.mac"; Python_Run
   ```

2. **Verify Connection**:
   ```python
   from ChemstationAPI import ChemstationAPI
   api = ChemstationAPI()
   print("ChemStation connected successfully!")
   ```

### 2. Hardware Configuration

**Identify COM Ports**:
```python
import serial.tools.list_ports

for port in serial.tools.list_ports.comports():
    print(f"{port.device}: {port.description}")
```

**Test SIA Devices**:
```python
from SIA_API.devices import SyringeController, ValveSelector

# Initialize and test
syringe = SyringeController(port="COM3", syringe_size=1000)
valve = ValveSelector(port="COM4", num_positions=8)

syringe.initialize()  # Home syringe
valve.position(1)     # Test valve movement
```

## 📁 Project Structure

```
SIA-CE/
├── ChemstationAPI/           # ChemStation control module
│   ├── controllers/          # CE, method, sequence controllers
│   ├── core/                 # Communication protocol
│   └── exceptions.py         # Error handling
├── SIA_API/                  # Sequential Injection module  
│   ├── devices/              # Syringe and valve controllers
│   ├── methods/              # High-level workflows
│   └── core/                 # Serial communication
├── examples/                 # Example applications
├── docs/                     # Documentation
└── tests/                    # Test suites
```

## 📚 Documentation

- **[Getting Started Guide](docs/getting-started.md)** - Installation and setup
- **[ChemStation API](docs/chemstation-api/introduction.md)** - CE instrument control
- **[SIA API](docs/sia-api/introduction.md)** - Sample preparation automation
- **[Tutorials](docs/tutorials/first-analysis.md)** - Step-by-step examples
- **[API Reference](docs/api-reference/)** - Complete function documentation

## 🎯 Use Cases

- **Routine Analysis**: Automate daily QC and sample testing
- **Method Development**: Systematic optimization studies
- **Research**: High-throughput analytical workflows
- **Validation**: Reproducible analytical procedures

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Xixaus/SIA-CE-code/issues)
- **Documentation**: [Project Documentation](docs/)
- **Contact**: Richard Maršala - risaniusl@gmail.com

## ⚠️ Important Notes

- **Development Status**: This project is actively developed and optimized for specific hardware configurations
- **Compatibility**: Tested with ChemStation C.01.07 SR2 [255] and Agilent 7100 CE
- **Safety**: Always follow proper laboratory safety procedures when working with automated systems
- **Validation**: Thoroughly test and validate all procedures before routine use
