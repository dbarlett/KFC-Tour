#!/usr/bin/env python

import requests
import simplekml
from subprocess import call

#  Search points for contintental U.S.
#  Adapted from http://dev.maxmind.com/geoip/legacy/codes/state_latlon/, plus
#  supplemental points for large states
SEARCH_POINTS = [
    ["AL", -86.8073, 32.799],
    ["AR", -92.3809, 34.9513],
    ["AZ", -111.3877, 33.7712],
    ["CA", -121.8328, 39.7029],  # Chico (Northern CA)
    ["CA", -119.7798, 36.7465],  # Fresno (Central CA)
    ["CA", -116.9934, 34.8588],  # Barstow (Southern CA)
    ["CO", -105.3272, 39.0646],
    ["CT", -72.7622, 41.5834],
    #["DC", -77.0262, 38.8964],
    #["DE", -75.5148, 39.3498],
    ["FL", -84.2733, 30.4249],  # Tallahassee (North FL)
    ["FL", -82.4571, 27.9505],  # Tampa (South FL)
    ["FL", -81.7799, 24.5550],  # Key West (South FL)
    ["GA", -83.6487, 32.9866],
    ["IA", -93.214, 42.0046],
    ["ID", -114.5103, 44.2394],
    ["IL", -89.0022, 40.3363],
    ["IN", -86.2604, 39.8647],
    ["KS", -96.8005, 38.5111],
    ["KY", -84.6514, 37.669],
    ["LA", -91.8749, 31.1801],
    ["MA", -71.5314, 42.2373],
    ["MD", -76.7902, 39.0724],
    ["ME", -69.3977, 44.6074],
    ["MI", -84.5603, 43.3504],
    ["MN", -93.9196, 45.7326],
    ["MO", -92.302, 38.4623],
    ["MS", -89.6812, 32.7673],
    #["MT", -110.3261, 46.9048],
    ["NC", -79.8431, 35.6411],
    ["ND", -99.793, 47.5362],
    ["NE", -98.2883, 41.1289],
    ["NH", -71.5653, 43.4108],
    #["NJ", -74.5089, 40.314],
    ["NM", -106.2371, 34.8375],
    ["NV", -117.1219, 38.4199],
    ["NY", -74.9384, 42.1497],
    ["OH", -82.7755, 40.3736],
    ["OK", -96.9247, 35.5376],
    ["OR", -122.1269, 44.5672],
    ["PA", -77.264, 40.5773],
    ["RI", -71.5101, 41.6772],
    ["SC", -80.9066, 33.8191],
    ["SD", -99.4632, 44.2853],
    ["TN", -86.7489, 35.7449],
    ["TX", -102.3376, 31.7842],  # Odessa (West TX)
    ["TX", -101.8103, 35.1917],  # Amarillo (North TX)
    ["TX", -98.4265, 29.4013],   # San Antonio (East TX)
    ["UT", -111.8535, 40.1135],
    ["VA", -78.2057, 37.768],
    ["VT", -72.7093, 44.0407],
    ["WA", -121.5708, 47.3917],
    ["WI", -89.6385, 44.2563],
    ["WV", -80.9696, 38.468],
    ["WY", -107.2085, 42.7475],
]


def get_all_kfc_locations():
    """Get ID and coordinates for all KFC locations
    :returns: dict of KFC locations, key = entityID, value = (lon, lat) tuple
    """

    kfc_url = "http://www.kfc.com/storelocator/Services/SpatialData.svc/findNearbyStoresFiltered"
    payload = {
        "dist": 1000,  # Server error if > 1000 (km?)
        "top": 250,  # Server limits responses to 250
    }

    locations = {}

    for state, lon, lat in SEARCH_POINTS:
        payload["lon"] = lon
        payload["lat"] = lat
        r = requests.get(kfc_url, params=payload)
        for i in r.json():
            locations[i["entityID"]] = (i["longitude"], i["latitude"])

    print "Found %i locations" % len(locations)
    return locations


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


def load_tsp_solution(filename, nodes):
    """Load a TSP solution
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
    kfc_us = get_all_kfc_locations()

    all_points = kfc_us.values()
    write_tsp("kfc_us.tsp", all_points)

    call(["./concorde", "kfc_us.tsp"])

    tour = load_tsp_solution("kfc_us.sol", all_points)

    write_kml("kfc_us.kml",
              "US KFC Tour",
              "Tour of KFC locations in the Continental U.S.",
              tour
              )
    print "Wrote KML file"
