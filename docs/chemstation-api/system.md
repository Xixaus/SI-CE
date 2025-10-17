# System Module - ChemStation System Monitoring

System monitoring and diagnostic control for ChemStation CE operations.

## Overview

The System module provides:

- **Status Monitoring**: Real-time acquisition and instrument status tracking
- **Method Execution Tracking**: Active analysis monitoring and timing information
- **Instrument Readiness**: System state validation with timeout handling
- **Diagnostic Tools**: Register browser and system analysis capabilities
- **Emergency Control**: Analysis abort and system recovery functions

**Key Capabilities**: Real-time status, method timing, readiness validation, diagnostic access

---

## Status Monitoring

### method_on()

Check if an analytical method is currently executing.

```python
is_running = api.system.method_on()
```

**Returns:**

- `True` if a method is currently executing (any phase)
- `False` if system is idle

**Examples:**
```python
# Wait for method completion
while api.system.method_on():
    print("Analysis in progress...")
    time.sleep(30)

# Check before starting new analysis
if not api.system.method_on():
    api.method.run("NewSample")

# Simple status check
if api.system.method_on():
    print("Method running")
else:
    print("System idle")
```

**Notes:**

- Covers all method phases (preconditioning, injection, separation, postconditioning)
- Essential for automation workflows to prevent overlapping analyses
- Use with `status()` for detailed phase information

---

### status()

Get current ChemStation acquisition status.

```python
current_status = api.system.status()
```

**Returns:**

- `"STANDBY"`: System idle, ready for new analysis
- `"PRERUN"`: Pre-analysis conditioning and preparation
- `"RUN"`: Active separation and detection phase
- `"POSTRUN"`: Post-analysis conditioning and cleanup
- `"ERROR"`: Error condition requiring attention
- `"ABORT"`: Analysis aborted or interrupted

**Examples:**
```python
# Monitor analysis phases
status = api.system.status()
if status == "RUN":
    print("Separation in progress")
elif status == "STANDBY":
    print("Ready for new sample")

# Wait for specific phase
while api.system.status() != "RUN":
    time.sleep(5)

# Status-based decisions
status = api.system.status()
if status == "ERROR":
    print("System error detected")
    api.system.abort_run()
```

**Notes:**

- Status updates in real-time
- STANDBY indicates readiness for new analysis
- Includes automatic retry logic for communication reliability

---

### RC_status()

Get current RC.NET module status for detailed instrument monitoring.

```python
module_status = api.system.RC_status(module="CE1")
```

**Parameters:**

- `module` (str): RC.NET module identifier (default: "CE1")

**Returns:**

- `"Idle"`: Module ready and available for operations
- `"Run"`: Module actively executing operations
- `"NotReady"`: Module initializing or in error state
- `"Error"`: Module error condition requiring attention
- `"Maintenance"`: Module in maintenance mode

**Examples:**
```python
# Monitor CE instrument status
if api.system.RC_status("CE1") == "Idle":
    print("CE instrument ready")

# Check multiple modules
for module in ["CE1", "DAD1"]:
    status = api.system.RC_status(module)
    print(f"{module}: {status}")

# Wait for module ready
while api.system.RC_status("CE1") != "Idle":
    print("Waiting for CE module...")
    time.sleep(5)
```

**Notes:**

- More detailed than acquisition status
- Useful for troubleshooting and system diagnostics
- Includes automatic retry logic

---

## Method Timing

### get_elapsed_analysis_time()

Get elapsed separation time since current analysis started.

```python
elapsed_time = api.system.get_elapsed_analysis_time()
```

**Returns:**

- `float`: Elapsed separation time in minutes
- `0.0` if no analysis running or separation hasn't started

**Examples:**
```python
# Monitor analysis progress
elapsed = api.system.get_elapsed_analysis_time()
total = api.system.get_analysis_time()
progress = (elapsed / total) * 100
print(f"Analysis {progress:.1f}% complete")

# Real-time monitoring with updates
while api.system.method_on():
    elapsed = api.system.get_elapsed_analysis_time()
    print(f"Running for {elapsed:.2f} minutes")
    time.sleep(30)
```

