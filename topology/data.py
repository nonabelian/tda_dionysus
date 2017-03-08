''' Author: Dylan Albrecht
    Date: March 6, 2017

    Functions for producing simulated topological data.  This includes,

    * 2D noisy circles
    * 2D disks
    * Cylinders
    * Tori
    * Coffee Mug
    * Bucket with handle

    TODO: Add 'real-world' topological data sets.

'''

import numpy as np


def circle_2D(radius=1.0, center=(0.0,0.0), n_samples=100., noise=0.01):
    pi = np.pi
    angle = np.linspace(0, 2 * pi, n_samples)
    r = radius + np.random.normal(0, noise, angle.shape)

    x = r * np.cos(angle) + center[0]
    y = r * np.sin(angle) + center[1]

    X = np.c_[x, y]
    
    return X


def disk_2D(radius=1.0, center=(0.0,0.0), n_samples=100., noise=0.01):
    X = np.array([]).reshape(0,2)

    count = 0
    while count < n_samples:
        x = np.random.uniform(-radius, radius)
        y = np.random.uniform(-radius, radius)

        if x**2 + y**2 <= radius:
            sample = np.c_[x, y]
            X = np.append(X, sample, axis=0)
            count += 1

    return X


def cylinder(radius=1.0, height=1.0, center=(0.0,0.0,0.0), n_samples=100,
             noise=0.01):
    z = np.random.uniform(-height/2.0, height/2.0, n_samples) 

    cylinder = np.array([]).reshape(0,3)

    for ring_height in z:
        ring = circle_2D(radius=radius, center=center[:2], n_samples=n_samples,
                         noise=noise)

        ring_z = np.array([ring_height] * len(ring))
        ring_3D = np.c_[ring, ring_z]

        cylinder = np.append(cylinder, ring_3D, axis=0)

    # Thin to proper number of samples.
    # NOTE: Not necessarily uniformly distributed area-wise...
    keep_indices = np.random.choice(cylinder.shape[0],
                                      n_samples,
                                      replace=False)
    cylinder = cylinder[keep_indices]

    return cylinder


def torus(radius=1.0, thickness=0.1, start_angle=0.0, end_angle=2*np.pi,
          center=(0.0,0.0,0.0), n_samples=100, noise=0.01):

    theta = np.linspace(start_angle, end_angle, n_samples)
    torus = np.array([]).reshape(0,3)

    for angle in theta:
        # Create a noisy circle
        ring = circle_2D(radius=thickness, center=(0.0,0.0),
                         n_samples=n_samples, noise=noise)
        ring_z = np.zeros(len(ring))
        ring_3D = np.c_[ring, ring_z]

        # Shift the circle over to the 'radius'
        offset = np.array([[0.0, radius, 0.0]])
        ring_3D += offset

        # Rotate the circle along the torus to the proper location
        rotation_matrix = np.array([[1,             0,              0],
                                    [0, np.cos(angle), -np.sin(angle)],
                                    [0, np.sin(angle),  np.cos(angle)]])
        ring_3D = rotation_matrix.dot(ring_3D.T)
        ring_3D = ring_3D.T

        # Add to torus
        torus = np.append(torus, ring_3D, axis=0)

    torus += np.array(center).reshape(-1, 3)

    # Thin to proper number of samples.
    # NOTE: Not necessarily uniformly distributed area-wise...
    keep_indices = np.random.choice(torus.shape[0],
                                    n_samples,
                                    replace=False)
    torus = torus[keep_indices]

    return torus


def coffee_mug(radius=1.0, height=1.0, center=(0.0,0.0,0.0), n_samples=100,
               noise=0.01, bottom_label=0, side_label=0, handle_label=1):
    bottom_label = bottom_label
    side_label = side_label
    handle_label = handle_label

    bottom = disk_2D(radius=radius, center=center[:2],
                     n_samples=n_samples//3,
                     noise=noise)
    bottom_z = np.array([-height/2.0] * len(bottom))
    bottom_3D = np.c_[bottom, bottom_z]
    labels = np.array([bottom_label] * len(bottom_3D))

    side = cylinder(radius=radius, height=height, center=center,
                    n_samples=n_samples, noise=noise)

    mug = np.append(bottom_3D, side, axis=0)
    labels = np.append(labels, np.array([side_label] * len(side)), axis=0)

    handle = torus(radius=height/4.0,
                   thickness=height/16.0,
                   start_angle=-np.pi/2.0,
                   end_angle=np.pi/2.0,
                   center=(0.0,radius,0.0),
                   n_samples=n_samples//3,
                   noise=noise)

    mug = np.append(mug, handle, axis=0)
    labels = np.append(labels, np.array([handle_label] * len(handle)), axis=0)

    # Thin to proper number of samples.
    # NOTE: Not necessarily uniformly distributed area-wise...
    keep_indices = np.random.choice(mug.shape[0],
                                    n_samples,
                                    replace=False)
    mug = mug[keep_indices]
    labels = labels[keep_indices]

    return mug, labels

def pail(radius=1.0, height=1.0, center=(0.0,0.0,0.0), n_samples=100,
         noise=0.01, bottom_label=0, side_label=0, handle_label=1):
    bottom_label = bottom_label
    side_label = side_label
    handle_label = handle_label

    bottom = disk_2D(radius=radius, center=center[:2],
                     n_samples=n_samples//3,
                     noise=noise)
    bottom_z = np.array([-height/2.0] * len(bottom))
    bottom_3D = np.c_[bottom, bottom_z]
    labels = np.array([bottom_label] * len(bottom_3D))

    side = cylinder(radius=radius, height=height, center=center,
                    n_samples=n_samples, noise=noise)

    pail = np.append(bottom_3D, side, axis=0)
    labels = np.append(labels, np.array([side_label] * len(side)), axis=0)

    handle = torus(radius=1.5*radius,
                   thickness=height/16.0,
                   start_angle=-np.pi/3.0,
                   end_angle=4*np.pi/3.0,
                   center=(0.0,0.0,height/2.0),
                   n_samples=n_samples//3,
                   noise=noise)

    pail = np.append(pail, handle, axis=0)
    labels = np.append(labels, np.array([handle_label] * len(handle)), axis=0)

    # Thin to proper number of samples.
    # NOTE: Not necessarily uniformly distributed area-wise...
    keep_indices = np.random.choice(pail.shape[0],
                                    n_samples,
                                    replace=False)
    pail = pail[keep_indices]
    labels = labels[keep_indices]

    return pail, labels

if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    mug, labels = pail(height=2.0, n_samples=300)
    c = ['r' if l else 'b' for l in labels]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(mug[:,0], mug[:,1], mug[:,2], c=c)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 3.0)
    plt.show()
