import framebuf
from futaba_8md06inkm_fb import futaba_8md06inkm_fb
from machine import Pin, SPI
from utime import sleep

rst_pin = Pin(4, Pin.OUT)
cs_pin = Pin(5, Pin.OUT)
en_pin = Pin(20, Pin.OUT)

spi = SPI(
    id=0,
    baudrate=100_000,
    polarity=1,
    phase=1,
    sck=Pin(18, Pin.OUT),
    mosi=Pin(19, Pin.OUT),
)

display = futaba_8md06inkm_fb(spi, rst_pin, cs_pin, en_pin, digits=6, dimming=10)

display.set_dimming(10)
sleep(1)
display.set_dimming(255)

bits = [0x0C, 0x1E, 0x3C, 0x1E, 0x0C]

i = 0
for _ in range(5 * display.digits):
    display.fill(0)
    display.text("01234567", i, 0 if (i % 2 == 0) else -1)
    display.show_fb()
    sleep(0.075)
    i += 1
for _ in range(5 * display.digits):
    i -= 1
    display.fill(0)
    display.text("01234567", i, 0)
    display.show_fb()
    sleep(0.03)

# sleep(1)
# display.write_str_scroll(display.digits, "Writing a long String to see scrolling.")
sleep(1)
display.write_str(0, "ÄäÖöÜü°")
sleep(1)

display.write_str(0, "01234567")
sleep(1)

buf = bytearray(5)
fbuf = framebuf.FrameBuffer(buf, 5, 7, framebuf.MONO_VLSB)
fbuf.rect(0, 0, 5, 7, 1)
display.write_fb(0, buf)
sleep(1)
display.write_bits(0, bits)
sleep(1)

display.disable()
sleep(1)
display.enable()
sleep(1)

display.clear(0)
sleep(1)
display.clear()
sleep(1)

display.disable()
