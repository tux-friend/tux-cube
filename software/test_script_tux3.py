import machine, time
import bme280_float as bme280

from machine import Pin, SoftI2C
from ssd import SSD1306_I2C
from vl53l1x import VL53L1X
from mpu6500 import MPU6500, SF_G, SF_DEG_S
from apds9900LITE import APDS9900LITE


i2c = SoftI2C(scl=Pin(6),sda=Pin(5),freq=400000)

oled = SSD1306_I2C(128,64,i2c)
tof = VL53L1X(i2c)
bme = bme280.BME280(i2c=i2c)
mpu6500 = MPU6500(i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S)
mpu = MPU9250(i2c, mpu6500=mpu6500)
optic = APDS9900LITE(i2c)

optic.prox.enableSensor()

print(tof.read())
bme.values
optic.prox.proximityLevel

