import numpy as np


class BirthDeathFeatures(object):


    def __init__(self, dynamic_persistence):
        self.dp = dynamic_persistence.dynamic_persistence
	self.smap = dynamic_persistence.simplex_map
	self.evaluator = dynamic_persistence.rips.eval


    def extract(self):
	features = []
	for node in self.dp:
	    if not node.sign():
		death = self.evaluator(self.smap[node])
		birth = self.evaluator(self.smap[node.pair()])

		if (death - birth) < 0.001:
		    continue

		cycle = [self.smap[ii] for ii in node.cycle]
		chain = [self.smap[ii] for ii in node.chain]

		if not chain or not cycle:
		    continue

		dim = chain[0].dimension()

#            features.append(dim)
		features.append(birth)
		features.append(death-birth)

        self._features = np.array(features)

        return self._features
