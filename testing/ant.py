import math
import random


class Ant():
    """
    Ant class which navigates a graph using a pheromone based choice mechanism.

    Requires an Identifier, start position in graph and an ant colony containing the graph.

    Provided by antgraph and antcolony
    """

    def __init__(self, ID, start_node, colony):
        self.ID = ID
        self.start_node = start_node
        self.colony = colony

        self.curr_node = self.start_node
        self.graph = self.colony.graph
        self.path_vec = []
        self.path_vec.append(self.start_node)
        self.path_cost = 0

        # same meaning as in standard equations
        self.Beta = 1.0
        # Q0 = 1 works just fine for 10 city case (no explore)
        self.Q0 = 0.5
        self.Rho = 0.99

        # store the nodes remaining to be explored here
        self.nodes_to_visit = {}

        for i in range(0, self.graph.num_nodes):
            if i != self.start_node:
                self.nodes_to_visit[i] = i

        # create n X n matrix 0'd out to start
        self.path_mat = []

        for i in range(0, self.graph.num_nodes):
            self.path_mat.append([0] * self.graph.num_nodes)

    def run(self):
        """
        Run function which directs the ant on a complete circuit of the graph.

        Will start and end at the defined starting position for the ant and will
        visit each other graph node once.

        When completed the ant will update the colony and the pheromone trails will
        be updated in the process.
        """
        graph = self.colony.graph
        while not self.end():
            new_node = self.state_transition_rule(self.curr_node)
            self.path_cost += graph.delta(self.curr_node, new_node)

            self.path_vec.append(new_node)
            self.path_mat[self.curr_node][new_node] = 1  # adjacency matrix representing path

            print "Ant %s : %s, %s" % (self.ID, self.path_vec, self.path_cost,)

            self.local_updating_rule(self.curr_node, new_node)

            self.curr_node = new_node

        # don't forget to close the tour
        self.path_cost += graph.delta(self.path_vec[-1], self.path_vec[0])

        # send our results to the colony
        self.colony.update(self)
        print "Ant thread %s terminating." % (self.ID,)

        # allows ant to be restarted
        self.__init__(self.ID, self.start_node, self.colony)

    def end(self):
        """
        Determines if an ant has visited everywhere.

        :return: true if no more places to visit, false otherwise
        """
        return not self.nodes_to_visit


    def state_transition_rule(self, curr_node):
        """
        Function to determine which location to visit next.

        Can be exploitation or exploration.

        See the Ant Colony Optimization methodology papers
        :param curr_node: - current location of the ant
        :return: returns the next node to visit based on the decision rules.
        """
        graph = self.colony.graph
        q = random.random()
        max_node = -1

        if q < self.Q0:
            print "Exploitation"
            max_val = -1
            val = None

            for node in self.nodes_to_visit.values():
                if graph.tau(curr_node, node) == 0:
                    raise Exception("tau = 0")

                val = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
                if val > max_val:
                    max_val = val
                    max_node = node
        else:
            print "Exploration"
            sum = 0
            node = -1

            for node in self.nodes_to_visit.values():
                if graph.tau(curr_node, node) == 0:
                    raise Exception("tau = 0")
                sum += graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
            if sum == 0:
                raise Exception("sum = 0")

            avg = sum / len(self.nodes_to_visit)

            print "avg = %s" % (avg,)

            for node in self.nodes_to_visit.values():
                p = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
                if p > avg:
                    print "p = %s" % (p,)
                    max_node = node

            if max_node == -1:
                max_node = node

        if max_node < 0:
            raise Exception("max_node < 0")

        del self.nodes_to_visit[max_node]

        return max_node


    def local_updating_rule(self, curr_node, next_node):
        """
        Updates the pheromone trail between two nodes
        :param curr_node: start node
        :param next_node: node being visited
        """
        graph = self.colony.graph
        val = (1 - self.Rho) * graph.tau(curr_node, next_node) + (self.Rho * graph.tau0)
        graph.update_tau(curr_node, next_node, val)

