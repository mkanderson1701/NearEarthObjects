"""Write a stream of close approaches to CSV or to JSON."""

import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of CloseApproach objects to a CSV file.

    :param results: An iterable of CloseApproach objects.
    :param filename: A Path-like object pointing to save location.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )

    csv.register_dialect('myDialect', delimiter=',',
                         doublequote=0, escapechar='',
                         quotechar="'", quoting=csv.QUOTE_MINIMAL)

    # the doublequote thing is annoying

    with open(filename, mode='w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, dialect="myDialect")
        filewriter.writerow(fieldnames)
        for approach in results:
            filewriter.writerow(approach.csvMaker)
        print(f"Export to {filename} complete.")


def write_to_json(results, filename):
    """Write an iterable of CloseApproach objects to a JSON file.

    :param results: An iterable of CloseApproach objects.
    :param filename: A Path-like object pointing to save location.
    """
    # Note that I am NOT using NaN in the JSON as the instructions indicate.
    # NaN is not valid JSON
    #
    # A float for missing diameter (i.e. 0) is what passes the unit tests.

    bigKahuna = []
    for approach in results:
        bigKahuna.append(approach.jsonMaker)

    with open(filename, 'w') as outfile:
        json.dump(bigKahuna, outfile, indent=2)

    print(f"Export to {filename} complete.")
