# Sample Processor

Automated batch sample processing with Excel integration and parallel workflow optimization.

## Overview

Processes multiple samples automatically using Excel input file. Optimizes timing by preparing the next sample during current CE analysis, with individual incubation timing for each sample.

## Quick Start

### 1. Prepare Excel File

Create an Excel file with sample parameters:

| Vial | MeOH | DI  | Method    | Name     |
| ---- | ---- | --- | --------- | -------- |
| 10   | 400  | 100 | CE_Method | Sample_1 |
| 11   | 350  | 150 | CE_Method | Sample_2 |
| 12   | 400  | 100 | CE_Method | Sample_3 |

**Columns:**

- `Vial` - Vial position
- `MeOH` - MeOH volume (µL)
- `DI` - DI water volume (µL)
- `Method` - CE method name
- `Name` - Sample name

### 2. Configure

Edit `examples/sample processor/config.py`:

```python
@dataclass
class ProcessorConfig:
    # Excel file
    excel_file_path: str = r"C:\SIA-CE\samples.xlsx"

    # Column names
    column_vial: str = "Vial"
    column_meoh: str = "MeOH"
    column_di: str = "DI"
    column_method: str = "Method"
    column_name: str = "Name"

    # SIA ports
    meoh_port: int = 5
    di_port: int = 3

    # Timing
    waiting_time_after_meoh: int = 450      # Seconds (7.5 min)
    time_prepare_and_homogenization: float = 2.0  # Minutes

    # Speeds (µL/min)
    batch_fill_speed_meoh: int = 1000
    batch_fill_speed_di: int = 1200

    # Homogenization
    homogenization_volume: int = 320
    homogenization_cycles: int = 3

    # Batch
    initial_batch_size: int = 3
```

### 3. Run

```bash
cd examples/sample\ processor/
python sample_processor.py
```

## How It Works

### Workflow

1. **Initial Batch** (first 3 samples):

   - Add MeOH to all 3 samples
   - Wait individually (each has own timer)
   - Add DI water after precise incubation
   - Homogenize all 3
2. **Analysis Loop** (for each sample):

   - Homogenize before analysis
   - Start CE analysis
   - **During analysis**: Prepare next sample (MeOH → wait → DI → homogenize)
   - Repeat for all samples
3. **Parallel Processing**: Next sample is prepared while current analysis runs, minimizing idle time.

### Individual Timing

Each sample tracks its own MeOH addition time:

```
Sample 1: MeOH added at T=0  → DI at T=450s
Sample 2: MeOH added at T=30 → DI at T=480s
Sample 3: MeOH added at T=60 → DI at T=510s
```

This ensures precise incubation for every sample.

## Example Output

```
======================================================================
SAMPLE PROCESSOR - START
======================================================================

📁 Loading data from: samples.xlsx
✓ Loaded 10 rows

======================================================================
PREPARING FIRST 3 SAMPLES
======================================================================

💧 FILLING MeOH
  → Vial 10: 400 µL MeOH
  → Vial 11: 350 µL MeOH
  → Vial 12: 400 µL MeOH

💧 FILLING DI WATER (with individual incubation)
  → Vial 10: wait 30.2s, add 100 µL DI
  → Vial 11: wait 18.5s, add 150 µL DI

🌀 Homogenizing all 3 samples
✓ Initial batch complete

======================================================================
PROCESSING SAMPLE 1/10 - Sample_1
======================================================================

🌀 Homogenize → 📊 Start analysis → ▶️ Running

🔄 PREPARING NEXT SAMPLE (4/10)
  Vial 13: MeOH → wait 450s → DI → homogenize
✓ Sample 4 ready

======================================================================
✅ ALL 10 SAMPLES SUCCESSFULLY PROCESSED
======================================================================
```

## Configuration Options

### Excel Integration

```python
excel_file_path: str = r"C:\SIA-CE\samples.xlsx"
sheet_name: str = "Sheet1"

# Column names (customize if needed)
column_vial: str = "Vial"
column_meoh: str = "MeOH"
column_di: str = "DI"
column_method: str = "Method"
column_name: str = "Name"
```

### Sample Preparation

```python
# SIA valve ports
meoh_port: int = 5
di_port: int = 3

# Filling speeds (µL/min)
batch_fill_speed_meoh: int = 1000       # MeOH speed
batch_fill_speed_di: int = 1200         # DI water speed

# Timing
waiting_time_after_meoh: int = 450      # Wait after MeOH (seconds)
time_prepare_and_homogenization: float = 2.0  # Minutes before analysis end

# Initial batch
initial_batch_size: int = 3             # Number of samples to prepare initially
```

### Homogenization

```python
homogenization_volume: int = 320        # Aspirate volume (µL)
homogenization_cycles: int = 3          # Number of mixing cycles
homogenization_aspirate_speed: int = 1000  # µL/min
homogenization_dispense_speed: int = 1000  # µL/min
homogenization_clean_after: bool = False
```

### ChemStation

```python
default_method_name: str = "Wait"       # Default CE method
ready_timeout: int = 10                 # Timeout for ready status (seconds)
verbose_chemstation: bool = False       # Verbose ChemStation output
```

### Logging

```python
log_file: str = "sample_processor.log"
log_level: str = "DEBUG"                # DEBUG, INFO, WARNING, ERROR
log_to_console: bool = True             # Print to console
show_progress_bars: bool = True         # Show tqdm progress bars
detailed_logging: bool = True           # Detailed operation logs
```

## Key Features

### Individual Incubation Timing

Each sample tracks its own MeOH addition time for precise incubation.

### Parallel Processing

Next sample is prepared during current CE analysis to minimize idle time.

### Separate Flow Rates

Different speeds for MeOH and DI water optimize preparation.

## Troubleshooting

**Excel File Not Found**
→ Check `excel_file_path` in config.py

**Missing Columns**
→ Ensure Excel has all required columns (case-sensitive)

**Timing Issues**
→ Increase `time_prepare_and_homogenization` or verify incubation times

**Vial Validation Fails**
→ Check vial numbers in Excel are valid for autosampler

## Best Practices

1. **Test with small batches** - Start with 3-5 samples to validate workflow
2. **Verify timing** - Ensure incubation times are appropriate for your samples
3. **Check methods** - Validate all CE methods exist before starting
4. **Monitor first run** - Watch the first complete cycle to verify timing
5. **Log files** - Keep logs for troubleshooting and documentation

## Example Files

The `examples/sample processor/` directory contains:

- **`sample_processor.py`** - Main processor implementation
- **`config.py`** - Configuration parameters
- **`sample_data_example.csv`** - Example input data (convert to Excel)
- **`README.md`** - Detailed documentation with examples

For more details, see the [README.md](../../examples/sample%20processor/README.md) in the examples directory.

## See Also

- [Calibration Maker](calibration.md) - Calibration solution preparation
- [Homogenization Study](homogenization.md) - Timing optimization
- [Getting Started](../getting-started.md)
