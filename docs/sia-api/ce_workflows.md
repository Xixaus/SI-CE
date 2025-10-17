# CE Workflows - SI Integration

## Overview

The `PreparedSIMethods` class provides high-level automation workflows that combine SI sample preparation with Capillary Electrophoresis system. These workflows handle complex sequences of operations for complete analytical automation.

Napsat že to obsahuje skript a konfigurák

## System Integration

```python
from ChemstationAPI import ChemstationAPI
from SI_API.devices import SyringeController, ValveSelector  
from SI_API.methods import PreparedSIMethods

# Initialize all components
ce_api = ChemstationAPI()
syringe = SyringeController("COM3", syringe_size=1000)
valve = ValveSelector("COM4", num_positions=8)

# Create integrated workflow system
workflow = PreparedSIMethods(
    chemstation_controller=ce_api,
    syringe_device=syringe,
    valve_device=valve
)
```

## Core Workflow Components

### System Initialization

Every analytical session starts with complete system preparation:

```python
# Complete system initialization and cleaning
workflow.system_initialization_and_cleaning(
    waste_vial=50,  # Waste collection vial
    bubble=20       # Air bubble size (µL)
)
```

**What happens during initialization:**

1. Syringe homing and speed setting
2. Holding coil flushing with methanol
3. DI water rinse cycles
4. Transfer line conditioning
5. Air bubble creation for separation kapaliny v holding coil a ventilem

### Sample Handling Integration

The workflows automatically coordinate between SI preparation and CE autosampler:

```python
# Load vial to CE replenishment position

# Perform SI operations on loaded vial
workflow.continuous_fill(vial=15, volume=500, solvent_port=3)

# Unload vial back to carousel  
```

## Flow Modes

### Continuous Flow Mode

Ideal for multiple samples with the same solvent:

```python
# Prepare system for continuous flow
workflow.prepare_continuous_flow(
    solvent_port=3,              # DI water port
    transfer_coil_flush=600,     # Transfer line volume
    speed=2000                   # Flow rate (µL/min)
)

# Fill multiple vials efficiently
sample_vials = [10, 11, 12, 13, 14]
for vial in sample_vials:
    workflow.continuous_fill(
        vial=vial,
        volume=1000,             # 1 mL per vial  
        solvent_port=3,          # DI water
        flush_needle=50          # Needle cleaning
    )
```

**Continuous flow characteristics:**

- Transfer line pre-filled with solvent
- Faster operation (no air gaps)
- Consistent flow properties
- Best for same solvent, multiple vials

### Batch Flow Mode

Better for different solvents or single operations:

```python
# Prepare for batch operations
workflow.prepare_batch_flow(
    solvent_port=5,              # Methanol port
    transfer_coil_volume=600,    # Line volume
    speed=1500                   # Flow rate
)

# Fill with air-driven dispensing
workflow.batch_fill(
    vial=20,
    volume=750,                  # Volume to dispense
    solvent_port=5,              # Methanol
    bubble_volume=15,            # Air separation
    wait=2                       # Wait after dispensing
)
```

**Batch flow characteristics:**

- Air-driven dispensing
- Complete separation between solutions
- Suitable for solvent changes
- Independent operations

## Sample Preparation Workflows

### Automated Dilution

```python
def add_solvent():
    """Add solvent k serii vialek"""
    
    # Initialize system
    workflow.system_initialization_and_cleaning()
    
    # Prepare for water addition
    workflow.prepare_continuous_flow(solvent_port=3)  # DI water
    
    sample_vials = [15, 16, 17, 18, 19]
    volme_solvent = 1000
    solvent_port = 3
    
    for vial in sample_vials:
        # Add 900 µL diluent (for 1:10 dilution)
        workflow.continuous_fill(
            vial=vial,
            volume=900,
            solvent_port=3,
        )
        
        print(f"Vial {vial}: Add {volume_solvent} µL")
    
    print("All dilutions prepared - add samples as indicated")

prepare_dilution_series()
```

### Multi-Solvent Sample Preparation

```python
def prepare_mixed_samples():
    """Prepare samples with multiple reagents"""
    
    sample_preparations = [
        {'vial': 20, 'water': 500, 'buffer': 200, 'reagent': 50},
        {'vial': 21, 'water': 600, 'buffer': 150, 'reagent': 25},
        {'vial': 22, 'water': 400, 'buffer': 300, 'reagent': 75}
    ]
    
    for prep in sample_preparations:
        print(f"Preparing vial {prep['vial']}")
        
        # Use batch mode for different solvents
        workflow.batch_fill_multiple_solvents(
            vial=prep['vial'],
            solvent_ports=[3, 6, 7],  # Water, buffer, reagent
            volumes=[prep['water'], prep['buffer'], prep['reagent']],
            air_push_volume=20
        )

prepare_mixed_samples()
```

## Sample Homogenization

### Liquid Mixing

Gentle mixing for sensitive samples:

```python
# Prepare system for liquid homogenization
workflow.prepare_for_liquid_homogenization()

# Mix by liquid aspiration/dispensing
workflow.homogenize_by_liquid_mixing(
    vial=15,
    volume_aspirate=400,         # Volume per cycle
    num_cycles=3,                # Number of cycles
    aspirate_speed=1500,         # Gentle aspiration
    dispense_speed=2000,         # Controlled dispensing
    clean_after=True             # Clean transfer line
)
```

### Air Bubble Mixing

Vigorous mixing for thorough homogenization:

```python
# Air bubble mixing for viscous samples
workflow.homogenize_by_air_mixing(
    vial=22,
    volume_aspirate=300,         # Liquid per cycle
    air_bubble_volume=100,       # Air bubble size
    num_cycles=5,                # More cycles for thorough mixing
    wait_between_cycles=8.0,     # Time for bubble action
    aspirate_speed=800           # Slower for viscous samples
)
```

## Best Practices

### 1. Always Initialize First
```python
# Start every session with system initialization
workflow.system_initialization_and_cleaning()
```

### 2. Match Flow Mode to Application
- **Continuous flow**: Same solvent, multiple samples, speed priority
- **Batch flow**: Different solvents, contamination concerns

### 3. Plan Needle Cleaning
```python
# Clean between different sample types
workflow.continuous_fill(vial=10, volume=1000, solvent_port=3, flush_needle=50)
# Skip cleaning within replicate groups  
workflow.continuous_fill(vial=11, volume=1000, solvent_port=3, flush_needle=None)
```

### 4. Monitor Critical Operations
```python
# Enable verbose mode for important workflows
workflow.update_config(verbose=True)

# Check system status
status = workflow.get_system_status()
print(f"Syringe size: {status['syringe_size']} µL")
print(f"Port assignments: {status['port_assignments']}")
```


## Custom Configuration

nějak tady popiš konfigurák