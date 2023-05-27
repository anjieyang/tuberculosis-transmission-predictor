class Group:
    def __init__(self, population, contacts):
        self.population = population
        self.contacts = contacts

    def get_contacts_proportion(self, gid):
        return self.contacts[gid]


class SIRGroup(Group):
    def __init__(self, *, population, susceptible, infected, removed, kappa, tau, gamma, contacts):
        super().__init__(population, contacts)
        self.susceptible = susceptible
        self.infected = infected
        self.removed = removed
        self.kappa = kappa
        self.tau = tau
        self.gamma = gamma

    def to_string(self):
        print(f'S: {self.susceptible}, I: {self.infected}, R: {self.removed}, K: {self.kappa}, T: {self.tau}, G: {self.gamma}\n C: {self.contacts}')


if __name__ == '__main__':
    contacts = [0.3, 0.5, 0.2]
    group = Group(population=1000, contacts=contacts)
    print(group.get_contacts_proportion(1))