**Notes:**

- Measures only separation phase, not total method time
- Updates in real-time with precision to 0.01 minutes
- Excludes pre-run conditioning and injection phases

---

### get_analysis_time()

Get total expected separation duration for current method.

```python
total_time = api.system.get_analysis_time()
```

**Returns:**

- `float`: Total separation duration in minutes

**Examples:**
```python
# Calculate remaining time
total_time = api.system.get_analysis_time()
elapsed_time = api.system.get_elapsed_analysis_time()
remaining = total_time - elapsed_time
print(f"Analysis completes in {remaining:.2f} minutes")

# Check method duration before starting
duration = api.system.get_analysis_time()
if duration > 60:  # More than 1 hour
    confirm = input(f"Long analysis ({duration:.1f}min). Continue? ")
```

**Notes:**

- Based on method's programmed stoptime parameter
- Does not include conditioning or injection time
- Remains constant during execution

---

### get_remaining_analysis_time()

Get remaining separation time until current analysis completes.

```python
remaining_time = api.system.get_remaining_analysis_time()
```

**Returns:**

- `float`: Remaining separation time in minutes
- `0.0` if no analysis running
- May be negative if analysis exceeds expected duration

**Examples:**
```python
# Display countdown
remaining = api.system.get_remaining_analysis_time()
print(f"Analysis completes in {remaining:.1f} minutes")

# Progress monitoring with updates
while api.system.method_on():
    remaining = api.system.get_remaining_analysis_time()
    if remaining > 0:
        print(f"Time remaining: {remaining:.2f} minutes")
    time.sleep(60)

# Automated scheduling
if api.system.get_remaining_analysis_time() < 5:  # Less than 5 minutes
    prepare_next_sample()
```

**Notes:**

- Updates continuously during analysis
- Useful for progress bars and time estimation
- Calculated as total_time - elapsed_time

---

## System Readiness

### ready_to_start_analysis()

Wait for all specified modules to reach ready state for analysis.

```python
api.system.ready_to_start_analysis(modules=["CE1", "DAD1"], timeout=None, verbose=True)
```

**Parameters:**

- `modules` (list): List of module identifiers to check (default: ["CE1", "DAD1"])
- `timeout` (int): Maximum waiting time in seconds (None = wait indefinitely)
- `verbose` (bool): Display real-time status updates (default: True)

**Examples:**
```python
# Quick readiness check before analysis
api.system.ready_to_start_analysis(timeout=10, verbose=False)

# Wait for CE and detector with status updates
api.system.ready_to_start_analysis(["CE1", "DAD1"], timeout=60)

# Wait indefinitely with progress display
api.system.ready_to_start_analysis(verbose=True)

# Custom module list
api.system.ready_to_start_analysis(["CE1"], timeout=30)
```

**Notes:**

- Displays progress when verbose=True
- Modules must be both "Idle" and have no NotReady conditions
- Typical timeouts: 10s (quick check), 60s (standard), 300s (long methods)

---

### wait_for_ready()

Wait for ChemStation to reach ready state for new analysis.

```python
is_ready = api.system.wait_for_ready(timeout=60)
```

**Parameters:**

- `timeout` (int): Maximum waiting time in seconds (default: 60)

**Returns:**

- `True` if system reaches ready state within timeout
- `False` if timeout expires before ready state achieved

**Examples:**
```python
# Standard workflow with timeout
if api.system.wait_for_ready():
    api.method.run("NextSample")
else:
    print("Timeout - check instrument status")

# Extended wait for long conditioning methods
if api.system.wait_for_ready(timeout=300):  # 5 minutes
    start_next_analysis()

# Sequence automation
for sample in sample_list:
    if api.system.wait_for_ready(timeout=120):
        process_sample(sample)
```

**Notes:**

