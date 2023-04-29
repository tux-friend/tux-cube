import machine, gc, os, time, framebuf
from machine import Pin, Timer, SoftI2C
from phyphoxBLE import PhyphoxBLE, Experiment
from writer import Writer
import disp
from phoxdisp import app

from vl53l1x import VL53L1X
import bme280_float as bme280
from mpu6500 import MPU6500, SF_G, SF_DEG_S
from apds9900LITE import APDS9900LITE

i2c = SoftI2C(scl=Pin(6),sda=Pin(5),freq=400000)
button = Pin(7, Pin.IN, Pin.PULL_UP)

tof = VL53L1X(i2c)
bme = bme280.BME280(i2c=i2c)
optic = APDS9900LITE(i2c)
optic.prox.enableSensor()

#Button press functions + debounce
def on_pressed(timer):
    global butstate
    butstate = (butstate + 1) % 6

def debounce(pin):
    timer.init(mode=Timer.ONE_SHOT, period=50, callback=on_pressed)

#Show memory and space usage
def free(full=False):
  gc.collect()
  F = gc.mem_free()
  A = gc.mem_alloc()
  T = F+A
  P = '{0:.2f}%'.format(F/T*100)
  if not full: return P
  else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))

def df():
  s = os.statvfs('//')
  return ('{0} MB'.format((s[0]*s[3])/1048576))
  
#Initialize App Design and output data to phyphox
def cube(x):
    global butstate
    disp.menu(x)
    app(x,p)
    while x == butstate:
        m = sens(x)
        disp.data(x,m)
        p.write(m[0],m[1],m[2],m[3])  #Send value to phyphox
        time.sleep_ms(250)
        gc.mem_free()

def sens(x):
    if x == 0:
        data = list(bme.values)+[0]
    elif x == 1:
        data = list(bme.values)+[0]
        print("Hallo")
    elif x == 2:
        data = list(bme.values)+[0]
        print("Hallo")
    elif x == 3:
        data = list(bme.values)+[0]
        print("Hallo")
    elif x == 4:
        data = list(bme.values)+[0]
        print("Hallo")
    else:
        data = list(bme.values)+[0]
        print("Hallo")
    return data

# Tux³ Cube Routine
disp.startani()

butstate = 0
timer = Timer(0)
p = PhyphoxBLE()
editValue = 0.0
firstCall = True
button.irq(debounce, Pin.IRQ_RISING)

while True:
    cube(butstate)
    time.sleep(0.1)
    gc.mem_free()
    print(df(),free())


