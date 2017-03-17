from time import time

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from topology.persistence import DynamicPersistence
from topology.data import circle_2D


if __name__ == '__main__':
    begin_power = 4
    end_power = 8
    num_powers = end_power - begin_power + 1
    n_points = np.logspace(begin_power, end_power, num=num_powers, base=2.0)

    run_times = []
    samples = []
    for pts in n_points:
        X = circle_2D(n_samples=pts, noise=0.2)

        print "=" * 40
        print "Number of samples:", pts

        start = time()
        dp = DynamicPersistence(X)
        dp.run()
        end = time()
        duration = end - start

        run_times.append(duration)
        samples.append(pts)

        print "=" * 40

    log2_rt = np.log2(np.array(run_times))
    log2_s = np.log2(np.array(samples))

    lr = LinearRegression()
    lr.fit(log2_s.reshape(-1, 1), log2_rt)
    slope = lr.coef_[0]

    plt.plot(log2_s, log2_rt, label='Slope: {}'.format(slope))
    plt.scatter(log2_s, log2_rt)
    plt.xlabel('$\log_{2}$ Number of Samples')
    plt.ylabel('$\log_{2}$ Run time (s)')
    plt.title('Runtime Efficiency (log-log plot)')
    plt.legend(loc='lower right')
    plt.savefig('images/runtime_efficiency.png')

    plt.show()
