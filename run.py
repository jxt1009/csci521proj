#!/usr/bin/env python3

import pandas as pd


def process_tsv(name,filename):
	table = pd.read_csv(filename, sep='\t')
		
	print(table.head(15))
	return {name:table}


	
files = process_tsv("ratings","title.ratings.tsv")
files.update(process_tsv("names","name.basics.tsv"))
files.update(process_tsv("title.basics","title.basics.tsv"))
files.update(process_tsv("akas","title.akas.tsv"))
s