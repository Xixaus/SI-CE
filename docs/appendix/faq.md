# Frequently Asked Questions

Common questions and solutions for SI-CE integration workflows.

## 🚀 Getting Started

### What is SI-CE?

**Quick Answer:** SI-CE is a Python package that integrates Sequential Injection (SI) with Capillary Electrophoresis (CE) through Agilent ChemStation for complete laboratory automation.

**Detailed Explanation:** 
This comprehensive system enables:

- **Automated sample preparation** - Streamlined sample handling and preparation workflows
- **CE instrument control** - Direct communication with ChemStation for method execution
- **Batch analysis workflows** - Process multiple samples with minimal manual intervention  
- **Complete analytical automation** - End-to-end automation from sample prep to data analysis

**Related Topics:** [Getting Started](../getting-started.md), [System Architecture](../index.md)

---

### What hardware is compatible?

**Quick Answer:** The system supports Agilent CE systems with OpenLab ChemStation C.01.07 SR2 and VICI/Valco valve selectors.

**Detailed Explanation:**

**Supported ChemStation Systems:**

- Developed and tested on OpenLab ChemStation ver. C.01.07 SR2 [255] with CE 7100
- Interface functionality tested on other ChemStation versions, but full compatibility is not guaranteed
- Not compatible with OpenLab CDS 2.x due to absence of command processor and lack of macro support

**SIA Components:**

- VICI/Valco valve selectors and switching systems
- Compatible third-party devices with similar command protocols
- Additional components can be integrated in future releases


---

### Do I need programming experience?

**Quick Answer:** Basic Python knowledge is helpful but not required - the package includes high-level methods and copy-paste examples.

**Detailed Explanation:**

The package is designed for accessibility with:

- **High-level workflow methods** - Simple functions for complex operations
- **Pre-built analytical procedures** - Ready-to-use templates for common analyses
- **Copy-paste examples** - Working code snippets you can adapt immediately
- **Comprehensive documentation** - Detailed guides and tutorials

**AI-Assisted Development:** You can leverage generative AI tools (ChatGPT, Claude, etc.) by providing them with the repository link. These tools can help you create custom methods tailored to your specific needs. However, always thoroughly test any AI-generated code before implementation in production workflows.

**Code Example:**
```python
# Simple one-line operations
workflow.continuous_fill(vial=15, volume=1500, solvent_port=5)
workflow.homogenize_sample(vial=15, speed=1000, time=30)
```

**Related Topics:** [First Analysis Tutorial](../tutorials/first-analysis.md), [Basic Operations](../sia-api/basic-operations.md)

---

## 🔌 Communication and Control

### How can I monitor ChemStation communication?

**Quick Answer:** Enable verbose logging or monitor communication files directly to see all commands and responses.

**Detailed Explanation:**
The system uses file-based communication that can be monitored in real-time for debugging and optimization.

**Code Example:**
```python
# Enable detailed logging
config = CommunicationConfig(verbose=True)
api = ChemstationAPI(config)

# Monitor communication files directly (PowerShell)
# Get-Content "communication_files\command" -Wait
```

**Related Topics:** [File Protocol](../chemstation-api/file-protocol.md), [Troubleshooting](../chemstation-api/troubleshooting.md)

---

### Why does communication occasionally drop?

**Quick Answer:** Communication drops typically occur when error dialogs appear in ChemStation or when timeout conditions aren't met.

**Detailed Explanation:**
Communication drops have been observed in specific cases:

1. **Error dialog appears in ChemStation:**

    May occur when starting a method while another is still running
    Timeout not met for command execution (see `validation.get_vialtable()` which uses higher timeout for longer macro execution)
    After closing the error dialog, operation can continue
    Always use validation before commands to ensure proper timing

2. **Communication deadlock:**

    Some commands called rapidly in succession may occasionally not receive responses
    Common with `system.status()` when checking status repeatedly
    Implementation includes retry logic (3 attempts before error)
    If this occurs, simply restart the script

**Code Example:**
```python
# Robust status checking with retry logic
def get_status_with_retry(api, max_retries=3):
    for attempt in range(max_retries):
        try:
            return api.system.status()
        except TimeoutError:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
```

**Related Topics:** [Error Handling](../api-reference/error-handling.md), [Communication Protocol](../chemstation-api/file-protocol.md)

---

### Can I send custom commands to ChemStation?

