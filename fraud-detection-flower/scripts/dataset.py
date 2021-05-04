from typing import Tuple, List

import tensorflow as tf
import numpy as np

XY = Tuple[np.ndarray, np.ndarray]

def shuffle(x: np.ndarray, y: np.ndarray) -> XY:
    """Shuffle x and y."""
    idx = np.random.permutation(len(x))
    return x[idx], y[idx]

def partition(x: np.ndarray, y: np.ndarray, num_partitions: int) -> List[XY]:
    """Return x, y as list of partitions."""
    return list(zip(np.split(x, num_partitions), np.split(y, num_partitions)))

def create_partitions():
    # Load dataset
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

    # Shuffle
    (x_train, y_train) = shuffle(x_train, y_train)
    (x_test, y_test) = shuffle(x_test, y_test)

    # Partition
    xy_train = partition(x_train, y_train, 2)
    xy_test = partition(x_test, y_test, 2)

    # Store train partitons
    for index, xy_part in enumerate(xy_train):
        (x,y) = xy_part
        np.save(f'./x_train_{index}.npy', x)
        np.save(f'./y_train_{index}.npy', y)

    # Store test partitions
    for index, xy_part in enumerate(xy_test):
        (x,y) = xy_part
        np.save(f'./x_test_{index}.npy', x) 
        np.save(f'./y_test_{index}.npy', y)

def load_partition(x_train, y_train, x_test, y_test):
    return (np.load(x_train), np.load(y_train)), (np.load(x_test), np.load(y_test))

# Load partition 0
def main():
    create_partitions()

    # Load partiton 0
    (x_train, y_train), (x_test, y_test) = load_partition('./x_train_0.npy', './y_train_0.npy', './x_test_0.npy', './y_test_0.npy')
    print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

main()