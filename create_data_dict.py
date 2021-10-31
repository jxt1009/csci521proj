#!/usr/bin/env python3

import pathlib
import sys
import pandas
import numpy as np
import csv
pandas.options.plotting.backend = "plotly"

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
output_table = [['Variable', 'Unique Entries', 'Total Entries', 'Data Type', 'Data Classification', 'Number of Empty Values', 'Range', 'Median', 'Mean', 'Mode', 'Min', 'Max', 'Outliers']]

csv_dat = pandas.read_csv(input_data, sep='\t', na_values=['\\N'])
for heading in csv_dat:
    numeric = csv_dat[heading].dtype in (INT_TYPE, FLOAT_TYPE)
    new_row = [
            heading, # The Variable column
            csv_dat[heading].nunique(), # The Unique Entries column
            csv_dat[heading].count(), # The Total Entries column
            data_type if (data_type := csv_dat[heading].dtype) != OBJECT_TYPE else 'String', # The Data Type column
            cols[heading], # Grab the DataClassification from the dict above
            csv_dat[heading].isna().sum(),
            f'{csv_dat[heading].min()} - {csv_dat[heading].max()}' if numeric else None
        ]
    if numeric:
        row_properties = [
                csv_dat[heading].median(),
                csv_dat[heading].mean(),
                mode[0] if len(mode := csv_dat[heading].mode()) else None,
                csv_dat[heading].min(),
                csv_dat[heading].max(),
                set(csv_dat[heading].loc[abs(csv_dat[heading] - csv_dat[heading].mean()) > csv_dat[heading].std() * 3])
            ]
        new_row += row_properties

    output_table.append(new_row)


import plotly.graph_objects as go
is_adult = go.Figure(data=[go.Pie(values=[(ones := csv_dat['isAdult'].sum()), csv_dat['isAdult'].count() - ones], labels=["1", "0"])])
is_adult.update_layout(title_text="isAdult")
is_adult.show()

is_original_title = go.Figure(data=[go.Pie(values=[(ones := csv_dat['isOriginalTitle'].sum()), csv_dat['isOriginalTitle'].count() - ones], labels=["1", "0"])])
is_original_title.update_layout(title_text="isOriginalTitle")
is_original_title.show()

runtime_minutes = csv_dat['runtimeMinutes'].plot.hist()
runtime_minutes.show()

ordering = csv_dat['ordering'].plot.hist()
ordering.show()

birth_year = csv_dat['birthYear'].plot.hist()
birth_year.show()

death_year = csv_dat['deathYear'].plot.hist()
death_year.show()

start_year = csv_dat['startYear'].plot.hist()
start_year.show()

rating = csv_dat['averageRating'].plot.hist()
rating.show()

votes = csv_dat['numVotes'].plot.box()
votes.show()

with open('data_dict.tsv', 'w') as csvF:
    writer = csv.writer(csvF, delimiter='\t')
    writer.writerows(output_table)
