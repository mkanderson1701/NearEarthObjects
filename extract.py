"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json
import time

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    print('Loading NEO and approach data...')
    neo_list = []

    with open(neo_csv_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        count = 0
        # t1 = time.perf_counter()
        for neo in reader:
            neo_list.append(NearEarthObject(pdes=neo[3], full_name=neo[2], name=neo[4], diameter=neo[15], pha=neo[7]))
            count += 1
        # t2 = time.perf_counter()
        # print(f'csv load complete in {t2-t1:0.6f} seconds')
        # print('neos loaded: ' + str(count))
    return neo_list


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    cad_list = []

    with open(cad_json_path, 'r') as file:
        cadData = json.load(file)
        count = 0
        # t1 = time.perf_counter()
        for approach in cadData['data']:
            cad_list.append(CloseApproach(des=str(approach[0]), cd=str(approach[3]), dist_min=float(approach[5]), v_rel=float(approach[7])))
            count += 1
        # t2 = time.perf_counter()
        # print(f'json load complete in {t2-t1:0.6f} seconds')
        # print('approaches loaded: ' + str(count))
    return cad_list
