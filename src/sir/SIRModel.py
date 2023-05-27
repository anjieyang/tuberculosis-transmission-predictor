import numpy
import numpy as np
import pandas as pd
from tqdm import trange

from src.sir.Generator import Generator


class SIRModel:
    def __init__(self, groups, time_steps):
        self.groups = groups
        self.time_steps = time_steps
        self.num_groups = len(groups)
        self.S = [[0] * time_steps for _ in range(self.num_groups)]
        self.I = [[0] * time_steps for _ in range(self.num_groups)]
        self.R = [[0] * time_steps for _ in range(self.num_groups)]
        self.S = numpy.array(self.S, dtype=numpy.float64)
        self.I = numpy.array(self.I, dtype=numpy.float64)
        self.R = numpy.array(self.R, dtype=numpy.float64)
        self.parameter = [[0] * 3 for _ in range(self.num_groups)]

        for group_id in range(self.num_groups):
            self.S[group_id][0], self.I[group_id][0], self.R[group_id][0] = groups[group_id].susceptible, groups[
                group_id].infected, groups[group_id].removed
            self.parameter[group_id][0], self.parameter[group_id][1], self.parameter[group_id][2] = groups[
                group_id].kappa, groups[group_id].tau, groups[group_id].gamma


if __name__ == '__main__':
    groups = Generator.generate_sir_groups(5, 0)

    sir = SIRModel(groups, 100)
