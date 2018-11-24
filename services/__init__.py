"""Services."""
import json


def get_json_payload(data):
    thunders = []
    for d in data:
        thunders.append(
            {
                'id': d[0],
                'lng': d[1],
                'lat': d[2]
            }
        )
    return json.dumps(thunders)


def parse_json_to_data(payload):
    return json.loads(payload)


def load_geo_json(file):
    with open(file) as f:
        data = json.load(f)
    return data['features'][0]['geometry']['coordinates'][0]
