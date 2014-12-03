import csv
import sys
import ConfigParser

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


def main(argv):
    """
    Plots a path between points onto a map defined by a config file.
    Intended to be called by another python module.
    Usage: plot_city_path.py <point coordinates file> <map properties file> <city path list>

    If the third argument is omitted a basic map will be drawn.

    Point Positions should have a point name, latitude and longitude.

    Map Properties file should be of the format:
        [figure]
            height=12
            width=5
        [map]
            projection=merc
            lat_0=55.9
            lon_0=-3.17
            resolution=h
            area_thresh=0.1
            llcrnrlon=-5
            llcrnrlat=55
            urcrnrlon=-1.8
            urcrnrlat=58

    figure defines the size of the plot.

    map defines the drawn map.
    See the basemap documentation for the parameters listed in full.

    Keyword arguments:

    args -- list of arguments. This must have three elements,
    the point positions file name, map properties file name and a list of point identifiers.
    """

    config = ConfigParser.RawConfigParser()
    config.read(argv[1])

    plt.figure(figsize=(config.getint('figure', 'width'), config.getint('figure', 'height')))
    map = Basemap(projection=config.get('map', 'projection'),
                  lat_0=config.getfloat('map', 'lat_0'), lon_0=config.getfloat('map', 'lon_0'),
                  resolution=config.get('map', 'resolution'), area_thresh=config.getfloat('map', 'area_thresh'),
                  llcrnrlon=config.getfloat('map', 'llcrnrlon'), llcrnrlat=config.getfloat('map', 'llcrnrlat'),
                  urcrnrlon=config.getfloat('map', 'urcrnrlon'), urcrnrlat=config.getfloat('map', 'urcrnrlat'))

    map.drawcoastlines()
    map.drawcountries()
    map.drawrivers(color='b')
    map.fillcontinents(color='green')
    map.drawmapboundary()

    csvfile = open(argv[0], 'rU')
    csvreader = csv.reader(csvfile)
    cities = {}

    for row in csvreader:
        cities[row[0]] = {'lat': float(row[1]), 'lon': float(row[2])}
    csvfile.close()

    lats = []
    lons = []
    path = []

    if len(argv) == 3:
        path = argv[2]
        for value in path:
            lats.append(cities[value]['lat'])
            lons.append(cities[value]['lon'])
        lats.append(cities[path[0]]['lat'])
        lons.append(cities[path[0]]['lon'])
        x, y = map(lons, lats)

        for label, xpt, ypt in zip(path, x, y):
            plt.text(xpt + 10000, ypt + 5000, label)

        map.plot(x, y, 'D-', markersize=10, linewidth=1, color='k', markerfacecolor='b')

    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
