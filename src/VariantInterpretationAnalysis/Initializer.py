################################################################################
# Initializer - Class
#
# Controls the initialization of the WekaData object used in the system.
#
import os
from Collections import WekaData
from Parser import MutationInfoParser
import logging


def getAAIndex2Map(data):
    (default_feature_map, default_features) = parse() #calls aaindex2parser
    data.__defaultFeatures = default_features
    data.__defaultFeatureMap = default_feature_map
    return


# ------------------------------------------------------------------------------
# Initializes a WekaData object with the names of mutations to be used in this
# session of the program
#
def init_weka_data(filename, cleaned=False):
    logging.getLogger('genevia').info("Initializing Weka Data")
    if os.path.exists(filename):
        data = WekaData()
        getAAIndex2Map(data)
        with open(filename, "r") as mutationFile:
            outfile = open("./mutations.txt", "w")
            outfile.write("ID\tName\tSymbol\tIndex\tRSNum"
                          "\tClinicalSignificance\n")
            headers = mutationFile.readline().strip().split()
            for line in mutationFile:
                mutation = MutationInfoParser.parseLine(line)
                if mutation is not None:
                    outfile.write(str(mutation) + "\n")
                    data.addMutation(mutation)
            outfile.close()
            mutationFile.close()
        logging.getLogger('genevia').info("Initialization complete!")
        return data
    else:
        return None


# Testing
if __name__ == '__main__':
    data = initWekaData("./data/cleaned_variants")
    print data.getMutation(hash("NM_014630.2(ZNF592):c.3136G>A"))
