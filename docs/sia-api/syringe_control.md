# Syringe Control

## Overview

The `SyringeController` class provides complete automation of syringe pumps for precise fluid handling in SIA systems. It supports Hamilton MVP series and compatible pumps with automatic volume tracking and safety features.

## Quick Start

```python
from SIA_API.devices import SyringeController

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
- **Initialization force**: Appropriate for syringe mechanics

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

## Volume Tracking

The controller automatically tracks syringe contents:

```python
# Check current volume
syringe.print_volume_in_syringe()
# Output: "The current volume in the syringe is: 250.0 µl"

# Get actual volume from pump
actual_volume = syringe.get_actual_volume()
print(f"Pump reports: {actual_volume} µL")

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
- And more (see API reference)

## Advanced Features

### Progress Monitoring

```python
# Show progress bar during long operations
syringe.aspirate(1000, show_progress=True)
# Output: Processing: 67%|████████  | 4.2s/6.3s [00:04<00:02]
```

### Non-blocking Operations

```python
# Start operation without waiting
syringe.aspirate(500, wait=False)

# Do other work...
print("Operation started, doing other tasks")

# Check if pump is ready
while not syringe._is_pump_ready():
    time.sleep(0.1)
print("Aspiration completed")
```

**Přidat emergency_stop**


### High-Resolution Mode

```python
# Enable microstep mode for higher precision
syringe.set_microstep_mode(True)
print(f"Resolution: {syringe.resolution:.3f} µL/step")
# Standard: ~0.33 µL/step → Microstep: ~0.04 µL/step
```

## Error Handling

### Common Error Types

```python
# Volume overflow
try:
    syringe.aspirate(1200)  # Exceeds 1000 µL
except ValueError as e:
    print(f"Volume error: {e}")

# Communication error
try:
    syringe.initialize()
except serial.SerialException as e:
    print(f"Communication error: {e}")
    # Check port, cable, power

# Speed out of range
try:
    syringe.set_speed_uL_min(100000)  # Too fast
except ValueError as e:
    print(f"Speed error: {e}")
```

### Recovery Procedures

```python
def reset_syringe():
    """Complete syringe reset"""
    try:
        syringe.emergency_stop()  # Stop immediately
        syringe.initialize()      # Re-home
        syringe.set_speed_uL_min(2000)  # Reset speed
        print("Syringe reset successful")
    except Exception as e:
        print(f"Reset failed: {e}")
```

## Integration Tips

### With ValveSelector

```python
# Coordinate syringe and external valve
from SI_API.devices import ValveSelector

syringe = SyringeController("COM3", 1000)
valve = ValveSelector("COM4", 8)

# Transfer from port 3 to port 6
valve.position(3)       # Select source
syringe.aspirate(500)   # Draw liquid
valve.position(6)       # Select destination  
syringe.dispense(500)   # Deliver liquid
```

### With Error Recovery

```python
def robust_operation():
    """Operation with automatic error recovery"""
    max_attempts = 3
    
    for attempt in range(max_attempts):
        try:
            syringe.aspirate(500)
            syringe.dispense(500)
            break  # Success
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt < max_attempts - 1:
                syringe.initialize()  # Reset and retry
            else:
                raise  # Final attempt failed
```

## Documentation References

For detailed hardware information, command specifications, and troubleshooting:

- **Cavro XP**: [https://github.com/Xixaus/SI-CE/tree/main/SIA_API/devices/manuals]

## Next Steps

- **[Valve Control](valve-control.md)**: Learn to control multi-position valves
- **[CE Workflows](ce-workflows.md)**: Combine syringe and valve for complete automation