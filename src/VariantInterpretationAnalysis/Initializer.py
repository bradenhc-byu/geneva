"""
Initializer Module

Controls the initialization of a WekaData object, populating it with Mutation objects and default Features (amino
acid properties)
"""
import os
from Collections import WekaData, Feature
from Parser import MutationInfoParser, aaindex2parser
from Definitions import DATA_DIR
import Logger as Log


def get_aaindex2_data(data):
    # Parse the aaindex2 file
    (default_feature_map, default_features) = aaindex2parser.parse()

    # Add all the features to the mutations in the WekaData object
    for mutation in data.getMutations():
        for feature in default_features:
            feature_key = feature + ":" + mutation.get_symbol(two=True)
            feature_value = default_feature_map.get(feature_key, "?")
            mutation.add_feature(feature, feature_value)
    data.setDefaultFeatures(default_features)
    return


# ------------------------------------------------------------------------------
# Initializes a WekaData object with the names of mutations to be used in this
# session of the program
#
def init_weka_data(data, filename="mutations_certain"):
    filepath = DATA_DIR + filename
    if os.path.exists(filepath):
        Log.info("Initializing WekaData...")
        Log.info("Gathering mutation info")
        with open(filepath, "r") as mutation_file:
            for line in mutation_file:
                mutation = MutationInfoParser.parse_mutation(line)
                data.addMutation(mutation)
        Log.info("Getting default features")
        get_aaindex2_data(data)
        Log.info("Initialization complete!")
        return True
    else:
        Log.error("Unable to open file: '" + filepath + "' does not exist")
        return False


################################################################################
# Unit Testing -----------------------------------------------------------------
def unit_test():
    Log.set_log_level("debug")
    data = WekaData()
    init_weka_data(data)
    print len(data.getMutations())


if __name__ == '__main__':
    unit_test()
