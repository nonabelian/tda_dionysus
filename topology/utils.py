import numpy as np

def pixel_to_xy(array, min_x=-1.0, min_y=-1.0, max_x=1.0, max_y=1.0):
    x = np.linspace(min_x, max_x, array.shape[1])
    y = np.linspace(min_y, max_y, array.shape[0])

    points = []
    for j, row in enumerate(array):
        for i, entry in enumerate(row):
            if entry:
                points.append([x[i], -y[j]])

    return np.array(points)
