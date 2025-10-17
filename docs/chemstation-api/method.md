# Methods Module - CE Method Management

Management and execution of ChemStation CE methods for analytical control.

## Overview

The Methods module provides:

- **Method file operations**: Load and save CE methods (.M files)
- **Method execution**: Run methods with standard or custom parameters
- **Parameter control**: Modify sample information without editing method files

**File Format**: ChemStation .M method files
**Default Directory**: ChemStation method directory (_METHPATH$)

---

## Method File Operations

### load()

Load CE method from file into ChemStation active memory.

```python
api.method.load(method_name, method_path="_METHODPATHS$")
```

**Parameters:**

- `method_name` (str): Method filename without .M extension
- `method_path` (str): Directory containing methods (defaults to ChemStation method directory)

**Examples:**
```python
# Load standard analysis method
api.method.load("CE_Protein_Analysis")

# Load method from custom directory
api.method.load("TestMethod", "C:\\Custom\\Methods\\")

# Load development method
api.method.load("MEKC_SmallMolecules")
```

**Notes:**

- Method loading overwrites current instrument settings
- All instrument parameters updated (voltage, temperature, vial assignments)
- Previous unsaved changes are lost

---

### save()

Save current method with specified name and optional comment.

```python
api.method.save(method_name="_METHFILE$", method_path="_METHODPATHS$", comment="\" \"")
```

**Parameters:**

- `method_name` (str): Filename for saved method (defaults to current method name)
- `method_path` (str): Directory for saving method (defaults to ChemStation method directory)  
- `comment` (str): Optional comment describing method changes

**Examples:**
```python
# Save current method with new name
api.method.save("Optimized_CE_Method", comment="Improved resolution")

# Overwrite current method
api.method.save()

# Save with detailed comment
api.method.save("Modified_Protein_v3", comment="Voltage increased to 30kV, temp reduced to 23C")
```

**Notes:**

- Existing files with same name are overwritten without warning
- Comment stored in method file metadata
- .M extension added automatically

---

## Method Execution

### run()

Execute current method and save data with specified name.

```python
api.method.run(data_name, data_dir="_DATAPATH$")
```

**Parameters:**

- `data_name` (str): Name for the data file (without extension)
- `data_dir` (str): Directory for data storage (defaults to ChemStation data directory)

**Examples:**
```python
# Run analysis with descriptive name
api.method.run("Protein_Sample_001")

# Run QC standard with custom directory
api.method.run("QC_Standard_Daily", "C:\\QC_Data\\")

# Run blank analysis
api.method.run("Blank_Run_20241201")
```

**Requirements:**

- Method must be loaded before execution
- Required vials must be present and positioned
- Instrument must be in ready state

**Notes:**

- Uses existing method parameters (vials, sample info, conditions)
- Only data filename changes
- Progress monitored via `system.method_on()`

---

### execution_method_with_parameters()

Execute CE method with custom vial and sample parameters.

```python
api.method.execution_method_with_parameters(vial, method_name, sample_name="", comment="", subdirectory_name="")
```

**Parameters:**

- `vial` (int): Carousel position for sample (1-48)
- `method_name` (str): Method to execute (without .M extension)
- `sample_name` (str): Descriptive sample name for data file and records
- `comment` (str): Path to text file containing method comment/description
- `subdirectory_name` (str): Optional subdirectory for data organization

**Examples:**
```python
# Analyze protein sample
api.method.execution_method_with_parameters(
    vial=15,
    method_name="CE_Protein_Analysis", 
    sample_name="BSA_Standard_1mg_ml"
)

# Run with comment file and subdirectory
api.method.execution_method_with_parameters(
    vial=22,
    method_name="Development_CZE",
    sample_name="Test_Sample_v3",
    comment="C:\\Comments\\protein_method.txt",
    subdirectory_name="Method_Development"
)

# Simple unknown sample analysis
api.method.execution_method_with_parameters(
    vial=30,
    method_name="CE_Screening",
    sample_name="Unknown_001"
)
```

**Process:**

1. Creates temporary method register (TemporaryRegisterMethod)
2. Loads specified method and copies parameters
3. Modifies vial number and sample information
4. Executes analysis with custom parameters
5. Data saved with automatic filename generation

**Notes:**

- Data filename generated automatically with timestamp
- Sample information stored in data file metadata
- Temporary register cleaned up after execution
- Vial must be physically present in carousel