import runpy
import sys

__all__ = ["run"]

def run(path):
    runpy.run_path(path)
