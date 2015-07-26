import itertools


def grouped(values, key):
    return itertools.groupby(sorted(values, key=key), key=key)
