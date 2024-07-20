# Futaba VFD Micropython Driver for the Raspberry Pi Pico, with Framebuffer support

## Verified supported displays
### 6 Digits
- Futaba 000FV959IN
- BOE CIG14-0604B
### 8 Digits
- Futaba 8-MD-06INKM
### 16 Digits
- Futaba 16-SD-13GINK (partial framebuffer support, wip)

## Functions

| Function | Parameters | Description |
| --- | --- | --- |
| init() | TODO | TODO |
| clear() | TODO | TODO |
| clear(address: int) | TODO | TODO |
| disable() | TODO | TODO |
| enable() | TODO | TODO |
| fadein(delay_ms: int, dimming: int) | TODO | TODO |
| fadeout(delay_ms: int, dimming: int) | TODO | TODO |
| off() | TODO | TODO |
| on() | TODO | TODO |
| reset() | TODO | TODO |
| scramble(address: int, n_times: int) | TODO | TODO |
| set_dimming(dimming: int) | TODO | TODO |
| show_fb() | TODO | TODO |
| standby(is_standby: bool) | TODO | TODO |
| store_custom_symbol(address: int, data: list) | TODO | TODO |
| write_bits(address: int, bits: list) | TODO | TODO |
| write_char(address: int, char: int) | TODO | TODO |
| write_fb(address: int, buf: bytearray) | TODO | TODO |
| write_str(address: int, msg: str, scroll: bool, delay_ms: int) | TODO | TODO |


## References
Based on the official datasheet and the following repositories:

[https://github.com/zhcong/8MD06INKM-for-micropython](https://github.com/zhcong/8MD06INKM-for-micropython)

[https://github.com/Reboot93/MicroPython-8MD-06INKM-display-driver](https://github.com/Reboot93/MicroPython-8MD-06INKM-display-driver)

[https://github.com/3KUdelta/Futaba-VFD-16bit_ESP32](https://github.com/3KUdelta/Futaba-VFD-16bit_ESP32)

[https://github.com/sfxfs/ESP32-VFD-8DM-Arduino](https://github.com/sfxfs/ESP32-VFD-8DM-Arduino)
