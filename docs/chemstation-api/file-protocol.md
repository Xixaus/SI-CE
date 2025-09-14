# File-Based Communication Protocol

Understanding how Python communicates with ChemStation is essential for troubleshooting and advanced usage. This guide explains the robust file-based protocol that enables reliable command execution between Python and ChemStation.

## Protocol Overview

The ChemStation API uses a file-based communication protocol to ensure reliable, bidirectional communication between Python and ChemStation. This approach provides superior reliability compared to direct socket connections, especially in Windows environments where COM interfaces can be unstable.

### Design Inspiration

This communication protocol is adapted and enhanced from the excellent work by the Cronin Group at the University of Glasgow. The original implementation can be found at: [https://github.com/croningp/analyticallabware/tree/master/AnalyticalLabware/devices/Agilent](https://github.com/croningp/analyticallabware/tree/master/AnalyticalLabware/devices/Agilent)

Our implementation extends this foundation with additional error handling, timeout management, and CE-specific optimizations for improved reliability and functionality.

---

## How It Works

The protocol operates through two files that act as communication channels between Python and ChemStation:

### Communication Flow

1. **Command Writing**: Python formats the command with a unique number and writes it to the command file
2. **Macro Monitoring**: The ChemStation macro continuously monitors the command file every 200 milliseconds
3. **Command Execution**: When a new command is detected, the macro reads it and sends it to ChemStation's Command Processor
4. **Response Writing**: Results are written to the response file with the matching command number
5. **Response Reading**: Python reads the response file and matches the response to the original command

### Architecture Benefits

- **Reliability**: File-based communication eliminates connection timeouts and port conflicts
- **Bidirectional**: Full command and response capabilities with proper synchronization
- **Error Handling**: Comprehensive error detection and automatic retry mechanisms
- **Cross-Platform**: Works consistently across different Windows versions and ChemStation releases

---

## Command Format and Examples

### Basic Commands (No Return Value)

For commands that perform actions without returning data:

```python
# Python code
api.send("LoadMethod _METHPATH$, MyMethod.M")

# Command file content
123 LoadMethod _METHPATH$, MyMethod.M

# Response file content (indicates successful execution)
123 None
```

### Commands with Return Values

To capture return values, prefix the command with `response$ = `:

```python
# Python code
method_path = api.send("response$ = _METHPATH$")
print(f"Current method path: {method_path}")

# Command file content
124 response$ = _METHPATH$

# Response file content
124 C:\Chem32\1\Methods\CE\Default\
```

### Complex Commands with Parameters

```python
# Setting system variables
api.send('_SAMPLE$ = "Sample_001"')

# Executing methods with parameters  
api.send('RunMethod _DATAPATH$,, _SAMPLE$')

# Querying instrument status
status = api.send("response$ = VAL$(_MethodOn)")
is_running = bool(int(status))
```

### Direct Module Communication

```python
# Send command to CE module
api.send('WriteModule "CE1", "FLSH 60,-2,-2"')  # 60s flush

# Query module status
response = api.send('response$ = SendModule$("CE1", "TRAY:GETVIALSTATE? 15")')
vial_state = response[-1]  # Get state code
```

---

## File Structure

The communication system uses a simple file structure within your project directory:

```
SIA-CE/
└── ChemstationAPI/
    └── core/
        ├── ChemPyConnect.mac              # ChemStation communication macro
        └── communication_files/           # Communication directory
            ├── command                   # Commands from Python → ChemStation
            └── response                  # Responses from ChemStation → Python
```

### File Content Format

**Command File:**
```
125 response$ = _METHPATH$
```

**Response File:**
```
125 C:\Chem32\1\Methods\CE\Migration\
```

---

## Command Numbering

The protocol uses sequential command numbers (1-256) to ensure proper command-response matching and prevent confusion when multiple commands are sent rapidly. Numbers automatically wrap around to 1 after reaching the maximum.

### Benefits
- **Prevents confusion** when multiple commands are sent quickly
- **Enables debugging** by tracking specific command execution
- **Supports error isolation** for failed commands

---

## Monitoring Communication

### Enable Verbose Logging

```python
from ChemstationAPI.core.communication_config import CommunicationConfig
from ChemstationAPI import ChemstationAPI

# Create configuration with verbose output
config = CommunicationConfig(verbose=True)
api = ChemstationAPI(config)

# All commands and responses will be logged
method_path = api.send("response$ = _METHPATH$")

# Console output:
# Sending command 1: response$ = _METHPATH$
# Received response 1: C:\Chem32\1\Methods\CE\Migration\
```

### Monitor Communication Files

You can monitor the communication files directly for debugging:

**PowerShell (Windows):**
```powershell
Get-Content "communication_files\command" -Wait
```

**Command Prompt:**
```cmd
type communication_files\response
```

---

## Quick Troubleshooting

### No Response Received (TimeoutError)

**Most common cause:** ChemStation macro not running

**Solution:**
1. In ChemStation command line, execute:
   ```chemstation
   macro "path\to\ChemPyConnect.mac"; Python_Run
   ```
2. Look for "Start Python communication" message
3. If message doesn't appear, check macro path

### File Access Issues

**Symptoms:** Permission denied, cannot create files

**Solutions:**
1. **Run as Administrator** - Right-click Python IDE and select "Run as administrator"
2. **Check antivirus** - Add communication directory to antivirus exclusions
3. **Verify paths** - Ensure communication directory exists and is writable

### Wrong Response or No Response

**Quick fixes:**
1. **Restart ChemStation** if responses seem corrupted
2. **Check multiple Python instances** - only one should communicate at a time
3. **Test basic command:**
   ```python
   try:
       api.send("Print 'Test'", timeout=1.0)
       print("✓ Communication working")
   except TimeoutError:
       print("✗ No response - check macro")
   ```

### Communication Slow or Unreliable

**Optimization:**
```python
# Adjust communication settings
config = CommunicationConfig(
    retry_delay=0.05,    # Faster polling (50ms)
    max_retries=10,      # More attempts
    verbose=False        # Disable logging for speed
)
```

---

## Error Detection

The API automatically detects and handles ChemStation errors:

```python
try:
    # Attempt invalid operation
    api.send("LoadMethod _METHPATH$, NonExistentMethod.M")
except ChemstationError as e:
    print(f"ChemStation Error: {e}")
    # Output: ERROR: Method file 'NonExistentMethod.M' not found
```

---

!!! tip "Protocol Reliability"
    The file-based protocol is extremely reliable once properly configured. Most issues stem from:
    1. **Macro not running** - Always verify macro status first  
    2. **File permission problems** - Run as administrator or check antivirus
    3. **Multiple Python instances** - Avoid concurrent communication attempts

!!! info "Performance Notes"
    While file-based communication adds slight overhead compared to direct connections, the reliability benefits far outweigh the minimal performance impact. Typical command execution times are 50-200ms depending on command complexity.