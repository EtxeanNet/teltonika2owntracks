import asyncio
from datetime import datetime
from functools import partial
import logging

from pynmeagps import NMEAMessage
from pynmeagps.nmeahelpers import knots2spd

from.settings import Settings
from .nmea_listener import NMEAListener
from .owntracks_message import OwnTracksMessage
from .owntracks_publisher import OwnTracksPublisher
from .utils import to_timestamp

logging.basicConfig(level=Settings().loglevel, format='%(asctime)s [%(levelname)s] %(name)s - %(message)s')

def from_nmea(nmea: NMEAMessage, client_id = 'TC') -> OwnTracksMessage:
        tst = to_timestamp(datetime.combine(nmea.date, nmea.time))
        lat = nmea.lat
        lon = nmea.lon
        vel = int(knots2spd(nmea.spd, 'KMPH'))
        cog = int(nmea.cog)
        tid = client_id

        return OwnTracksMessage(tst, lat, lon, vel, cog, tid)

async def publish(publisher: OwnTracksPublisher, nmea: NMEAMessage):
        if nmea.msgID != "RMC":
            return
        await publisher.publish(from_nmea(nmea))

async def main():
    settings = Settings()
    publisher = OwnTracksPublisher(settings)
    listener = NMEAListener(settings)
    await listener.listen(partial(publish,publisher))

if __name__ == '__main__':
    asyncio.run(main())