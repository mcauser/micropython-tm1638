# Uptime

Display a millisecond counter.

```
# Wemos D1 Mini
import tm1638
from machine import Pin
tm = tm1638.TM1638(stb=Pin(13), clk=Pin(14), dio=Pin(12))

import utime

while True:
    tm.number(utime.ticks_ms())
```
