"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    with open(filename, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(fieldnames)
        for approach in results:
            approach_attrs = approach.serialize()
            neo_attrs = approach.neo.serialize()
            writer.writerow([approach_attrs['datetime_utc'], approach_attrs['distance_au'], approach_attrs['velocity_km_s'], neo_attrs['designation'], neo_attrs['name'], neo_attrs['diameter_km'], neo_attrs['potentially_hazardous']])


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    approaches = []
    for approach in results:
        approach_for_json = {}
        approach_attrs = approach.serialize()
        neo_attrs = approach.neo.serialize() 
        approach_for_json['datetime_utc'] = approach_attrs['datetime_utc']
        approach_for_json['distance_au'] = approach_attrs['distance_au']
        approach_for_json['velocity_km_s'] = approach_attrs['velocity_km_s']
        approach_for_json['neo'] = {}
        approach_for_json['neo']['designation'] = neo_attrs['designation']
        approach_for_json['neo']['name'] = neo_attrs['name']
        approach_for_json['neo']['diameter_km'] = neo_attrs['diameter_km']
        approach_for_json['neo']['potentially_hazardous'] = neo_attrs['potentially_hazardous']

        approaches.append(approach_for_json)
    with open(filename, 'w') as outfile:
        json.dump(approaches, outfile, indent=2)