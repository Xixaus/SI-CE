# Homogenization Time Study

Automated measurement of homogenization timing to optimize CE sample preparation protocols.

## Overview

Measures elapsed time from sample preparation to CE injection at different homogenization intervals. Helps determine optimal homogenization timing for consistent sample analysis.

## Quick Start

### 1. Configure

Edit `examples/homogenization study/config.py`:

```python
@dataclass
class HomogenizationConfig:
    # Valve ports
    meoh_port: int = 5
    di_port: int = 3

    # Volumes (µL)
    meoh_volume: int = 400
    di_volume: int = 100
    homog_volume: int = 290

    # Speeds (µL/min)
    meoh_speed: int = 1000
    di_speed: int = 1200
    homog_speed: int = 1000

    # Homogenization
    homog_cycles: int = 2

    # Timing
    wait_after_meoh: int = 400      # Seconds

    # Experiment
    vial_number: int = 10
    num_repetitions: int = 3
    method_name: str = "Wait"
```

### 2. Run

```bash
cd examples/homogenization\ study/
python homogenization_study.py
```

## How It Works

### Workflow

1. **Sample Preparation** (once):

   - Add MeOH → Wait → Add DI water → Start timer (T=0)
2. **For each repetition**:

   - Homogenize sample
   - Start CE analysis
   - Record time from T=0 to injection
3. **Output**: Timing data saved to file

### Timing Diagram

```
T=0: DI water added → Timer starts
T=X: Homogenization
T=Y: CE injection → Time recorded
```

## Example Output

### Console

```
======================================================================
HOMOGENIZATION TIME STUDY - START
======================================================================

📡 Initializing ChemStation API...
✓ ChemStation connected

======================================================================
SAMPLE PREPARATION (Vial 10)
======================================================================

💧 Adding MeOH: 400 µL @ 1000 µL/min
⏳ Waiting 400s after MeOH...
💧 Adding DI water: 100 µL @ 1200 µL/min
⏱️  Timer started (T=0)
✓ Sample preparation complete

──────────────────────────────────────────────────────────────────────
MEASUREMENT 1/3 - Sample: 1_homogenization_test
──────────────────────────────────────────────────────────────────────

🌀 Homogenizing (T=15.2s)
📊 Starting analysis...
📊 Timing recorded: 245.67s
✓ Analysis running

======================================================================
✅ TIME STUDY COMPLETED
======================================================================
Results saved to: time_elution.txt
```

### Output File (`time_elution.txt`)

```
2024-01-15 14:30:25    1_homogenization_test    245.67
2024-01-15 14:35:12    2_homogenization_test    278.43
2024-01-15 14:40:08    3_homogenization_test    311.89
```

Format: `timestamp   sample_name   elapsed_time(s)`

## Configuration Options

### Sample Preparation

```python
meoh_volume: int = 400              # MeOH to add (µL)
di_volume: int = 100                # DI water to add (µL)
homog_volume: int = 290             # Aspirate volume (µL)

meoh_speed: int = 1000              # MeOH speed (µL/min)
di_speed: int = 1200                # DI water speed (µL/min)
homog_speed: int = 1000             # Homogenization speed (µL/min)

wait_after_meoh: int = 400          # Wait after MeOH (seconds)
homog_cycles: int = 2               # Mixing cycles
```

### Experiment

```python
vial_number: int = 10               # Sample vial
num_repetitions: int = 3            # Number of measurements
method_name: str = "Wait"           # CE method
output_file: str = "time_elution.txt"
```

### Sample Naming

```python
# Template with {i} placeholder
sample_name_template: str = "{i}_homogenization_test"
# Result: 1_homogenization_test, 2_homogenization_test, ...

# OR use prefix + suffix
sample_name_prefix: str = "S"
sample_name_suffix: str = "_A"
# Result: S1_A, S2_A, ...
```

### Logging

```python
log_file: str = "homogenization_study.log"
log_level: str = "INFO"             # DEBUG, INFO, WARNING, ERROR
log_to_console: bool = True
```

## Example Files

The `examples/homogenization study/` directory contains:

- **`homogenization_study.py`** - Main homogenization study implementation
- **`config.py`** - Configuration parameters

## See Also

- [Calibration Maker](calibration.md) - Calibration solution preparation
- [Sample Processor](sample_processor.md) - Batch sample processing
- [Getting Started](../getting-started.md)
- [ChemStation API](../api-reference/chemstation-api.md)
- [SIA Workflows](../api-reference/sia-workflows.md)
