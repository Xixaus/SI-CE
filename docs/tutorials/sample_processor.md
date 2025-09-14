# Advanced Sample Processing - Excel Integration

Batch processing system that reads sample parameters from Excel and performs automated preparation with parallel processing.

## Overview

Processes multiple samples automatically using Excel input file. Optimizes timing by preparing next sample during current CE analysis. Each sample gets individual incubation timing.

## Key Features

- **Excel Integration:** Direct reading of sample parameters
- **Parallel Processing:** Next sample preparation during analysis
- **Individual Timing:** Per-sample incubation periods
- **Separate Flow Rates:** Different speeds for MeOH and DI water

## Configuration

```python
@dataclass
class ProcessorConfig:
    # Excel file
    excel_file_path: str = "samples.xlsx"
    
    # Column mapping
    column_vial: str = "Vial"
    column_meoh: str = "MeOH" 
    column_di: str = "DI"
    column_method: str = "Method"
    column_name: str = "Name"
    
    # Timing
    waiting_time_after_meoh: int = 450  # seconds
    
    # Flow rates
    batch_fill_speed_meoh: int = 1000  # µL/min
    batch_fill_speed_di: int = 1200    # µL/min
    
    # Homogenization
    homogenization_volume: int = 320
    homogenization_cycles: int = 3
```

## Excel Format

| Vial | MeOH | DI | Method | Name |
|------|------|----|---------|----|
| 10 | 400 | 100 | CE_Method | Sample_1 |
| 11 | 350 | 150 | CE_Method | Sample_2 |

## Workflow

1. **Initial Batch:** MeOH to first 3 samples → individual incubation → DI water addition
2. **Analysis Loop:** Homogenize → start CE analysis → prepare next sample during analysis
3. **Parallel Processing:** Next sample preparation optimally timed during current analysis

## Usage

```python
from config import ProcessorConfig
from sample_processor import SampleProcessor

config = ProcessorConfig()
config.excel_file_path = "my_samples.xlsx"

processor = SampleProcessor(config, chemstation, sia_methods)
processor.process_all_samples()
```

## Technical Details

**Individual Incubation:**
- Each sample tracks its own MeOH addition time
- DI water added after precise incubation period
- Eliminates over-incubation

**Timing Optimization:**
- Next sample prepared when 2 minutes remain in current analysis
- Minimizes idle time between samples
- Automatic progress coordination

**Validation:**
- Excel file and column validation
- Method and vial existence checking
- Comprehensive error handling and logging