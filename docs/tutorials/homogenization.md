# Homogenization Study - Time Analysis

Automated measurement of homogenization timing for CE sample preparation optimization.

## Overview

Measures elapsed time from sample preparation to CE injection to determine optimal homogenization protocols. Records timing data for three types of experiments.

## Experiment Types

**Time Elution Experiment**
- Adds MeOH and DI water to sample
- Measures time from preparation start to CE injection
- Configurable repetitions with automatic timing

**Standards Analysis**
- Runs reference standards for validation
- Optional multiple measurements

**Full Homogenization Samples**
- Processes pre-homogenized reference samples
- Comparison against time-series data

## Configuration

```python
@dataclass
class Config:
    # Volumes (µL)
    meoh_volume: int = 400
    di_volume: int = 100
    homog_volume: int = 290
    
    # Timing
    wait_after_meoh: int = 400  # seconds
    
    # Experiment
    vial_number: int = 10
    num_repetitions: int = 3
    method_name: str = "Wait"
```

## Workflow

1. **Preparation:** MeOH addition → waiting period → DI water addition
2. **Timing:** Automatic time recording from preparation start
3. **Homogenization:** Liquid mixing before CE injection
4. **Analysis:** CE method execution with timing data capture
5. **Output:** Time records saved to file

## Usage

```python
from homogenization_time import SampleProcessor, Config

config = Config()
config.num_repetitions = 5
processor = SampleProcessor(config)

# Run time study
run_time_elution_experiment(processor)
```

## Output Format

**Time Records:**
```
2024-01-15 14:30:25    Sample_1_homog    245.67
2024-01-15 14:35:12    Sample_2_homog    278.43
```

**Features:**
- Comment file validation (UTF-8, .txt format)
- Method and vial validation
- Detailed logging with error handling
- Template-based sample naming