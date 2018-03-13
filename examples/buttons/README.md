# Buttons

Demonstrates the key scanning ability.

```
# Wemos D1 Mini
import tm1638
from machine import Pin
tm = tm1638.TM1638(stb=Pin(13), clk=Pin(14), dio=Pin(12))

from time import sleep_ms

# press a button to illuminate the matching individual LED
# you can press multiple buttons simultaneously
while True:
    pressed = tm.keys()
    for i in range(8):
        tm.led(i, (pressed >> i) & 1)
    sleep_ms(10)
```
