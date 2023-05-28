import random

from src.config.app_config import PATH_RAW_MAPS, PATH_GEO_COORDINATES, K_MEANS
from src.map.MapController import MapController
from src.map.MapModel import MapModel
from src.map.MapView import MapView


class Group:
    def __init__(self, id, population, contacts):
        self.id = id
        self.population = population
        self.contacts = contacts

    def get_contacts_proportion(self, gid):
        return self.contacts[gid]


class SIRGroup(Group):
    def __init__(self, id, population, infected, removed, kappa, tau, gamma, contacts):
        contacts[id] = 1.2
        sum_contacts = sum(contacts)
        contacts = [contact / sum_contacts for contact in contacts]

        super().__init__(id, population, contacts)
        self.susceptible = population - infected - removed
        self.infected = infected
        self.removed = removed
        self.kappa = kappa
        self.tau = tau
        self.gamma = gamma

    def to_string(self):
        print(f'S: {self.susceptible}, I: {self.infected}, R: {self.removed}, K: {self.kappa}, T: {self.tau}, G: {self.gamma}\n C: {self.contacts}')


# if __name__ == '__main__':
#     map_model = MapModel(PATH_RAW_MAPS, PATH_GEO_COORDINATES, K_MEANS, 10)
#     map_view = MapView()
#     map_controller = MapController(map_model, map_view)
#     map = map_controller.get_map_by_name('Arctic_Bay')
#
#     sir_groups = []
#     for cluster in map.clusters:
#         id = cluster.id
#         population = cluster.size * 3
#         infected = 0
#         removed = 0
#         kappa = 15
#         tau = 0.1
#         gamma = 0.1
#         contact = map.adjacency_matrix[cluster.id]
#         sir_group = SIRGroup(id, population, infected, removed, kappa, tau, gamma, contact)
#         sir_groups.append(sir_group)
#
#     random.choice(sir_groups).infected = 1
#
#     for sir_group in sir_groups:
#         print(sir_group.to_string())