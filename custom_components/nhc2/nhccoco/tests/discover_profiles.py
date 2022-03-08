import asyncio

from nhc2_coco.coco_discover_profiles import CoCoDiscoverProfiles

disc = CoCoDiscoverProfiles()

loop = asyncio.get_event_loop()


def print_u(text):
    print('\033[4m' + text +'\033[0m')


print('Searching for NiKo Home Control Controllers and profiles on them...')
try:
    results = loop.run_until_complete(disc.get_all_profiles())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()

print('Done searching controllers. %d controller(s) found.' % (len(results)))
print('')
for i, result in enumerate(results):
    print_u('Controler #%d' % i)
    print(' IP: %s' % result[0])
    print(' host: %s' % result[3])
    print(' MAC: %s' % result[1])
    profiles = result[2]
    print(' %d profile(s) found.' % (len(profiles)))
    for j, profile in enumerate(profiles):
        print(' Profile #%d:' % j)
        print('  uuid: %s' % profile.get('Uuid'))
        print('  Name: %s' % profile.get('Name'))
        print('  Type: %s' % profile.get('Type'))

