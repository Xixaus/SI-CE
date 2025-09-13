# SI-CE Integration Package

A Python package for automated control of Agilent ChemStation CE systems integrated with Sequential Injection (SI) hardware. Enables programmatic sample preparation, method execution, and data acquisition for analytical chemistry workflows.

This package was developed for OpenLab ChemStation ver. C.01.07 SR2 [255] with Agilent Technologies 7100 Capillary Electrophoresis system combined with sequential injection components. Compatibility with other systems has not been tested.

!!! info "Project Status"
    This project is actively developed.
## What is SI-CE?

SI-CE combines two powerful analytical techniques:

- **Capillary Electrophoresis (CE)**: High-resolution separation technique for analyzing charged molecules
- **Sequential Injection (SI)**: Automated sample preparation and liquid handling system

Connection of these techniques provides user with:

- Fully automated sample preparation and analysis
- Reduced manual intervention and human error
- Increased throughput and reproducibility
- Complex analytical workflows with minimal supervision

## Key Features

### ChemStation API
- Direct communication with OpenLab CDS ChemStation command processor
- Method and sequence management functions
- Instrument status monitoring and control
- Automated vial handling for CE7100 systems

### SIA API  
- Serial communication modules for SI hardware
- Device controllers for syringe pumps (Cavro XCalibur) and valve selectors (VICI)
- Pre-configured workflows for common analytical procedures


## Code preview

```python
from ChemstationAPI import ChemstationAPI
from SIA_API.devices import SyringeController, ValveSelector
from SIA_API.methods import PreparedSIMethods

# Initialize system components
ce = ChemstationAPI()
syringe = SyringeController(port="COM3", syringe_size=1000)
valve = ValveSelector(port="COM4", num_positions=8)
workflow = PreparedSIMethods(ce, syringe, valve)

# Automated sample preparation and analysis
workflow.system_initialization_and_cleaning()
workflow.batch_fill(vial=15, volume=1500, solvent_port=3)
ce.method.execution_method_with_parameters(
    vial=15, method_name="Protein_Analysis", sample_name="Sample_001"
)
```


## Support and Contributing

- **Issues**: Report bugs on [GitHub Issues](https://github.com/yourusername/SIA-CE/issues)
- **Discussions**: Join our [community discussions](https://github.com/yourusername/SIA-CE/discussions)
- **Contributing**: See our [contribution guidelines](https://github.com/yourusername/SIA-CE/blob/main/CONTRIBUTING.md)

