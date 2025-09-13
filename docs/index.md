# SI-CE Integration Package

## Automated Capillary Electrophoresis with Sequential Injection

Welcome to the SI-CE Integration documentation. This package provides a unified Python interface for controlling Agilent ChemStation CE systems and Sequential Injection (SI) hardware, enabling fully automated analytical workflows. 

Specific coding mentioned later in text was developed for Openlab ChemStation ver. C.01.07 SR2 [255] with use of instrumentation consisting of Agilent Technologies 7100 Capillary Electrophoresis (CE) in combination with sequential injection (SI) system. Compatibility with different systems was not tested and specific use is left on user consideration.

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
- Direct control of OpenLab CDS ChemStation by command processor
- Comprehensive method and sequence management
- Real-time instrument status monitoring
- Automated vial handling
- Něco o tom, že je to přispůsobeno pro CE 7100

### SIA API
- Ovládání SI zařízení skrze COM porty
- Moduly pro ventil (VICI) a stříkačku (Cavro XCalibur)
- Pre-built workflows for common operations


## Code preview

```python
from ChemstationAPI import ChemstationAPI
from SIA_API.devices import SyringeController, ValveSelector
from SIA_API.methods import PreparedSIAMethods

# Initialize systems
syringe = SyringeController(port="COM8", syringe_size=1000)
valve = ValveSelector(port="COM8", num_positions=8)
ce = ChemstationAPI()
sia = PreparedSIAMethods(ce, syringe, valve)

# Automated workflow
sia.system_initialization_and_cleaning()
sia.batch_fill(vial=15, volume=1500, solvent_port=5)
ce.method.execution_method_with_parameters(
    vial=15, 
    method_name="Protein_Analysis",
    sample_name="BSA_Standard"
)
```


## Support and Contributing

- **Issues**: Report bugs on [GitHub Issues](https://github.com/yourusername/SIA-CE/issues)
- **Discussions**: Join our [community discussions](https://github.com/yourusername/SIA-CE/discussions)
- **Contributing**: See our [contribution guidelines](https://github.com/yourusername/SIA-CE/blob/main/CONTRIBUTING.md)

