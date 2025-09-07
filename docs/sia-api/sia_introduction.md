# SI API - Sequential Injection Module

## What is Sequential Injection?

Sequential Injection (SI) is an automated liquid handling technique that enables precise control of fluid movement for analytical chemistry applications. Unlike manual pipetting, SI provides reproducible, computer-controlled operations with microliter precision.

## System Components

### 1. Syringe Pump

The heart of the SI system - provides bidirectional fluid movement with precise volume control:

- **Volume range**: Typically 50-5000 µL syringes
- **Precision**: Sub-microliter accuracy
- **Flow control**: Variable speed operation
- **Automation**: Computer-controlled aspiration and dispensing

### 2. Multi-Position Valve

Routes fluids between different sources and destinations:

- **Positions**: 6-12 port configurations
- **Fast switching**: Rapid fluid path selection
- **Low dead volume**: Minimal fluid waste
- **Computer control**: Automated position switching

### 3. Holding Coil

Temporary storage for fluids during complex operations:

- **Capacity**: 1-5 mL typical volume
- **Mixing**: Enables complex fluid manipulations via liquid mixing or air bubble segmentation
- **Segmentation**: Air bubbles separate different solutions, preventing cross-contamination
- **Flow path**: Connects valve to sample needle, acting as a fluid reservoir

**Basic Operation Sequence:**

1. Valve selects source (sample, reagent, wash solution)
2. Syringe aspirates fluid through holding coil (fluid stays in coil, not syringe)
3. Valve switches to destination 
4. Syringe pushes fluid from holding coil to destination
5. Repeat for complex procedures

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
- **Hamilton MVP compatibility**: Tested with industry-standard pumps
- **VICI valve support**: Compatible with common valve selectors

### Workflow Methods (`methods/`)
- **High-level automation**: Complete analytical procedures
- **CE integration**: Seamless connection with ChemStation
- **Sample preparation**: Automated dilution, mixing, homogenization
- **Configurable parameters**: Adaptable to different applications

## Key Benefits

**Automation**
- Unattended operation for hours
- Consistent, reproducible results
- Reduced manual errors

**Precision**
- Microliter volume accuracy
- Controlled flow rates
- Precise timing

**Flexibility** 
- Multiple sample handling modes
- Custom workflow creation
- Integration with analytical instruments

**Efficiency**
- Parallel sample preparation
- Minimal reagent consumption
- High sample throughput

## Documentation Resources

For detailed hardware specifications and setup procedures:

- **[Device Manuals](https://github.com/Xixaus/SI-CE/tree/main/SIA_API/devices/manuals)** - Complete hardware documentation and setup guides
- **[Syringe Pump Manual](https://github.com/Xixaus/SI-CE/blob/main/SIA_API/devices/manuals/Cavro%20XCalibur.pdf)** - Cavro XCalibur manual
- **[Valve Manual](https://github.com/Xixaus/SI-CE/blob/main/SIA_API/devices/manuals/universal-actuator.pdf)** - VICI Universal Actuator documentation

## Quick Start Example

```python
from SI_API import SyringeController, ValveSelector
from SI_API.methods import PreparedSIMethods

# Initialize hardware
syringe = SyringeController(port="COM3", syringe_size=1000)
valve = ValveSelector(port="COM4", num_positions=8)

# Create workflow system
workflow = PreparedSIMethods(chemstation_api, syringe, valve)

# Initialize and clean system
workflow.system_initialization_and_cleaning()

# Prepare samples
workflow.continuous_fill(vial=15, volume=500, solvent_port=3)
workflow.homogenize_sample(vial=15, speed=1000, time=30)
```

## Next Steps

- **[Core Communication](core-communication.md)**: Learn about the underlying communication system
- **[Syringe Control](syringe-control.md)**: Master precise fluid handling
- **[Valve Control](valve-control.md)**: Control fluid routing
- **[CE Workflows](ce-workflows.md)**: Build complete analytical procedures