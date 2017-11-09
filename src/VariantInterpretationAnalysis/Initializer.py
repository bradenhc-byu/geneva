################################################################################
# Initializer - Class
#
# Controls the initialization of the WekaData object used in the system.
#
import os


from Collections import WekaData,Mutation
from aaindex2parser import parse

def getAAIndex2Map(data):
    (default_feature_map, default_features) = parse() #calls aaindex2parser
    data.__defaultFeatures = default_features
    data.__defaultFeatureMap = default_feature_map
    return

# ------------------------------------------------------------------------------
# Initializes a WekaData object with the names of mutations to be used in this
# session of the program
#
def initWekaData(filename):
    if os.path.exists(filename):
        data = WekaData()
        getAAIndex2Map(data)
        with open(filename,"r") as mutationFile:
            for line in mutationFile:
                data = line.strip().split()

                mutation = Mutation()
                data.addMutation(mutation)
            file.close()
        return data
    else:
        return None
