# Core Communication System

## Overview

The `CommandSender` class provides the foundation for all SIA device communication. It handles serial port management, command formatting, and response processing for any RS-232/USB device.

## How It Works

### Command Formatting
Commands are automatically formatted as: `{prefix}{address}{command}\r`

```python
# Your command: "MOVE 5"
# Sent to device: "/1MOVE 5\r"
```

### Port Management
- Opens port only when needed
- Handles connection errors gracefully
- Closes port after each operation

### Response Handling
- Optional response capture with timeout
- Automatic encoding/decoding
- Error detection and reporting

## Basic Usage

```python
from SI_API.core import CommandSender

# Initialize device communication
device = CommandSender(
    port="COM3",
    prefix="/",      # Command prefix (device-specific)
    address="1",     # Device address (for multi-device setups)
    baudrate=9600    # Communication speed
)

# Send command without response
device.send_command("INITIALIZE")

# Send command and get response
response = device.send_command("STATUS?", get_response=True)
print(f"Device status: {response}")
```

## Advanced Features

### Completion Waiting
```python
def wait_for_ready():
    """Custom function to wait for operation completion"""
    time.sleep(2)

# Send command and wait for completion
device.send_command(
    "MOVE_TO_POSITION 5",
    wait_for_completion=wait_for_ready,
    response_timeout=10
)
```

**Important**: The wait_for_completion function is called while the serial port remains open. This allows for continuous monitoring or additional operations during the waiting period.


## Custom Device Integration

### Arduino Example
If you have a pre-programmed Arduino controlling a custom stirrer:

Udělat to pobrobněji krok po kroku a vysvětlit jak funguje sestavování nového modulu, že je potřeba zjistit si příkazy, které se budou odesílat (a Arduina to bude naprogramované ale u jiných to může být v dokumetaci zařízení)

```python
class StirrerController(CommandSender):
    """Control custom Arduino-based stirrer"""
    
    def __init__(self, port):
        super().__init__(port=port, prefix="", address="")
    
    def start_stirring(self, speed):
        """Start stirring at specified speed (RPM)"""
        self.send_command(f"START {speed}")
    
    def stop_stirring(self):
        """Stop stirring"""
        self.send_command("STOP")
    
    def get_temperature(self):
        """Read current temperature from Arduino"""
        temp = self.send_command("TEMP?", get_response=True)
        return float(temp.strip())

# Usage
stirrer = StirrerController("COM5")
stirrer.start_stirring(500)  # 500 RPM
current_temp = stirrer.get_temperature()
stirrer.stop_stirring()
```

The CommandSender design allows easy integration with any device that uses serial communication by understanding the device's command protocol and implementing the appropriate prefix, address, and command formatting.