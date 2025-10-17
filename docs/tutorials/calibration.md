# Calibration Solution Maker

Automated preparation of calibration solutions from Excel file using volumetric dilution.

## Quick Start

### 1. Prepare Excel File

Create an Excel file with these columns:

| Vial | Concentration | Volume |
|------|---------------|--------|
| 10   | 0.0           | 1000   |
| 11   | 0.5           | 1000   |
| 12   | 1.0           | 1000   |
| 13   | 5.0           | 1000   |
| 14   | 10.0          | 1000   |
| 15   | 50.0          | 1000   |
| 16   | 100.0         | 1000   |

**Columns:**
- `Vial` - Vial position
- `Concentration` - Target concentration (mg/L)
- `Volume` - Total volume (µL)

### 2. Configure

Edit `examples/make calibration/config.py`:

```python
@dataclass
class CalibrationConfig:
    excel_file_path: str = r"C:\SIA-CE\calibration_data.xlsx"

    standard_concentration: float = 100.0    # Stock concentration (mg/L)
    standard_port: int = 7                   # Valve port for standard
    solvent_port: int = 3                    # Valve port for solvent

    standard_fill_speed: int = 2000          # µL/min
    solvent_fill_speed: int = 2000           # µL/min

    syringe_port: str = "COM3"
    syringe_size: int = 1000
```

### 3. Run

```bash
cd examples/make\ calibration/
python calibration_maker.py
```

## How It Works

### Dilution Calculation

Uses the equation: **C₁ × V₁ = C₂ × V₂**

**Example:**
```
Target: 5.0 mg/L in 1000 µL
Stock:  100.0 mg/L

Standard needed: (5.0 × 1000) / 100.0 = 50 µL
Solvent needed:  1000 - 50 = 950 µL
```

### Preparation Process

For each calibration point:
1. Flush transfer line
2. Add standard solution (if concentration > 0)
3. Add solvent to reach total volume
4. Move to next vial

**Special cases:**
- Blank (0.0): Only solvent
- 100% stock: Only standard

## Example Output

```
======================================================================
CALIBRATION MAKER - START
======================================================================

📡 Initializing ChemStation API...
✓ ChemStation connected

📁 Loading data from: calibration_data.xlsx
✓ Loaded 7 rows

======================================================================
VOLUME CALCULATION
======================================================================

 Vial  Concentration  Volume  standard_volume  solvent_volume
   10            0.0    1000              0.0          1000.0
   11            0.5    1000              5.0           995.0
   12            1.0    1000             10.0           990.0
   13            5.0    1000             50.0           950.0
   14           10.0    1000            100.0           900.0
   15           50.0    1000            500.0           500.0
   16          100.0    1000           1000.0             0.0

Proceed with calibration solution preparation? (y/n): y

======================================================================
SOLUTION PREPARATION
======================================================================

Preparing calibration solutions: 100%|████████| 7/7 [02:24<00:00]

✅ ALL 7 CALIBRATION SOLUTIONS PREPARED SUCCESSFULLY

💾 Results saved to: calibration_results.xlsx
```

## Configuration Options

### Excel Settings

```python
excel_file_path: str = r"C:\SIA-CE\calibration_data.xlsx"
sheet_name: str = "Sheet1"

# Customize column names
column_vial: str = "Vial"
column_concentration: str = "Concentration"
column_volume: str = "Volume"
```

### Solution Parameters

```python
standard_concentration: float = 100.0    # Stock concentration
standard_port: int = 7                   # Valve position for standard
solvent_port: int = 3                    # Valve position for solvent

standard_fill_speed: int = 2000          # µL/min
solvent_fill_speed: int = 2000

transfer_line_volume: int = 240          # µL
flush_needle_volume: int = 10            # µL
```

### System Options

```python
perform_system_init: bool = True         # Clean before start
validate_vials: bool = True              # Check vial positions
require_user_confirmation: bool = True   # Ask before preparation
show_progress_bars: bool = True
```

### Logging

```python
log_file: str = "calibration_preparation.log"
log_level: str = "INFO"                  # DEBUG, INFO, WARNING, ERROR
log_to_console: bool = True
```

## Advanced Features

### Custom Column Names

```python
column_vial: str = "Position"
column_concentration: str = "Conc_mgL"
column_volume: str = "Total_Vol"
```

## Troubleshooting

### Excel File Not Found
```
FileNotFoundError: Excel file not found
```
→ Check `excel_file_path` in config.py

### Missing Columns
```
ValueError: Missing columns in Excel file: ['Concentration']
```
→ Ensure Excel has all required columns (case-sensitive)

### Target Exceeds Stock
```
ValueError: Target concentration 150.0 exceeds stock 100.0
```
→ Reduce target concentrations or increase stock concentration

### COM Port Error
```
SerialException: could not open port 'COM3'
```
→ Check device connection and COM port in Device Manager

## Best Practices

1. **Include blank** (0.0 concentration) to check for contamination
2. **Include replicates** for statistical validation
3. **Cover your range** - from detection limit to upper validation
4. **Validate stock** - check concentration, expiration, storage
5. **Clean between runs** - set `perform_system_init: True`

## Files Location

`examples/make calibration/`
- `config.py` - Configuration
- `calibration_maker.py` - Main script
- `calibration_example.xlsx` - Example template

## Example Files

The `examples/make calibration/` directory contains:

- **`calibration_maker.py`** - Main calibration maker implementation
- **`config.py`** - Configuration parameters
- **`calibration_example.xlsx`** - Example Excel template

## See Also

- [Sample Processor](sample_processor.md) - Batch sample processing
- [Homogenization Study](homogenization.md) - Timing optimization
- [Getting Started Guide](../getting-started.md)
- [ChemStation API](../api-reference/chemstation-api.md)
- [SIA Workflows](../api-reference/sia-workflows.md)
