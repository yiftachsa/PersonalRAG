from datetime import datetime
import json
import os

import time

ROOT_PATH = r"C:\Users\Yifta\Documents\Projects Experiments\personalRAG"  # "D:\\DataSets"


# def create_dir(dir_path):
#     """
#     Checks if a directory exists. If not, create it.
#     If it does exist raises an exception.
#
#     Args:
#       dir_path (str): The path to the directory.
#     """
#     if not os.path.exists(dir_path):
#         print(f"{dir_path} does not exist - creating it")
#         os.makedirs(dir_path)
#     else:
#         raise Exception(f"{dir_path} already exists")


def init_date_dir(version):
    """
    initialize a new experiment directory and return its path
    :param version: the version of the experiment.
    :return: the path of the new experiment directory
    """
    time_now = datetime.now().strftime('%H-%M_%d-%m-%Y')
    path = rf"{ROOT_PATH}\v_{version}\{time_now}"
    os.makedirs(path, exist_ok=False)
    return path


def get_prev_date_dir(version):
    """
    Scan the ROOT_PATH directory for the latest date directory.
    The directory name is the date in the format '%H-%M_%d-%m-%Y'.
    If no directory is found in the root directory, return None.

    :param version: The version of the experiment.
    :return: The path of the latest date directory. None if no directory is found.
    """
    path = rf"{ROOT_PATH}\v_{version}"

    latest_dir_path = None
    latest_time = None
    if not os.path.exists(path):
        return None
    for dir_name in os.listdir(path):
        dir_time = datetime.strptime(dir_name, '%H-%M_%d-%m-%Y')
        if latest_time is None or dir_time > latest_time:
            latest_time = dir_time
            latest_dir_path = os.path.join(path, dir_name)
    return latest_dir_path


def get_prev_files_details(prev_data_path, new_source_path):
    """
    Load the previous files details from disk. If the prev_data_path is None, return None.
    Check that the source path of the previous experiment is the same as the new source path.
    If it is not, raise an exception.

    :param prev_data_path: The path of the previous experiment's data.
    :param new_source_path: The source path of the new experiment.
    :return: The previous files details.
    """
    if prev_data_path is None:
        return None
    prev_details = load_dict(fr"{prev_data_path}\version_details")
    try:
        assert prev_details["source_path"] == new_source_path
        prev_files_details = load_dict(fr"{prev_data_path}\files_details")
        return prev_files_details
    except Exception as e:
        raise Exception("Different sources paths, please create a new version", e)


def list_files(root_dir, save_path=None):
    """
    Create a list of all files in the given root directory.
    Returns a dictionary of file paths and their last modified time.
    :param root_dir: The root directory to create a list of files from.
    :return: A list of file paths.
    """
    files = {}
    for dir_path, dir_names, file_names in os.walk(root_dir):
        for filename in file_names:
            file_path = os.path.join(dir_path, filename)
            # last modified time
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            files[os.path.join(dir_path, filename)] = file_mod_time.isoformat()

    if save_path is not None:
        save_dict(files, save_path)
    return files


def save_dict(dict_to_save, path):
    """
    Save the dict to a JSON file.
    :param dict_to_save: Dictionary to save.
    :param path: destination path.
    """
    with open(f"{path}.json", "w") as f:
        json.dump(dict_to_save, f)


def load_dict(path):
    """
    Load a dictionary from a JSON file.
    :param path: source path.
    :return: dictionary
    """
    with open(f"{path}.json", "r") as f:
        return json.load(f)


def get_changed_files(curr_files_details, prev_files_details=None):
    """
    Returns a list of files that have been modified since the last run.

    :param curr_files_details: dictionary of file paths and their last modified time.
    :param prev_files_details: dictionary of file paths and their last modified time. Defaults to None.
    :return: a list of file paths.
    """
    if prev_files_details is None:
        return list(curr_files_details.keys())
    changed_files = []
    for curr_file_path, curr_file_mod_time in curr_files_details.items():
        if curr_file_path in prev_files_details:
            prev_file_mod_time = prev_files_details[curr_file_path]
            if datetime.fromisoformat(curr_file_mod_time) > datetime.fromisoformat(prev_file_mod_time):
                changed_files.append(curr_file_path)
        else:
            changed_files.append(curr_file_path)
    return changed_files

# files = list_files('/content')
# print(files)
# filtered_files = filter_by_extension(files.keys(), extensions=DOCLING_FILE_TYPES)
# print(filtered_files)

# csv_files = filter_by_extension(files.keys(), extensions=[".csv"])
# print(csv_files)
