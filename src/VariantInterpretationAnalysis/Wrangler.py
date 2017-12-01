#############################
# Wrangler class
#
# Takes WekaData and populates desired features for each mutation
# Gets feature values from data maps after calling the parser for the appropriate files, if they exist
# If file does not exist, it fetches and saves the needed data first
#
# Returns populated WekaData object

from Definitions import DATA_DIR,AMINO_ACIDS_3_1,AVAILABLE_FEATURES
from Collections import Mutation, Feature
import Parser
import os
import DataBridge

class Wrangler:
    def __init__(self, wekaData):
        self.__wekaData = wekaData

    def addGeneFamilyToMutation(mutation, gfMap):
        mutation.add_feature("GENE_FAMILY", gfMap.get(mutation.get_gene(),"?"))
        return True

    @staticmethod
    def addAlleleFreqToMutation(mutation, mafMap):
        mutation.add_feature("ALLELE_FREQUENCY", mafMap.get(mutation.get_rs_number(), "?"))
        return True

    # dict of feature type to function
    dispatcher = {
        "GENE_FAMILY": addGeneFamilyToMutation,
        'ALLELE_FREQUENCY': addAlleleFreqToMutation
        #"y": addYToMutation()
    }

    parserDispatcher = {

    }

    def populateWekaData(self):
        # get genomic locations for mutations
        DataBridge.DataBridge.loadSNPData(AVAILABLE_FEATURES["allele-frequency"][1], self.__wekaData.getMutations())

        # populate feature data
        for feature in self.__wekaData.getFeatures():

            dataMap = DataBridge.DataBridge.loadMap(feature, self.__wekaData.getMutations())
            
            addFeature = Wrangler.dispatcher[feature.get_name()]
            for m in self.__wekaData.getMutations():
                addFeature(m, dataMap)