**Quick Answer:** Yes, use the `send()` method to execute any valid ChemStation command directly.

**Detailed Explanation:**
The API provides direct access to ChemStation's command processor for advanced operations not covered by high-level methods.

**Code Example:**
```python
# Read current oven temperature
response = api.send('response$ = VAL$(ObjHdrVal(RCCE1Status[1], "Temperature_actual"))')
print(f"Current oven temperature: {response}°C")

# Get method path
method_path = api.send("response$ = _METHPATH$")
print(f"Active method: {method_path}")

# Execute custom macro
api.send('macro "C:\\custom_macro.mac"; custom_procedure 15, "parameter"')
```

**Related Topics:** [ChemStation Macros](../tutorials/chemstation-macros.md), [API Reference](../api-reference/chemstation-api.md)

---

## ⚗️ Capillary Electrophoresis Operations

### Unable to load vials into the carousel

**Quick Answer:** Vial loading fails when the CE system is in an incompatible state or when pressure is applied during run.

**Detailed Explanation:**

**System State Issues:**

The carousel may be locked in certain states:
- **IDLE state**: Normal operation - carousel accessible    
- **RUN state**: Analysis in progress - carousel may be locked
- **Apply pressure in run**: If pressure is applied at any time (including additional pressure during analysis), the carousel is locked
- **Other states**: Carousel typically locked for safety

**Missing Vial Validation:**
The system cannot locate the specified vial in the carousel.

**Code Example:**
```python
# Wait for appropriate system state before vial operations
while not api.is_carousel_available():
    time.sleep(5)  # Wait for system to reach appropriate state

# Validate all required vials are present before starting
required_positions = [1, 2, 3, 5, 8]
missing_vials = carousel.validate_vials(required_positions)
if missing_vials:
    raise ValueError(f"Missing vials at positions: {missing_vials}")
```

**Related Topics:** [Basic Operations](../chemstation-api/basic-operations.md), [Validation Module](../api-reference/chemstation-validation.md)

---

### Can I modify method parameters programmatically?

**Quick Answer:** Yes, method parameters can be modified using ChemStation registry commands, though this feature is experimental.

**Detailed Explanation:**
Method parameters are stored in RC{module}Method[1] registers and can be modified directly. During RC.Net log analysis (see ChemStation Macros tutorial), commands for parameter modification were discovered. When these commands are executed, parameters are successfully updated. However, this approach has not been thoroughly tested.

**Code Example:**
```python
# Example: Modify separation voltage (experimental - test thoroughly)
api.send('SetObjHdrVal RCCE1Method[1], "Voltage", 10')

# Upload method, modify, download
api.send('UploadRCMethod CE1')
api.send('SetObjHdrVal RCCE1Method[1], "Temperature", 25')
api.send('DownloadRCMethod CE1')
```

**Additional Resources:**

