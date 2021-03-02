import argparse
from sklearn.linear_model import LinearRegression
import os
import pandas as pd

import joblib

def train():

    train_set = pd.read_csv(args.train_data_path + "/processed.csv")
    test_set = pd.read_csv(args.test_data_path + "/processed.csv")

    selected_columns = ['pickup_weekday', 'pickup_hour', 'distance', 'passengers', 'vendor', 'cost']
    train_set = train_set[selected_columns]
    test_set = test_set[selected_columns]

    train_features = train_set.drop("cost", axis=1)
    train_labels = train_set["cost"].copy()
    lr = LinearRegression()
    lr.fit(train_features, train_labels)

    filename = os.path.join('outputs', 'taxi.pkl')

    joblib.dump(lr, filename)

    test_features = test_set.drop("cost", axis=1)[:3]
    test_labels = test_set["cost"].copy()
    preds = lr.predict(test_features)

    print("preds", preds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("split")
    parser.add_argument("--train_data_path", type=str, help="train data path")
    parser.add_argument("--test_data_path", type=str, help="test data path")
    args = parser.parse_args()
    train()