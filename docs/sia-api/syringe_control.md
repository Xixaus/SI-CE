# Syringe Control

## Overview

The `SyringeController` class provides complete automation of syringe pumps for precise fluid handling in SI systems. It supports Cavro XCalibur series.

## Quick Start

```python
from SI_API.devices import SyringeController

# Initialize syringe pump
syringe = SyringeController(
    port="COM3",        # Serial port
    syringe_size=1000,  # 1000 µL syringe
    microstep_mode=False  # Standard resolution
)

# Basic operations
syringe.initialize()                    # Home to zero position
syringe.set_speed_uL_min(1500)         # Set flow rate
syringe.aspirate(500)                   # Draw 500 µL
syringe.dispense(250)                   # Dispense 250 µL
```

## Supported Syringe Sizes

The controller supports standard syringe volumes:

- 50, 100, 250, 500, 1000, 2500, 5000 µL

Each size has optimized parameters for:

- **Resolution**: Volume per increment (0.02-1.67 µL depending on size)
- **Speed limits**: Minimum and maximum flow rates

## Basic Operations

### Initialization
Always start with syringe initialization:

```python
# Initialize to home position (volume = 0)
syringe.initialize()
print(f"Syringe ready: {syringe.volume_counter} µL")
```

### Volume Control

```python
# Aspirate specific volume
syringe.aspirate(300)           # Draw 300 µL
print(f"Current volume: {syringe.volume_counter} µL")  # Shows 300

# Aspirate to full capacity
syringe.aspirate()              # Fill completely (700 µL remaining)

# Dispense specific volume  
syringe.dispense(200)           # Dispense 200 µL

# Dispense all contents
syringe.dispense()              # Empty completely
```

### Flow Rate Control

```python
# Set different speeds for different operations
syringe.set_speed_uL_min(3000)  # Fast transfer
syringe.set_speed_uL_min(1000)  # Precise dispensing  
syringe.set_speed_uL_min(500)   # Gentle mixing

# Speed limits depend on syringe size:
# Minimum: 0.05 × syringe_size µL/min
# Maximum: 60 × syringe_size µL/min
```

## Emergency Operations

### Emergency Stop

```python
# Immediately halt all syringe operations
syringe.emergency_stop()
```

## Volume Tracking

The controller automatically tracks syringe contents:

```python
# Check current volume
syringe.print_volume_in_syringe()
# Output: "The current volume in the syringe is: 250.0 µl"

# Volume validation prevents errors
try:
    syringe.aspirate(2000)  # Exceeds 1000 µL capacity
except ValueError as e:
    print(f"Error: {e}")
```

## Valve Control

For syringes with attached valves:

```python
# Configure valve type first
syringe.configuration_valve_type('3-Port')

# Control valve positions
syringe.valve_in()    # Input position (aspiration)
syringe.valve_out()   # Output position (dispensing)  
syringe.valve_up()    # Bypass/waste position
```

### Supported Valve Types

- 'No' - No valve attached
- '3-Port' - Standard 3-way valve
- '4-Port' - 4-way selection valve
- '6-Port distribution' - 6-port selection
- '12-Port distribution' - 12-port selection
- And more (see documentation)

## Advanced Features

### Progress Monitoring

```python
# Show progress bar during long operations
syringe.aspirate(1000, show_progress=True)
# Output: Processing: 67%|████████  | 4.2s/6.3s [00:04<00:02]
```

### High-Resolution Mode

```python
# Enable microstep mode for higher precision
syringe.set_microstep_mode(True)
print(f"Resolution: {syringe.resolution:.3f} µL/step")
# Standard: ~0.33 µL/step → Microstep: ~0.04 µL/step
```

## Documentation References

For detailed hardware information, command specifications, and troubleshooting:

- **[Cavro XCalibur Operating Manual](https://github.com/Xixaus/SI-CE/blob/main/SIA_API/devices/manuals/Cavro%20XCalibur.pdf)** - Comprehensive pump specifications and setup