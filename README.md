# SI-CE Integration Package

Python package for automated control of Agilent ChemStation CE systems integrated with Sequential Injection (SI) hardware. Enables complete laboratory automation from sample preparation to data acquisition.

## Features

### ChemStation API
- Direct communication with Agilent ChemStation command processor
- Automated vial handling for CE systems (load/unload, position tracking)
- Method and sequence management with parameter control
- Real-time instrument status monitoring and diagnostics

### SIA API
- Serial communication with SI hardware (syringe pumps, valve selectors)
- Pre-configured workflows for sample preparation and mixing
- Automated dilution, homogenization, and batch processing
- High-level methods for complex analytical procedures

### Integration
- Parallel sample preparation during CE analysis
- Excel-based batch processing with individual sample timing
- Automated method execution with custom parameters
- Comprehensive error handling and validation

## Quick Start

### Installation

```bash
# Download and extract the package
git clone https://github.com/yourusername/SI-CE.git
cd SI-CE

# Install dependencies
python -m pip install -e .
```

### Basic Usage

```python
from ChemstationAPI import ChemstationAPI
from SIA_API.devices import SyringeController, ValveSelector
from SIA_API.methods import PreparedSIMethods

# Initialize systems
ce = ChemstationAPI()
syringe = SyringeController(port="COM3", syringe_size=1000)
valve = ValveSelector(port="COM4", num_positions=8)
workflow = PreparedSIMethods(ce, syringe, valve)

# Automated sample preparation and analysis
workflow.system_initialization_and_cleaning()
workflow.continuous_fill(vial=15, volume=1500, solvent_port=3)
ce.method.execution_method_with_parameters(
    vial=15, method_name="CE_Analysis", sample_name="Sample_001"
)
```

## Hardware Compatibility

### Tested Systems
- **CE:** Agilent 7100 CE with OpenLab ChemStation C.01.07 SR2
- **Syringe Pumps:** Cavro XCalibur series
- **Valve Selectors:** VICI/Valco multi-position valves

### Requirements
- ChemStation with command processor access
- Serial communication ports for SI devices
- Python 3.7 or higher

## Project Structure

```
SI-CE/
├── ChemstationAPI/          # ChemStation communication and control
│   ├── core/                # File-based communication protocol
│   └── controllers/         # CE modules (vials, methods, sequences)
├── SIA_API/                 # Sequential Injection automation
│   ├── devices/             # Hardware controllers
│   └── methods/             # High-level workflows
├── examples/                # Example scripts and applications
└── docs/                    # Complete documentation
```

## Examples

### Automated Batch Processing
Process multiple samples from Excel file with optimized timing:

```python
# Configure from Excel
processor = SampleProcessor(config, chemstation, sia_methods)
processor.process_all_samples()  # Handles entire batch automatically
```

### Homogenization Study
Automated optimization of mixing parameters:

```python
# Time-resolved homogenization analysis
run_time_elution_experiment(processor)
```

See `examples/` directory for complete implementations.

## Development Status

**Current Version:** 0.1.0

**Stability:** 
- ChemStation API: Stable, production-ready
- SIA API: Stable, tested with multiple hardware configurations
- Integration workflows: Active development

**Compatibility:**
- Developed on ChemStation C.01.07 SR2 with CE7100
- Tested on Windows 7, 10, 11
- Compatible with Python 3.7-3.11

## Support

- **Documentation:** [Project Wiki](https://xixaus.github.io/SI-CE/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- File-based communication protocol adapted from [Cronin Group's AnalyticalLabware](https://github.com/croningp/analyticallabware)
- ChemStation macro concepts from Agilent Community Forum
- SIA control patterns inspired by CoCoSoft framework

---

**Note:** This package was developed for specific laboratory automation needs. While designed for general use, compatibility with different ChemStation versions and hardware configurations may require testing and adaptation.
