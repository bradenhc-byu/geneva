#############################
# Wrangler class
#
# Takes WekaData and populates desired features for each mutation
# Gets feature values from data maps after calling the parser for the appropriate files, if they exist
# If file does not exist, it fetches and saves the needed data first
#
# Returns populated WekaData object

from Definitions import DATA_DIR

def Wrangler:
    def __init__(self, wekaData):
        self.__wekaData = wekaData

    def addXToMutation(mutation):
        return False

    def addYToMutation(mutation):
        return False

    # dict of feature type to function
    dispatcher = {
        "x" : addXToMutation(),
        "y" : addYToMutation()
    }

    def populateWekaData(self):
        for f in self.wekaData.getFeatures():
            addFeature = dispatcher(f)
            for m in self.wekaData.getMutations():
                addFeature(m)
