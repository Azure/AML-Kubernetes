import argparse
from sklearn.linear_model import LinearRegression
import os
from azureml.core import Run

import joblib

def train():
    run = Run.get_context()

    # To learn more about how to access dataset in your script, please
    # see https://docs.microsoft.com/en-us/azure/machine-learning/how-to-train-with-datasets.
    train_set_data = run.input_datasets["output_split_train"]
    test_set_data = run.input_datasets["output_split_test"]
    train_set = train_set_data.to_pandas_dataframe()
    test_set = test_set_data.to_pandas_dataframe()

    #train_set = pd.read_parquet(train_data_path)

    train_features = train_set.drop("cost", axis=1)
    train_labels = train_set["cost"].copy()
    lr = LinearRegression()
    lr.fit(train_features, train_labels)

    filename = os.path.join('outputs', 'taxi.pkl')

    joblib.dump(lr, filename)

    #test_set = pd.read_parquet(test_data_path)

    test_features = test_set.drop("cost", axis=1)[:3]
    test_labels = test_set["cost"].copy()
    preds = lr.predict(test_features)

    print("preds", preds)
if __name__ == "__main__":
    train()