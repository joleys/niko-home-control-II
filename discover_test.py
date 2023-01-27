"""Script to detect NHC2 controller on the network."""
import socket
from time import sleep


def _get_32bit_int(bytz, index):
    return int.from_bytes(bytes=bytz[index: index + 4], byteorder='little')

def _get_16bit_int(bytz, index):
    return int.from_bytes(bytes=bytz[index: index + 2], byteorder='little')


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server.sendto(bytes([0x44]), ('<broadcast>', 10000))
loops = 0
while loops < 100:
    data, addr = server.recvfrom(1024)

    header_ok = data[0] is 0x44
    message_length_ok = len(data) is 25
    checks_out = message_length_ok and header_ok

    is_ok = "YES" if checks_out else "NO"

    print("\nheader checks out :", is_ok, "\n")
    print(data)
    if header_ok:

        serial = _get_32bit_int(data, 2)  # index 17 & 18
        mac = ''.join('{:02X}'.format(a) for a in data[2:6])
        ip = list(map(lambda x: data[x], (6, 7, 8, 9)))
        submask = list(map(lambda x: data[x], (10, 11, 12, 13)))
        message_length = data[14]
        version = data[15]
        exteneded_type = data[16]
        major = _get_16bit_int(data, 17)  # index 17 & 18
        minor = _get_16bit_int(data, 19)  # index 19 & 20
        bugfix = _get_16bit_int(data, 21)  # index 21 & 22
        buildnr = _get_16bit_int(data, 23)  # index 23 & 24
        print("""NHC2 Message
Version: {}
Extended: {}
Serial: {}
Mac: {}
Ip: {}.{}.{}.{}
Submask: {}.{}.{}.{}
Version: {}.{}.{}.{}""".format(version, exteneded_type, serial, mac, *ip, *submask, major, minor, bugfix, buildnr))
        break
    loops = loops + 1
    sleep(0.100)
