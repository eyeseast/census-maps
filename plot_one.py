#!/usr/bin/env python3
import sys
import fiona
import matplotlib.pyplot as plt

from dotdensity import points_in_feature


def main(filename, key="POP10"):
    """
    Plot the first feature in filename
    """
    with fiona.open(filename) as collection:
        features = filter(lambda f: f["properties"][key] > 0, iter(collection))
        feature = next(features)
        return points_in_feature(feature, key)


def plot(points):
    x, y = zip(*points)
    plt.scatter(x, y, s=0.5)
    plt.show()


if __name__ == "__main__":
    points = main(sys.argv[1])
    plot(points)
