"""Websocket client sending package with active storms."""
import asyncio
import websocket
import time
import os
import sys
from threading import Thread
import random
import thunder_generator
from services import get_json_payload, parse_json_to_data, load_geo_json
from copy import deepcopy


warsaw_polygon = [
    [20.887139, 52.364040],
    [21.068216, 52.376500],
    [21.228303, 52.282293],
    [21.275555, 52.153123],
    [21.115990, 52.088304],
    [20.957783, 52.108739],
    [20.765620, 52.201336]
]
is_warsaw = True
poland_polygon = None
locked = False
vector_range = (-0.059, 0.059)
storms = []

socket_address = 'ws://192.168.43.245:90/storm?server'
# socket_address = 'ws://10.250.194.196:90/storm?server'


def calculate_vector_coords(range):
    """Calculate vector coordinates."""
    vector = {
        'lat': 0.0,
        'lng': 0.0
    }
    vector['lat'] = random.uniform(*range)
    vector['lng'] = random.uniform(*range)
    return vector


def calculate_vector_life():
    """Calculate vector for given life."""
    return random.randint(5, 15)


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
    life = calculate_vector_life()
    vector = calculate_vector_coords(vector_range)
    # start_lat = random.uniform(50.82355, 53.266994)
    # start_lng = random.uniform(19.999999, 22.068806)
    if is_warsaw:
        start_lat = random.uniform(50.82355, 53.266994)
        start_lng = random.uniform(19.999999, 22.068806)
        is_warsaw = False
    else:
        start_lat = random.uniform(49.82355, 54.266994)
        start_lng = random.uniform(19.999999, 22.068806)
    print(start_lat, start_lng)
    s = thunder_generator.Thunder(
        id,
        deepcopy(start_lat),
        deepcopy(start_lng),
        poland_polygon,
        life,
        vector
        )
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
    random.seed(time.time())
    file_path = os.path.dirname(os.path.abspath(__file__)) + '/geo_data/custom.geo.json'
    poland_polygon = load_geo_json(file_path)
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(socket_address,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
