import os


def is_in_directory(directory_path, subpath):
    return os.path.commonprefix([directory_path, os.path.abspath(subpath)]) == directory_path


def is_in_any_directory(directory_paths, subpath):
    return any(
        is_in_directory(directory_path, subpath)
        for directory_path in directory_paths
    )
