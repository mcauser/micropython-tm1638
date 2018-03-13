# Brightness

Demonstrates setting the display brightness.

```
# Wemos D1 Mini
import tm1638
from machine import Pin
tm = tm1638.TM1638(stb=Pin(13), clk=Pin(14), dio=Pin(12))

# light up some LEDs
tm.leds(0b10101010)

# write some characters
tm.show('abcdefgh')

# dim both the individual LEDs and the segments
tm.brightness(0)

# a little less than half brightness
tm.brightness(3)

# what is the current brightness? returns 3
tm.brightness()

# back to full brightness
tm.brightness(7)
```
