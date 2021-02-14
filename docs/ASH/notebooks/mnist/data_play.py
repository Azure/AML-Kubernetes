from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.core import Workspace, ComputeTarget
import os
import numpy as np

ws = Workspace.from_config()
compute = ComputeTarget(ws, "nc6")
ws.compute_targets
pass
print("Found workspace {} at location {}".format(ws.name, ws.location))

from azureml.core import Dataset
from azureml.opendatasets import MNIST

data_folder = os.path.join(os.getcwd(), 'data')
os.makedirs(data_folder, exist_ok=True)

mnist_file_dataset = MNIST.get_file_dataset()
mnist_file_dataset.download(data_folder, overwrite=True)

mnist_file_dataset = mnist_file_dataset.register(workspace=ws,
                                                 name='mnist_opendataset',
                                                 description='training and test dataset',
                                                 create_new_version=True)
pass