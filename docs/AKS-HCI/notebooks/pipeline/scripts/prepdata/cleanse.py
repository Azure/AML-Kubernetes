# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.

import argparse
import os
from azureml.core import Run
import pandas as pd


def get_dict(dict_str):
    pairs = dict_str.strip("{}").split("\;")
    new_dict = {}
    for pair in pairs:
        key, value = pair.strip().split(":")
        new_dict[key.strip().strip("'")] = value.strip().strip("'")

    return new_dict


print("Cleans the input data")

parser = argparse.ArgumentParser("cleanse")
parser.add_argument('--data-path', type=str, help='input data path')
parser.add_argument("--output_cleanse", type=str, help="cleaned taxi data directory")
parser.add_argument("--useful_columns", type=str, help="useful columns to keep")
#parser.add_argument("--columns", type=str, help="rename column pattern")
parser.add_argument("--columns_key", type=str, help="rename column pattern")
parser.add_argument("--columns_value", type=str, help="rename column pattern")

args = parser.parse_args()

print("Argument 1(columns to keep): %s" % str(args.useful_columns.strip("[]").split("\;")))
print("Argument 2(columns renaming mapping Key): %s" % str(args.columns_key.strip("{}").split("\;")))
print("Argument 2(columns renaming mapping value): %s" % str(args.columns_value.strip("{}").split("\;")))
print("Argument 3(output cleansed taxi data path): %s" % args.output_cleanse)

# These functions ensure that null data is removed from the dataset,
# which will help increase machine learning model accuracy.

useful_columns = [s.strip().strip("'") for s in args.useful_columns.strip("[]").split("\;")]
columns_key = [s.strip().strip("'") for s in args.columns_key.strip("[]").split("\;")]
columns_value = [s.strip().strip("'") for s in args.columns_value.strip("[]").split("\;")]

columns = {key: value for key, value in zip(columns_key, columns_value)}


raw_df = pd.read_csv(args.data_path)
new_df = (raw_df
          .dropna(how='all')
          .rename(columns=columns))[useful_columns]

new_df.reset_index(inplace=True, drop=True)

if not (args.output_cleanse is None):
    os.makedirs(args.output_cleanse, exist_ok=True)
    print("%s created" % args.output_cleanse)
    path = args.output_cleanse + "/processed.csv"
    write_df = new_df.to_csv(path)
