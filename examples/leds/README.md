# Individual LEDs

Demonstrates toggling the Individual LEDs at the top.

```
# Wemos D1 Mini
import tm1638
from machine import Pin
tm = tm1638.TM1638(stb=Pin(13), clk=Pin(14), dio=Pin(12))

from time import sleep_ms

# turn them on, one by one
for i in range(8):
    tm.led(i, 1)
    sleep_ms(200)

# turn them off, one by one
for i in range(8):
    tm.led(i, 0)
    sleep_ms(200)

# toggle 1st LED
tm.led(0, 1)
tm.led(0, 0)

# toggle the 2nd LED
tm.led(1, True)
tm.led(1, False)

# turn on only the 4th LED
tm.leds(8)

# turn on only the first 3 LEDs
tm.leds(7)

# every 2nd led on
for i in range(10):
    tm.leds(0b01010101)
    sleep_ms(100)
    tm.leds(0b10101010)
    sleep_ms(100)

# leds off
tm.leds(0)
```
