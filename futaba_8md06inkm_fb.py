# -*- coding: utf-8 -*-
"""Futaba 8MD06INKM VFD Micropython Driver for Pico, with Framebuffer support.
"""

__author__ = "Salvatore La Bua"
__copyright__ = "Copyright 2024, Salvatore La Bua"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Salvatore La Bua"
__email__ = "slabua@gmail.com"
__status__ = "Development"

import framebuf
from micropython import const
from utime import sleep, sleep_ms

DGRAM_DATA_CLEAR = const(0x10)
DCRAM_DATA_WRITE = const(0x20)
CGRAM_DATA_WRITE = const(0x40)
URAM_DATA_WRITE = const(0x80)
SET_DISPLAY_TIMING = const(0xE0)
SET_DIMMING_DATA = const(0xE4)
SET_DISPLAY_LIGHT_ON = const(0xE8)
SET_DISPLAY_LIGHT_OFF = const(0xEA)
SET_STAND_BY_MODE = const(0xEC)
EMPTY_DATA = const(0x00)


class futaba_8md06inkm_fb(framebuf.FrameBuffer):

    def __init__(self, spi, rst, cs, en, digits=8, dimming=255):
        self.spi = spi
        self.rst = rst
        self.cs = cs
        self.en = en
        self.digits = digits
        self.dimming = dimming

        self.en.value(1)
        self.rst.value(1)
        sleep(0.1)
        self.cs.value(1)

        self.rst.value(0)
        sleep_ms(10)
        self.rst.value(1)
        sleep_ms(3)

        self.buffer = bytearray(5 * self.digits)
        super().__init__(self.buffer, 5 * self.digits, 7, framebuf.MONO_VLSB)

        self.init()

    def init(self):
        for cmd in (
            (SET_DISPLAY_TIMING, self.digits - 1),
            (SET_DIMMING_DATA, self.dimming),
            (SET_DISPLAY_LIGHT_ON, EMPTY_DATA),
        ):
            self.__write_cmd(cmd)

        self.standby(False)
        self.clear()

        for i in range(10, 0, -1):
            for j in range(self.digits):
                self.write_str(j, chr(i + 0x30))
                sleep(0.008)
        self.clear()

    def clear(self, *address: int):
        if address:
            self.__write_cmd((DCRAM_DATA_WRITE | address[0], DGRAM_DATA_CLEAR))
        else:
            for i in range(self.digits):
                self.__write_cmd((DCRAM_DATA_WRITE | i, DGRAM_DATA_CLEAR))

    def disable(self):
        self.en.value(0)

    def enable(self):
        self.en.value(1)

    def fadein(self, delay_ms, dimm=None):
        if dimm is None:
            dimm = self.dimming
        for dim in range(dimm):
            self.set_dimming(dim)
            sleep_ms(delay_ms)

    def fadeout(self, delay_ms, dimm=None):
        if dimm is None:
            dimm = self.dimming
        for dim in range(dimm, -1, -1):
            self.set_dimming(dim)
            sleep_ms(delay_ms)

    def off(self):
        self.__write_cmd([SET_DISPLAY_LIGHT_OFF, EMPTY_DATA])

    def on(self):
        self.__write_cmd([SET_DISPLAY_LIGHT_ON, EMPTY_DATA])

    def reset(self):
        self.rst.value(0)
        sleep(0.1)
        self.rst.value(1)

    def scramble(self, address, n_times=10):
        for i in range(n_times):
            self.write_char(address, i + 48)
            sleep_ms(10)

    def set_dimming(self, dimming: int):
        self.dimming = dimming
        self.__write_cmd((SET_DIMMING_DATA, dimming))

    def show_fb(self):
        buf = bytearray(5)
        fbuf = framebuf.FrameBuffer(buf, 5, 7, framebuf.MONO_VLSB)
        for i in range(self.digits):
            fbuf.fill(0)
            fbuf.blit(self, 0 - (i * 5), 0)
            self.__write_data(i, buf)
        for i in range(self.digits):
            self.__write_cmd((DCRAM_DATA_WRITE | i, i))

    def standby(self, is_standby):
        self.__write_cmd([SET_STAND_BY_MODE | is_standby, EMPTY_DATA])

    def write_bits(self, address, bits_list):
        self.__store_custom_symbol(address, bits_list)
        self.write_char(address, address)

    def write_char(self, address, char):
        self.__write_cmd((DCRAM_DATA_WRITE | address, char))

    def write_fb(self, address: int, buf: bytearray):
        self.__write_data(address, buf)
        self.__write_cmd((DCRAM_DATA_WRITE | address, address))

    def write_str(self, address: int, msg: str):
        for i in msg:
            self.__write_cmd((DCRAM_DATA_WRITE | address, ord(i)))
            if address < self.digits - 1:
                address += 1
            else:
                break

    # # TODO
    # def write_str_scroll(self, address, msg, delay_ms=100):
    #     for i in range(address + len(msg) - self.digits + 1):
    #         for j in range(len(msg)):
    #             self.write_char(address - i + j, ord(msg[j]))
    #         sleep_ms(delay_ms)

    def __msb_to_lsb(self, msb_data):
        lsb_data = EMPTY_DATA
        lsb_data = lsb_data | ((msb_data & (URAM_DATA_WRITE >> 0)) >> 7)
        lsb_data = lsb_data | ((msb_data & (URAM_DATA_WRITE >> 1)) >> 5)
        lsb_data = lsb_data | ((msb_data & (URAM_DATA_WRITE >> 2)) >> 3)
        lsb_data = lsb_data | ((msb_data & (URAM_DATA_WRITE >> 3)) >> 1)
        lsb_data = lsb_data | ((msb_data & (URAM_DATA_WRITE >> 4)) << 1)
        lsb_data = lsb_data | ((msb_data & (URAM_DATA_WRITE >> 5)) << 3)
        lsb_data = lsb_data | ((msb_data & (URAM_DATA_WRITE >> 6)) << 5)
        lsb_data = lsb_data | ((msb_data & (URAM_DATA_WRITE >> 7)) << 7)

        return lsb_data

    def __store_custom_symbol(self, address, data_list):
        self.cs.value(0)
        data = bytearray(1)
        data[0] = self.__msb_to_lsb(CGRAM_DATA_WRITE + address)
        self.spi.write(data)
        sleep_ms(1)
        data[0] = self.__msb_to_lsb(data_list[0])
        self.spi.write(data)
        sleep_ms(1)
        data[0] = self.__msb_to_lsb(data_list[1])
        self.spi.write(data)
        sleep_ms(1)
        data[0] = self.__msb_to_lsb(data_list[2])
        self.spi.write(data)
        sleep_ms(1)
        data[0] = self.__msb_to_lsb(data_list[3])
        self.spi.write(data)
        sleep_ms(1)
        data[0] = self.__msb_to_lsb(data_list[4])
        self.spi.write(data)
        self.cs.value(1)

    def __write_cmd(self, cmd):
        self.cs.value(0)
        for i in cmd:
            data_list = bytearray(1)
            data_list[0] = self.__msb_to_lsb(i)
            self.spi.write(data_list)
        self.cs.value(1)

    def __write_data(self, address: int, buf):
        self.cs.value(0)
        data_list = bytearray(1)
        data_list[0] = self.__msb_to_lsb(CGRAM_DATA_WRITE | address)
        self.spi.write(data_list)
        for i in buf:
            data_list = bytearray(1)
            data_list[0] = self.__msb_to_lsb(i)
            self.spi.write(data_list)
        self.cs.value(1)