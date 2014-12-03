import csv
import pickle
import argparse
import sys


def main(args):
    """
    Read a pickled data file and output data in CSV format into a file.
    Usage: write_data_csv.py <pickled file> <output file>

    Keyword arguments:

    args -- list of command-line arguments. This must have two elements,
    the pickled file name and  data output file name.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", help="Name of pickled data file")
    parser.add_argument("out_file", help="Name of output csv data file")
    args = parser.parse_args()
    process(args.in_file, args.out_file)


def process(infilename, outfilename):
    """
    Processes a pickled data file which contains an MxN array of cities
    and distances and outputs the data in CSV format into a file.

    The file uses the city names as a header row and the distances are output
    in city input order as rows - i.e. the nth city will be the n+1th row.
    (+1 due to header)
    Keyword arguments:

    infilename -- name and path of input pickle file
    outfilename -- name and path of output CSV file
    """
    stuff = pickle.load(open(infilename, "r"))
    csvfile = open(outfilename, 'w')
    filewriter = csv.writer(csvfile)
    filewriter.writerow(stuff[0])
    for drow in stuff[1]:
        filewriter.writerow(drow)
    csvfile.close()


if __name__ == "__main__":
    main(sys.argv[1:])
