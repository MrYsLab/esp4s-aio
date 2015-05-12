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

import serial


class EsploraSerial():
    """
    This class encapsulates management of the serial port that communicates with the Arduino Esplora
    It initializes the serial port, provides write capabilities to send data to the Esplora.
    """

    def __init__(self, com_port='/dev/ttyACM0', speed=115200):
        """
        This is the constructor for the aio serial handler
        :param com_port: Com port designator
        :param speed: baud rate
        :return: None
        """
        self.my_serial = serial.Serial(com_port, speed, timeout=1, writeTimeout=1)

    def get_serial(self):
        """
        This method returns a reference to the serial port in case the user wants to call pyserial methods directly
        :return: pyserial instance
        """
        return self.my_serial

    @asyncio.coroutine
    def write(self, data):
        """
        This is an asyncio adapted version of pyserial write. It provides a non-blocking write and returns the
        number of bytes written upon completion
        :param data: Data to be written
        :return: Number of bytes written
        """
        # the secret sauce
        future = asyncio.Future()
        result = None
        try:
            result = self.my_serial.write(str.encode(data))
        except serial.SerialException:
            print('Write exception')

        future.set_result(result)
        while True:
            if not future.done():
                # spin our asyncio wheels until future completes
                asyncio.sleep(.1)
            else:
                return future.result()

    @asyncio.coroutine
    def readline(self):
        """
        This is an asyncio adapted version of pyserial read. It provides a non-blocking read and returns a line of
        data read.
        :return: A line of data
        """
        future = asyncio.Future()
        data_available = False
        while True:
            if not data_available:
                if not self.my_serial.inWaiting():
                    asyncio.sleep(.001)
                else:
                    data_available = True
                    data = self.my_serial.readline()
                    future.set_result(data)
            else:
                if not future.done():
                    asyncio.sleep(.1)
                else:
                    return future.result()


class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

