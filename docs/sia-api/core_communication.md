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
from SIA_API.core import CommandSender

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

---

## Custom Device Integration

### Arduino Integration

If you have a pre-programmed Arduino (or similar microcontroller) that responds to specific serial commands, you can easily create a Python controller to integrate it with your SIA system.

#### Step 1: Identify Device Commands

First, determine what commands your Arduino understands by checking your Arduino code or documentation:

**Example Arduino commands:**
```
START 150     -> Starts operation at speed 150, returns "OK"
STOP          -> Stops operation, returns "OK"  
STATUS?       -> Returns current status: "SPEED:150,RUNNING:YES"
TEMP?         -> Returns temperature: "TEMP:25.4"
```

#### Step 2: Create Python Controller

Create a Python class that wraps your Arduino commands:

```python
from SIA_API.core import CommandSender

class ArduinoController(CommandSender):
    """Controller for pre-programmed Arduino device."""
    
    def __init__(self, port, baudrate=9600):
        # Most Arduino devices don't need prefix/address
        super().__init__(port=port, prefix="", address="", baudrate=baudrate)
    
    def start_operation(self, speed):
        """Start Arduino operation at specified speed."""
        response = self.send_command(f"START {speed}", get_response=True)
        
        if "OK" in response:
            print(f"✓ Started at speed {speed}")
            return True
        else:
            raise RuntimeError(f"Start failed: {response}")
    
    def stop_operation(self):
        """Stop Arduino operation."""
        response = self.send_command("STOP", get_response=True)
        
        if "OK" in response:
            print("✓ Operation stopped")
            return True
        else:
            raise RuntimeError(f"Stop failed: {response}")
    
    def get_status(self):
        """Get current Arduino status."""
        response = self.send_command("STATUS?", get_response=True)
        
        # Parse response: "SPEED:150,RUNNING:YES"
        status = {}
        
        if "SPEED:" in response:
            speed_part = response.split("SPEED:")[1].split(",")[0]
            status['speed'] = int(speed_part)
        
        if "RUNNING:" in response:
            running_part = response.split("RUNNING:")[1]
            status['running'] = "YES" in running_part
            
        return status
    
    def get_temperature(self):
        """Read temperature from Arduino sensor."""
        response = self.send_command("TEMP?", get_response=True)
        
        # Parse response: "TEMP:25.4"
        if "TEMP:" in response:
            temp_str = response.split("TEMP:")[1]
            return float(temp_str)
        else:
            raise RuntimeError(f"Failed to parse temperature: {response}")

# Usage example
arduino = ArduinoController("COM5")
arduino.start_operation(150)
status = arduino.get_status()
temperature = arduino.get_temperature()
arduino.stop_operation()
```

The CommandSender design allows easy integration with any device that uses serial communication by understanding the device's command protocol and implementing the appropriate Python wrapper class.