################################################################################
# Mutation - Data Structure
#
# Holds key,value pairs for features associated with this mutation
#


class Mutation:

    def __init__(self, id, symbol="", index=-1, clinical_significance="",
                 rs_num=-1):
        self.__id = id
        self.__symbol = symbol
        self.__index = index
        self.__clinical_sig = clinical_significance
        self.__rs_num = rs_num
        self.__features = dict()

    def getId(self):
        return self.__id

    def getSymbol(self,three=False):
        if three:
            self.__symbol
        else:
            return

    def addFeature(self,feature,value):
        self.__features[feature] = value
        return True

    def getFeature(self,feature):
        if feature in self.__features.keys():
            return self.__features[feature]
        else:
            return None


################################################################################
# WekaData - Data Structure
#
# Contains a map of mutation objects that store information about features
# associated with each mutation
#


class WekaData:

    def __init__(self):
        self.__mutations = dict()
        self.__features = list()
        self.__algorithms = list()

    def getMutation(self,mutation):
        if mutation in self.__mutations.keys():
            return self.__mutations[mutation]

    def addMutation(self,mutation):
        if mutation in self.__mutations.keys():
            return False
        else:
            self.__mutations[mutation.getName()] = mutation
            return True

    def getFeatures(self):
        return self.__features

    def addFeature(self, feature):
        if feature not in self.__features:
            self.__features.append(feature)
            return True
        else:
            return False

    def getAlgorithms(self):
        return self.__algorithms

    def addAlgorithm(self, algorithm):
        if algorithm not in self.__algorithms:
            self.__algorithms.append(algorithm)
            return True
        else:
            return False
