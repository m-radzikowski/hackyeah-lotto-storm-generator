"""Websocket client for simulation generator."""
import asyncio
import websockets
import time


# socket_address = 'ws://demos.kaazing.com/echo'
socket_address = 'ws://10.250.194.196:90/storm?server'


async def socket_client(uri):
    """Run async socket client.

    :argument uri: websocket server uri address
    :return: void
    """
    while True:
        async with websockets.connect(uri) as websocket:
            await websocket.send('greeting')
            time.sleep(1)


if __name__ == '__main__':
    ws = asyncio.get_event_loop()
    ws.run_until_complete(socket_client(socket_address))
