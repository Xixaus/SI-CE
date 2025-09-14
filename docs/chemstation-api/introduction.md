# ChemStation API Introduction

## What is ChemStation API?

The ChemStation API provides a comprehensive Python interface for controlling Agilent ChemStation software and CE instruments. It enables complete automation of capillary electrophoresis systems, eliminating manual intervention in routine analytical workflows through direct communication with ChemStation's Command Processor (CP). The API uses a sophisticated file-based communication protocol to bridge Python applications with ChemStation's native command structure, providing reliable, bidirectional control of all instrument functions.

**Development & Compatibility:** Originally developed and optimized for OpenLab ChemStation version C.01.07 SR2 [255] with Agilent Technologies 7100 Capillary Electrophoresis system, the API has been successfully tested across multiple ChemStation versions (C.01.05-C.01.10), various CE instrument models (7100, G7100A), and Windows operating systems (Windows 7, 10, 11). With minor code modifications, compatibility extends to legacy systems including Windows XP with Python 3.4+.

---

## Key Features

### CE Instrument Control
- **Automated vial handling** - Load/unload vials between carousel and analysis positions
- **Capillary operations** - Conditioning, flushing, and pressure control
- **Position monitoring** - Real-time tracking of vial locations and system state
- **Safety validation** - Prevent operations during incompatible instrument states

### Method Management
- **Method execution** - Load and run CE methods with custom parameters
- **Parameter control** - Modify sample information without editing method files
- **File operations** - Save, load, and validate method existence
- **Batch execution** - Run same method on different samples automatically

### Sequence Operations
- **Sequence automation** - Create and execute multi-sample analysis workflows  
- **Excel integration** - Import sample lists directly from spreadsheets
- **Progress monitoring** - Real-time tracking of batch analysis progress
- **Error recovery** - Pause, resume, and handle sequence interruptions

### System Monitoring
- **Real-time status** - Continuous monitoring of instrument and analysis state
- **Progress tracking** - Elapsed time, remaining time, and completion estimates
- **Diagnostic access** - Direct access to RC.NET status registers
- **Error detection** - Comprehensive system health monitoring

---

## Module Overview

The ChemStation API organizes functionality into specialized modules for different aspects of CE automation:

### Core Communication (`core/`)
- **File-based protocol** for reliable ChemStation communication
- **Command processor integration** for direct instrument control  
- **Error handling** and timeout management with automatic retry logic
- **Configuration management** for communication parameters

### Device Controllers (`controllers/`)
- **CEModule**: Complete vial handling and capillary operations
- **MethodsModule**: CE method loading, execution, and parameter management
- **SequenceModule**: Batch analysis control and sequence table management
- **SystemModule**: Real-time status monitoring and diagnostic functions
- **ValidationModule**: Pre-operation checks and error prevention

### Automation Workflows
- **High-level operations** - Complete analytical procedures in single calls
- **Validation systems** - Comprehensive pre-flight checks prevent common errors
- **Integration patterns** - Seamless connectivity with SIA sample preparation systems

---

## Quick Start

```python
from ChemstationAPI import ChemstationAPI

# Initialize connection to ChemStation
api = ChemstationAPI()

# Basic workflow example
api.ce.load_vial_to_position(15, "inlet")     # Load sample vial
api.method.load("CE_Protein_Analysis")        # Load method
api.method.run("Sample_001")                  # Execute analysis

# Monitor progress
while api.system.method_on():
    remaining = api.system.get_remaining_analysis_time()
    print(f"Analysis remaining: {remaining:.1f} minutes")
    time.sleep(30)
```

---

## Documentation Resources

For comprehensive information, theoretical background, and technical specifications:

### Research & Literature
- **[Literature Collection](https://github.com/Xixaus/SI-CE/tree/main/literature)** - Research papers, analytical methods, and CE theory
- **[Technical Documentation](https://github.com/Xixaus/SI-CE/tree/main/docs)** - Detailed API documentation and tutorials