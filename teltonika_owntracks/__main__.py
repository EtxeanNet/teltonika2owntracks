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
from .movement_detector import MovementDetector
from .utils import to_timestamp

logging.basicConfig(level=Settings().loglevel, format='%(asctime)s [%(levelname)s] %(name)s - %(message)s')
logger = logging.getLogger(__name__)

def from_nmea(nmea: NMEAMessage, client_id = 'TC') -> OwnTracksMessage:
        tst = to_timestamp(datetime.combine(nmea.date, nmea.time))
        lat = nmea.lat
        lon = nmea.lon
        vel = int(knots2spd(nmea.spd, 'KMPH'))
        cog = int(nmea.cog)
        tid = client_id

        return OwnTracksMessage(tst, lat, lon, vel, cog, tid)

async def publish(publisher: OwnTracksPublisher, detector: MovementDetector, nmea: NMEAMessage):
        if nmea.msgID != "RMC":
            return
               
        ot_msg: OwnTracksMessage = from_nmea(nmea)
        has_moved = detector.has_moved(ot_msg.tst, ot_msg.lat, ot_msg.lon)
        if has_moved:
            await publisher.publish(ot_msg)
        else:
            logger.debug('No movement detected')


async def main():
    settings = Settings()
    publisher = OwnTracksPublisher(settings)
    listener = NMEAListener(settings)
    detector = MovementDetector()
    await listener.listen(partial(publish,publisher, detector))

if __name__ == '__main__':
    asyncio.run(main())