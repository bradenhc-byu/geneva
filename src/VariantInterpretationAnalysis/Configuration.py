################################################################################
# Module to hold configuration for the Gene VIA project
#
import os
import copy

__configuration_map = dict()

def init(filename):
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

def getConfig(key):
    return __configuration_map.get(key, None)

def setConfig(key, value):
    __configuration_map[key] = copy.deepcopy(value)