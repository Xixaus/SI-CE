# SI-CE Integration Package

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://xixaus.github.io/SI-CE/)

Python package for automated control of Agilent ChemStation CE systems integrated with Sequential Injection (SI) hardware. Enables complete laboratory automation from sample preparation to data acquisition.

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Key Features](#-key-features)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [Hardware Compatibility](#-hardware-compatibility)
- [Documentation](#-documentation)
- [License](#-license)

## 🔬 About the Project

SI-CE combines two powerful analytical techniques:

- **Capillary Electrophoresis (CE)**: High-resolution separation for analyzing charged molecules
- **Sequential Injection (SI)**: Automated sample preparation and liquid handling system

This integration provides:

- ✅ Fully automated sample preparation and analysis
- ✅ Reduced manual intervention and human error
- ✅ Increased throughput and reproducibility
- ✅ Complex analytical workflows with minimal supervision

### Development

The package was developed for OpenLab ChemStation ver. C.01.07 SR2 [255] with Agilent Technologies 7100 Capillary Electrophoresis system combined with sequential injection components.

**Author:** Richard Maršala
**Status:** Active development

## 🎯 Key Features

### ChemStation API

- 📡 Direct communication with Agilent ChemStation command processor
- 🧪 Automated vial handling for CE systems (load/unload, position tracking)
- 📋 Method and sequence management with parameter control
- 📊 Real-time instrument status monitoring and diagnostics
- ✔️ Data validation and result integrity checking

### SIA API

- 🔌 Serial communication with SI hardware (syringe pumps, valve selectors)
- ⚙️ Pre-configured workflows for sample preparation and mixing
- 🔄 Automated dilution, homogenization, and batch processing
- 🎛️ High-level methods for complex analytical procedures
- 📈 Real-time volume monitoring and system status

### System Integration

- ⚡ Parallel sample preparation during CE analysis
- 📊 Excel-based batch processing with individual sample timing
- 🤖 Automated method execution with custom parameters
- 🛡️ Comprehensive error handling and validation
- 📝 Logging of all operations and events

## 🚀 Quick Start

### Installation

#### Method 1: Direct Installation from GitHub (Recommended)

Install directly from the repository with a single command:

```bash
pip install https://github.com/Xixaus/SI-CE/archive/refs/heads/main.zip
```

This will automatically download and install the package with all dependencies.

#### Method 2: Development Installation

For development or if you want to modify the code:

1. **Download** the ZIP file from GitHub: [Download SI-CE](https://github.com/Xixaus/SI-CE/archive/refs/heads/main.zip)
2. **Extract** the ZIP file to your preferred location (e.g., `C:\SI-CE\`)
3. Open **Command Prompt** in the extracted folder and install:

   ```bash
   pip install -e . --config-settings editable_mode=strict
   ```

The `-e` flag installs the package in editable mode, meaning any changes you make to the source code will be immediately reflected without reinstalling. The `--config-settings editable_mode=strict` ensures proper integration with development tools.

**⚠️ Important:** The folder where you extract and install the package must remain in that location. If you move the folder after installation, the package will stop working and you'll need to reinstall it.

### ChemStation Setup

After installation, the macro is automatically configured. To get the correct command for your ChemStation:

```python
python -c "from ChemstationAPI import get_macro_path; print(f'macro \"{get_macro_path()}\"; Python_Run')"
```

This will output the command to paste into ChemStation's command line, for example:

```
macro "C:\Python311\Lib\site-packages\ChemstationAPI\core\ChemPyConnect.mac"; Python_Run
```

**Note:** If automatic configuration failed during installation, run:

```bash
python -c "from ChemstationAPI import configure; configure()"
```

Detailed instructions can be found in the [Getting Started documentation](https://xixaus.github.io/SI-CE/getting-started/).

### Basic Usage

This example demonstrates a complete automated workflow: initializing the SI-CE system, preparing a sample, and running a CE analysis.

```python
# Import packages
from ChemstationAPI import ChemstationAPI
from SIA_API.devices import SyringeController, ValveSelector
from SIA_API.methods import PreparedSIMethods

# Initialize systems
ce = ChemstationAPI()  # Connect to ChemStation
syringe = SyringeController(port="COM3", syringe_size=1000)  # Connect syringe pump
valve = ValveSelector(port="COM4", num_positions=8)  # Connect valve selector
workflow = PreparedSIMethods(ce, syringe, valve)  # Create automated workflow

# Automated sample preparation and analysis
workflow.system_initialization_and_cleaning()  # Initialize and clean the SI system
workflow.continuous_fill(vial=15, volume=1500, solvent_port=3)  # Prepare sample in vial 15
ce.method.execution_method_with_parameters(  # Run CE analysis
    vial=15,
    method_name="CE_Analysis",
    sample_name="Sample_001"
)
```

**What this does:**

1. Connects to ChemStation CE system and SI hardware (syringe pump, valve)
2. Initializes and cleans the Sequential Injection system
3. Automatically fills vial 15 with 1500 µL from solvent port 3
4. Runs CE method "CE_Analysis" on the prepared sample

## 💡 Usage Examples

### 1. Automated Batch Processing

Process multiple samples from Excel file with optimized timing:

```python
from examples.sample_processor import SampleProcessor

# Load configuration from Excel
processor = SampleProcessor(config, chemstation, sia_methods)

# Process all samples automatically
processor.process_all_samples()
```

**Example located in:** [`examples/sample processor/`](examples/sample%20processor/)

### 2. Homogenization Study

Automated optimization of mixing parameters:

```python
from examples.homogenization_study import run_time_elution_experiment

# Time-resolved homogenization analysis
run_time_elution_experiment(processor)
```

**Example located in:** [`examples/homogenization study/`](examples/homogenization%20study/)

### 3. Calibration Curve Generation

Automated calibration curve creation:

```python
from examples.make_calibration import CalibrationMaker

# Load calibration plan from Excel
calibration = CalibrationMaker("calibration_example.xlsx")
calibration.run_calibration()
```

**Example located in:** [`examples/make calibration/`](examples/make%20calibration/)

## 📁 Project Structure

```
SI-CE/
├── ChemstationAPI/              # ChemStation communication and control
│   ├── core/                    # File-based communication protocol
│   │   ├── chemstation_communication.py
│   │   ├── communication_config.py
│   │   └── ChemPyConnect.mac    # Communication macro
│   ├── controllers/             # CE modules
│   │   ├── ce_module.py         # Vial control
│   │   ├── methods_module.py    # Method management
│   │   ├── sequence_module.py   # Sequence management
│   │   ├── system_module.py     # System status
│   │   └── validation.py        # Data validation
│   ├── ChemstationAPI.py        # Main API class
│   └── exceptions.py            # Custom exceptions
│
├── SIA_API/                     # Sequential Injection automation
│   ├── core/                    # Core communication
│   │   └── command_sender.py    # Serial communication
│   ├── devices/                 # Hardware controllers
│   │   ├── syringe_controller.py
│   │   └── valve_selector.py
│   └── methods/                 # High-level workflows
│       ├── prepared_methods.py  # Pre-configured methods
│       └── config.py            # SI configuration
│
├── examples/                    # Example applications
│   ├── sample processor/        # Batch sample processing
│   ├── homogenization study/    # Mixing optimization
│   └── make calibration/        # Automated calibration
│
├── docs/                        # Complete documentation (MkDocs)
│   ├── getting-started.md       # Installation and setup
│   ├── chemstation-api/         # ChemStation API docs
│   ├── sia-api/                 # SIA API docs
│   ├── tutorials/               # Guides and tutorials
│   └── api-reference/           # API reference
│
├── setup.py                     # Setup script
├── install.py                   # Installation helper
├── mkdocs.yml                   # Documentation config
└── README.md                    # This file
```

## 🔧 Hardware Compatibility

### Tested Systems

| Component                 | Model                           | Status             |
| ------------------------- | ------------------------------- | ------------------ |
| **CE System**       | Agilent 7100 CE                 | ✅ Fully supported |
| **Software**        | OpenLab ChemStation C.01.07 SR2 | ✅ Tested          |
| **Syringe Pumps**   | Cavro XCalibur series           | ✅ Supported       |
| **Valve Selectors** | VICI/Valco multi-position       | ✅ Supported       |

### Requirements

- 🖥️ **OS:** Windows 7, 10, 11
- 🐍 **Python:** 3.7 - 3.11
- 🔌 **Hardware:** ChemStation with command processor access
- 🔗 **Communication:** Serial ports for SI devices (COM ports)
- 📦 **Dependencies:** pyserial, pandas, tqdm, pywin32

## 📚 Documentation

Complete documentation is available at: **[https://xixaus.github.io/SI-CE/](https://xixaus.github.io/SI-CE/)**

### Documentation Sections

- **[Getting Started](https://xixaus.github.io/SI-CE/getting-started/)** - Installation and first steps
- **[ChemStation API](https://xixaus.github.io/SI-CE/chemstation-api/introduction/)** - Complete ChemStation API documentation
- **[SIA API](https://xixaus.github.io/SI-CE/sia-api/sia_introduction/)** - Sequential Injection API documentation
- **[Tutorials](https://xixaus.github.io/SI-CE/tutorials/sample_processor/)** - Practical guides
- **[API Reference](https://xixaus.github.io/SI-CE/api-reference/)** - Detailed module reference

### Quick Links

- 📖 [Communication Protocol Guide](docs/chemstation-api/file-protocol.md)
- 🔧 [Macro Tutorial](docs/chemstation-api/macro_tutorial.md)
- ❓ [FAQ](docs/appendix/faq.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENCE](LICENCE) file for details.

## 🙏 Acknowledgments

- File-based communication protocol adapted from [Cronin Group&#39;s AnalyticalLabware](https://github.com/croningp/analyticallabware)
- ChemStation macro concepts from Agilent Community Forum
- SIA control patterns inspired by CoCoSoft framework

## ⚠️ Note

This package was developed for specific laboratory automation needs. While designed for general use, compatibility with different ChemStation versions and hardware configurations may require testing and adaptation.

For issue reporting or questions, please use [GitHub Issues](https://github.com/Xixaus/SI-CE/issues).
