import asyncio

from nhc2_coco.coco_discover_profiles import CoCoDiscoverProfiles

# Enter the IP/Host you want to test here
host = 'nhc2.local'
disc = CoCoDiscoverProfiles(host)

loop = asyncio.get_event_loop()


def print_u(text):
    print('\033[4m' + text + '\033[0m')


print('Searching for NiKo Home Control Controllers and profiles on them...')
try:
    results = loop.run_until_complete(disc.get_all_profiles())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()

print(results)
