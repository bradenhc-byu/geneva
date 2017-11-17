################################################################################
# Initializer - Class
#
# Controls the initialization of the WekaData object used in the system.
#
import os
from Collections import WekaData
from Parser import MutationInfoParser, aaindex2parser
import Logger as Log


def getAAIndex2Map(data):
    (default_feature_map, default_features) = aaindex2parser.parse()
    data.setDefaultFeatures(default_features)
    data.setDefaultFeatureMap(default_feature_map)
    return


# ------------------------------------------------------------------------------
# Initializes a WekaData object with the names of mutations to be used in this
# session of the program
#
def init_weka_data(filename):
    if os.path.exists(filename):
        Log.info("Initializing WekaData")
        data = WekaData()
        getAAIndex2Map(data)
        with open(filename, "r") as mutation_file:
            for line in mutation_file:
                mutation = MutationInfoParser.parse_mutation(line)
                data.addMutation(mutation)
        Log.info("Initialization complete!")
        return data
    else:
        Log.error("Unable to open file: does not exist")
        return None


################################################################################
# Unit Testing -----------------------------------------------------------------
def unit_test():
    Log.set_log_level(Log.LEVEL_DEBUG)
    data = init_weka_data("./data/mutations_certain")
    print len(data.getMutations())


if __name__ == '__main__':
    unit_test()
