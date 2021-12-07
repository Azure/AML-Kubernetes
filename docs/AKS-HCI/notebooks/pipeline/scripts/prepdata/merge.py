import argparse
import os
import pandas as pd

print("Merge Green and Yellow taxi data")

parser = argparse.ArgumentParser("merge")
parser.add_argument("--output_merge", type=str, help="green and yellow taxi data merged")
parser.add_argument("--green_data_path", type=str, help="green data path")
parser.add_argument("--yellow_data_path", type=str, help="yellow data path")

args = parser.parse_args()
print("Argument (output merge taxi data path): %s" % args.output_merge)


green_df = pd.read_csv(args.green_data_path + "/processed.csv")
yellow_df = pd.read_csv(args.yellow_data_path + "/processed.csv")

# Appending yellow data to green data
combined_df = green_df.append(yellow_df, ignore_index=True)
combined_df.reset_index(inplace=True, drop=True)

if not (args.output_merge is None):
    os.makedirs(args.output_merge, exist_ok=True)
    print("%s created" % args.output_merge)
    path = args.output_merge + "/processed.csv"
    write_df = combined_df.to_csv(path)
