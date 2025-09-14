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

# All commands and responses will be logged to console
method_path = api.send("response$ = _METHPATH$")

# Console output:
# Sending command 1: response$ = _METHPATH$
# Received response 1: C:\Chem32\1\Methods\CE\Migration\
```

---

## Quick Troubleshooting

### No Response Received (TimeoutError)

**Most common causes:**

1. **ChemStation macro not running** - The communication macro must be active in ChemStation
   
    **Solution:** In ChemStation command line, execute:
   ```chemstation
   macro "path\to\ChemPyConnect.mac"; Python_Run
   ```
   Look for "Start Python communication" message.


2. **Error dialog appeared in ChemStation** - Communication is blocked while dialog is open
   
   **Solution:** Check ChemStation for any open error dialogs or message boxes. Close all dialogs and try again. This commonly occurs when:
   - Starting a method while another is running
   - Attempting operations on non-existent files
   - Hardware communication errors

3. **Incorrect paths in macro** - Macro is running but using wrong communication directory
   
   **Solution:** Check that the path in `ChemPyConnect.mac` matches your actual communication files directory. The macro contains a hardcoded path that may need updating for your installation.

### Test Communication

```python
try:
    api.send("Print 'Test'", timeout=1.0)
    print("✓ Communication working")
except TimeoutError:
    print("✗ No response - check macro and dialogs")
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