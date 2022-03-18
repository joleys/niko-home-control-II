from enum import Enum


class CoCoDeviceClass(Enum):
    SWITCHES = 'switches'
    LIGHTS = 'lights'
    SHUTTERS = 'shutters'
    GATE = 'gate'
    FANS = 'fans'
    SWITCHED_FANS = 'switched-fans'
    THERMOSTATS = 'thermostats'
    ENERGYMETERS = 'energymeters'
    GARAGEDOORS = 'garagedoors'
    GENERIC = 'generic'
