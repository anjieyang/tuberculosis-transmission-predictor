import random

import networkx as nx

from src.sir.Group import SIRGroup


class Generator:
    @staticmethod
    def generate_sir_groups(n, k):
        groups = []

        # Generate a regular graph
        G = nx.random_regular_graph(k, n)

        A = nx.to_numpy_array(G)

        for i in range(n):
            A[i, i] = 1.2

        # Normalize the adjacency matrix so that each row sums to 1
        A /= A.sum(axis=0, keepdims=True)

        # Generate groups with random parameters
        for i in range(n):
            population = random.randint(5, 100000)
            kappa = random.randint(1, 15)
            tau = random.uniform(0, 0.3)
            gamma = random.uniform(0.05, 0.15)

            contacts = A[i]

            # Ensure at least one infected individual in the first group
            if i == 0:
                infected = random.randint(1, 10)
                susceptible = population - infected
            else:
                infected = random.randint(0, 10)
                susceptible = population - infected

            removed = 0

            groups.append(SIRGroup(population=population, susceptible=susceptible, infected=infected, removed=removed,
                                   kappa=kappa, tau=tau, gamma=gamma, contacts=contacts))

        return groups

