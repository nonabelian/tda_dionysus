''' Author: Dylan Albrecht
    Date: March 7, 2017

    Various plotting and plotting utility functions for topology, to be
    integrated with Dionysus.  Includes various example plotting functions,
    for presentation purposes, and useful functions like 'draw_complex' which
    is a matplotlib version of function in Dionysus

'''


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
#from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from dionysus import Simplex

from data import circle_2D
from data import coffee_mug
from data import pail


def plot_circle_2D():
    circle = circle_2D(n_samples=100, noise=0.2)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(circle[:,0], circle[:,1])
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Noisy Circle')
    
    return ax


def plot_mug_3D():
    mug, labels = coffee_mug(height=2.0, n_samples=300, bottom_label=0,
                             side_label=0, handle_label=1)
    c = ['r' if l else 'b' for l in labels]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(mug[:,0], mug[:,1], mug[:,2], c=c)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('Data Mug')
    
    return ax


def plot_pail_3D():
    bucket, labels = pail(height=2.0, n_samples=300, bottom_label=0,
                          side_label=0, handle_label=1)
    c = ['r' if l else 'b' for l in labels]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(bucket[:,0], bucket[:,1], bucket[:,2], c=c)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 3.0)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('Data Bucket')

    return ax


def persistent_cycles(dynamic_persistence, smap, evaluator):
    pcycle = []
    for sigma in dynamic_persistence:
        if not sigma.sign():
            death = evaluator(smap[sigma])
            birth = evaluator(smap[sigma.pair()])

            if (death - birth) < 0.001:
                continue

            cycle = [smap[ii] for ii in sigma.cycle]
            pcycle.append(((birth, death), cycle))

    return pcycle


def animate_persistence(X, pcycle):
    ''' Saves a series of .png images of the persistent cycles as the 'time'
        scale changes.
        INPUT: Nx2 numpy array(dataset), list (from 'persistent_cycles')
        OUTPUT: None

        Command to create the movie:

        $ ffmpeg -f image2 -r 1 -i image%04d.png -vcodec mpeg4 -y
                 animated_persistence.mp4
    '''
    _, ymin, _, _ = _get_padded_box(X, padding=0.0)

    bd = np.array([list(bd) for bd, cycle in pcycle])

    begin_scale = 0.0
    end_scale = np.max(bd[:,1])

    time = np.linspace(begin_scale, end_scale, 50)

    for count, t in enumerate(time):
        ax = draw_complex(X, [])

        for ((birth, death), cycle) in pcycle:
            if birth < t and death > t:
                ax = draw_complex(X, cycle, ax=ax)

        # Sliding scale indicator
        ax.plot([0.0, t], [ymin, ymin], lw=2)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Persistent Homology')

        plt.annotate('scale', xy=(0.0, ymin+0.01), xytext=(0.0, ymin+0.01))
        plt.savefig('image{:04d}.png'.format(count))



def draw_complex(X, simplicial_complex, ax=None):
    xmin, ymin, xmax, ymax = _get_padded_box(X, padding=0.1)

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    point_complex = [Simplex([i]) for i in range(len(X))]
    sc = point_complex + simplicial_complex

    sc.sort(lambda s1, s2: -cmp(s1.dimension(), s2.dimension()))
    for s in sc:
        vertices = [v for v in s.vertices]
        points = X[np.array(vertices)]

        if s.dimension() == 0:
            ax.scatter(X[:,0], X[:,1], c='c')
        else:
            polygon = Polygon(points, closed=False, linewidth=20)
            p = PatchCollection([polygon])
            ax.add_collection(p)
            
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    return ax

def _get_padded_box(X, padding=0.1):

    xmin, ymin = X.min(axis=0)
    xmax, ymax = X.max(axis=0)

    paddingx = padding * abs(xmax - xmin)
    paddingy = padding * abs(ymax - ymin)

    xmin -= paddingx
    ymin -= paddingy

    xmax += paddingx
    ymax += paddingy

    return xmin, ymin, xmax, ymax

