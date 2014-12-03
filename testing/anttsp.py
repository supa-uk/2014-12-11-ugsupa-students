import pickle
import sys
import traceback

from antcolony import AntColony
from antgraph import AntGraph


def main(argv):
    """
    Program to show a possible approach to the Travelling Salesman Problem using Ant Colony Optimization

    To use the anttsp.py from the command line:
    Useage: python anttsp.py <cities> <city data file> <output file>

    :param argv - should contain 3 elements, a number of cities to visit, a city data file and a target output

    The number of cities should be a non-negative integer equal to or less than the number of cities in the data file.
    The function will use the first n cities in the data file.

    The data file should be a pickled data file of the form
    [[cityA,cityB,...cityN], [[distanceAA, distanceAB..distanceAN],[distanceBA, distanceBB,.. distanceBN]]]

    This is a list composed of a list of city names and a list of lists represents the NxN array of distances between
    cities.

    The output file should be a target space to write the output information to, this will be a pickled form of:
    [[list of graph node indices], [list of node names], path cost]
    """
    # default
    num_nodes = 10

    if len(argv) >= 3 and argv[0]:
        num_nodes = int(argv[0])

    if num_nodes <= 10:
        num_ants = 20
        num_iterations = 12
        num_repetitions = 1
    else:
        num_ants = 28
        num_iterations = 20
        num_repetitions = 1

    stuff = pickle.load(open(argv[1], "r"))
    cities = stuff[0]
    cost_mat = stuff[1]

    if num_nodes < len(cost_mat):
        cost_mat = cost_mat[0:num_nodes]
        for i in range(0, num_nodes):
            cost_mat[i] = cost_mat[i][0:num_nodes]

    # print cost_mat

    try:
        graph = AntGraph(num_nodes, cost_mat)
        best_path_vec = None
        best_path_cost = sys.maxint
        for i in range(0, num_repetitions):
            print "Repetition %s" % i
            graph.reset_tau()
            ant_colony = AntColony(graph, num_ants, num_iterations)
            print "Colony Started"
            ant_colony.start()
            if ant_colony.best_path_cost < best_path_cost:
                print "Colony Path"
                best_path_vec = ant_colony.best_path_vec
                best_path_cost = ant_colony.best_path_cost

        print "\n------------------------------------------------------------"
        print "                     Results                                "
        print "------------------------------------------------------------"
        print "\nBest path = %s" % (best_path_vec,)
        city_vec = []
        for node in best_path_vec:
            print cities[node] + " ",
            city_vec.append(cities[node])
        print "\nBest path cost = %s\n" % (best_path_cost,)
        results = [best_path_vec, city_vec, best_path_cost]
        pickle.dump(results, open(argv[2], 'w+'))
    except Exception, e:
        print "exception: " + str(e)
        traceback.print_exc()


if __name__ == "__main__":
    main(sys.argv[1:])
