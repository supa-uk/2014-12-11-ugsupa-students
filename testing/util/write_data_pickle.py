import pickle
import argparse
import csv
import sys


def main(args):
    """
    Read a CSV data file and output a pickled data file.
    Usage: write_data_pickle.py <CSV file> <pickle file>

    Keyword arguments:

    args -- list of command-line arguments. This must have two elements,
    the CSV file name and pickled data output file name.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", help="Name of csv data file")
    parser.add_argument("out_file", help="Name of output pickle data file")
    args = parser.parse_args()
    process(args.in_file, args.out_file)


def process(infilename, outfilename):
    """
    Processes a CSV data file which contains an MxN array of cities
    and distances and outputs the data in pickle format into a file.

    The output pickle will be a list containing a list of place names and
    a list of lists containing distances between cities.

    The CSV file uses the city names as a header row and
    the distances are input in city input order as rows
     - i.e. the nth city will be the n+1th row.
    (+1 due to header)
    Keyword arguments:

    infilename -- name and path of input CSV file
    outfilename -- name and path of output pickle file
    """
    csvfile = open(infilename, 'rU')
    csvreader = csv.reader(csvfile)
    distance_mat = []
    distance_mat.append(next(csvreader))
    distances = []
    for row in csvreader:
        print type(row)
        distances.append([int(i) for i in row])
    distance_mat.append(distances)
    csvfile.close()
    pickle.dump(distance_mat, open(outfilename, 'wb'))


if __name__ == "__main__":
    main(sys.argv[1:])

