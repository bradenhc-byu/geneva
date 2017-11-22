################################################################################
# Initializer - Class
#
# Controls the initialization of the WekaData object used in the system.
#
import os
from Collections import WekaData, Feature
from Parser import MutationInfoParser, aaindex2parser
import Logger as Log


def get_aaindex2_data(data):
    # Parse the aaindex2 file
    (default_feature_map, default_features) = aaindex2parser.parse()

    # Add the features to the weka data feature list
    for feature in default_features:
        data.addFeature(Feature(feature,
                                feature+".txt",
                                dataType=Feature.NUMERIC_TYPE))

    # Add all the features to the mutations in the WekaData object
    for mutation in data.getMutations():
        for feature in default_features:
            feature_key = feature + ":" + mutation.get_symbol(two=True)
            feature_value = default_feature_map.get(feature_key, "0")
            mutation.add_feature(feature, feature_value)

    data.setDefaultFeatures(default_features)
    data.setDefaultFeatureMap(default_feature_map)
    return


# ------------------------------------------------------------------------------
# Initializes a WekaData object with the names of mutations to be used in this
# session of the program
#
def init_weka_data(filename):
    if os.path.exists(filename):
        Log.info("Initializing WekaData...")
        data = WekaData()
        Log.info("Gathering mutation info")
        with open(filename, "r") as mutation_file:
            for line in mutation_file:
                mutation = MutationInfoParser.parse_mutation(line)
                data.addMutation(mutation)
        Log.info("Getting default features")
        get_aaindex2_data(data)
        Log.info("Initialization complete!")
        return data
    else:
        Log.error("Unable to open file: does not exist")
        return None


################################################################################
# Unit Testing -----------------------------------------------------------------
def unit_test():
    Log.set_log_level("debug")
    data = init_weka_data("./data/mutations_certain")
    print len(data.getMutations())


if __name__ == '__main__':
    unit_test()
