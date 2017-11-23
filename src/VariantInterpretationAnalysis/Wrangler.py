#############################
# Wrangler class
#
# Takes WekaData and populates desired features for each mutation
# Gets feature values from data maps after calling the parser for the appropriate files, if they exist
# If file does not exist, it fetches and saves the needed data first
#
# Returns populated WekaData object

from Definitions import DATA_DIR,AMINO_ACIDS_3_1,AVAILABLE_FEATURES,AVAILABLE_FEATURES_MAP
from Collections import Mutation
import Parser
import os
import DataBridge

class Wrangler:
    def __init__(self, wekaData):
        self.__wekaData = wekaData

    #def addDefaultFeatureToMutation(self, feature, mutation):
    #    dfMap = self.__wekaData.getDefaultFeatureMap()
    #    (part1,part2) = mutation.get_symbol(True)
    #    part1_short = AMINO_ACIDS_3_1.get(part1, "?")
    #    part2_short = AMINO_ACIDS_3_1.get(part2, "?")
    #    featureMutationCode = feature + " " + part1_short + " " + part2_short
    #    value = dfMap.get(featureMutationCode, "?")
    #    # add to mutation
    #    mutation.add_feature(feature,value)
    #    return True

    def addGeneFamilyToMutation(self, mutation, gfMap):
        mutation.add_feature("GENE_FAMILY", gfMap[mutation.__gene])
        return True

    def addYToMutation(self, mutation):
        return False

    # dict of feature type to function
    dispatcher = {
        "GENE_FAMILY": addGeneFamilyToMutation,
        #"y": addYToMutation()
    }

    parserDispatcher = {

    }

    def populateWekaData(self):
        # This is now done in the Initializer
        #for df in self.__wekaData.getDefaultFeatures():
        #    for m in self.__wekaData.getMutations():
        #        self.addDefaultFeatureToMutation(df, m)

        #for m in self.__wekaData.getMutations():
        #    myStr = ""
        #    for df in self.__wekaData.getDefaultFeatures():
        #        myStr = myStr + m.get_feature(df)+ " "
        #    print myStr
        

        for feature in self.__wekaData.getFeatures():
            feature_path=AVAILABLE_FEATURES_MAP.get(feature)

            dataMap = DataBridge.DataBridge.loadMap(feature, AVAILABLE_FEATURES_MAP[feature], self.__wekaData.getMutations())
            
            addFeature = Wrangler.dispatcher[f]
            for m in self.__wekaData.getMutations():
                addFeature(m, dataMap)
