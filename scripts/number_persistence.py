import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist
from dionysus import PairwiseDistances
from dionysus import ExplicitDistances
from dionysus import Rips
from dionysus import Filtration
from dionysus import DynamicPersistenceChains

from topology.persistence import DynamicPersistence
from topology.utils import pixel_to_xy
from topology.plotting import draw_barcode

if __name__ == '__main__':

    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    num = X_train[0]
    num_xy = pixel_to_xy(num)
    deviation = np.random.uniform(-1, 1, size=num_xy.size).reshape(num_xy.shape)
    num_xy += 0.01 * deviation

    dp = DynamicPersistence(num_xy)
    dp.run()

    draw_barcode(dp.dynamic_persistence, dp.simplex_map, dp.rips.eval)
    plt.show()
