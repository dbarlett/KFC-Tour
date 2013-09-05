#!/usr/bin/env python

import requests
import simplekml
from subprocess import call


def get_kfc_locations(search_points, state):
    """Get ID and coordinates for all KFC locations in a state

    :param search_points: iterable of lon, lat tuples to use as starting addresses for search
    :param state: two-letter state abbreviation
    :returns: list of KFC locations, each a (lon, lat) tuple
    """

    KFC_URL = "http://www.kfc.com/storelocator/Services/SpatialData.svc/findNearbyStoresFiltered"
    payload = {
        "dist": 1000,  # Server error if > 1000 (km?)
        "top": 250,  # Server limits responses to 250
    }

    locations = {}

    for lon, lat in search_points:
        payload["lon"] = lon
        payload["lat"] = lat
        r = requests.get(KFC_URL, params=payload)
        for i in r.json():
            if i["state"] == state:
                locations[i["entityID"]] = (i["longitude"], i["latitude"])

    return locations.values()


def write_tsp(filename, nodes):
    """Write nodes to file in TSPLIB format

    :param filename: TSP filename
    :param nodes: list of node locations, each a (lon, lat) tuple
    """
    with open(filename, "w") as f:
        f.write("NAME : kfc\n")
        f.write("TYPE : TSP\n")
        f.write("DIMENSION : %i\n" % len(nodes))
        f.write("EDGE_WEIGHT_TYPE : EUC_2D\n")
        f.write("NODE_COORD_SECTION\n")
        for index, loc in enumerate(nodes):
            f.write("%i %f %f\n" % (index + 1, loc[0], loc[1]))
        f.write("EOF\n")


def read_tsp_solution(filename, nodes):
    """Read a Concorde TSP solution
    :param filename: solution file (.sol)
    :param nodes: list of node locations, each a (lon, lat) tuple
    :return: list of node locations in tour order, each a (lon, lat) tuple
    """
    tour = []
    with open(filename, "r") as sol:
        sol.readline()  # First line is number of nodes in tour
        for line in sol:
            for node in line.strip().split(" "):
                tour.append(nodes[int(node)])
    return tour


def write_kml(filename, linestring_name, linestring_desc, points):
    """Write a KML file containing a LineString of points
    :param filename: KML filename
    :param linestring_name: LineString name
    :param linestring_desc: LineString description
    :param points: list of tuples containing LineString points (lon, lat)
    """
    kml = simplekml.Kml()
    lin = kml.newlinestring(
        name=linestring_name,
        description=linestring_desc,
        coords=points
    )
    kml.save(filename)


if __name__ == '__main__':
    state = "CA"
    ca_points = (
        (-121.832886, 39.702961),  # Chico (Northern CA)
        (-119.779816, 36.746587),  # Fresno (Central CA)
        (-116.993408, 34.858890),  # Barstow (Southern CA)
    )

    kfc_ca = get_kfc_locations(ca_points, "CA")
    print "Found %d KFC locations in %s" % (len(kfc_ca), state)
    write_tsp("kfc_ca.tsp", kfc_ca)

    call(["./concorde", "kfc_ca.tsp"])

    tour = read_tsp_solution("kfc_ca.sol", kfc_ca)

    write_kml("kfc_ca.kml",
              "CA KFC Tour",
              "Tour of California KFC locations",
              tour
              )
    print "Wrote KML file"
