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
import logging
import sys
import signal

from esp4s_http_server import Esp4sHttpServer
import esplora_serial

# logging.basicConfig(level=logging.DEBUG)

# set the comport based upon command line parameter
if len(sys.argv) == 2:
    com_port = str(sys.argv[1])
else:
    com_port = '/dev/ttyACM0'

print('esp4s-aio version 1.0    Copyright(C) 2015 Alan Yorinks   All Rights Reserved')
print('{} {}'.format('Using COM port ', com_port))

arduino = esplora_serial.EsploraSerial(com_port)
http_server = Esp4sHttpServer(arduino)

loop = asyncio.get_event_loop()
asyncio.Task(http_server.init(loop))

# signal handler function called when Control-C occurs
def signal_handler(signal, frame):
    print("Control-C detected. See you soon.")
    loop.stop()
    loop.close()

# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)

try:
    loop.run_forever()
    loop.close()
except:
    pass