from pydantic import Field, RootModel
from pydantic.dataclasses import dataclass
from datetime import datetime

@dataclass
class OwnTracksMessage:
    tst: int
    '''EPOCH timestamp'''
    lat: float 
    '''Latitude'''
    lon: float 
    '''Longitude'''
    vel: int
    '''Velocity in km/h'''
    cog: int
    '''Course over ground'''
    tid: str
    '''clientid'''
    created_at: int = Field(default_factory=lambda: int(datetime.timestamp(datetime.now())))
    '''Timestamp when message was created'''
    _type: str = 'location'
    '''OwnTracks message type'''

    def to_mqtt_payload(self):
        return RootModel[OwnTracksMessage](self).model_dump_json()

