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

from aiohttp import web


# noinspection PyUnusedLocal
class Esp4sHttpServer():
    def __init__(self, serial_handler):
        """
        This is the constructor for the Esplora HTTP server
        :param serial_handler: An instance to an existing serial handler
        :return: None
        """
        self.serial_handler = serial_handler
        self.command = None
        self.counter = 0

    @asyncio.coroutine
    def init(self, loop):
        """
        This is the method that starts the HTTP server to run
        :param loop: The asyncio event loop
        :return: An reference to this server
        """
        app = web.Application(loop=loop)

        # command blocks
        app.router.add_route('Get', '/poll', self.poll)
        app.router.add_route('GET', '/board_led/{off_on}', self.board_led)
        app.router.add_route('GET', '/leds/{leds}/{intensity}', self.leds)
        app.router.add_route('GET', '/play_tone/{notes}', self.play_tone)
        app.router.add_route('GET', '/tone2/{frequency}', self.tone2)
        app.router.add_route('Get', '/tinker_out/{tk_chan}/{value}', self.tinker_out)
        app.router.add_route('GET', '/orientation/{orientation}', self.board_orientation)
        app.router.add_route('GET', '/temp_units/{temp_units}', self.temp_units)

        # reporter blocks for Snap! (Scratch gets all sensor data in one shot from /poll
        app.router.add_route('GET', '/slider', self.slider)
        app.router.add_route('GET', '/light', self.light)
        app.router.add_route('GET', '/temp', self.temperature)
        app.router.add_route('GET', '/sound', self.sound)
        app.router.add_route('GET', '/buttons/{switch}', self.buttons)
        app.router.add_route('GET', '/joystick/{control}', self.joystick)
        app.router.add_route('GET', '/accel/{axis}', self.accelerometer)
        app.router.add_route('GET', '/tkInput/{tk_chan}', self.tkinput)

        srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 50209)
        print("Server started at http://127.0.0.1:50209")
        return srv

    @asyncio.coroutine
    def poll(self, request):
        """

        :param request: http request
        :return: All sensors status formatted for a Scratch poll response
        """
        # a set of dummy request objects to retrieve sensor status for a Scratch poll command
        rbd = RequestBD()
        rbu = RequestBU()
        rbl = RequestBL()
        rbr = RequestBR()

        jsb = RequestJB()
        jsx = RequestJX()
        jsy = RequestJY()

        asx = RequestAX()
        asy = RequestAX()
        asz = RequestAZ()

        tka = RequestTA()
        tkb = RequestTB()

        request = RequestTA()

        coros = [self.buttons(rbd, True), self.buttons(rbu, True), self.buttons(rbl, True), self.buttons(rbr, True),
                 self.slider(request, True), self.light(request, True), self.temperature(request, True),
                 self.sound(request, True),
                 self.joystick(jsb, True), self.joystick(jsx, True), self.joystick(jsy, True),
                 self.accelerometer(asx, True), self.accelerometer(asy, True), self.accelerometer(asz, True),
                 self.tkinput(tka, True), self.tkinput(tka, True)]

        #
        sensor_data_list = yield from asyncio.gather(*coros)

        sensor_poll_reply = 'buttons/Down ' + sensor_data_list[0] + '\n' + \
                            'buttons/Left ' + sensor_data_list[1] + '\n' + \
                            'buttons/Up ' + sensor_data_list[2] + '\n' + \
                            'buttons/Right ' + sensor_data_list[3] + '\n' + \
                            'slider ' + sensor_data_list[4] + '\n' + \
                            'light ' + sensor_data_list[5] + '\n' + \
                            'temp ' + sensor_data_list[6] + '\n' + \
                            'sound ' + sensor_data_list[7] + '\n' + \
                            'joystick/Button ' + sensor_data_list[8] + '\n' + \
                            'joystick/Left-Right_(X) ' + sensor_data_list[9] + '\n' + \
                            'joystick/Up-Down_(Y) ' + sensor_data_list[10] + '\n' + \
                            'accel/X__Side-Twist ' + sensor_data_list[11] + '\n' + \
                            'accel/Y__Front-Twist ' + sensor_data_list[12] + '\n' + \
                            'accel/Z__Raise-Lower ' + sensor_data_list[13] + '\n' + \
                            'tkInput/A ' + sensor_data_list[14] + '\n' + \
                            'tkInput/B ' + sensor_data_list[15] + '\n'

        return web.Response(headers={"Access-Control-Allow-Origin": "*"},
                            content_type="text/html; charset=ISO-8859-1", text=sensor_poll_reply)

    @asyncio.coroutine
    def board_led(self, request):
        """
        This method will toggle the "L" LED connected to pin 13
        :param request: http request
        :return: OK web response
        """

        off_on = request.match_info['off_on']
        self.command = 'L0\r\n'

        if off_on == 'On':
            self.command = 'L1\r\n'

        yield from self.serial_handler.write(self.command)
        return web.Response(body="ok".encode('utf-8'))

    @asyncio.coroutine
    def leds(self, request):
        """
        This method sets the Red, Green, or Blue RGB LED to a specified intensity
        :param request:
        :return:
        """
        leds = request.match_info['leds']
        intensity = request.match_info['intensity']
        self.command = leds + intensity + '\r\n'
        yield from self.serial_handler.write(self.command)
        return web.Response(body="ok".encode('utf-8'))

    @asyncio.coroutine
    def play_tone(self, request):
        """
        This will play a tone continuously at the specified frequency.
        To Turn off tone, set the frequency to 0.
        :param request: Command sent from Scratch/Snap!
        :return: HTTP response string
        """
        tone_chart = {"C": "523", "C_Sharp--D_Flat": "554", "D": "587", "D_Sharp--E_Flat": "622",
                      "E": "659", "F": "698", "F_Sharp--G_Flat": "740", "G": "783",
                      "G_Sharp--A_Flat": "831",
                      "A": "880", "A_Sharp--B_Flat": "932", "B": "958", "Note_Off": "0"}

        notes = request.match_info['notes']
        self.command = "T"
        self.command += tone_chart[notes] + '\r\n'
        yield from self.serial_handler.write(self.command)
        return web.Response(body="ok".encode('utf-8'))

    @asyncio.coroutine
    def tone2(self, request):
        """
        This method sends the Tone command to the Esplora
        :param request: Command sent from Scratch/Snap!
        :return: HTTP response string
        """
        frequency = request.match_info['frequency']
        self.command = "T"
        self.command += frequency + '\r\n'
        yield from self.serial_handler.write(self.command)
        return web.Response(body="ok".encode('utf-8'))

    @asyncio.coroutine
    def tinker_out(self, request):
        """
        This method sends the desired output level to the selected tinkerkit channel
        :param request: Command sent from Scratch/Snap
        :return: HTTP response string
        """
        tk_chan = request.match_info['tk_chan']
        value = request.match_info['value']
        # set up for channel A
        self.command = 'J'
        # but if it's B, modify the command
        if tk_chan == 'B':
            self.command = 'K'
        self.command += value + '\r\n'
        yield from self.serial_handler.write(self.command)
        return web.Response(body="ok".encode('utf-8'))

    @asyncio.coroutine
    def board_orientation(self, request):
        """
        This command sets board orientation state
        :param request: Command sent from Scratch/Snap
        :return: HTTP response string
        """
        orientation = request.match_info['orientation']
        if orientation == 'Joystick_On_Left':
            self.command = 'O1\r\n'
        else:
            self.command = 'O2\r\n'
        yield from self.serial_handler.write(self.command)
        return web.Response(body="ok".encode('utf-8'))

    @asyncio.coroutine
    def temp_units(self, request):
        """
        This command sets temp reporting units
        :param request: Command sent from Scratch/Snap
        :return: HTTP response string
        """
        temp_units = request.match_info['temp_units']
        if temp_units == 'Celcius':
            self.command = 'U0\r\n'
        else:
            self.command = 'U1\r\n'

        yield from self.serial_handler.write(self.command)
        return web.Response(body="ok".encode('utf-8'))

    @asyncio.coroutine
    def retrieve_status(self, status_command):
        """
        This method retrieves status data for the supplied status command.
        :param status_command: Command to be sent to the Esplora
        :return: The data value for the requested sensor
        """
        status_command += '\r\n'
        yield from self.serial_handler.write(status_command)
        data = yield from self.serial_handler.readline()
        return data

    @asyncio.coroutine
    def slider(self, request, poll=False):
        """
        This method retrieves the slider status value and returns it to HTTP client
        :param request: Command sent from Scratch/Snap!
        :param poll: This flag is used to return sensor data as opposed to an HTTP reply string
        :return: HTTP response
        """
        data = yield from self.retrieve_status("p")
        if poll:
            return data.decode('utf-8')
        else:
            return web.Response(headers={"Access-Control-Allow-Origin": "*"},
                                content_type="text/html; charset=ISO-8859-1", text=data.decode('utf-8'))

    @asyncio.coroutine
    def light(self, request, poll=False):
        """
        This method retrieves the status value for the light sensor
        :param request: Command sent from Scratch/Snap!
        :param poll: This flag is used to return sensor data as opposed to an HTTP reply string
        :return: HTTP response
        """
        data = yield from self.retrieve_status("l")
        if poll:
            return data.decode('utf-8')
        else:
            return web.Response(headers={"Access-Control-Allow-Origin": "*"},
                                content_type="text/html; charset=ISO-8859-1", text=data.decode('utf-8'))

    @asyncio.coroutine
    def temperature(self, request, poll=False):
        """
        This method retrieves the status value for the temperature sensor
        :param request: Command sent from Scratch/Snap!
        :param poll: This flag is used to return sensor data as opposed to an HTTP reply string
        :return: HTTP response
        """
        data = yield from self.retrieve_status("t")
        if poll:
            return data.decode('utf-8')
        else:
            return web.Response(headers={"Access-Control-Allow-Origin": "*"},
                                content_type="text/html; charset=ISO-8859-1", text=data.decode('utf-8'))

    @asyncio.coroutine
    def sound(self, request, poll=False):
        """
        This method retrieves the status value for the sound sensor
        :param request: Command sent from Scratch/Snap!
        :param poll: This flag is used to return sensor data as opposed to an HTTP reply string
        :return: HTTP response
        """
        data = yield from self.retrieve_status("s")
        if poll:
            return data.decode('utf-8')
        else:
            return web.Response(headers={"Access-Control-Allow-Origin": "*"},
                                content_type="text/html; charset=ISO-8859-1", text=data.decode('utf-8'))

    @asyncio.coroutine
    def buttons(self, request, poll=False):
        """
        This method retrieves the current requested button state
        :param request: Command sent from Scratch/Snap!
        :param poll: This flag is used to return sensor data as opposed to an HTTP reply string
        :return: response string containing current value
        """

        try:
            switch = request.match_info['switch']
            if switch == 'Down':
                self.command = "a"
            elif switch == 'Left':
                self.command = "b"
            elif switch == 'Up':
                self.command = "c"
            elif switch == 'Right':
                self.command = "d"
            else:
                raise MyHttpServerError('Unknown button designator')
            data = yield from self.retrieve_status(self.command)
            if poll:
                return data.decode('utf-8')
            else:
                return web.Response(headers={"Access-Control-Allow-Origin": "*"},
                                    content_type="text/html; charset=ISO-8859-1", text=data.decode('utf-8'))

        except MyHttpServerError as e:
            print(e.value)

    @asyncio.coroutine
    def joystick(self, request, poll=False):
        """
        This method retrieves the current requested joystick status item state
        :param request: Command sent from Scratch/Snap!
        :param poll: This flag is used to return sensor data as opposed to an HTTP reply string
        :return: response string containing current value
        """
        try:
            control = request.match_info['control']
            if control == 'Button':
                self.command = "e"
            elif control == 'Left-Right_(X)':
                self.command = "f"
            elif control == 'Up-Down_(Y)':
                self.command = "g"
            else:
                raise MyHttpServerError('Unknown joystick designator')
            data = yield from self.retrieve_status(self.command)
            if poll:
                return data.decode('utf-8')
            else:
                return web.Response(headers={"Access-Control-Allow-Origin": "*"},
                                    content_type="text/html; charset=ISO-8859-1", text=data.decode('utf-8'))

        except MyHttpServerError as e:
            print(e.value)

    @asyncio.coroutine
    def accelerometer(self, request, poll=False):
        """
        This method retrieves the current requested accelerometer axis status
        :param request: Command sent from Scratch/Snap!
        :param poll: This flag is used to return sensor data as opposed to an HTTP reply string
        :return: response string containing current value
        """
        try:
            axis = request.match_info['axis']
            if axis == 'X__Side-Twist':
                self.command = "x"
            elif axis == 'Y__Front-Twist':
                self.command = "y"
            elif axis == 'Z__Raise-Lower':
                self.command = "z"
            else:
                raise MyHttpServerError('Unknown accelerometer designator')
            data = yield from self.retrieve_status(self.command)
            if poll:
                return data.decode('utf-8')
            else:
                return web.Response(headers={"Access-Control-Allow-Origin": "*"},
                                    content_type="text/html; charset=ISO-8859-1", text=data.decode('utf-8'))

        except MyHttpServerError as e:
            print(e.value)

    @asyncio.coroutine
    def tkinput(self, request, poll=False):
        """
        This method retrieves the current requested tinker kit input channel status
        :param request: Command sent from Scratch/Snap!
        :param poll: This flag is used to return sensor data as opposed to an HTTP reply string
        :return: response string containing current value
        """
        try:
            tk_chan = request.match_info['tk_chan']
            if tk_chan == 'A':
                self.command = "u"
            elif tk_chan == 'B':
                self.command = "v"
            else:
                raise MyHttpServerError('Unknown tkinput designator')
            data = yield from self.retrieve_status(self.command)
            if poll:
                return data.decode('utf-8')
            else:
                return web.Response(headers={"Access-Control-Allow-Origin": "*"},
                                    content_type="text/html; charset=ISO-8859-1", text=data.decode('utf-8'))

        except MyHttpServerError as e:
            print(e.value)

