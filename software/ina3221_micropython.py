# The MIT License (MIT)
#
# Copyright (c) 2019 Barbudor (IRL Jean-Michel Mercier)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# imports
from micropython import const

_DEFAULT_ADDRESS                 = const(0x40)
#
# Registers and bits definitions
#

# Config register
_REG_CONFIG                      = const(0x00)

_RESET                           = const(0x8000)
_ENABLE_CH                       = (None,const(0x4000),const(0x2000),const(0x1000)) # default set

_AVERAGING_MASK                  = const(0x0E00)
_AVERAGING_NONE                  = const(0x0000)     # 1 sample, default
_AVERAGING_4_SAMPLES             = const(0x0200)
_AVERAGING_16_SAMPLES            = const(0x0400)
_AVERAGING_64_SAMPLES            = const(0x0600)
_AVERAGING_128_SAMPLES           = const(0x0800)
_AVERAGING_256_SAMPLES           = const(0x0A00)
_AVERAGING_512_SAMPLES           = const(0x0C00)
_AVERAGING_1024_SAMPLES          = const(0x0E00)

_VBUS_CONV_TIME_MASK             = const(0x01C0)
_VBUS_CONV_TIME_140US            = const(0x0000)
_VBUS_CONV_TIME_204US            = const(0x0040)
_VBUS_CONV_TIME_332US            = const(0x0080)
_VBUS_CONV_TIME_588US            = const(0x00C0)
_VBUS_CONV_TIME_1MS              = const(0x0100)     # 1.1ms, default
_VBUS_CONV_TIME_2MS              = const(0x0140)     # 2.116ms
_VBUS_CONV_TIME_4MS              = const(0x0180)     # 4.156ms
_VBUS_CONV_TIME_8MS              = const(0x01C0)     # 8.244ms

_SHUNT_CONV_TIME_MASK            = const(0x0038)
_SHUNT_CONV_TIME_140US           = const(0x0000)
_SHUNT_CONV_TIME_204US           = const(0x0008)
_SHUNT_CONV_TIME_332US           = const(0x0010)
_SHUNT_CONV_TIME_588US           = const(0x0018)
_SHUNT_CONV_TIME_1MS             = const(0x0020)     # 1.1ms, default
_SHUNT_CONV_TIME_2MS             = const(0x0028)     # 2.116ms
_SHUNT_CONV_TIME_4MS             = const(0x0030)     # 4.156ms
_SHUNT_CONV_TIME_8MS             = const(0x0038)     # 8.244ms

_MODE_MASK                       = const(0x0007)
_MODE_POWER_DOWN                 = const(0x0000)     # Power-down
_MODE_SHUNT_VOLTAGE_TRIGGERED    = const(0x0001)     # Shunt voltage, single-shot (triggered)
_MODE_BUS_VOLTAGE_TRIGGERED      = const(0x0002)     # Bus voltage, single-shot (triggered)
_MODE_SHUNT_AND_BUS_TRIGGERED    = const(0x0003)     # Shunt and bus, single-shot (triggered)
_MODE_POWER_DOWN2                = const(0x0004)     # Power-down
_MODE_SHUNT_VOLTAGE_CONTINUOUS   = const(0x0005)     # Shunt voltage, continous
_MODE_BUS_VOLTAGE_CONTINUOUS     = const(0x0006)     # Bus voltage, continuous
_MODE_SHUNT_AND_BUS_CONTINOUS    = const(0x0007)     # Shunt and bus, continuous (default)

# Other registers
_REG_SHUNT_VOLTAGE_CH            = (None, const(0x01), const(0x03), const(0x05))
_REG_BUS_VOLTAGE_CH              = (None, const(0x02), const(0x04), const(0x06))
_REG_CRITICAL_ALERT_LIMIT_CH     = (None, const(0x07), const(0x09), const(0x0B))
_REG_WARNING_ALERT_LIMIT_CH      = (None, const(0x08), const(0x0A), const(0x0C))
_REG_SHUNT_VOLTAGE_SUM           = const(0x0D)
_REG_SHUNT_VOLTAGE_SUM_LIMIT     = const(0x0E)

# Mask/enable register
_REG_MASK_ENABLE                 = const(0x0F)
_SUM_CONTROL_CH                  = (None,const(0x4000),const(0x2000),const(0x1000)) #default not set
_WARNING_LATCH_ENABLE            = const(0x0800)     # default not set
_CRITICAL_LATCH_ENABLE           = const(0x0400)     # default not set
_CRITICAL_FLAG_CH                = (None,const(0x0200),const(0x0100),const(0x0080))
_SUM_ALERT_FLAG                  = const(0x0040)
_WARNING_FLAG_CH                 = (None,const(0x0020),const(0x0010),const(0x0008))
_POWER_ALERT_FLAG                = const(0x0004)
_TIMING_ALERT_FLAG               = const(0x0002)
_CONV_READY_FLAG                 = const(0x0001)