- Polls status every second to minimize system load
- Both STANDBY and PRERUN are considered ready states
- Returns immediately if already ready

---

## Emergency Control

### abort_run()

Immediately abort current analysis or sequence execution.

```python
api.system.abort_run()
```

**Examples:**
```python
# Emergency stop
api.system.abort_run()

# Conditional abort on error detection
if error_detected:
    api.system.abort_run()
    print("Analysis aborted due to error")

# Abort with cleanup
api.system.abort_run()
time.sleep(5)  # Wait for system stabilization
```

**Notes:**

- Results in immediate termination without post-run conditioning
- Data up to abort point may be saved
- Instrument requires manual return to ready state after abort
- Brief wait for abort completion and system stabilization

---

## Diagnostic Tools

### add_register_reader()

Add comprehensive register inspection tool to ChemStation Debug menu.

```python
api.system.add_register_reader(register_reader_macro=r"ChemstationAPI\controllers\macros\register_reader.mac")
```

**Parameters:**

- `register_reader_macro` (str): Path to register reader macro file (default: included tool)

**Examples:**
```python
# Add register browser with default tool
api.system.add_register_reader()

# Use custom register reader
api.system.add_register_reader("C:\\Custom\\debug_tools.mac")
```

**Usage:**

After execution, look for "Show Registers" item in ChemStation's Debug menu. Tool provides:
- Browse all ChemStation registers (RC.NET, sequence, method, system)
- Inspect object structures and data tables interactively
- View and modify header values and text fields
- Navigate complex register hierarchies with tree view

**Notes:**

- Tool remains available until ChemStation restart
- Exercise caution when modifying system registers
- Invaluable for debugging and advanced parameter editing

---

## Practical Examples

### Analysis Progress Monitoring

```python
# Complete progress monitoring
def monitor_analysis():
    start_time = time.time()
    
    while api.system.method_on():
        # Get timing information
        elapsed = api.system.get_elapsed_analysis_time()
        remaining = api.system.get_remaining_analysis_time()
        total = api.system.get_analysis_time()
        
        # Calculate progress
        if total > 0:
            progress = (elapsed / total) * 100
        else:
            progress = 0
        
        # Get status
        status = api.system.status()
        
        # Display progress
        print(f"\rStatus: {status} | Progress: {progress:.1f}% | "
              f"Remaining: {remaining:.1f} min", end='')
        
        time.sleep(10)
    
    total_time = (time.time() - start_time) / 60
    print(f"\nAnalysis complete! Total time: {total_time:.1f} minutes")

# Start monitoring
monitor_analysis()
```

### System Readiness Check

```python
# Complete system validation
def check_system_ready():
    print("Checking system status...")
    
    # Check basic status
    status = api.system.status()
    print(f"Acquisition status: {status}")
    
    # Check RC modules
    ce_status = api.system.RC_status("CE1")
    print(f"CE module: {ce_status}")
    
    # Wait for ready if needed
    if status != "STANDBY" or ce_status != "Idle":
        print("Waiting for system ready...")
        api.system.ready_to_start_analysis(timeout=60)
    
    print("✓ System ready for analysis")

check_system_ready()
```

### Automated Error Recovery

```python
# Error detection and recovery
def safe_analysis_with_recovery(sample_name):
    max_attempts = 3
    
    for attempt in range(max_attempts):
        try:
            # Check system ready
            api.system.ready_to_start_analysis(timeout=30)
            
            # Start analysis
            api.method.run(sample_name)
            
            # Monitor for errors
            while api.system.method_on():
                status = api.system.status()
                if status == "ERROR":
                    raise RuntimeError("Analysis error detected")
                time.sleep(10)
            
            print(f"✓ Analysis {sample_name} completed successfully")
            return True
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            
            if attempt < max_attempts - 1:
                print("Attempting recovery...")
                api.system.abort_run()
                time.sleep(30)
            else:
                print("All attempts failed")
                return False
    
    return False

# Use with error recovery
safe_analysis_with_recovery("Sample_001")
```