# a custom exception
class MyHttpServerError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# dummy requests supplied to sensor data retrieval methods to support Scratch poll requests
class RequestBD:
    def __init__(self):
        self._match_info = None

    @property
    def match_info(self):
        return {'switch': "Down"}


class RequestBU:
    def __init__(self):
        self._match_info = None

    @property
    def match_info(self):
        return {'switch': "Up"}


class RequestBR:
    def __init__(self):
        self._match_info = None

    @property
    def match_info(self):
        return {'switch': "Left"}


class RequestBL:
    def __init__(self):
        self._match_info = None

    @property
    def match_info(self):
        return {'switch': "Right"}


class RequestJB:
    def __init__(self):
        self._match_info = None

    @property
    def match_info(self):
        return {'control': "Button"}


class RequestJX:
    def __init__(self):
        self._match_info = None

    @property
    def match_info(self):
        return {'control': "Left-Right_(X)"}


class RequestJY:
    def __init__(self):
        self._match_info = None

    @property
    def match_info(self):
        return {'control': "Up-Down_(Y)"}


class RequestAX:
    def __init__(self):
        self._match_info = None

    @property
    def match_info(self):
        return {'axis': "X__Side-Twist"}


class RequestAY:
    def __init__(self):
        self._match_info = None

    @property
    def match_info(self):
        return {'axis': "Y__Front-Twist"}


class RequestAZ:
    def __init__(self):
        self._match_info = None

    @property
    def match_info(self):
        return {'axis': "Y__Front-Twist"}


class RequestTA:
    def __init__(self):
        self._match_info = None

    @property
    def match_info(self):
        return {'tk_chan': 'A'}


class RequestTB:
    def __init__(self):
        self._match_info = None

    @property
    def match_info(self):
        return {'tk_chan': 'B'}