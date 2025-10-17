# Validation Module - Input Validation and System State Checking

Comprehensive validation capabilities for ChemStation operations including file existence, system state, and prerequisite checking.

## Overview

The Validation module provides:

- **File System Validation**: Method and sequence file existence checking
- **Vial Management Validation**: Carousel vial presence and position verification
- **System State Validation**: Instrument readiness and operational state checking
- **Method Execution Validation**: Analysis startup and execution verification

**Validation Philosophy**: Fail fast - detect problems before they cause system errors

---

## File System Validation

### validate_sequence_name()

Validate that sequence file exists in specified directory.

```python
api.validation.validate_sequence_name(sequence, dir_path="_SEQPATH$")
```

**Parameters:**

- `sequence` (str): Sequence name (without .S extension)
- `dir_path` (str): Path to sequence directory (defaults to ChemStation sequence directory)

**Examples:**
```python
# Validate before loading
api.validation.validate_sequence_name("Protein_Analysis")

# Validate custom directory
api.validation.validate_sequence_name("TestSeq", "C:\\Custom\\Sequences\\")
```

**Notes:**

- Case-insensitive matching
- Automatically appends .S extension for checking
- Essential for preventing sequence loading failures

---

### validate_method()

Validate that CE method file exists in specified directory.

```python
api.validation.validate_method(method, dir_path="_METHODPATHS$", check_vials=False)
```

**Parameters:**

- `method` (str): Method name (without .M extension)
- `dir_path` (str): Path to method directory (defaults to ChemStation method directory)
- `check_vials` (bool): If True, also validates that method's vials are in carousel

**Examples:**
```python
# Basic method validation
api.validation.validate_method("CE_Protein_Analysis")

# Validate with vial checking
api.validation.validate_method("CE_Analysis", check_vials=True)

# Validate custom directory
api.validation.validate_method("TestMethod", "C:\\Methods\\Special\\")
```

**Notes:**

- Case-insensitive filename matching
- .M extension added automatically
- Vial validation extracts requirements from method XML

---

### validate_vials_in_method()

Validate that all vials required by the method are present in carousel.

```python
api.validation.validate_vials_in_method(method="_METHFILE$", dir_path="_METHODPATHS$")
```

**Parameters:**

- `method` (str): Method name or "_METHFILE$" for currently loaded method
- `dir_path` (str): Path to method directory

**Examples:**
```python
# Validate current loaded method
api.validation.validate_vials_in_method()

# Validate specific method
api.validation.validate_vials_in_method("CE_Protein_Analysis")
```

**Notes:**

- Extracts vial numbers from method XML file
- Validates all required vials are present in system
- Essential before method execution

---

## Vial Management Validation

### validate_vial_in_system()

Validate that specified vial is present somewhere in the CE system.

```python
api.validation.validate_vial_in_system(vial)
```

**Parameters:**

- `vial` (int): Vial position number to check (1-50)

**Examples:**
```python
# Validate before loading
api.validation.validate_vial_in_system(15)

# Validate sample list
sample_vials = [10, 11, 12, 15, 20]
for vial in sample_vials:
    api.validation.validate_vial_in_system(vial)
```

**Notes:**

- Checks all possible vial locations (carousel + lift positions)
- State "4" (out_system) indicates vial not detected
- Essential before any vial manipulation operations

---

### vial_in_position()

Validate that a vial is loaded at the specified lift position.

```python
api.validation.vial_in_position(position)
```

**Parameters:**

- `position` (str): Lift position to check ("inlet", "outlet", "replenishment")

**Examples:**
```python
# Check before injection
api.validation.vial_in_position("inlet")

# Verify setup before analysis
api.validation.vial_in_position("inlet")   # Sample vial
api.validation.vial_in_position("outlet")  # Waste vial
```

**Notes:**

- Essential before operations requiring vial contact
- Different from vial_in_system which checks any location
- Prevents electrode contact failures and injection errors

---

### get_vialtable()

Get comprehensive status of all carousel positions.

```python
vial_table = api.validation.get_vialtable()
```

**Returns:**

- `dict`: Dictionary mapping position numbers (1-48) to boolean presence status

**Examples:**
```python
# Get complete vial overview
vial_table = api.validation.get_vialtable()
occupied_positions = [pos for pos, present in vial_table.items() if present]
print(f"Vials present at positions: {occupied_positions}")

# Check specific positions
vial_table = api.validation.get_vialtable()
for pos in [10, 11, 12]:
    if vial_table[pos]:
        print(f"Vial at position {pos} ready")

# Find empty positions
empty_positions = [pos for pos, present in vial_table.items() if not present]
```

