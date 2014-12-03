class AntGraph:
    """
    Module to represent the graph used in the travelling salesman problem.

    The module uses a distance matrix which is NxN representing the distance between the nodes on hte graph.

    A  matrix containing tau or pheromone values for each path in the graph is used so that the pheromone trails can be
    accessed and updated.
    """

    def __init__(self, num_nodes, delta_mat, tau_mat=None):
        print len(delta_mat)
        if len(delta_mat) != num_nodes:
            raise Exception("len(delta) != num_nodes")

        self.num_nodes = num_nodes
        self.delta_mat = delta_mat  # matrix of node distance deltas

        # tau mat contains the amount of phermone at node x,y
        if tau_mat is None:
            self.tau_mat = []
            for i in range(0, num_nodes):
                self.tau_mat.append([0] * num_nodes)

    def delta(self, r, s):
        """
        Function returns the distance between two nodes, r and s. Note order is important as the
        distance between r and s may not be the same as between s and r
        :param r: origin node
        :param s: target node
        :return: distance value
        """
        return self.delta_mat[r][s]

    def tau(self, r, s):
        """
        Function returns the pheromone or tau value for the path between two nodes, r and s.
        Note order is important as the path between r and s may not be the same as between s and r
        :param r: origin node
        :param s: target node
        :return: distance value
        """
        return self.tau_mat[r][s]

    # 1 / delta = eta or etha 
    def etha(self, r, s):
        """
        Function returns the etha value between two nodes, r and s. This is determined by using the 1/delta(r,s)
        Note order is important as the distance between r and s may not be the same as between s and r
        :param r: origin node
        :param s: target node
        :return: etha value
        """
        return 1.0 / self.delta(r, s)

    def update_tau(self, r, s, val):
        """
        Updates the tau value in the tau array between the nodes r and s with the value val.
        Note tau(r,s) does not always equal tau(s,r)
        :param r: origin node
        :param s: target node
        :param val: new tau value
        """
        self.tau_mat[r][s] = val

    def reset_tau(self):
        """
        Resets the tau array/matrix to a default state where all values are equal.
        """
        avg = self.average_delta()

        # initial tau 
        self.tau0 = 1.0 / (self.num_nodes * 0.5 * avg)

        print "Average = %s" % (avg,)
        print "Tau0 = %s" % (self.tau0)

        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                self.tau_mat[r][s] = self.tau0

    # average delta in delta matrix
    def average_delta(self):
        """
        Returns the average distance between nodes in the distance matrix for the graph.
        :return: average distance value
        """
        return self.average(self.delta_mat)

    # average tau in tau matrix
    def average_tau(self):
        """
        Returns the average tau value between nodes in the tau matrix for the graph.
        :return: average tau value
        """
        return self.average(self.tau_mat)

    # average val of a matrix
    def average(self, matrix):
        """
        Returns the average value for the given Num_nodes x Num_nodes matrix for the graph.
        :return: average value
        """
        sum = 0
        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                sum += matrix[r][s]

        avg = sum / (self.num_nodes * self.num_nodes)
        return avg

