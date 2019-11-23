from Adafruit_BBIO.Encoder import RotaryEncoder, eQEP2
import time
# Instantiate the class to access channel eQEP2, and initialize
# that channel
myEncoder = RotaryEncoder(eQEP2)

# Get the current position
cur_position = myEncoder.position

# Set the current position
next_position = 15
#myEncoder.position = next_position

# Reset position to 0
myEncoder.zero()

# Change mode to relative (default is absolute)
# You can use setAbsolute() to change back to absolute
# Absolute: the position starts at zero and is incremented or
#           decremented by the encoder's movement
# Relative: the position is reset when the unit timer overflows.
myEncoder.setAbsolute()

# Read the current mode (0: absolute, 1: relative)
# Mode can also be set as a property
mode = myEncoder.mode

# Get the current frequency of update in Hz
freq = myEncoder.frequency

# Set the update frequency to 1 kHz
myEncoder.frequency = 1000

# Check if the channel is enabled
# The 'enabled' property is read-only
# Use the enable() and disable() methods to
# safely enable or disable the module
isEnabled = myEncoder.enabled
myEncoder.enable()

while True:
    print(str(myEncoder.position))
    time.sleep(0.3)
# Disable the eQEP channel
myEncoder.disable()
