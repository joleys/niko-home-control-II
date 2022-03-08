import binascii
import select
import threading
import socket
import netifaces
from getmac import get_mac_address


class CoCoDiscover:
    """CoCoDiscover will help you discover NHC2.
    It will also tell you about NHC1, but the result will differ.

    You create CoCoDiscover, passing along a callback an the time you max want to wait.
    By default we wait 3 seconds.
    
    For every result with matching header the callback is called,
    with the address, mac-address and a boolean if it's a NHC2.
    """

    def __init__(self, on_discover, on_done):
        self._get_broadcast_ips()

        self._thread = threading.Thread(target=self._scan_for_nhc)
        self._on_discover = on_discover
        self._on_done = on_done
        self._thread.start()
        # If we discover one, we don't want to keep looking too long...
        self._discovered_at_least_one = False

    def _get_broadcast_ips(self):
        interfaces = netifaces.interfaces()
        return filter(lambda x: x,
                              map(lambda x: netifaces.ifaddresses(x).get(netifaces.AF_INET)[0].get('broadcast') if (
                                      (netifaces.AF_INET in netifaces.ifaddresses(x))
                                      and ('broadcast' in netifaces.ifaddresses(x).get(netifaces.AF_INET)[0])

                              ) else None, interfaces))

    def _scan_for_nhc(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        """ We search for all broadcast ip4s, so that we don't only search the main interface """
        broadcast_ips = self._get_broadcast_ips()
        for broadcast_ip in broadcast_ips:
            server.sendto(bytes([0x44]), (broadcast_ip, 10000))
        server.setblocking(0)
        loops = 0

        while loops < 200 and ((not self._discovered_at_least_one) or loops < 20):
            loops = loops + 1
            ready = select.select([server], [], [], 0.01)
            if ready[0]:
                data, addr = server.recvfrom(4096)
                if data[0] == 0x44:  # NHC2 Header
                    is_nhc2 = (len(data) >= 16) and (data[15] == 0x02)
                    mac = get_mac_address(ip=addr[0])
                    if self._on_discover:
                        self._discovered_at_least_one = True
                        self._on_discover(addr[0], mac, is_nhc2)
        server.close()
        self._on_done()