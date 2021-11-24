import argparse
import os
import pandas as pd
import pandas as pd

print("Replace undefined values to relavant values and rename columns to meaningful names")

parser = argparse.ArgumentParser("normalize")
parser.add_argument('--data-path', type=str, help='input data path')
parser.add_argument("--output_normalize", type=str, help="replaced undefined values and renamed columns")

args = parser.parse_args()

print("Argument (output normalized taxi data path): %s" % args.output_normalize)

combined_converted_df = pd.read_csv(args.data_path + "/processed.csv")

# These functions replace undefined values and rename to use meaningful names.
replaced_stfor_vals_df = (combined_converted_df.replace({"store_forward": "0"}, {"store_forward": "N"})
                          .fillna({"store_forward": "N"}))

replaced_distance_vals_df = (replaced_stfor_vals_df.replace({"distance": ".00"}, {"distance": 0})
                             .fillna({"distance": 0}))

normalized_df = replaced_distance_vals_df.astype({"distance": 'float64'})

temp = pd.DatetimeIndex(normalized_df["pickup_datetime"])
normalized_df["pickup_date"] = temp.date
normalized_df["pickup_time"] = temp.time

temp = pd.DatetimeIndex(normalized_df["dropoff_datetime"])
normalized_df["dropoff_date"] = temp.date
normalized_df["dropoff_time"] = temp.time

del normalized_df["pickup_datetime"]
del normalized_df["dropoff_datetime"]

normalized_df.reset_index(inplace=True, drop=True)

if not (args.output_normalize is None):
    os.makedirs(args.output_normalize, exist_ok=True)
    print("%s created" % args.output_normalize)
    path = args.output_normalize + "/processed.csv"
    write_df = normalized_df.to_csv(path)
