import random
import sys

from ant import Ant


class AntColony:
    """
    AntColony represent the graph and collection of ants which will traverse the graph.

    This uses the antgraph and ant python files.

    The colony will operate through the constructor and start methods.

    At any point in its operation, after start has been initiated,
    the colony will hold a best path vector and the cost/distance value for that vector.
    """

    def __init__(self, graph, num_ants, num_iterations):
        """
        Create ant colony with a given graph representing the distances between nodes, the number of ants to use and
        the number of times to run through the population of ants.
        :param graph: distance nxn matrix
        :param num_ants: ant population size
        :param num_iterations: times to run over the population
        """
        self.graph = graph
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.Alpha = 0.1
        self.reset()

    def reset(self):
        """
        Resets the colony values to default starting state.
        """
        self.best_path_cost = sys.maxint
        self.best_path_vec = None
        self.best_path_mat = None
        self.last_best_path_iteration = 0

    def start(self):
        """
        Function to begin the ant movements across the graph - this will create the ants and run the population over the
        graph. It will run through the population until it has completed num_iterations iterations.
        """
        self.ants = self.create_ants()
        self.iter_counter = 0

        while self.iter_counter < self.num_iterations:
            self.iteration()
            self.global_updating_rule()

    def iteration(self):
        """
        Runs an iteration of the ant population traversing the graph.

        Looping over the ant population this will call the run function on each ant.
        :return:
        """
        self.avg_path_cost = 0
        self.ant_counter = 0
        self.iter_counter += 1
        print "iter_counter = %s" % (self.iter_counter,)
        for ant in self.ants:
            print "starting ant = %s" % (ant.ID)
            ant.run()

    def num_ants(self):
        """
        Returns the number of ants in the population.
        :return: number value of the population
        """
        return len(self.ants)

    def num_iterations(self):
        """
        Returns the number of iterations the colony will perform when initiated
        :return: number vlaue of iterations
        """
        return self.num_iterations

    def iteration_counter(self):
        """
        returns the current iteration number
        :return: number value of current iteration
        """
        return self.iter_counter

    # called by individual ants
    def update(self, ant):
        """
        Method for an ant to call to update the current best path information.
        This can if the ant has a better path update the best_path_cost, best_path_mat, best_path_vec values.
        :param ant: ant which is calling the update method.
        :return:
        """
        print "Update called by %s" % (ant.ID,)
        self.ant_counter += 1

        self.avg_path_cost += ant.path_cost

        # book-keeping
        if ant.path_cost < self.best_path_cost:
            self.best_path_cost = ant.path_cost
            self.best_path_mat = ant.path_mat
            self.best_path_vec = ant.path_vec
            self.last_best_path_iteration = self.iter_counter

        if self.ant_counter == len(self.ants):
            self.avg_path_cost /= len(self.ants)
            print "Best: %s, %s, %s, %s" % (
                self.best_path_vec, self.best_path_cost, self.iter_counter, self.avg_path_cost,)


    def done(self):
        """
        returns a true/false result for if the number of iterations is equal to the num_iterations value.
        :return: boolean true if complete, false otherwise
        """
        return self.iter_counter == self.num_iterations

    # assign each ant a random start-node
    def create_ants(self):
        """
        Creates the ant population assigning starting nodes randomly to each ant.
        """
        self.reset()
        ants = []
        for i in range(0, self.num_ants):
            ant = Ant(i, random.randint(0, self.graph.num_nodes - 1), self)
            ants.append(ant)

        return ants

    # changes the tau matrix based on evaporation/deposition 
    def global_updating_rule(self):
        """
        Function to carry out the evaporation and deposition updates on the graph representing the pheromones at the end
         of each iteration.
        """
        evaporation = 0
        deposition = 0

        for r in range(0, self.graph.num_nodes):
            for s in range(0, self.graph.num_nodes):
                if r != s:
                    delt_tau = self.best_path_mat[r][s] / self.best_path_cost
                    evaporation = (1 - self.Alpha) * self.graph.tau(r, s)
                    deposition = self.Alpha * delt_tau

                    self.graph.update_tau(r, s, evaporation + deposition)
