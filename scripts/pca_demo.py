import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

import topology.data as td


def run_coffee_mug_pca_example():
    X, y = td.coffee_mug(bottom_label=0, side_label=0, handle_label=1)
    c = ['r' if l else 'b' for l in y]

    # Nontrivial rotation around the x-axis
    angle = np.pi / 4.0
    rotation_matrix = np.array([[1,             0,              0],
				[0, np.cos(angle), -np.sin(angle)],
				[0, np.sin(angle),  np.cos(angle)]])
    X = rotation_matrix.dot(X.T).T

    # Perform PCA 3D down to 2D
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(X_pca[:,0], X_pca[:,1], c=c)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    plt.savefig('images/coffee_mug_pca.png')
    plt.show()


def run_pail_pca_example():
    X, y = td.pail(bottom_label=0, side_label=0, handle_label=1)
    c = ['r' if l else 'b' for l in y]

    # Nontrivial rotation around the x-axis
    angle = np.pi / 4.0
    rotation_matrix = np.array([[1,             0,              0],
				[0, np.cos(angle), -np.sin(angle)],
				[0, np.sin(angle),  np.cos(angle)]])
    X = rotation_matrix.dot(X.T).T

    # Perform PCA 3D down to 2D:
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(X_pca[:,0], X_pca[:,1], c=c)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    plt.savefig('images/pail_pca.png')
    plt.show()


if __name__ == '__main__':
    run_coffee_mug_pca_example()
    run_pail_pca_example()
