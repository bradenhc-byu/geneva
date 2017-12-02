#############################
# Wrangler class
#
# Takes WekaData and populates desired features for each mutation
# Gets feature values from data maps after calling the parser for the appropriate files, if they exist
# If file does not exist, it fetches and saves the needed data first
#
# Returns populated WekaData object

from Definitions import DATA_DIR,AMINO_ACIDS_3_1,AVAILABLE_FEATURES
from Collections import Mutation, Feature, WekaData
import Parser
import os
import DataBridge
import Logger as Log

class Wrangler:
    def __init__(self, wekaData):
        self.__wekaData = wekaData

    @staticmethod
    def addGeneFamilyToMutation(mutation, gfMap):
        mutation.add_feature("GENE_FAMILY", gfMap.get(mutation.get_gene(),"?"))
        return True

    @staticmethod
    # MAF stands for minor allele frequency
    def addAlleleFreqToMutation(mutation, snpMap):
        mutation.add_feature("ALLELE_FREQUENCY", snpMap.get(mutation.get_rs_number(), (-1, -1, "?"))[2])
        return True

    @staticmethod
    def addPhastConsToMutation(mutation, pcMap):
        mutation.add_feature("PHAST_CONS", pcMap.get(mutation.get_rs_number(), "?"))



    def populateWekaData(self):
        # populate feature data
        for feature in self.__wekaData.getFeatures():
            Log.info("Gathering %s data for %d mutations" % (feature.get_name(), len(self.__wekaData.getMutations())))
            dataMap = DataBridge.DataBridge.loadMap(feature, self.__wekaData.getMutations())
            
            addFeature = Wrangler.dispatcher[feature.get_name()]
            for m in self.__wekaData.getMutations():
                addFeature(m, dataMap)

# dict of feature type to function
Wrangler.dispatcher = {
    "GENE_FAMILY": Wrangler.addGeneFamilyToMutation,
    'ALLELE_FREQUENCY': Wrangler.addAlleleFreqToMutation,
    "PHAST_CONS": Wrangler.addPhastConsToMutation
    #"y": addYToMutation()
}

def feature_test_setup(feature, wekaData):
    feature.set_filename(feature.get_fileName() + "test")
    try: os.remove(feature.get_fileName())
    except: pass
    wekaData.addFeature(feature)

def unit_test():
    mutations = [Mutation("name", gene="TWNK", rs_num="374997012"),
                 Mutation("blabla", gene="FBN1", rs_num="2228241"),
                 Mutation("junk", gene="xylophoneMonster", rs_num="rubbish")]

    wekaData = WekaData()
    feature_test_setup(Feature(*AVAILABLE_FEATURES['allele-frequency']), wekaData)
    feature_test_setup(Feature(*AVAILABLE_FEATURES['phast-cons']), wekaData)
    feature_test_setup(Feature(*AVAILABLE_FEATURES['gene-family']), wekaData)

    for m in mutations:
        wekaData.addMutation(m)

    wrangler = Wrangler(wekaData)
    wrangler.populateWekaData()

    Log.debug("WRANGLER UNIT TESTS PASSED")

if __name__ == "__main__":
    unit_test()