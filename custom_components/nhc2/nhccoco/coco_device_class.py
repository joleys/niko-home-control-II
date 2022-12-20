from enum import Enum

class CoCoDeviceClass(Enum):
    SWITCHES = 'switches'
    LIGHTS = 'lights'
    COVERS = 'covers'
    GATE = 'gate'
    FANS = 'fans'
    SWITCHED_FANS = 'switched-fans'
    THERMOSTATS = 'thermostats'
    ENERGYMETERS = 'energymeters'
    ACCESSCONTROL = 'accesscontrol'
    BUTTONS = 'buttons'
    SMARTPLUGS = 'smartplugs'
    GENERIC = 'generic'
    VIRTUAL = 'virtual'
