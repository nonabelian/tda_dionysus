from time import time

import numpy as np
from dionysus import PairwiseDistances
from dionysus import ExplicitDistances
from dionysus import Rips
from dionysus import Filtration
from dionysus import DynamicPersistenceChains


def timeit(method):
    def timed(*args, **kw):
        start = time()
        result = method(*args, **kw)
        end = time()

        print "{0}: time {1:0.2f}s".format(method.__name__, end-start)

    return timed


class DynamicPersistence(object):
    ''' Container class for creating dynamic persistence chains '''

    def __init__(self, X, y=None, max_dimension=2, skeleton=1.7):
        self.X_ = X
        self.y_ = y
        self.max_dimension = max_dimension
        self.skeleton = skeleton

        self.distances = None
        self._set_distances(X)

        self.rips = None
        self.filtration = None
        self.dynamic_persistence = None
        self.simplex_map = None

    def _set_distances(self, X):
        d = self._pairwise_distances(X.tolist())
        d = self._explicit_distances(d)


    @timeit
    def _pairwise_distances(self, X_list):
        self.distances = PairwiseDistances(X_list)


    @timeit
    def _explicit_distances(self, d):
        self.distances = ExplicitDistances(self.distances)


    @timeit
    def _rips_generate(self):
        self.rips.generate(self.max_dimension, self.skeleton,
                           self.filtration.append)


    @timeit
    def _filtration_sort(self):
        self.filtration.sort(self.rips.cmp)


    @timeit
    def _pair_simplices(self):
        self.dynamic_persistence.pair_simplices()


    @timeit
    def _make_simplex_map(self):
        self.simplex_map = self.dynamic_persistence.make_simplex_map(
                            self.filtration)


    @timeit
    def run(self):
        self.rips = Rips(self.distances)
        self.filtration = Filtration()

        self._rips_generate()
        self._filtration_sort()

        self.dynamic_persistence = DynamicPersistenceChains(self.filtration)

        self._pair_simplices()
        self._make_simplex_map()