**Notes:**

- Includes positions 1-48 (position 49 handled separately)
- True means vial detected (any location in system)
- Useful for sequence planning and vial management

---

### list_vial_validation()

Validate that all vials in list are present in carousel system.

```python
api.validation.list_vial_validation(vials)
```

**Parameters:**

- `vials` (list): List of vial position numbers to validate

**Examples:**
```python
# Validate sequence vials
sequence_vials = [10, 11, 12, 15, 20]
api.validation.list_vial_validation(sequence_vials)

# Validate range of positions
api.validation.list_vial_validation(list(range(1, 25)))  # Check 1-24

# Handle validation errors
try:
    api.validation.list_vial_validation([1, 2, 3, 4, 5])
except VialError as e:
    print(f"Missing vials: {e}")
```

**Notes:**

- Efficient batch checking using single carousel query
- Reports all missing vials simultaneously
- Essential before sequence execution

---

## System State Validation

### validate_use_carousel()

Validate that carousel is available for vial operations.

```python
api.validation.validate_use_carousel(num_attempt=3)
```

**Parameters:**

- `num_attempt` (int): Number of validation attempts before raising error

**Examples:**
```python
# Check before vial operations
api.validation.validate_use_carousel()

# Check with custom attempts
api.validation.validate_use_carousel(num_attempt=5)

# Validate before batch operations
api.validation.validate_use_carousel()
for vial in vial_list:
    api.ce.load_vial_to_position(vial, "inlet")
```

**Notes:**

- "Idle" and "Run" states allow carousel operations
- Other states (Error, Maintenance) block carousel use
- Function waits 2 seconds between validation attempts

---

### validate_method_run()

Validate that method execution started successfully.

```python
api.validation.validate_method_run()
```

**Examples:**
```python
# Validate after method start
api.method.run("Sample001")
api.validation.validate_method_run()  # Confirm it started

# Use in automated workflows
try:
    api.method.execution_method_with_parameters(15, "CE_Method", "Sample")
    api.validation.validate_method_run()
    print("Method started successfully")
except MethodError:
    print("Method failed to start - check instrument status")
```

**Notes:**

- Should be called shortly after method start commands
- _MethodOn=1 indicates successful method execution
- Essential for detecting silent method startup failures

---

## Utility Functions

### extract_vials_from_xml()

Extract vial numbers from CE method XML configuration file.

```python
vials = api.validation.extract_vials_from_xml(method_path)
```

**Parameters:**

- `method_path` (str): Path to the CE method directory (.M folder)

**Returns:**

- `list`: Sorted list of unique vial position numbers (integers)

**Examples:**
```python
# Extract vials from method
vials = api.validation.extract_vials_from_xml("C:/Methods/CE_Protein.M")
print(f"Method requires vials: {vials}")

# Use with method validation
method_dir = os.path.join(methods_path, "CE_Protein.M")
required_vials = api.validation.extract_vials_from_xml(method_dir)
api.validation.list_vial_validation(required_vials)
```

**Notes:**

- Automatically constructs path to method XML file
- Searches for all `<Vialnumber></Vialnumber>` tags
- Filters negative vial numbers (-1, etc.)
- Returns empty list on file read errors

---

## Practical Examples

### Pre-Analysis Validation

```python
# Complete validation before starting analysis
def validate_analysis_ready(method_name, sample_vial):
    try:
        # Check method exists
        api.validation.validate_method(method_name, check_vials=True)
        
        # Check sample vial present
        api.validation.validate_vial_in_system(sample_vial)
        
        # Check carousel available
        api.validation.validate_use_carousel()
        
        print("✓ All validations passed - ready to start")
        return True
        
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return False

# Use before analysis
if validate_analysis_ready("CE_Protein", 15):
    api.method.execution_method_with_parameters(15, "CE_Protein", "Sample_001")
```

### Batch Validation

```python
# Validate entire batch before starting
sample_vials = [10, 11, 12, 15, 20]
methods = ["CE_Analysis", "CE_QC"]

# Check all vials
api.validation.list_vial_validation(sample_vials)

# Check all methods
for method in methods:
    api.validation.validate_method(method)

print("Batch validation complete")
```