# Segments

Demonstrates writing characters to the 7-segment LED modules.

```
# Wemos D1 Mini
import tm1638
from machine import Pin
tm = tm1638.TM1638(stb=Pin(13), clk=Pin(14), dio=Pin(12))

from time import sleep_ms

# cycle through all possible LED combinations on the first segment
for i in range(256):
	tm.write([i], 0)
	sleep_ms(50)

# display "01234567" using bytes from the tm1638._SEGMENTS font
tm.segments([0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07])

# encode string will give you a byte array which you can pass to .segments()
tm.encode_string('abcdefgh')

# display "abcdefgh"
tm.segments(tm.encode_string('abcdefgh'))

# there is a .show() method for simplifying this
tm.show('abcdefgh')

# show supports a position offset, so you can insert characters anywhere in the 8x segments
tm.show('abcdefg', 1)
tm.show('abcd')
tm.show('efgh', 4)

# you can write blank segments by using spaces
tm.show('   123.45')

# a dot trailing a supported character will get merged with the character as the decimal place
tm.show('a.b.cdefgh')
tm.show('a.b.c.d.e.f.g.h.')
tm.show('0.0000000')
tm.show('0.0.0.0.0000')

# the scroll method accepts any length string and displays it by scrolling in from the right until it is completely offscreen on the left
tm.scroll('cool')
tm.scroll('4 FPS', 250)
tm.scroll('faster', 125)
tm.scroll('slower', 500)

# displays a number in hexidecimal format (0-9a-f), with leading zeros.
# displays "00000001" (0x1)
tm.hex(0x01)

# displays "00001234" (0x1234)
tm.hex(4660)

# displays "12345678" (0x12345678)
tm.hex(305419896)

# displays "0000cafe"
tm.hex(0xcafe)

# displays "deadbeef"
tm.hex(0xdeadbeef)

# displays numbers ranging from -9999999 to 99999999, right aligned, with no leading zeros
# negative numbers have a dash for a minus symbol
tm.number(-9999999)
tm.number(-123)
tm.number(123)
tm.number(99999999)
```
