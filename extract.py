"""File data extract module for NearEarthObjects."""

import csv
import json
import time

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data
        about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    print('Loading NEO and approach data...')
    neo_list = []

    with open(neo_csv_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        count = 0
        for neo in reader:
            neo_list.append(NearEarthObject(pdes=neo[3], full_name=neo[2],
                                            name=neo[4], diameter=neo[15],
                                            pha=neo[7]))
            count += 1
    return neo_list


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file.
    :return: A collection of CloseApproaches.
    """
    cad_list = []

    with open(cad_json_path, 'r') as file:
        cadData = json.load(file)
        count = 0
        # t1 = time.perf_counter()
        for approach in cadData['data']:
            cad_list.append(CloseApproach(
                des=str(approach[0]),
                cd=str(approach[3]),
                dist_min=float(approach[5]),
                v_rel=float(approach[7])))
            count += 1
    return cad_list