- See tutorial/chemstation_scripting section on Registry RCNET
- Reference implementation: [HPLC Method Optimization GUI](https://github.com/Bourne-Group/HPLCMethodOptimisationGUI)

**Related Topics:** [ChemStation Macros](../tutorials/chemstation-macros.md), [Methods Module](../api-reference/chemstation-methods.md)

---

## 💉 Sequential Injection Components

### Can I integrate additional components?

**Quick Answer:** Yes, additional components (stirrers, pumps, etc.) can be integrated using the common communication interface in SIA_API/Core.

**Detailed Explanation:**

- The SIA_API/Core provides a common communication interface for sending and receiving commands via COM port
- Most SI components like pumps, valves, or microcontrollers (Arduino, ESP32) communicate through this interface
- To add new components, you need to identify their control commands and test them thoroughly before deployment

**Background:**
Current control modules were developed from the source code of [CocoSoft](https://link.springer.com/article/10.1007/s00216-015-8834-8) 7.2, which could control additional components. Unfortunately, this software is no longer accessible.

**Code Example:**
```python
# Example: Adding a custom stirrer component
class StirrerController:
    def __init__(self, port, baudrate=9600):
        self.device = SerialDevice(port, baudrate)
    
    def set_speed(self, rpm):
        self.device.send_command(f"SPEED {rpm}")
    
    def start(self):
        self.device.send_command("START")
```

**Related Topics:** [Port Configuration](../sia-api/port-configuration.md), [Device Integration](../api-reference/sia-api.md)

---

### Getting syringe volume tracking errors

**Quick Answer:** Check current syringe volume, reset tracking if needed, or perform complete reinitialization.

**Detailed Explanation:**

The API automatically tracks syringe volume but errors can occur due to:
- Mismatch between actual and tracked volume
- Incomplete operations
- Communication interruptions

**Code Example:**
```python
# Check current syringe volume counter
syringe.print_volume_in_syringe()

# Reset volume tracking - empty syringe completely
syringe.dispense()  # Empty and reset internal counter

# Get actual volume and update counter
syringe.get_actual_volume()  # Return drawn volume and overwrite counter

# Complete reinitialization
syringe.initialize()  # Full reset to home position
```

**Related Topics:** [Basic SIA Operations](../sia-api/basic-operations.md), [Troubleshooting](../troubleshooting.md)

---

## 🛠️ Troubleshooting Guide

### Systematic Diagnosis Approach

**Quick Answer:** Follow the diagnostic sequence: verify connections → validate software → analyze errors → test components.

**Detailed Explanation:**

**1. Verify Physical Connections**

- Confirm power status on all devices
- Check cable connections and COM port assignments
- Test basic communication with each component

**2. Validate Software Prerequisites**

- ChemStation running and responsive
- Required macros loaded and active
- All specified vials present in carousel
- Target methods exist and are accessible

**3. Analyze Error Messages**

- Note specific exception types and error codes
- Look for recurring error patterns
- Enable verbose mode for detailed diagnostics

**Code Example:**
```python
# Component-level testing
def test_all_components():
    results = {}
    
    # Test syringe
    try:
        syringe.initialize()
        results['syringe'] = "✓ OK"
    except Exception as e:
        results['syringe'] = f"✗ Error: {e}"
    
    # Test valve
    try:
        valve.position(1)
        results['valve'] = "✓ OK"
    except Exception as e:
        results['valve'] = f"✗ Error: {e}"
    
    # Test ChemStation
    try:
        response = api.send("response$ = _METHPATH$")
        results['chemstation'] = f"✓ OK: {response}"
    except Exception as e:
        results['chemstation'] = f"✗ Error: {e}"
    
    return results
```

**Related Topics:** [Troubleshooting Guide](../chemstation-api/troubleshooting.md), [Error Handling](../api-reference/error-handling.md)

---

### Common Issues Quick Reference

**Quick Answer:** 90% of issues stem from: macro not loaded, incorrect COM ports, missing vials/methods, or insufficient timeouts.

**Most Frequent Problems:**

1. **ChemStation macro not running** → Reload macro in ChemStation command line
2. **Incorrect COM port configuration** → Use device manager to verify port assignments  
3. **Missing vials or methods** → Implement validation checks at workflow start
4. **Timeout settings too short** → Increase timeout values for complex operations
5. **Volume tracking errors** → Reset syringe and reinitialize volume counter

**Code Example:**
```python
# Complete system reset procedure
def full_system_reset():
    print("Performing full system reset...")
    
    # 1. Abort any running operations
    try:
        api.system.abort_run()
    except:
        pass
    
    # 2. Unload all vials
    for position in ["inlet", "outlet", "replenishment"]:
        try:
            api.ce.unload_vial_from_position(position)
        except:
            pass
    
    # 3. Reinitialize
    time.sleep(5)
    api = ChemstationAPI()
    syringe.initialize()
    
    return api
```

**Related Topics:** [Getting Started](../getting-started.md), [System Recovery](../troubleshooting.md)

---

## 📚 Getting Support

### Available Resources

- **GitHub Issues**: Report bugs, request features, and track development
- **Documentation**: Comprehensive guides covering all package functionality
- **Tutorial Examples**: Working code examples for common workflows

### Reporting Issues Effectively

When requesting support, please include:

- **Environment Details**: Python version, package version, operating system
- **Hardware Configuration**: CE model, SIA components, COM port assignments  
- **Error Information**: Complete error messages and stack traces
- **Minimal Example**: Simplified code that reproduces the issue
- **Context**: What you were trying to accomplish and what happened instead

---

!!! tip "Quick Resolution Tips"
    **Always check these fundamentals first:**
    1. ChemStation macro properly loaded and running
    2. COM port conflicts or incorrect assignments
    3. Missing physical components (vials, methods)
    4. Insufficient timeout values for complex operations