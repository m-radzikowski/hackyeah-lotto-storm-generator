import numpy as np
from time import sleep
import random
import matplotlib.pyplot as plt


hurricane_array_symmetric = np.array([
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
[1, 2, 3, 3, 3, 3, 3, 3, 2, 1],
[1, 2, 3, 4, 4, 4, 4, 3, 2, 1],
[1, 2, 3, 4, 5, 5, 4, 3, 2, 1],
[1, 2, 3, 4, 5, 5, 4, 3, 2, 1],
[1, 2, 3, 4, 4, 4, 4, 3, 2, 1],
[1, 2, 3, 3, 3, 3, 3, 3, 2, 1],
[1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]], dtype='int')
map_size = (50, 50)
num_of_hurricanes = 10


def calculate_map_edge(map_size, hurricane_array):
    """Calculate edge coordinates in 2-D map, hurricane array
    left top corner can take this coordinates as maximum possible
    position.

    :argument map_size: tuple representing map grid size
    :argument hurricane_array: hurricane 2-D array that will be applied to map
    :return: tuple containing width and height coordinates of map edge
    """
    width = map_size[0] - hurricane_array_symmetric.shape[0] - 1
    height = map_size[1] - hurricane_array_symmetric.shape[1] - 1
    return width, height


def vector_convolution_based(hurricane):
    """Calculate vector based on convolution scanning.

    :argument hurricane: hurricane array
    :return: vector as 2-D tuple
    """
    x_s, y_s = hurricane.shape
    if x_s % 2 != 0 or y_s % 2 != 0:
        raise ValueError('Hurricane array has to be even.')
    x_h = int(x_s / 2)
    y_h = int(y_s / 2)
    l_u = np.sum(hurricane[0:x_h,0:y_h])
    r_u = np.sum(hurricane[0:x_h,y_h:])
    l_d = np.sum(hurricane[x_h:,0:y_h])
    r_d = np.sum(hurricane[x_h:,y_h:])
    x = 1 if l_u + l_d < r_u + r_d else -1
    y = 1 if l_u + r_u > l_d + r_d else -1
    return x, y


def vector_median_based(hurricane):
    """Calculate vector based on median of max value.

    :argument hurricane: hurricane array
    :return: vector as 2-D tuple
    """
    max_value = np.amax(hurricane)
    positions = np.argwhere(hurricane==max_value)
    x_m, y_m = int(np.median(positions[:,:1])), int(np.median(positions[:,1:2]))
    x_s, y_s = hurricane.shape
    x = 1 if x_m > (x_s / 2) - 1 else -1
    y = 1 if y_m > (y_s / 2) - 1 else -1
    return x, y


def calculate_moving_vector(hurricane, method=None):
    """Calculate vector according to chosen method.

    :argument hurricane: hurricane array to be applied to map
    :argument method: method of calculation
    :return: calculated hurricane movement vector as 2-D tuple
    """
    return {
        'median': vector_median_based,
        'convolution': vector_convolution_based
    }.get(method, vector_median_based)(hurricane)


def generate_map(hurricanes_list, map_size, vectors):
    """Generate np array representing full playground map.

    :argument hurricane_list: hurricanes list to be applied to map
    :argument map_size: tuple representing map size
    :argument vectors: list of vectors corresponding n size to hurricanes list
    :return: numpy representation of map
    """
    if len(hurricanes_list) != len(vectors):
        raise ValueError('Vectors list are not corresponding to hurricane list in size')
    map_array = np.zeros(map_size, 'int')
    for hurricane_array, moving_vector in zip(hurricanes_list, vectors):
        for i, v in enumerate(hurricane_array):
            for ii, vv in enumerate(v):
                map_array[i + moving_vector[0], ii + moving_vector[1]] += vv
    return map_array


def save_2d_hist(hist2D):
    """Save given 2-D histogram to png file.

    :argument hist2D: histogram in 2-D array format
    """
    plt.imshow(hist2D, cmap='Reds', interpolation='nearest')
    plt.savefig('graph.png')


def update_hurricane(hurricane_array, pattern_array):
    """Updates shape of hurricane array.

    :argument hurricane_array: numpy array representing shape before update_hurricane
    :argument pattern_array: numpy array of perfectly shaped hurricane
    :return: numpy array of new shape
    """
    def compensator(arr, compensation, max_value):
        """Compensate overall values by updating values that are to large.

        :argument arr: array sliced from np array to be reevaluated
        :argument compensation: value to which we should compensate
        :argument max_value: maximal allowed value of array arguments
        :return: reevaluated np array
        """
        return np.array([i if i < max_value else compensation for i in arr])

    for i, _ in enumerate(hurricane_array):
        hurricane_array[i] = compensator(hurricane_array[i], 50, 50)
    reshape_factors_array = np.random.randint(1, 4, size=pattern_array.shape, dtype='int')
    calculated_hurricane_array = pattern_array * reshape_factors_array
    reshape_factors_array = np.random.randint(1, 4, size=pattern_array.shape, dtype='int')
    temporary_array = calculated_hurricane_array / reshape_factors_array
    temporary_array = hurricane_array * calculated_hurricane_array / 5 + 1
    for i, _ in enumerate(temporary_array):
        temporary_array[i] = compensator(temporary_array[i], 150, 149)
    finally_updated_array = temporary_array.astype('int')
    return finally_updated_array


if __name__ == '__main__':
    hurricanes_list = []
    vectors = []
    map_edge = calculate_map_edge(map_size, hurricane_array_symmetric)
    for hurricane_i in range(num_of_hurricanes):
        hurricane_array = update_hurricane(np.copy(hurricane_array_symmetric), hurricane_array_symmetric)
        moving_vector = [random.randint(0, map_edge[0]), random.randint(0, map_edge[1])]
        hurricanes_list.append(hurricane_array)
        vectors.append(moving_vector)
    while True:
        for hurricane_array, moving_vector in zip(hurricanes_list, vectors):
            hurricane_array = update_hurricane(hurricane_array, hurricane_array_symmetric)
            fresh_vector = calculate_moving_vector(hurricane_array, 'convolution')
            moving_vector[0] += fresh_vector[0] if moving_vector[0] > 0 else 1
            moving_vector[0] = moving_vector[0] if moving_vector[0] < map_edge[0] else map_edge[0]
            moving_vector[1] += fresh_vector[1] if moving_vector[1] > 0 else 1
            moving_vector[1] = moving_vector[1] if moving_vector[1] < map_edge[1] else map_edge[1]
        map_array = generate_map(hurricanes_list, map_size, vectors)
        save_2d_hist(map_array)
        sleep(.3)
