# Topology and Data Analysis with Dionysus

This repository contains a demonstration of Topological Data Analysis (TDA),
interfacing with Dionysus

## Introduction

Topological Data Analysis main points, extremely informally:
* Topology is classes of surfaces continuously deformable into each other.
* Surface is infinitely stretchy and compressible, but no ripping of the surface allowed.
* Topological data is a discretization of ideas from topology.
* Provides access to invariants (and more) under deformation.
* Data has shape, and shape has meaning.
* Difficult to understand high-dimensional (>3) space.

Famously, "the coffee cup is topologically equivalent to a donut", which
can be viewed
[on Wikipedia](https://upload.wikimedia.org/wikipedia/commons/2/26/Mug_and_Torus_morph.gif).

**Think of rescaling features as a deformation**

![cycle persistence](images/animated_persistence.gif)

## Installation

Please see the [installation doc](docs/Installation.md).

## Requirements

* Dionysus
* NetworkX
* Matplotlib
* Numpy
