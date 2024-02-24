from teltonika_owntracks.owntracks_message import OwnTracksMessage
from teltonika_owntracks.__main__ import from_nmea
from pynmeagps import NMEAReader


def test_from_nmea():
    nmea = NMEAReader.parse('$GPRMC,153056.00,A,5128.167840,N,00530.031668,E,0.0,212.1,230224,1.5,W,A*2C')
    ot_msg: OwnTracksMessage = from_nmea(nmea)
    
    assert ot_msg.lat == 51 + 28.167840/60
    assert ot_msg.lon == 5 +30.031668/60

def test_from_nmea_02():
    nmea = NMEAReader.parse("$GPRMC,145733.00,A,5128.162939,N,00530.024650,E,0.4,302.7,240224,1.5,W,A*2F")
    ot_msg: OwnTracksMessage = from_nmea(nmea)

def test_as_mqtt_payload():
    nmea = NMEAReader.parse('$GPRMC,153056.00,A,5128.167840,N,00530.031668,E,0.0,212.1,230224,1.5,W,A*2C')
    ot_msg: OwnTracksMessage = from_nmea(nmea)
    payload = ot_msg.to_mqtt_payload()
    assert payload is not None

