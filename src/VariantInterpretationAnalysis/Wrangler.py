#############################
# Wrangler class
#
# Takes WekaData and populates desired features for each mutation
# Gets feature values from data maps after calling the parser for the appropriate files, if they exist
# If file does not exist, it fetches and saves the needed data first
#
# Returns populated WekaData object

from Definitions import DATA_DIR,AMINO_ACIDS_3_1
from Collections import Mutation
import Parser
import os
import DataBridge

class Wrangler:
    def __init__(self, wekaData):
        self.__wekaData = wekaData

    def addDefaultFeatureToMutation(self, feature, mutation):
        dfMap = self.__wekaData.__defaultFeatures
        (part1,part2) = mutation.get_symbol(True)
        part1_short = AMINO_ACIDS_3_1[part1]
        part2_short = AMINO_ACIDS_3_1[part2]
        featureMutationCode = feature + " " + part1_short + " " + part2_short
        value = dfMap[featureMutationCode]
        # add to mutation
        mutation.addFeature(feature,value)
        return True

    def addGeneFamilyToMutation(self, mutation, gfMap):
        mutation.addFeature("GENE_FAMILY", gfMap[mutation.__gene])
        return True

    def addYToMutation(self, mutation):
        return False

    # dict of feature type to function
    dispatcher = {
        #"GENE_FAMILY": addGeneFamilyToMutation(),
        #"y": addYToMutation()
    }

    parserDispatcher = {

    }

    def populateWekaData(self):
        for df in self.__wekaData.getDefaultFeatures():
            for m in self.__wekaData.getMutations():
                self.addDefaultFeatureToMutation(df, m)

        for feature in self.__wekaData.getFeatures():
            # check if file is there
            # if it isn't, download
            if not os.path.isfilename(feature.fileName):
                DataBridge.download(feature, self.__wekaData.getMutations())

            # call parser on feature
            dataMap = Parser.parse(feature)

            addFeature = Wrangler.dispatcher[f]
            for m in self.__wekaData.getMutations():
                addFeature(m, dataMap)
