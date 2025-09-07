# Valve Control

## Overview

The `ValveSelector` class controls multi-position valve selectors for automated fluid routing in SI systems. It supports VICI/Valco and compatible valves with 2-12 positions.

## Quick Start

```python
from SI_API.devices import ValveSelector

# Initialize valve selector
valve = ValveSelector(
    port="COM4",         # Serial port
    num_positions=8,     # 8-position valve
    prefix="/Z",         # VICI standard prefix
    baudrate=9600        # Communication speed
)

# Basic operation
valve.position(1)        # Move to position 1
valve.position(5)        # Move to position 5
```

## Valve Types and Configurations

### Common Valve Configurations

**6-Position Valve**:
```python
valve = ValveSelector("COM4", num_positions=6)
```

**8-Position Valve**:
```python
valve = ValveSelector("COM4", num_positions=8)
```

**12-Position Valve**:
```python
valve = ValveSelector("COM4", num_positions=12)
```

## Basic Operations

### Position Control

```python
# Move to specific positions
valve.position(1)    # Position 1
valve.position(3)    # Position 3
valve.position(8)    # Position 8

# Position validation is automatic
try:
    valve.position(15)  # Error: exceeds 8 positions
except ValueError as e:
    print(f"Invalid position: {e}")
```

### Reliable Positioning

```python
# Use multiple attempts for critical operations
valve.position(5, num_attempts=5)  # Try up to 5 times

# Some valves may not respond on first attempt
# Multiple attempts ensure reliable positioning
```

## Integration with Syringe

### Basic Fluid Transfer

```python
from SI_API.devices import SyringeController, ValveSelector

syringe = SyringeController("COM3", 1000)
valve = ValveSelector("COM4", 8)

def transfer_fluid(source_port, dest_port, volume):
    """Transfer fluid between ports"""
    # Select source
    valve.position(source_port)
    syringe.aspirate(volume)
    
    # Select destination
    valve.position(dest_port)
    syringe.dispense(volume)

# Transfer 500 µL from port 3 to port 6
transfer_fluid(source_port=3, dest_port=6, volume=500)
```

### Multi-Step Procedures

```python
def prepare_dilution(sample_port, buffer_port, waste_port):
    """Prepare diluted sample"""
    
    # Aspirate buffer first (reverse order prevents contamination)
    valve.position(buffer_port)
    syringe.aspirate(900)  # 900 µL buffer
    
    # Add sample
    valve.position(sample_port)  
    syringe.aspirate(100)  # 100 µL sample (1:10 dilution)
    
    # Mix by dispensing to waste and re-aspirating
    valve.position(waste_port)
    syringe.dispense(50)   # Remove air bubble
    
    valve.position(sample_port)
    syringe.dispense()     # Deliver mixture
    
prepare_dilution(sample_port=4, buffer_port=3, waste_port=1)
```

## Best Practices

### 1. Port Assignment Planning
```python
# Document your port assignments clearly
PORT_ASSIGNMENTS = {
    'WASTE': 1,
    'AIR': 2,
    'DI_WATER': 3, 
    'SAMPLE_A': 4,
    'SAMPLE_B': 5,
    'BUFFER': 6,
    'CLEANING': 7,
    'TO_INSTRUMENT': 8
}

# Use constants instead of numbers
valve.position(PORT_ASSIGNMENTS['WASTE'])  # Clear intent
valve.position(1)                          # Unclear
```

### 2. Minimize Valve Switching
```python
# Inefficient: many valve switches
valve.position(3)
syringe.aspirate(100)
valve.position(4) 
syringe.aspirate(100)
valve.position(3)
syringe.aspirate(100)

# Better: group operations by port
valve.position(3)
syringe.aspirate(200)  # Get all water at once
valve.position(4)
syringe.aspirate(100)
```

## Documentation References

For comprehensive valve specifications and setup procedures:

- **[VICI Universal Actuator Manual](https://github.com/Xixaus/SI-CE/blob/main/SIA_API/devices/manuals/universal-actuator.pdf)** - Complete hardware specifications and setup procedures

## Next Steps

- **[CE Workflows](ce-workflows.md)**: Learn to combine valve and syringe control for complete analytical workflows