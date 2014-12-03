import plot_city_path as pcp


def main():
    """
    Create a basic route on a map for predetermined output based on set data files.

    Only to be used as an example - not to be used otherwise.
    Usage: sample_map.py
    """
    pcp.main(['../data/scottish_city_loc.csv', '../data/scottish_map.properties',
              ['Glasgow', 'Edinburgh', 'Inverness', 'Perth', 'Dundee', 'Stirling', 'Aberdeen']])


if __name__ == "__main__":
    main()