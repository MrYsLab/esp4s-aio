# -*- coding: utf-8 -*-
"""
Created on April 28 11:39:15 2015

@author: Alan Yorinks
Copyright (c) 2015 Alan Yorinks All right reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import asyncio
import aiohttp

@asyncio.coroutine
def toggle_led():
    while True:
        yield from aiohttp.request('GET', 'http://localhost:50209/leds/Red/100')
        yield from asyncio.sleep(1)
        yield from aiohttp.request('GET', 'http://localhost:50209/leds/Red/0')
        yield from asyncio.sleep(1)
        yield from aiohttp.request('GET', 'http://localhost:50209/leds/Green/100')
        yield from asyncio.sleep(1)
        yield from aiohttp.request('GET', 'http://localhost:50209/leds/Green/0')
        yield from asyncio.sleep(1)
        yield from aiohttp.request('GET', 'http://localhost:50209/leds/Blue/100')
        yield from asyncio.sleep(1)
        yield from aiohttp.request('GET', 'http://localhost:50209/leds/Blue/0')
        yield from asyncio.sleep(1)

@asyncio.coroutine
def get_down_button():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/buttons/Down')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    data = val.decode('utf-8')
    return data

@asyncio.coroutine
def get_up_button():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/buttons/Up')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return val.decode('utf-8')

@asyncio.coroutine
def get_left_button():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/buttons/Left')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return val.decode('utf-8')

@asyncio.coroutine
def get_right_button():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/buttons/Right')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return val.decode('utf-8')

@asyncio.coroutine
def get_slider():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/slider')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return  val.decode('utf-8')

@asyncio.coroutine
def get_light():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/light')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return  val.decode('utf-8')

@asyncio.coroutine
def get_temp():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/temp')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return  val.decode('utf-8')

@asyncio.coroutine
def get_sound():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/sound')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return  val.decode('utf-8')

@asyncio.coroutine
def get_joystick_button():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/joystick/Button')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return  val.decode('utf-8')

@asyncio.coroutine
def get_joystick_x():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/joystick/Left-Right_(X)')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return  val.decode('utf-8')

@asyncio.coroutine
def get_joystick_y():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/joystick/Up-Down_(Y)')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return  val.decode('utf-8')

@asyncio.coroutine
def get_acc_x():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/accel/X__Side-Twist')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return  val.decode('utf-8')

@asyncio.coroutine
def get_acc_y():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/accel/Y__Front-Twist')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return  val.decode('utf-8')

@asyncio.coroutine
def get_acc_z():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/accel/Z__Raise-Lower')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return  val.decode('utf-8')

@asyncio.coroutine
def get_tk_a():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/tkInput/A')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return  val.decode('utf-8')

@asyncio.coroutine
def get_tk_b():
    resp = yield from aiohttp.request('GET', 'http://localhost:50209/tkInput/B')
    val = yield from resp.read()
    val = val[:-2]
    yield from asyncio.sleep(.1)
    return  val.decode('utf-8')

@asyncio.coroutine
def retrieve_sensors():
    while True:
        coros = [get_down_button(), get_up_button(), get_left_button(), get_right_button(),
                 get_slider()]


        z = yield from asyncio.gather(*coros)
        asyncio.sleep(.001)
        print(z)

loop = asyncio.get_event_loop()
asyncio.Task(retrieve_sensors())
asyncio.Task(toggle_led())

loop.run_forever()
loop.close()

