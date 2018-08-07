# MicroPython TM1638 LED display driver for 8x 7-segment decimal LED modules with 8x individual LEDs and 8x switches
# 8x push buttons

from micropython import const
from machine import Pin
from time import sleep_us, sleep_ms

TM1638_CMD1 = const(64)  # 0x40 data command
TM1638_CMD2 = const(192) # 0xC0 address command
TM1638_CMD3 = const(128) # 0x80 display control command
TM1638_DSP_ON = const(8) # 0x08 display on
TM1638_READ = const(2)   # 0x02 read key scan data
TM1638_FIXED = const(4)  # 0x04 fixed address mode

# 0-9, a-z, blank, dash, star
_SEGMENTS = bytearray(b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\x77\x7C\x39\x5E\x79\x71\x3D\x76\x06\x1E\x76\x38\x55\x54\x3F\x73\x67\x50\x6D\x78\x3E\x1C\x2A\x76\x6E\x5B\x00\x40\x63')

class TM1638(object):
    """Library for the TM1638 LED display driver."""
    def __init__(self, stb, clk, dio, brightness=7):
        self.stb = stb
        self.clk = clk
        self.dio = dio

        if not 0 <= brightness <= 7:
            raise ValueError("Brightness out of range")
        self._brightness = brightness

        self._on = TM1638_DSP_ON

        self.clk.init(Pin.OUT, value=1)
        self.dio.init(Pin.OUT, value=0)
        self.stb.init(Pin.OUT, value=1)

        self.clear()
        self._write_dsp_ctrl()

    def _write_data_cmd(self):
        # data command: automatic address increment, normal mode
        self._command(TM1638_CMD1)

    def _set_address(self, addr=0):
        # address command: move to address
        self._byte(TM1638_CMD2 | addr)

    def _write_dsp_ctrl(self):
        # display command: display on, set brightness
        self._command(TM1638_CMD3 | self._on | self._brightness)

    def _command(self, cmd):
        self.stb(0)
        self._byte(cmd)
        self.stb(1)

    def _byte(self, b):
        for i in range(8):
            self.clk(0)
            self.dio((b >> i) & 1)
            self.clk(1)

    def _scan_keys(self):
        """Reads one of the four bytes representing which keys are pressed."""
        pressed = 0
        self.dio.init(Pin.IN, Pin.PULL_UP)
        for i in range(8):
            self.clk(0)
            if self.dio.value():
                pressed |= 1 << i
            self.clk(1)
        self.dio.init(Pin.OUT)
        return pressed

    def power(self, val=None):
        """Power up, power down or check status"""
        if val is None:
            return self._on == TM1638_DSP_ON
        self._on = TM1638_DSP_ON if val else 0
        self._write_dsp_ctrl()

    def brightness(self, val=None):
        """Set the display brightness 0-7."""
        # brightness 0 = 1/16th pulse width
        # brightness 7 = 14/16th pulse width
        if val is None:
            return self._brightness
        if not 0 <= val <= 7:
            raise ValueError("Brightness out of range")
        self._brightness = val
        self._write_dsp_ctrl()

    def clear(self):
        """Write zeros to each address"""
        self._write_data_cmd()
        self.stb(0)
        self._set_address(0)
        for i in range(16):
            self._byte(0x00)
        self.stb(1)

    def write(self, data, pos=0):
        """Write to all 16 addresses from a given position.
        Order is left to right, 1st segment, 1st LED, 2nd segment, 2nd LED etc."""
        if not 0 <= pos <= 15:
            raise ValueError("Position out of range")
        self._write_data_cmd()
        self.stb(0)
        self._set_address(pos)
        for b in data:
            self._byte(b)
        self.stb(1)

    def led(self, pos, val):
        """Set the value of a single LED"""
        self.write([val], (pos << 1) + 1)

    def leds(self, val):
        """Set all LEDs at once. LSB is left most LED.
        Only writes to the LED positions (every 2nd starting from 1)"""
        self._write_data_cmd()
        pos = 1
        for i in range(8):
            self.stb(0)
            self._set_address(pos)
            self._byte((val >> i) & 1)
            pos += 2
            self.stb(1)

    def segments(self, segments, pos=0):
        """Set one or more segments at a relative position.
        Only writes to the segment positions (every 2nd starting from 0)"""
        if not 0 <= pos <= 7:
            raise ValueError("Position out of range")
        self._write_data_cmd()
        for seg in segments:
            self.stb(0)
            self._set_address(pos << 1)
            self._byte(seg)
            pos += 1
            self.stb(1)

    def keys(self):
        """Return a byte representing which keys are pressed. LSB is SW1"""
        keys = 0
        self.stb(0)
        self._byte(TM1638_CMD1 | TM1638_READ)
        for i in range(4):
            keys |= self._scan_keys() << i
        self.stb(1)
        return keys

    def encode_digit(self, digit):
        """Convert a character 0-9, a-f to a segment."""
        return _SEGMENTS[digit & 0x0f]

    def encode_string(self, string):
        """Convert an up to 8 character length string containing 0-9, a-z,
        space, dash, star to an array of segments, matching the length of the
        source string excluding dots, which are merged with previous char."""
        segments = bytearray(len(string.replace('.','')))
        j = 0
        for i in range(len(string)):
            if string[i] == '.' and j > 0:
                segments[j-1] |= (1 << 7)
                continue
            segments[j] = self.encode_char(string[i])
            j += 1
        return segments

    def encode_char(self, char):
        """Convert a character 0-9, a-z, space, dash or star to a segment."""
        o = ord(char)
        if o == 32:
            return _SEGMENTS[36] # space
        if o == 42:
            return _SEGMENTS[38] # star/degrees
        if o == 45:
            return _SEGMENTS[37] # dash
        if o >= 65 and o <= 90:
            return _SEGMENTS[o-55] # uppercase A-Z
        if o >= 97 and o <= 122:
            return _SEGMENTS[o-87] # lowercase a-z
        if o >= 48 and o <= 57:
            return _SEGMENTS[o-48] # 0-9
        raise ValueError("Character out of range: {:d} '{:s}'".format(o, chr(o)))

    def hex(self, val):
        """Display a hex value 0x00000000 through 0xffffffff, right aligned, leading zeros."""
        string = '{:08x}'.format(val & 0xffffffff)
        self.segments(self.encode_string(string))

    def number(self, num):
        """Display a numeric value -9999999 through 99999999, right aligned."""
        # limit to range -9999999 to 99999999
        num = max(-9999999, min(num, 99999999))
        string = '{0: >8d}'.format(num)
        self.segments(self.encode_string(string))

    #def float(self, num):
    #    # needs more work
    #    string = '{0:>9f}'.format(num)
    #    self.segments(self.encode_string(string[0:9]))

    def temperature(self, num, pos=0):
        """Displays 2 digit temperature followed by degrees C"""
        if num < -9:
            self.show('lo', pos) # low
        elif num > 99:
            self.show('hi', pos) # high
        else:
            string = '{0: >2d}'.format(num)
            self.segments(self.encode_string(string), pos)
        self.show('*C', pos + 2) # degrees C

    def humidity(self, num, pos=4):
        """Displays 2 digit humidity followed by RH"""
        if num < -9:
            self.show('lo', pos) # low
        elif num > 99:
            self.show('hi', pos) # high
        else:
            string = '{0: >2d}'.format(num)
            self.segments(self.encode_string(string), pos)
        self.show('rh', pos + 2) # relative humidity

    def show(self, string, pos=0):
        """Displays a string"""
        segments = self.encode_string(string)
        self.segments(segments[:8], pos)

    def scroll(self, string, delay=250):
        """Display a string, scrolling from the right to left, speed adjustable.
        String starts off-screen right and scrolls until off-screen left."""
        segments = string if isinstance(string, list) else self.encode_string(string)
        data = [0] * 16
        data[8:0] = list(segments)
        for i in range(len(segments) + 9):
            self.segments(data[0+i:8+i])
            sleep_ms(delay)
