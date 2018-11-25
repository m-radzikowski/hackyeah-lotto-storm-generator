"""Websocket client sending package with active storms."""
import asyncio
import websocket
import time
import os
from threading import Thread
import thunder_generator
from services import get_json_payload, parse_json_to_data, load_geo_json


poland_polygon = None
locked = False
warsaw_loc = {
    'lat': 52.2922104,
    'lng': 21.0023798
}
num_of_storms = 10
storms = []

socket_address = 'ws://192.168.43.55:90/storm?server'
# socket_address = 'ws://10.250.194.196:90/storm?server'


def generate(ws):
    """Generate package with active storms movement coordinates."""
    while True:
        t_start = time.time()
        if not locked:
            data = []
            for s in storms:
                d = s.get_next_coordinates()
                data.append(d)
            payload_msg = get_json_payload(data)
            ws.send(payload_msg)
            t_after = time.time()
            print('Number of active storms: {}'.format(len(data)))
            time.sleep(1 - (t_after - t_start))


def create(id):
    """Create new storm with given id."""
    s = thunder_generator.Thunder(id, warsaw_loc['lng'], warsaw_loc['lat'], poland_polygon)
    storms.append(s)


def remove(id):
    """Remove storm of given id."""
    for s in storms:
        if s.id == id:
            storms.remove(s)


def actions(command, id):
    """Dispatch corresponding action for given command."""
    {
        'CREATE': create,
        'REMOVE': remove
    }.get(command, print)(id)


def on_message(ws, message):
    """Handle server message."""
    data = parse_json_to_data(message)
    locked = True
    for d in data:
        print('{} storm of id: {}'.format(d['commandType'], d['id']))
        actions(d['commandType'], d['id'])
    locked = False


def on_error(ws, error):
    """Handle server error."""
    print(error)


def on_close(ws):
    """Handle socket close."""
    ws.close()
    print('Closed...')


def on_open(ws):
    """Handle socket connection when opened and
    start separate thread for sending messages to server."""
    print('Connected...')
    t = Thread(
            target=generate,
            args=(ws, ),
            name=f'worker_generator'
            )
    t.start()


if __name__ == "__main__":
    file_path = os.path.dirname(os.path.abspath(__file__)) + '/geo_data/custom.geo.json'
    poland_polygon = load_geo_json(file_path)
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(socket_address,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
