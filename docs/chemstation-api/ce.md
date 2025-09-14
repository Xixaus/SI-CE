# CE Module - Capillary Electrophoresis Control

Control of Agilent 7100 CE instrument for vial handling and capillary operations.

## Overview

The CE module provides direct control of:

- **Carousel system**: 50 positions (1-48 samples, 49-50 parking)
- **Lift positions**: inlet (positive electrode), outlet (ground), replenishment  
- **Capillary operations**: conditioning, flushing, pressure control

**Hardware**: Agilent 7100 CE system with automated carousel

**Module ID**: CE1

---

## Vial Management

### load_vial_to_position()

Load vial from carousel to specified lift position.

```python
api.ce.load_vial_to_position(vial, position="replenishment")
```

**Parameters:**

- `vial` (int): Carousel position number (1-48 for samples, 49 for parking)
- `position` (str): Target lift position
  - `"inlet"`: Sample injection, positive electrode contact
  - `"outlet"`: Waste collection, negative electrode (ground)  
  - `"replenishment"`: Buffer system maintenance

**Examples:**
```python
# Load sample for analysis
api.ce.load_vial_to_position(15, "inlet")

# Load waste collection vial
api.ce.load_vial_to_position(20, "outlet") 

# Load buffer vial (default position)
api.ce.load_vial_to_position(1)
```

**Important:**

- Carousel operations only work during voltage application (analysis runtime)
- Completely blocked during pressure operations
- Vial must be present in carousel

---

### unload_vial_from_position()

Return vial from lift position back to its carousel slot.

```python
api.ce.unload_vial_from_position(position="replenishment")
```

**Parameters:**

- `position` (str): Lift position to unload from
  - `"inlet"`: Return sample vial
  - `"outlet"`: Return waste vial
  - `"replenishment"`: Return buffer vial

**Examples:**
```python
# Return vials after analysis
api.ce.unload_vial_from_position("inlet")
api.ce.unload_vial_from_position("outlet")

# Return buffer vial (default)
api.ce.unload_vial_from_position()
```

**Warning:** 
NEVER unload inlet or outlet vials during voltage application! Can cause severe electrical damage to electrode system. Replenishment vials can be safely unloaded during voltage application.

---

### get_vial_state()

Get current position and state of a vial within the CE system.

```python
state = api.ce.get_vial_state(vial)
```

**Parameters:**

- `vial` (int): Vial position number to check (1-50)

**Returns:**

- `"carousel"`: Available in tray position, ready for loading
- `"inlet"`: At inlet lift (sample/buffer introduction)
- `"outlet"`: At outlet lift (waste/collection)
- `"replenishment"`: At replenishment lift (buffer maintenance)
- `"out_system"`: Not detected anywhere in the system

**Examples:**
```python
# Check sample preparation status
if api.ce.get_vial_state(15) == "inlet":
    print("Sample ready for injection")

# Monitor multiple vials
for vial in [10, 11, 12]:
    print(f"Vial {vial}: {api.ce.get_vial_state(vial)}")

# Find empty positions
for pos in range(1, 49):
    if api.ce.get_vial_state(pos) == "out_system":
        print(f"Position {pos} is empty")
```

---

## Capillary Operations

### flush_capillary()

Perform high-pressure capillary conditioning flush.

```python
api.ce.flush_capillary(time_flush, wait=True)
```

**Parameters:**

- `time_flush` (float): Flush duration in seconds
- `wait` (bool): If True, shows progress bar and waits for completion. If False, starts flush and returns immediately.

**Examples:**
```python
# Standard conditioning flush
api.ce.flush_capillary(60.0)

# Extended conditioning with progress
api.ce.flush_capillary(180.0, wait=True)

# Start flush without waiting
api.ce.flush_capillary(30.0, wait=False)
# Continue with other operations...
```

**Notes:**

- Uses maximum system pressure (~950 mbar)
- Buffer drawn from inlet vial, expelled through outlet
- Carousel completely blocked during operation
- Requires adequate buffer volume

---

### apply_pressure_to_capillary()

Apply precise pressure to capillary for controlled operations.

```python
api.ce.apply_pressure_to_capillary(pressure, time_pressure, wait=True)
```

**Parameters:**

- `pressure` (float): Pressure in mbar (range: -100 to +100)
  - Positive: Pushes liquid from inlet toward outlet
  - Negative: Creates vacuum, pulls liquid toward inlet
- `time_pressure` (float): Duration of pressure application in seconds
- `wait` (bool): If True, shows progress bar and waits for completion

**Examples:**
```python
# Hydrodynamic injection
api.ce.apply_pressure_to_capillary(50.0, 5.0)

# Vacuum rinse
api.ce.apply_pressure_to_capillary(-30.0, 10.0)

# Gentle conditioning
api.ce.apply_pressure_to_capillary(20.0, 30.0, wait=True)

# Start pressure without waiting
api.ce.apply_pressure_to_capillary(75.0, 3.0, wait=False)
```

**Notes:**

- Injection pressure directly affects sample volume and peak shape
- Carousel blocked during pressure application
- Position vials beforehand

---

## System State Dependencies

**Carousel Access:**

- **Available**: During voltage application (analysis runtime)
- **Blocked**: During pressure operations, door open, error states

**Safety Constraints:**

- Never manipulate inlet/outlet vials during voltage
- Always check vial presence before loading operations  
- Verify carousel availability before batch operations

**Pressure Operations:**

- Block all carousel movement
- Require inlet vial for source liquid
- Monitor buffer levels for extended operations