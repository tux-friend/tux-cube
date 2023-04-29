from machine import Pin, SoftI2C
from writer import Writer
import baticon, diceicon, cmu, latobold
import time, framebuf
from ssd import SSD1306_I2C

i2c = SoftI2C(scl=Pin(6),sda=Pin(5),freq=400000)
oled = SSD1306_I2C(128,64,i2c)

# Define Fonts
latof = Writer(oled, latobold)
batf = Writer(oled, baticon)
dicef = Writer(oled, diceicon)
cmuf = Writer(oled, cmu)

# Startup Animation Sensor Cube Tux³
def startani():
    oled.fill(0)
    Writer.set_textpos(oled,0,10)
    for i in ['S','e','n','s','o','r',' ','C','u','b','e']:
        latof.printstring(i)
        time.sleep(0.05)
        oled.show()
    Writer.set_textpos(oled,45,45)
    for i in ['T','u','x']:
        latof.printstring(i)
        time.sleep(0.05)
        oled.show()
    time.sleep(0.05)
    Writer.set_textpos(oled,41,76)
    cmuf.printstring('3')
    logo = framebuf.FrameBuffer(bytearray(b'\x00\x00\x00\x00\xff\x00\x03\xff\xc0\x0f\xff\xf0\x1f\x00\xf8\x1c\x0088\x00\x1cx\x00\x1epB\x0e\xe0\xe7\x0e\xe0\xff\x0e\xe0~\x0f\xe0<\x0f\xe0~\x0f\xe0\xff\x0ep\xe7\x0exB\x1e8\x00\x1c<\x008\x1f\x00\xf8\x0f\xc3\xf0\x03\xff\xc0\x01\xff\x80\x00~\x00'), 24,24, framebuf.MONO_HLSB)    
    oled.blit(logo,52,20)
    oled.show()
    time.sleep(1)

def menu(num):
    oled.fill(0)
    Writer.set_textpos(oled,48,0)
    dicef.printstring("ABCDEF")
    dice=["G","H","I","J","K","L"]
    Writer.set_textpos(oled,48,num*16)
    dicef.printstring(dice[num])
    if num==0:
        text = ["T:", "p:", "hum."]
        Writer.set_textpos(oled, 0,80)
        cmuf.printstring("T1:")
        Writer.set_textpos(oled, 17,80)
        cmuf.printstring("T2:")
    elif num==1:
        text = ["s:", "v:", "a:"]
    elif num==2:
        text = ["U:", "I:", "P:"]
    elif num==3:
        text = ["a:", "v:", "t:"]
        Writer.set_textpos(oled, 0,50)
        cmuf.printstring("Magnet:")
    elif num==4:
        text = ["Lux:", "Tux:", "Fux:"]
    else:
        text = ["sound:", "Tux:", "Fux:"]
    for item,j in zip(text, [0,17,34]):
        Writer.set_textpos(oled,j,0)
        cmuf.printstring(item)
    oled.show()

def data(num,x):
    if num == 0:
        fdata = ("{:.2f}C".format(x[0]), "{:.2f}hPa".format(x[1]/100),
                "{:.2f}%".format(x[2]))
        for i,j,k in zip(fdata,[0,17,34],[14,14,30]):
            Writer.set_textpos(oled,j,k)
            cmuf.printstring(i)
        oled.show()
    else:
        x = [1,2,3,4,5]
        for i,j,k in zip(x,[0,17,34,0,15],[0,0,30,70,70]):
            Writer.set_textpos(oled,j,k)
            cmuf.printstring(str(i))
        oled.show()
        