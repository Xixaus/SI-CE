# CE Workflows - SI Integration

## Overview

The `PreparedSIMethods` class provides high-level automation workflows that combine SI sample preparation with Capillary Electrophoresis analysis. These workflows handle complex sequences of operations for complete analytical automation.

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
5. Air bubble creation for separation

### Sample Handling Integration

The workflows automatically coordinate between SI preparation and CE autosampler:

```python
# Load vial to CE replenishment position
workflow.load_to_replenishment(vial_number=15)

# Perform SI operations on loaded vial
workflow.continuous_fill(vial=15, volume=500, solvent_port=3)

# Unload vial back to carousel  
workflow.unload_from_replenishment()
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
def prepare_dilution_series():
    """Prepare 1:10 dilution series"""
    
    # Initialize system
    workflow.system_initialization_and_cleaning()
    
    # Prepare for water addition
    workflow.prepare_continuous_flow(solvent_port=3)  # DI water
    
    sample_vials = [15, 16, 17, 18, 19]
    
    for vial in sample_vials:
        # Add 900 µL diluent (for 1:10 dilution)
        workflow.continuous_fill(
            vial=vial,
            volume=900,
            solvent_port=3,
            flush_needle=None  # No wash between same solvent
        )
        
        print(f"Vial {vial}: Add 100 µL sample manually")
    
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

## Complete Analytical Workflows

### Automated Analysis

```python
def analysis_workflow():
    """Complete sample preparation and analysis"""

    # Sample preparation
    samples = [10, 11, 12, 13]
    method_name = "CE_Protein_Analysis"

    ce_api.validation.list_vial_validation(samples)
    ce_api.validation.validate_method(method_name)

    # System initialization
    workflow.system_initialization_and_cleaning()
    
    # Prepare buffer dilutions  
    workflow.prepare_continuous_flow(solvent_port=6)  # Buffer
    
    for vial in samples:
        # Add buffer
        workflow.continuous_fill(
            vial=vial,
            volume=500,      # 500 µL buffer
            solvent_port=6,
            flush_needle=25
        )
    
    print("Samples ready for CE analysis")

    workflow.prepare_for_liquid_homogenization()

    # Proceed with CE analysis using ChemStation integration
    for vial in samples:
    
        #čekání až bude možné použít carousel
        while ce_api.system.RC_status() not in ["Idle", "Run"]:
            time.sleep(5)

        #homogenizace vzorku před analýzou
        workflow.homogenize_by_liquid_mixing(
            vial=vial,
            volume_aspirate=200,
            num_cycles=2,
            aspirate_speed=1000,  # Gentle
            dispense_speed=1200
        )

        #čekání až bude systém připraven na spuštění analýzy
        ce_api.system.ready_to_start_analysis()

        #spuštění analýzy s parametry
        ce_api.method.execution_method_with_parameters(
            vial=vial,
            method_name="CE_Protein_Analysis",
            sample_name=f"Protein_Sample_{vial}"
        )

analysis_workflow()
```

## Configuration and Optimization

### Custom Port Configuration

```python
from SI_API.methods import create_custom_config

# Create custom port mapping
custom_ports = create_custom_config(
    waste_port=8,        # Move waste to end
    air_port=1,          # Air at beginning  
    di_port=2,           # Water nearby
    transfer_port=7,     # Transfer near waste
    meoh_port=3,         # Cleaning solvents grouped
    buffer_port=4,       # Sample prep solvents  
    sample_port=5        # Sample input
)

# Use custom configuration
workflow = PreparedSIMethods(
    chemstation_controller=ce_api,
    syringe_device=syringe,
    valve_device=valve,
    ports_config=custom_ports
)
```

### Performance Optimization

```python
# Optimize for speed
speed_config = {
    'speed_fast': 4000,           # Fast transfers
    'speed_normal': 2500,         # Normal operations  
    'wait_after_aspirate': 0.5,   # Minimal delays
    'wait_after_dispense': 0.2,
    'homogenization_liquid_cycles': 1,  # Fewer mixing cycles
    'verbose': False              # Reduce output for speed
}

workflow.update_config(**speed_config)

# Optimize for precision  
precision_config = {
    'speed_fast': 2000,           # Slower, more controlled
    'speed_normal': 1200,
    'wait_after_aspirate': 2.0,   # Allow settling
    'wait_after_dispense': 1.0,
    'homogenization_liquid_cycles': 4,  # More thorough mixing
    'verbose': True               # Full feedback
}

workflow.update_config(**precision_config)
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

### Port Configuration
```python
from SI_API.methods import create_custom_config

# Create custom port mapping
custom_ports = create_custom_config(
    waste_port=8,        # Move waste to end
    air_port=1,          # Air at beginning  
    di_port=2,           # Water nearby
    transfer_port=7,     # Transfer near waste
    meoh_port=3          # Cleaning solvents grouped
)

# Use custom configuration
workflow = PreparedSIMethods(
    chemstation_controller=ce_api,
    syringe_device=syringe,
    valve_device=valve,
    ports_config=custom_ports
)
```

### Performance Optimization
```python
# Optimize for speed
workflow.update_config(
    speed_fast=4000,
    speed_normal=2500,
    wait_after_dispense=0.2,
    verbose=False
)

# Optimize for precision  
workflow.update_config(
    speed_fast=2000,
    speed_normal=1200,
    wait_after_aspirate=2.0,
    homogenization_liquid_cycles=4,
    verbose=True
)
```

## Advanced Integration

The SI-CE integration enables sophisticated analytical workflows:

- **Unattended operation**: Complete sample prep and analysis
- **Method development**: Automated optimization studies  
- **Quality control**: Reproducible sample handling
- **High throughput**: Parallel processing capabilities
- **Adaptive methods**: Sample-specific preparations

This integration transforms manual, time-intensive procedures into fully automated analytical workflows suitable for research, quality control, and routine analysis applications.