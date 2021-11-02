# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.

import os
import argparse
import pandas

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
# sklearn.externals.joblib is removed in 0.23
from sklearn import __version__ as sklearnver
from packaging.version import Version
if Version(sklearnver) < Version("0.23.0"):
    from sklearn.externals import joblib
else:
    import joblib

parser = argparse.ArgumentParser()
parser.add_argument('--data-dir', required=True, help='path to input data directory')
args = parser.parse_args()

# get input data
data_file = os.path.join(args.data_dir, 'iris.csv')
df = pandas.read_csv(data_file)

x_col = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
y_col = ['species']
x_df = df.loc[:, x_col]
y_df = df.loc[:, y_col]

#dividing X,y into train and test data
x_train, x_test, y_train, y_test = train_test_split(x_df, y_df, test_size=0.2, random_state=223)

data = {'train': {'X': x_train, 'y': y_train},

        'test': {'X': x_test, 'y': y_test}}

clf = DecisionTreeClassifier().fit(data['train']['X'], data['train']['y'])
model_file_name = 'decision_tree.pkl'

print('Accuracy of Decision Tree classifier on training set: {:.2f}'.format(clf.score(x_train, y_train)))
print('Accuracy of Decision Tree classifier on test set: {:.2f}'.format(clf.score(x_test, y_test)))

os.makedirs('./outputs', exist_ok=True)
with open(model_file_name, 'wb') as file:
    joblib.dump(value=clf, filename='outputs/' + model_file_name)
