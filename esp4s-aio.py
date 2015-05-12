__author__ = 'afy'

import asyncio
from esp4s_http_server import Esp4sHttpServer
import esplora_serial
import logging


logging.basicConfig(level=logging.DEBUG)

arduino = esplora_serial.EsploraSerial()
http_server = Esp4sHttpServer(arduino)

loop = asyncio.get_event_loop()
asyncio.Task(http_server.init(loop))

try:
    loop.run_forever()
    loop.close()
except:
    pass