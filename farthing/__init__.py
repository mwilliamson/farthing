import runpy

__all__ = ["run"]

def run(path):
    runpy.run_path(path)
