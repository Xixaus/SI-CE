# SI API - Sequential Injection Module

## What is Sequential Injection?

Sequential Injection (SI) is an automated liquid handling technique that enables precise control of fluid movement for analytical chemistry applications. Unlike manual pipetting, SI provides reproducible, computer-controlled operations with microliter precision.

## SI_API Module Overview

The SI_API provides Python control for Sequential Injection systems with three main components:

### Core Communication (`core/`)
- **Universal serial interface** for analytical instruments
- **Extensible design** for custom devices (Arduino, ESP32, etc.)
- **Error handling** and connection management
- **Protocol abstraction** for different command formats

### Device Controllers (`devices/`)
- **SyringeController**: Complete syringe pump automation
- **ValveSelector**: Multi-position valve control

### Workflow Methods (`methods/`)
- **High-level automation**: Complete analytical procedures
- **CE integration**: Seamless connection with ChemStation
- **Sample preparation**: Automated dilution, mixing, homogenization

## Documentation Resources

For detailed hardware specifications and setup procedures:

- **[Device Manuals](https://github.com/Xixaus/SI-CE/tree/main/SIA_API/devices/manuals)** - něco tam napiš o tom, že ve složce jsou všechny dokumetace k používaným komponentám
