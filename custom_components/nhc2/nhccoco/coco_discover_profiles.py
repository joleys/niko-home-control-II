import asyncio
import socket
import time

from .coco_profiles import CoCoProfiles

loop = asyncio.get_event_loop()


class CoCoDiscoverProfiles:
    """CoCoDiscover will help you discover NHC2 Profiles on all devices on the network. It will NOT find hobby
    profiles. The username then is provided by Niko (eg. hobby) This relies on not publicly documented API calls! It
    also broadcasts a UDP packet on all available (ipV4) broadcast addresses.
    """

    def __init__(self, host):
        self._controllers_found = []
        self._profiles_found = []
        self._done_scanning_profiles = asyncio.Event()
        self._search_for_one_host(host)

    def _done(self):
        self._done_scanning_profiles.set()

    async def _wait_until_done(self):
        await self._done_scanning_profiles.wait()

    async def get_all_profiles(self):
        await self._wait_until_done()
        return self._profiles_found

    def _discover_profiles_callback(self, address, mac, skip_host_search=False):
        def inner_function(profiles):
            if skip_host_search is not True:
                try:
                    host = socket.gethostbyaddr(address)[0]
                except:
                    host = None
            else:
                host = None

            self._profiles_found.append((address, mac, profiles, host))

        return inner_function

    def _done_discovering_profiles_callback(self):
        while len(self._controllers_found) != len(self._profiles_found):
            time.sleep(1)
        loop.call_soon_threadsafe(callback=self._done)

    def _search_for_one_host(self, host):
        self._controllers_found = [(host, None)]
        for ctrl in self._controllers_found:
            CoCoProfiles(
                self._discover_profiles_callback(host, None, True),
                host,
                self._done_discovering_profiles_callback
            )
