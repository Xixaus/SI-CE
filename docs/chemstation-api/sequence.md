# Sequence Module - Batch Analysis Management

Management and execution of ChemStation sequences for automated batch analysis.

## Overview

The Sequence module provides:

- **Sequence file operations**: Load and save sequence files (.S files)
- **Table editing**: Modify sequence parameters row by row
- **Excel integration**: Import sequence data from spreadsheets
- **Batch control**: Start, pause, and resume sequence execution

**File Format**: ChemStation .S sequence files
**Default Directory**: ChemStation sequence directory (_SEQPATH$)

---

## Sequence File Operations

### load_sequence()

Load an existing sequence from file.

```python
api.sequence.load_sequence(seq_name, seq_dir="_SEQPATH$")
```

**Parameters:**

- `seq_name` (str): Sequence filename (without .S extension)
- `seq_dir` (str): Directory containing sequence files (defaults to ChemStation sequence directory)

**Examples:**
```python
# Load standard sequence
api.sequence.load_sequence("Protein_Analysis_Batch")

# Load from custom directory
api.sequence.load_sequence("TestSeq", "C:\\Custom\\Sequences\\")

# Load daily QC sequence
api.sequence.load_sequence("Daily_QC_2024")
```

**Notes:**

- Sequence loading overwrites current sequence in memory
- All unsaved changes to current sequence are lost
- Sequence parameters become active immediately

---

### save_sequence()

Save current sequence to file.

```python
api.sequence.save_sequence(seq_name="_SEQFILE$", seq_dir="_SEQPATH$")
```

**Parameters:**

- `seq_name` (str): Filename for saved sequence (defaults to current sequence name)
- `seq_dir` (str): Directory for saving sequence (defaults to ChemStation sequence directory)

**Examples:**
```python
# Save with new name
api.sequence.save_sequence("Modified_Protein_Sequence")

# Overwrite current sequence
api.sequence.save_sequence()

# Save to custom location
api.sequence.save_sequence("Backup_Sequence", "D:\\Backups\\")
```

**Notes:**

- Saved sequence includes all table data and parameters
- Existing files with same name are overwritten
- .S extension added automatically

---

## Sequence Table Editing

### modify_sequence_row()

Modify parameters in specific sequence table row.

```python
api.sequence.modify_sequence_row(row, vial_sample="", method="", sample_name="", sample_info="", data_file_name="")
```

**Parameters:**

- `row` (int): Row number in sequence table (1-based indexing)
- `vial_sample` (str): Carousel position for sample vial (1-48)
- `method` (str): CE method name (without .M extension)
- `sample_name` (str): Descriptive sample name for identification
- `sample_info` (str): Additional sample metadata and notes
- `data_file_name` (str): Custom data filename (optional)

**Examples:**
```python
# Modify sample vial and method
api.sequence.modify_sequence_row(
    row=1,
    vial_sample="15",
    method="CE_Protein_Analysis"
)

# Update sample information only
api.sequence.modify_sequence_row(
    row=3,
    sample_name="Unknown_Sample_001",
    sample_info="Customer sample, urgent analysis"
)

# Complete row modification
api.sequence.modify_sequence_row(
    row=5,
    vial_sample="22",
    method="MEKC_SmallMolecules",
    sample_name="Caffeine_Standard",
    sample_info="1mg/mL in water"
)
```

**Notes:**

- Only specified parameters are modified (empty parameters remain unchanged)
- Sequence must be loaded before modification
- Changes made to memory - use `save_sequence()` to persist
- Row numbering starts from 1

---

## Excel Integration

### prepare_sequence_table()

Import and create sequence table from Excel spreadsheet.

```python
api.sequence.prepare_sequence_table(excel_file_path, sequence_name=None, sheet_name=0, vial_column=None, method_column=None, filename_column=None, sample_name_column=None, sample_info_column=None, replicate_column=None)
```

**Parameters:**

- `excel_file_path` (str): Full path to Excel file containing sequence data
- `sequence_name` (str): Existing sequence to load before modification (optional)
- `sheet_name` (int): Excel worksheet index to read (0-based, default: first sheet)
- `vial_column` (str): Excel column name containing vial positions
- `method_column` (str): Excel column name containing method names
- `sample_name_column` (str): Excel column name containing sample names
- `sample_info_column` (str): Excel column name containing sample metadata
- `filename_column` (str): Excel column name containing custom filenames
- `replicate_column` (str): Excel column name containing replicate information

**Examples:**
```python
# Basic import
api.sequence.prepare_sequence_table(
    excel_file_path="sample_list.xlsx",
    vial_column="Vial",
    method_column="Method",
    sample_name_column="Sample"
)

# Full import with all columns
api.sequence.prepare_sequence_table(
    excel_file_path="complex_sequence.xlsx",
    sequence_name="Research_Project_2024",
    sheet_name=0,
    vial_column="Vial_Position",
    method_column="CE_Method",
    sample_name_column="Sample_ID",
    sample_info_column="Description",
    filename_column="Data_Name",
    replicate_column="Rep_Number"
)

# Import from second worksheet
api.sequence.prepare_sequence_table(
    excel_file_path="batch_data.xlsx",
    sheet_name=1,
    vial_column="Position",
    method_column="Analysis_Method",
    sample_name_column="Sample_Name"
)
```

**Requirements:**

- Excel must be installed on the system
- File should not be open during import
- Column names must match exactly (case-sensitive)
- Referenced methods must exist in method directory

**Notes:**

- Excel application briefly visible during processing
- Temporary Excel file created during processing
- Sequence automatically saved after import
- Method names validated against method directory

---

## Sequence Execution Control

### start()

Start execution of the current sequence.

```python
api.sequence.start()
```

**Examples:**
```python
# Start loaded sequence
api.sequence.load_sequence("Daily_Analysis")
api.sequence.start()
```

**Notes:**

- Sequence must be loaded and validated before starting
- Instrument enters sequence mode with limited manual control
- Progress monitored via system status methods

---

### pause()

Pause the currently running sequence.

```python
api.sequence.pause()
```

**Examples:**
```python
# Pause during execution
api.sequence.pause()
```

**Notes:**

- Current analysis completes before pausing
- Sequence stops before starting next sample
- Manual operations possible while paused

---

### resume()

Resume a paused sequence from where it stopped.

```python
api.sequence.resume()
```

**Examples:**
```python
# Resume after pause
api.sequence.resume()
```

**Notes:**

- Resumes from next unprocessed sample
- All sequence parameters remain unchanged
- Instrument returns to automated sequence mode

---

## Practical Examples

### Manual Sequence Creation

```python
# Load existing sequence or create new
api.sequence.load_sequence("Daily_QC")

# Add samples
api.sequence.modify_sequence_row(
    row=1,
    vial_sample="1",
    method="CE_QC",
    sample_name="QC_Standard",
    sample_info="Daily system suitability"
)

api.sequence.modify_sequence_row(
    row=2,
    vial_sample="10",
    method="CE_Analysis",
    sample_name="Sample_001",
    sample_info="Customer sample"
)

# Save and run
api.sequence.save_sequence("Daily_QC_Modified")
api.sequence.start()
```

### Excel-Based Sequence

```python
# Import from Excel
api.sequence.prepare_sequence_table(
    excel_file_path="protein_samples.xlsx",
    vial_column="Vial",
    method_column="Method",
    sample_name_column="Sample_ID",
    sample_info_column="Notes"
)

# Start batch analysis
api.sequence.start()

# Monitor and control
while api.system.method_on():
    print("Sequence running...")
    time.sleep(60)
```