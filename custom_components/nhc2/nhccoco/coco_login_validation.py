import asyncio

from .mqtt import NHCMQTTClient


class CoCoLoginValidation:
    """ Validate one can login on the CoCo
    """

    def __init__(self, address, username, password, port=8883):
        self._address = address
        self._username = username
        self._password = password
        self._port = port

    """
        Try to connect with given parameters
        The return indicates success or not:
            0: Connection successful
            1: Connection refused - incorrect protocol version
            2: Connection refused - invalid client identifier
            3: Connection refused - server unavailable
            4: Connection refused - bad username or password
            5: Connection refused - not authorised
            6-255: Currently unused.
    """

    async def check_connection(self, timeout=10):
        result_code = 0
        done_testing = asyncio.Event()
        loop = asyncio.get_running_loop()
        client = NHCMQTTClient.create(self._username, self._password)

        def done():
            nonlocal done_testing
            done_testing.set()

        def on_connect(x, xx, xxx, reason_code):
            nonlocal result_code
            result_code = reason_code
            loop.call_soon_threadsafe(callback=done)

        client.on_connect = on_connect
        client.loop_start()
        client.connect_async(self._address, self._port)

        try:
            await asyncio.wait_for(done_testing.wait(), timeout + 2)
        except:
            pass

        client.disconnect()
        client.loop_stop()
        return result_code
