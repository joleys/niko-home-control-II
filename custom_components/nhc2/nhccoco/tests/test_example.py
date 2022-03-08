from nhc2_coco import CoCo
from nhc2_coco.coco_device_class import CoCoDeviceClass
from nhc2_coco.tests.credentials import HOST, USER, PASS, PORT

"""
 Please leave this file intact. Copy/paste it and the credentials_example.py to
 test.py and credentials.py and use those to test stuff.
"""
print('Connecting and waiting for results...')
coco = CoCo(HOST, USER, PASS, port=PORT)
coco.connect()


def generics(all):
    print('generics')
    def light_changed(generic):
        def callback():
            base_state = 'ON' if generic.is_on else 'OFF'
            print('State of generic %s has changed to %s' % (generic.name, base_state))
        return callback

    for generic in all:
        generic.on_change = light_changed(generic)

    print()
    print("Found %d generic(s) on the CoCo" % len(all))
    for generic in all:
        base_state = 'ON' if generic.is_on else 'OFF'
        print("[ %s ] is at %s" % (generic.name, base_state))


def shutters(all):
    print()
    print("Found %d shutter(s) on the CoCo" % len(all))
    for shutter in all:
        print("[ %s ] is at %s%%" % (shutter.name, shutter.position))


def switches(all):
    def switch_changed(switch):
        def callback():
            print('State of switch %s has changed to %s' % (switch.name, 'ON' if switch.is_on else 'OFF'))

        return callback

    are_on = list(map(lambda x: x.name, filter(lambda x: x.is_on, all)))
    are_off = list(map(lambda x: x.name, filter(lambda x: not x.is_on, all)))
    # Put all callbacks in place to react to state changes
    for switch in all:
        switch.on_change = switch_changed(switch)

    print()
    print("Found %d switch(es) on the CoCo" % len(all))
    print("Are  ON: ", are_on)
    print("Are OFF: ", are_off)


def lights(all):
    def light_changed(light):
        def callback():
            base_state = 'ON' if light.is_on else 'OFF'
            if light.support_brightness:
                print('State of light %s has changed to %s, brightness %i%%' % (light.name, base_state, light.brightness))
            else:
                print('State of light %s has changed to %s' % (light.name, base_state))
        return callback

    dimmable = list(filter(lambda x: x.support_brightness, all))
    are_on = list(map(lambda x: x.name, filter(lambda x: x.is_on, all)))
    are_off = list(map(lambda x: x.name, filter(lambda x: not x.is_on, all)))
    # Put all callbacks in place to react to state changes
    for light in all:
        light.on_change = light_changed(light)

    print()
    print("Found %d light(s) on the CoCo of which %d are/is dimmable." % (len(all), len(dimmable)))
    print("Are  ON: ", are_on)
    print("Are OFF: ", are_off)


coco.get_devices(CoCoDeviceClass.SHUTTERS, shutters)
coco.get_devices(CoCoDeviceClass.SWITCHES, switches)
coco.get_devices(CoCoDeviceClass.LIGHTS, lights)
coco.get_devices(CoCoDeviceClass.GENERIC, generics)
