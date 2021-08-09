
"""
This module parses and cleans original data to be used with Pandas.

Interactive usage: 	open IPython console import this module and use `clean` function.
Usage: 			execute command `python3 helpers/preprocessing.py <path to datasheet>`

In the latter usage, cleaned datasheet and its dtypes are saved in two `csv` files.
"""

import pandas as pd
import numpy as np
import sys


def read_df(path):

	"""
	Load the original datasheet skipping the beginning descriptive rows.
	"""

	df = pd.read_excel(path, skiprows=[1,2,3,4])
	return df


def read_units(path):

	"""
	Read units reported in the original datasheet.
	"""

	T = pd.read_excel(path).iloc[3]
	T.name = "units"
	return T


def parse_date(x):
	x = None if x=="^" or x==0 else pd.Timestamp(x)
	return x


def parse_dollar(x):
	if type(x)==str and "Max Benefit" in x:
		x = x.rsplit(" ")[-1].strip("$")
	elif type(x)==str and x==".":
		x = np.nan
	x = float(x)
	return x


def parse_rate(x):
	x = np.nan if type(x)==str and x=="-" else float(x)
	return x


def parse_pct(x):
	x = np.nan if type(x)==str and x=="-" else float(x)
	return x


def parse_day(x):
	x = np.nan if type(x)==str and (x=="-" or x==".") else int(x)
	return x


def clean(
	path,
	T_funcs = {
		"unit": lambda x: x,
		"text": lambda x: x,
		"attribute": int,
		"date": parse_date,
		"end": parse_date,
		"flag": bool,
		"": parse_date,
		"dollars": parse_dollar,
		"weeks": int,
		"rate": parse_rate,
		"percent": parse_pct,
		"Calendar Quarters": int,
		"days": parse_day,
		"people/sq mi": float,
		"people": int,
		"sq mi": float,
		"people/year": int,
		"per 100,000": float,
		"start": parse_date
	}
):

	"""
	Clean original datasheet and return Pandas DataFrame.
	"""

	df = read_df(path)
	T = read_units(path)

	for col in T.index:

		unit = T.loc[col]

		if type(unit)!=str and np.isnan(unit):
			unit = ""

		# fix an error (described as text but it is a flag)
		if col=="LMABRN":
			unit="flag"

		func = T_funcs[unit]
		df.loc[:,col] = df.loc[:,col].apply(func)

	return df


if __name__ == "__main__":
	path = sys.argv[1]
	df = clean(path)
	outpath = "data.csv"
	df.to_csv(outpath, index=False)
	print("Cleaned data saved as \"{}\"".format(outpath))
	outpath = "dtypes.csv"
	df.dtypes.to_csv(outpath)
	print("Cleaned data dtypes saved as \"{}\"".format(outpath))
