from enum import Enum

class CoCoDeviceClass(Enum):
    SWITCHES = 'switches'
    LIGHTS = 'lights'
    SHUTTERS = 'shutters'
    COVERS = 'covers'
    GATE = 'gate'
    FANS = 'fans'
    SWITCHED_FANS = 'switched-fans'
    THERMOSTATS = 'thermostats'
    ENERGYMETERS = 'energymeters'
    ACCESSCONTROL = 'accesscontrol'
    GENERIC = 'generic'