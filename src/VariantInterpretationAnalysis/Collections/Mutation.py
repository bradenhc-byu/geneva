################################################################################
# Mutation - Data Structure
#
# Holds key,value pairs for features associated with this mutation
#


class Mutation:

    def __init__(self, name):
        self.__name = name
        self.__features = dict()

    def addFeature(self,feature,value):
        self.__features[feature] = value

    def getFeature(self,feature):
        if feature in self.__features.keys():
            return self.__features[feature]
        else:
            return None