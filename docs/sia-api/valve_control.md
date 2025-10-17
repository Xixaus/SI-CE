# Valve Control

## Overview

The `ValveSelector` class controls multi-position valve selectors for automated fluid routing in SI systems.

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
```


## Basic Operations

### Position Control

```python
# Move to specific positions
valve.position(1)    # Position 1
valve.position(3)    # Position 3
valve.position(8)    # Position 8

valve.position(15)  # Error: exceeds 8 positions
```

### Reliable Positioning

```python
valve.position(5, num_attempts=5)  # Pošle příkaz 5x

# Some valves may not move on first attempt
# Multiple attempts ensure reliable positioning
```

## Documentation References

For comprehensive valve specifications and setup procedures:

- **[VICI Universal Actuator Manual](https://github.com/Xixaus/SI-CE/blob/main/SIA_API/devices/manuals/universal-actuator.pdf)** - Complete hardware specifications and setup procedures
