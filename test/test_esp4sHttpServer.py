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
import pytest

from esp4s_http_server import Esp4sHttpServer
from esplora_serial import EsploraSerial


# noinspection PyUnusedLocal,PyUnresolvedReferences
class TestEsp4sHttpServer:
    @pytest.mark.asyncio
    def test_board_led(self, mocker):
        # allow the instantiation of EsploraSerial to proceed without a real serial connection
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        # test for LED Off
        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'off_on': 'Off'}

        r = Request()
        yield from my_server.board_led(r)
        assert my_server.command == 'L0\r\n'

        # test for LED On
        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'off_on': 'On'}

        r = Request()
        yield from my_server.board_led(r)
        assert my_server.command == 'L1\r\n'

    @pytest.mark.asyncio
    def test_leds(self, mocker):
        # allow the instantiation of EsploraSerial to proceed without a real serial connection
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        # test for LED Off
        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'leds': 'red', 'intensity': '100'}

        r = Request()
        yield from my_server.leds(r)
        assert my_server.command == 'red100\r\n'

    @pytest.mark.asyncio
    def test_play_tone(self, mocker):
        # allow the instantiation of EsploraSerial to proceed without a real serial connection
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        # test for LED Off
        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'notes': 'G_Sharp--A_Flat'}

        r = Request()
        yield from my_server.play_tone(r)
        assert my_server.command == 'T831\r\n'

    @pytest.mark.asyncio
    def test_tone2(self, mocker):
        # allow the instantiation of EsploraSerial to proceed without a real serial connection
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'frequency': '1000'}

        r = Request()
        yield from my_server.tone2(r)
        assert my_server.command == 'T1000\r\n'

    @pytest.mark.asyncio
    def test_tinker_out(self, mocker):
        # allow the instantiation of EsploraSerial to proceed without a real serial connection
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'tk_chan': 'A', 'value': '123'}

        r = Request()
        yield from my_server.tinker_out(r)
        assert my_server.command == 'J123\r\n'

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'tk_chan': 'B', 'value': '456'}

        r = Request()
        yield from my_server.tinker_out(r)
        assert my_server.command == 'K456\r\n'

    @pytest.mark.asyncio
    def test_board_orientation(self, mocker):
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'orientation': 'Joystick_On_Left'}

        r = Request()

        yield from my_server.board_orientation(r)
        assert my_server.command == 'O1\r\n'

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'orientation': 'Joystick_On_Right'}

        r = Request()

        yield from my_server.board_orientation(r)
        assert my_server.command == 'O2\r\n'

    @pytest.mark.asyncio
    def test_temp_units(self, mocker):
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'temp_units': 'Celcius'}

        r = Request()

        status_text = yield from my_server.temp_units(r)
        assert my_server.command == 'U0\r\n'

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'temp_units': 'Fahrenheit'}

        r = Request()

        yield from my_server.temp_units(r)
        assert my_server.command == 'U1\r\n'

    @pytest.mark.asyncio
    def test_slider(self, monkeypatch, mocker):
        # allow the instantiation of EsploraSerial to proceed without a real serial connection
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        @asyncio.coroutine
        def mockreturn(readline):
            return b'440'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'slider': 'slider'}

        r = Request()
        # my_server.status_text = ""
        status_text = yield from my_server.slider(r, True)
        assert status_text == '440'

    @pytest.mark.asyncio
    def test_light(self, monkeypatch, mocker):
        # allow the instantiation of EsploraSerial to proceed without a real serial connection
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        @asyncio.coroutine
        def mockreturn(readline):
            return b'955'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'light': 'light'}

        r = Request()

        status_text = yield from my_server.light(r, True)
        assert status_text == '955'

    @pytest.mark.asyncio
    def test_temperature(self, monkeypatch, mocker):
        # allow the instantiation of EsploraSerial to proceed without a real serial connection
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        @asyncio.coroutine
        def mockreturn(readline):
            return b'19'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'temp': 'temp'}

        r = Request()

        status_text = yield from my_server.temperature(r, True)
        assert status_text == '19'

    @pytest.mark.asyncio
    def test_sound(self, monkeypatch, mocker):
        # allow the instantiation of EsploraSerial to proceed without a real serial connection
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        @asyncio.coroutine
        def mockreturn(readline):
            return b'55'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'sound': 'sound'}

        r = Request()

        status_text = yield from my_server.sound(r, True)
        assert status_text == '55'

    @pytest.mark.asyncio
    def test_buttons(self, monkeypatch, mocker):
        # allow the instantiation of EsploraSerial to proceed without a real serial connection
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        @asyncio.coroutine
        def mockreturn(readline):
            return b'2'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'switch': 'Down'}

        r = Request()

        status_text = yield from my_server.buttons(r, True)
        assert status_text == '2'

        @asyncio.coroutine
        def mockreturn(readline):
            return b'4'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'switch': 'Up'}

        r = Request()

        status_text = yield from my_server.buttons(r, True)
        assert status_text == '4'

        @asyncio.coroutine
        def mockreturn(readline):
            return b'6'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'switch': 'Left'}

        r = Request()

        status_text = yield from my_server.buttons(r, True)
        assert status_text == '6'

        @asyncio.coroutine
        def mockreturn(readline):
            return b'8'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'switch': 'Right'}

        r = Request()

        status_text = yield from my_server.buttons(r, True)
        assert status_text == '8'

    @pytest.mark.asyncio
    def test_joystick(self, monkeypatch, mocker):
        # allow the instantiation of EsploraSerial to proceed without a real serial connection
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        @asyncio.coroutine
        def mockreturn(readline):
            return b'2'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'control': 'Button'}

        r = Request()

        status_text = yield from my_server.joystick(r, True)
        assert status_text == '2'

        @asyncio.coroutine
        def mockreturn(readline):
            return b'4'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'control': 'Left-Right_(X)'}

        r = Request()

        status_text = yield from my_server.joystick(r, True)
        assert status_text == '4'

        @asyncio.coroutine
        def mockreturn(readline):
            return b'6'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'control': 'Up-Down_(Y)'}

        r = Request()

        status_text = yield from my_server.joystick(r, True)
        assert status_text == '6'

    @pytest.mark.asyncio
    def test_accelerometer(self, monkeypatch, mocker):
        # allow the instantiation of EsploraSerial to proceed without a real serial connection
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        @asyncio.coroutine
        def mockreturn(readline):
            return b'2'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'axis': 'X__Side-Twist'}

        r = Request()

        status_text = yield from my_server.accelerometer(r, True)
        assert status_text == '2'

        @asyncio.coroutine
        def mockreturn(readline):
            return b'4'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'axis': 'Y__Front-Twist'}

        r = Request()

        status_text = yield from my_server.accelerometer(r, True)
        assert status_text == '4'

        @asyncio.coroutine
        def mockreturn(readline):
            return b'6'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'axis': 'Z__Raise-Lower'}

        r = Request()

        status_text = yield from my_server.accelerometer(r, True)
        assert status_text == '6'

    @pytest.mark.asyncio
    def test_tkinput(self, monkeypatch, mocker):
        # allow the instantiation of EsploraSerial to proceed without a real serial connection
        mocker.patch('serial.Serial')

        # instantiate necessary objects
        my_serial = EsploraSerial("/dev/ttyACM0")
        my_server = Esp4sHttpServer(my_serial)

        @asyncio.coroutine
        def mockreturn(readline):
            return b'2'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'tk_chan': 'A'}

        r = Request()

        status_text = yield from my_server.tkinput(r, True)
        assert status_text == '2'

        @asyncio.coroutine
        def mockreturn(readline):
            return b'4'

        monkeypatch.setattr(EsploraSerial, 'readline', mockreturn)

        class Request:
            def __init__(self):
                self._match_info = None

            @property
            def match_info(self):
                return {'tk_chan': 'B'}

        r = Request()

        status_text = yield from my_server.tkinput(r, True)
        assert status_text == '4'
