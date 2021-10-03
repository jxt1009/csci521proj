#!/usr/bin/env python3

import pathlib
import sys
import pandas
import numpy as np
import csv

input_data = pathlib.Path('data/us.movies.actors.tsv') if len(sys.argv) < 2 else sys.argv[1]

# Dictionary indicates whether each value is a scalar, nominal, or ordinal
NOMINAL = 'N'
SCALAR = 'S'
ORDINAL = 'O'
EMPTY = 'E'

OBJECT_TYPE = 'O'
INT_TYPE = 'int64'
FLOAT_TYPE = 'float64'

cols = {
    'tconst': NOMINAL,
    'nconst': NOMINAL,
    'primaryName': NOMINAL,
    'birthYear': SCALAR,
    'deathYear': SCALAR,
    'primaryProfession': NOMINAL,
    'titleType': NOMINAL,
    'primaryTitle': NOMINAL,
    'originalTitle': NOMINAL,
    'isAdult': SCALAR, # Not just a nominal because the value indicates more than just a label
    'startYear': SCALAR,
    'endYear': SCALAR,
    'runtimeMinutes': SCALAR,
    'genres': NOMINAL,
    'ordering': ORDINAL, # Ordered because the 5th title in the series comes after the 4th
    'title': NOMINAL,
    'region': NOMINAL,
    'language': NOMINAL,
    'types': NOMINAL,
    'attributes': NOMINAL,
    'isOriginalTitle': SCALAR, # Same reasoning as for isAdult
    'averageRating': SCALAR,
    'numVotes': SCALAR
}


# Start the output table off with the header names
output_table = [['Variable', 'Unique Entries', 'Total Entries', 'Data Type', 'Data Classification', 'Number of Empty Values', 'Range']]

csv_dat = pandas.read_csv(input_data, sep='\t', na_values=['\\N'])
for heading in csv_dat:
    new_row = [
            heading, # The Variable column
            csv_dat[heading].nunique(), # The Unique Entries column
            csv_dat[heading].count(), # The Total Entries column
            data_type if (data_type := csv_dat[heading].dtype) != OBJECT_TYPE else 'String', # The Data Type column
            cols[heading], # Grab the DataClassification from the dict above
            csv_dat[heading].isna().sum(),
            f'{csv_dat[heading].min()} - {csv_dat[heading].max()}' if csv_dat[heading].dtype in (INT_TYPE, FLOAT_TYPE) else None
        ]
    output_table.append(new_row)

with open('data_dict.tsv', 'w') as csvF:
    writer = csv.writer(csvF, delimiter='\t')
    writer.writerows(output_table)
