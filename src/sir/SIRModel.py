import random

import numpy

from src.config.app_config import KAPPA, TAU, GAMMA
from src.sir.Group import SIRGroup


class SIRModel:
    def __init__(self, map, time_steps):
        self.sir_groups = []
        self.num_groups = self._create_sir_groups(map)
        self.time_steps = time_steps
        self.S = numpy.zeros((self.num_groups, time_steps), dtype=numpy.float64)
        self.I = numpy.zeros((self.num_groups, time_steps), dtype=numpy.float64)
        self.R = numpy.zeros((self.num_groups, time_steps), dtype=numpy.float64)
        self.parameter = numpy.zeros((self.num_groups, 3), dtype=numpy.float64)

        for sir_group in self.sir_groups:
            self.S[sir_group.id][0] = sir_group.susceptible
            self.I[sir_group.id][0] = sir_group.infected
            self.R[sir_group.id][0] = sir_group.removed
            self.parameter[sir_group.id] = [sir_group.kappa, sir_group.tau, sir_group.gamma]

    def _create_sir_groups(self, map):
        for cluster in map.clusters:
            id = cluster.id
            population = cluster.size * 5
            infected = 0
            removed = 0
            kappa = KAPPA
            tau = TAU
            gamma = GAMMA
            contact = map.adjacency_matrix[cluster.id]
            sir_group = SIRGroup(id, population, infected, removed, kappa, tau, gamma, contact)
            self.sir_groups.append(sir_group)
        random.choice(self.sir_groups).infected = 1

        return len(map.clusters)
