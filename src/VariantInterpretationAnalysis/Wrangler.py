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
import copy

class Wrangler:
    def __init__(self, wekaData):
        self.__wekaData = wekaData

    @staticmethod
    def addGeneFamilyToMutation(mutation, gfMap):
        gfList = gfMap.get(mutation.get_gene(), ['?'])
        extraMutations = []
        for gf in gfList[1:]:
            # make repeat mutations for additional gene families
            m = copy.deepcopy(mutation)
            m.add_feature("GENE_FAMILY", gf)
            extraMutations.append(m)
        # assign first gene family to mutation passed in
        mutation.add_feature("GENE_FAMILY", gfList[0])
        # returns extra mutations (when mutation has more than one gene family) to be added to mutations
        return extraMutations

    @staticmethod
    # MAF stands for minor allele frequency
    def addAlleleFreqToMutation(mutation, snpMap):
        mutation.add_feature("ALLELE_FREQUENCY", snpMap.get(mutation.get_rs_number(), (-1, -1, "?"))[2])
        return True

    @staticmethod
    def addPhastConsToMutation(mutation, pcMap):
        mutation.add_feature("PHAST_CONS", pcMap.get(mutation.get_rs_number(), "?"))
        return True


    def populateWekaData(self, loadFromCloud=False):
        for feature in self.__wekaData.getFeatures():
            if loadFromCloud:
                try:
                    os.remove(feature.get_fileName())
                    Log.debug("Deleting %s to re-download data" % (feature.get_fileName()))
                except: pass

        # populate feature data
        for feature in self.__wekaData.getFeatures():
            Log.info("Gathering %s data for %d mutations" % (feature.get_name(), len(self.__wekaData.getMutations())))
            dataMap = DataBridge.DataBridge.loadMap(feature, self.__wekaData.getMutations())
            
            addFeature = Wrangler.dispatcher[feature.get_name()]
            mutationsToAdd = []
            for m in self.__wekaData.getMutations():
                potentialExtraMutations = addFeature(m, dataMap)
                if type(potentialExtraMutations) is list:
                    mutationsToAdd.extend(potentialExtraMutations)
                # else should be True (fr
                else:
                    assert type(potentialExtraMutations) == bool
            self.__wekaData.addMutations(mutationsToAdd)

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