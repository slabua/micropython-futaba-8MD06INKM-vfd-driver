# -*- coding: utf-8 -*-
"""Futaba 000FV959IN / BOE CIG14-0604B, 8-MD-06INKM, 16-SD-13GINK VFD
   Micropython Driver for the Raspberry Pi Pico, with Framebuffer support.
"""

__author__ = "Salvatore La Bua"

import framebuf
from futaba_vfd_fb import FutabaVFD
from machine import Pin, SPI
from random import randrange
from utime import sleep, sleep_ms

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

display = FutabaVFD(spi, rst_pin, cs_pin, en_pin, digits=8, dimming=10)

sleep(1)

display.set_dimming(255)

display.write_str(0, "0123456789ABCDEF")
sleep(1)

display.fadeout(delay_ms=5)
display.fadein(delay_ms=5, dimming=10)
sleep(1)

for i in range(display.digits):
    display.scramble(address=randrange(display.digits), n_times=randrange(10))
    sleep_ms(randrange(50, 500))
sleep(1)

i = 0
for _ in range(5 * display.digits):
    display.fill(0)
    display.text("0123456789ABCDEF", i, 0 if (i % 2 == 0) else -1)
    display.show_fb()
    sleep(0.075)
    i += 1
for _ in range(5 * display.digits):
    i -= 1
    display.fill(0)
    display.text("0123456789ABCDEF", i, 0)
    display.show_fb()
    sleep(0.03)
sleep(1)

display.clear()
display.write_str(
    display.digits, "Writing a long String to see scrolling.", scroll=True, delay_ms=100
)
sleep(1)

display.write_str(0, "ÄäÖöÜü°")
sleep(1)

display.write_str(0, "0123456789ABCDEF")
sleep(1)

buf = bytearray(5)
fbuf = framebuf.FrameBuffer(buf, 5, 7, framebuf.MONO_VLSB)
fbuf.rect(0, 0, 5, 7, 1)
display.write_fb(0, buf)
sleep(1)

bits = [0x0C, 0x1E, 0x3C, 0x1E, 0x0C]
display.write_bits(0, bits)
# buf[:] = bytearray(bits)
# display.write_fb(display.digits - 1, buf)
display.write_bits(display.digits - 1, bits)
sleep(1)

display.clear(0)
display.clear(display.digits - 1)
sleep(1)

display.clear()
sleep(1)

display.disable()
sleep(1)

display.enable()
sleep(1)

display.disable()
display.off()
