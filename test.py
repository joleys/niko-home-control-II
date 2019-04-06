import asyncio

from nhc2 import NHC2


def glc(devices):
    lights = devices.lights
    for light in lights:
        light.turn_off()


async def start():
    nhc2 = NHC2('192.168.2.9', 8883, 'ef38cd4e-bd3b-46e3-869c-ec3e106fcc82', 'B7e7ew4e', 'niko_ca.pem')
    nhc2.get_lights(glc)
    nhc2.connect()


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(start())
    loop.run_forever()


main()
