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
