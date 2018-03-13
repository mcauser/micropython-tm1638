# Power control

Demonstrates toggling the power control register.

```
# Wemos D1 Mini
import tm1638
from machine import Pin
tm = tm1638.TM1638(stb=Pin(13), clk=Pin(14), dio=Pin(12))

# get the current status, returns True since you just initialised the driver
tm.power()

# switch on all of the LEDs
tm.leds(255)

# switch on all of the segments
tm.show('8.8.8.8.8.8.8.8.')

# switch off the display, both individual LEDs and 7-segments
tm.power(False)

# get the current status, returns False
tm.power()

# you can still write to the display registers
tm.leds(0b10101010)
tm.show('abcdefgh')

# the changes wont be visible until you power on the display
tm.power(True)
```
