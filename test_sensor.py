import board
import adafruit_bh1750

i2c = board.I2C()
sensor = adafruit_bh1750.BH1750(i2c)

print(f"SENSOR MEASURING: {sensor.lux} LUX")
