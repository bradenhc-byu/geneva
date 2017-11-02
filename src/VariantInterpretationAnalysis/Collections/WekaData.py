################################################################################
# WekaData - Data Structure
#
# Contains a map of mutation objects that store information about features
# associated with each mutation
#
from VariantInterpretationAnalysis.Collections.Mutation import Mutation


class WekaData:

    def __init__(self):
        self.__mutations = dict()
        self.__features = list()
        self.__algorithms = list()

    def getMutation(self,mutation):
        if mutation in self.__mutations.keys():
            return self.__mutations[mutation]

    def getMutations(self):
        return self.__mutations

    def addMutation(self,mutation):
        if mutation in self.__mutations.keys():
            return False
        else:
            m = Mutation(mutation)
            self.__mutations[mutation] = m
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
