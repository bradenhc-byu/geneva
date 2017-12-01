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
import Logger as Log

class Wrangler:
    def __init__(self, wekaData):
        self.__wekaData = wekaData

    def addGeneFamilyToMutation(mutation, gfMap):
        mutation.add_feature("GENE_FAMILY", gfMap.get(mutation.get_gene(),"?"))
        return True

    @staticmethod
    # MAF stands for minor allele frequency
    def addAlleleFreqToMutation(mutation, mafMap):
        mutation.add_feature("ALLELE_FREQUENCY", mafMap.get(mutation.get_rs_number(), "?"))
        return True

    def addPhastConsToMutation(self, mutation, pcMap):
        mutation.add_feature("PHAST_CONS", pcMap.get(mutation.get_rs_number(), "?"))

    # dict of feature type to function
    dispatcher = {
        "GENE_FAMILY": addGeneFamilyToMutation,
        'ALLELE_FREQUENCY': addAlleleFreqToMutation,
        "PHAST_CONS": addPhastConsToMutation
        #"y": addYToMutation()
    }

    parserDispatcher = {

    }

    def populateWekaData(self):
        # populate feature data
        for feature in self.__wekaData.getFeatures():
            Log.info("Gathering %s data for %d mutations" % (feature.get_name(), len(self.__wekaData.getMutations())))
            dataMap = DataBridge.DataBridge.loadMap(feature, self.__wekaData.getMutations())
            
            addFeature = Wrangler.dispatcher[feature.get_name()]
            for m in self.__wekaData.getMutations():
                addFeature(m, dataMap)
