"""Services."""
import json


def get_json_payload(data):
    """Return data parsed to json."""
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
    """Return json payload as object."""
    return json.loads(payload)


def load_geo_json(file):
    """Return object composed from json file from given path."""
    with open(file) as f:
        data = json.load(f)
    return data['features'][0]['geometry']['coordinates'][0]
