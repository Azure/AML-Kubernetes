import os
import glob
import tarfile
import matplotlib.pyplot as plt
import numpy as np

data_folder = os.path.join(os.getcwd(), 'cifar10-data')
extracted_folder = os.path.join(data_folder, "extracted")
os.makedirs(extracted_folder, exist_ok=True)

cifar_gz = glob.glob(os.path.join(data_folder,"**/cifar-10-python.tar.gz"), recursive=True)[0]

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='latin1')
    return dict

with tarfile.open(cifar_gz, "r:gz") as tar:
    tar.extractall(path=extracted_folder)
    tar.close()

train_batches = glob.glob(os.path.join(extracted_folder, "**/data_batch_*"), recursive=True)
test_batch = glob.glob(os.path.join(extracted_folder, "**/test_batch*"), recursive=True)[0]
meta_file = glob.glob(os.path.join(extracted_folder, "**/batches.meta"), recursive=True)[0]

# data_batch = unpickle(train_batches[0])
data_batch = unpickle(test_batch)
meta_data = unpickle(meta_file)

# take the images data from batch data
images = data_batch['data']
# reshape and transpose the images
images = images.reshape(len(images),3,32,32).transpose(0,2,3,1)
# take labels of the images 
labels = data_batch['labels']
# label names of the images
label_names = meta_data['label_names']

# dispaly random images
# define row and column of figure
rows, columns = 1, 1
# take random image idex id
# imageId = np.random.randint(0, len(images), rows * columns)
imageId = np.arange(0, rows * columns)
# take images for above random image ids
images = images[imageId]
# take labels for these images only
labels = [labels[i] for i in imageId]

# define figure
fig=plt.figure(figsize=(10, 10))
# visualize these random images
for i in range(1, columns*rows +1):
    fig.add_subplot(rows, columns, i)
    plt.imshow(images[i-1])
    plt.xticks([])
    plt.yticks([])
    plt.title("{}"
          .format(label_names[labels[i-1]]))
# plt.show()

import torchvision.datasets as datasets
import torchvision.transforms as transforms

transform_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    # transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
])

test_set = datasets.CIFAR10(root=extracted_folder, train=False, download=False, transform=transform_test)
# print(test_set[0])
img, target = test_set[0]
print(img.numpy())
print(target)
print(test_set.classes[target])

