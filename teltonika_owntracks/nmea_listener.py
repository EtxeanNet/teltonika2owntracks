import logging
import asyncio
from pynmeagps import NMEAReader, NMEAMessage
from collections.abc import Callable, Awaitable

from .settings import Settings

logger = logging.getLogger(__name__)

class NMEAListener:
    '''Listener for NMEA messages on TCP socket'''
    def __init__(self, settings: Settings):
        self._host = settings.listen_host
        self._port = settings.listen_port
        self._server = None

    async def listen(self, publisher_func: Callable[[NMEAMessage], Awaitable[None]]):
        self._publish = publisher_func
        self._server = await asyncio.start_server(
            self.handle, self._host, self._port)

        logger.info('Listening on %s:%s' % (self._host, self._port))
        async with self._server:
            await self._server.serve_forever()
        logger.info('Stopped listening')

    @property
    def started(self):
        return self._server is not None and self._server.sockets

    def stop(self):
        logger.info('Stopping...')
        self._server.close()

    async def handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        try:
            logger.debug('Handle connection')
            while True:
                line = await reader.readline()
                if not line:
                    break

                try:
                    line = line.decode().rstrip()
                    if line:
                        await self.process_nmea(line)
                except UnicodeDecodeError:
                    # silently ignore line decoding errors
                    pass

            logger.debug('Connection closed')

        except Exception as _:
            logging.exception("Error occurred while handling connection")
            self.stop()

    async def process_nmea(self, nmea_sentence: str):
        logger.debug(f'Received {nmea_sentence}')
        nmea_msg: NMEAMessage = NMEAReader.parse(nmea_sentence)
        await self._publish(nmea_msg)