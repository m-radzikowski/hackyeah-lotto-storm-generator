import thunder_generator
import time


coordinates = {
    'lat': 52.2922104,
    'lng': 21.0023798
}
coordinates_range = {
    'start': {
        'lat': 0.12,
        'lng': 11.12
    },
    'stop': {
        'lat': 1111111.12,
        'lng': 123123.12
    }
}
max_size = 60
min_size = 20
gradient_size = 5
longevity = 10000

def looper():
    thunder = thunder_generator.Thunder(coordinates, coordinates_range, min_size, max_size, gradient_size, longevity)
    while True:
        result = thunder.generate()
        print(result)
        time.sleep(1)



if __name__ == '__main__':
    looper()
