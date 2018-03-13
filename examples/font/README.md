# 7-segment font

Show all of the supported characters. 0-9, a-z, space, dash, degrees.

```
# Wemos D1 Mini
import tm1638
from machine import Pin
tm = tm1638.TM1638(stb=Pin(13), clk=Pin(14), dio=Pin(12))

# scroll through all supported characters
tm.scroll(list(tm1638._SEGMENTS))

# 01234567
tm.clear()
tm.segments(tm1638._SEGMENTS[0:8])

# 89abcdef
tm.clear()
tm.segments(tm1638._SEGMENTS[8:16])

# ghijklmn
tm.clear()
tm.segments(tm1638._SEGMENTS[16:24])

# opqrstuv
tm.clear()
tm.segments(tm1638._SEGMENTS[24:32])

# wxyz (space) (dash) (degrees)
tm.clear()
tm.segments(tm1638._SEGMENTS[32:39])
```
