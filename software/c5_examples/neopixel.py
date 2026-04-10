import machine
import neopixel

pin = machine.Pin(27)
np = neopixel.NeoPixel(pin, 1)  # 1 LED

np[0] = (255, 0, 0)  # RGB — red
np.write()

