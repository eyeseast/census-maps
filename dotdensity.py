#!/usr/bin/env python3
import itertools
import random
import sys

import fiona
from fiona.crs import from_epsg

import geojson
import numpy as np
from shapely.geometry import shape
from shapely.ops import triangulate


def main(src, dest, key="POP10"):
    """
    Open *src* with fiona
    Filter out features with no population
    Run points_in_feature on each feature
    Write each point as a new Point feature to *dest*
    """
    # crs = from_epsg(4326)
    # schema = {"geometry": "MultiPoint", "properties": {}}
    with fiona.open(src) as source, open(dest, "w") as sink:
        features = filter(lambda f: f["properties"][key] > 0, iter(source))
        for feature in features:
            points = points_in_feature(feature, key)
            multipoint = geojson.MultiPoint(map(list, points))
            f = geojson.Feature(geometry=multipoint)
            sink.write(geojson.dumps(f) + "\n")


def points_in_feature(feature, key="POP10"):
    """
    Take a geojson *feature*, create a shape
    Get population from feature.properties using *key*
    Concatenate all points yielded from points_in_shape
    """
    geom = shape(feature["geometry"])
    population = feature["properties"][key]
    return itertools.chain(*points_in_shape(geom, population))


def points_in_shape(geom, population):
    """
    plot n points randomly within a shapely geom
    first, cut the shape into triangles
    then, give each triangle a portion of points based on relative area
    within each triangle, distribute points using a weighted average
    yield each set of points (one yield per triangle)
    """
    triangles = triangulate(geom)
    for triangle in triangles:
        ratio = triangle.area / geom.area
        n = round(ratio * population)
        vertices = triangle.exterior.coords[:3]
        if n > 0:
            yield points_on_triangle(vertices, n)


def point_on_triangle(pt1, pt2, pt3):
    """
    Random point on the triangle with vertices pt1, pt2 and pt3.
    """
    s, t = sorted([random.random(), random.random()])
    return (
        s * pt1[0] + (t - s) * pt2[0] + (1 - t) * pt3[0],
        s * pt1[1] + (t - s) * pt2[1] + (1 - t) * pt3[1],
    )


def points_on_triangle(vertices, n):
    """
    Give n random points uniformly on a triangle.

    The vertices of the triangle are given by the shape
    (2, 3) array *vertices*: one vertex per row.
    """
    x = np.sort(np.random.rand(2, n), axis=0)
    return np.column_stack([x[0], x[1] - x[0], 1.0 - x[1]]) @ vertices


if __name__ == "__main__":
    main(*sys.argv[1:])
