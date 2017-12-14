"""
This module holds configuration for GeneVA. Use of this module as of the current version is depreciated, but we leave
the module here in case future updates require it.
"""
import os
import copy

__configuration_map = dict()


def init(filename):
    """
    This method must be called at the beginning of execution. It loads configuration from the config file passed in
    as an argument.

    :param filename: The path to the configuration file to load values from. The file is formated as key: value.
    """
    file_path = os.path.dirname(os.path.abspath(__file__)) + "/" + filename
    if os.path.exists(file_path):
        with open(file_path, "r") as config_file:
            for line in config_file:
                if not line:
                    continue
                if line[0] == "#":
                    continue
                pair = line.split(":")
                key = pair[0].strip()
                value = ":".join(pair[1:]).strip()
                __configuration_map[key] = value
    else:
        print "[ERROR] Configuration failed: file does not exist:", file_path


def get_config(key):
    """
    Returns the config value stored in memory associated with the provided key

    :param key: The key in a key,value pair
    :return: The value associated with the key
    """
    return __configuration_map.get(key, None)


def set_config(key, value):
    """
    Updates or creates a configuration value in memory

    :param key: The key in a key,value pair
    :param value: The new value
    """
    __configuration_map[key] = copy.deepcopy(value)