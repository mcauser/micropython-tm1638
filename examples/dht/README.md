# DHT temperature and humidity

Show the current temperature and humidity.

```
# Wemos D1 Mini
import tm1638
from machine import Pin
tm = tm1638.TM1638(stb=Pin(13), clk=Pin(14), dio=Pin(12))

# display 23*C 75rh
tm.temperature(23)
tm.humidity(75)

# display 45rh 26*C
tm.temperature(26,4)
tm.humidity(45,0)

# display temp and humidity from a DHT11 sensor
import dht
d = dht.DHT11(Pin(4))

d.measure()
tm.temperature(d.temperature())
tm.humidity(d.humidity())
```