# Other registers
_REG_POWER_VALID_UPPER_LIMIT     = const(0x10)
_REG_POWER_VALID_LOWER_LIMIT     = const(0x11)
_REG_MANUFACTURER_ID             = const(0xFE)
_REG_DIE_ID                      = const(0xFF)

# Constants for manufacturer and device ID
_MANUFACTURER_ID                 = const(0x5449)     # "TI"
_DIE_ID                          = const(0x3220)


class INA3221:
    """Driver class for Texas Instruments INA3221 3 channel current sensor device"""

    IS_FULL_API = False

    @staticmethod
    def _to_signed(val):
        if val > 32767:
            return val - 65536
        return val

    @staticmethod
    def _to_unsigned(val):
        if val < 0:
            return val + 65536
        return val

    def write(self, reg, value):
        """Write value in device register"""
        seq = bytearray([reg, (value >> 8) & 0xFF, value & 0xFF])
        with self.i2c_device as i2c:
            i2c.writeto(seq)

    def read(self, reg):
        """Return value from device register"""
        buf = bytearray(3)
        buf[0] = reg
        with self.i2c_device as i2c:
            i2c.writeto(buf, end=1, stop=False)
            i2c.readinto(buf, start=1)
        value = (buf[1] << 8) | (buf[2])
        return value

    def update(self, reg, mask, value):
        """Read-modify-write value in register"""
        regvalue = self.readfrominto(reg)
        regvalue &= ~mask
        value &= mask
        self.writeto(reg, regvalue | value)


    def __init__(self, i2c_bus, i2c_addr = _DEFAULT_ADDRESS, shunt_resistor = (0.1, 0.1, 0.1)):
        self.i2c_device = i2c_bus
        self.i2c_addr = i2c_addr
        self.shunt_resistor = shunt_resistor
        self.buf = bytearray(2) # ROAR la til
        

#         self.i2c_device.writeto(_REG_CONFIG,  _AVERAGING_16_SAMPLES | \
#                                   _VBUS_CONV_TIME_1MS | \
#                                   _SHUNT_CONV_TIME_1MS | \
#                                   _MODE_SHUNT_AND_BUS_CONTINOUS )
        
# ROARnyg added:
        self.set_calibration()
    
    def set_calibration(self):
        config = (_AVERAGING_16_SAMPLES |
                                  _VBUS_CONV_TIME_1MS |
                                  _SHUNT_CONV_TIME_1MS |
                                  _MODE_SHUNT_AND_BUS_CONTINOUS)
        self._write_register(_REG_CONFIG, config)
    def _write_register(self, reg, value):
        self.buf[0] = (value >> 8) & 0xFF
        self.buf[1] = value & 0xFF
        self.i2c_device.writeto_mem(self.i2c_addr, reg, self.buf)

    def is_channel_enabled(self, channel=1):
        """Returns if a given channel is enabled or not"""
        #assert 1 <= channel <= 3, "channel argument must be 1, 2, or 3"
        bit = _ENABLE_CH[channel]
        return self.readfrominto(_REG_CONFIG) & bit != 0

    def enable_channel(self, channel=1, enable=True):
        """Enables or disable a given channel"""
        #assert 1 <= channel <= 3, "channel argument must be 1, 2, or 3"
        bit = _ENABLE_CH[channel]
        value = 0
        if enable:
            value = bit
        self.update(_REG_CONFIG, bit, value)

    def shunt_voltage(self, channel=1):
        """Returns the channel's shunt voltage in Volts"""
        #assert 1 <= channel <= 3, "channel argument must be 1, 2, or 3"
        value = self._to_signed(self.readfrominto(_REG_SHUNT_VOLTAGE_CH[channel])) / 8.0
        # convert to volts - LSB = 40uV
        return value * 0.00004

    def current(self, channel=1):
        """Return's the channel current in Amps"""
        #assert 1 <= channel <= 3, "channel argument must be 1, 2, or 3"
        return self.shunt_voltage(channel) / self.shunt_resistor[channel-1]

    def bus_voltage(self, channel=1):
        """Returns the channel's bus voltage in Volts"""
        #assert 1 <= channel <= 3, "channel argument must be 1, 2, or 3"
        value = self._to_signed(self.readfrominto(_REG_BUS_VOLTAGE_CH[channel])) / 8
        # convert to volts - LSB = 8mV
        return value * 0.008
