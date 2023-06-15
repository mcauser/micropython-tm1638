# Address mode

In fixed address mode, each display data byte is written to the same address.
In address increasing mode, after each display data byte is written the address increments.

```
# Wemos D1 Mini
import tm1638
from machine import Pin
tm = tm1638.TM1638(stb=Pin(13), clk=Pin(14), dio=Pin(12))

from time import sleep_ms

# set fixed mode
tm._command(tm1638.TM1638_CMD1 | tm1638.TM1638_FIXED)
# or simply
tm._command(68)

# write 255 bytes to the first address (1st segment)
tm.stb(0)
tm._set_address(0)
for i in range(256):
    tm._byte(i)
    sleep_ms(50)
tm.stb(1)

# set normal address increasing mode
tm._command(tm1638.TM1638_CMD1)
# or simply
tm._command(64)
# or as other methods call it
tm._write_data_cmd()

# repeat the write 255 bytes and you'll see each byte moves to the next address
tm.stb(0)
tm._set_address(0)
for i in range(256):
    tm._byte(i)
    sleep_ms(50)
tm.stb(1)

# these methods reset to normal address increasing mode:
# .clear, .write(), .leds(), .segments()
```
