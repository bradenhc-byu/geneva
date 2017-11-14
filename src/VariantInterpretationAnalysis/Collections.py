################################################################################
# Mutation - Data Structure
#
# Holds key,value pairs for features associated with this mutation
#


class Mutation:

    # Constants to define classifications of mutations
    PATHOGENIC = 1
    BENIGN = 2
    CONFLICTING = 3
    RISK = 4
    UNKNOWN = 5

    def __init__(self, name, symbol="", index=-1, gene="NONE",
                 clinical_significance="",
                 rs_num=-1):
        """
        Represents data about a gene mutation from the cleaned_variants file

        :param name: The name containing additional information about the
                     mutation
        :param symbol: The three-character representation of the amino acid
                       mutation
        :param index: The position at which the mutation takes place in the
                      sequence
        :param gene: The name of the gene in which the mutation was found
        :param clinical_significance: Usually 'pathogenic' or 'benign'
        :param rs_num: The unique identifier of the mutation in the dbSNP
        """
        self.__name = name
        self.__symbol = symbol
        self.__index = index
        self.__gene = gene
        self.__clinical_sig = clinical_significance
        self.__rs_num = rs_num
        self.__features = dict()

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_symbol(self, two=False):
        if two:
            return self.__symbol
        else:
            return self.__symbol

    def get_index(self):
        return self.__index

    def get_gene(self):
        return self.__gene

    def get_clinical_significance(self):
        return self.__clinical_sig

    def get_rs_number(self):
        return self.__rs_num

    def get_features(self):
        return self.__features

    def add_feature(self, feature,value):
        self.__features[feature] = value
        return True

    def get_feature(self, feature):
        if feature in self.__features.keys():
            return self.__features[feature]
        else:
            return None

    def __str__(self):
        out_string = str(self.__name) + "\t" + \
                     str(self.__symbol) + "\t" + \
                     str(self.__index) + "\t" + \
                     str(self.__gene) + "\t" + \
                     str(self.__rs_num) + "\t" + \
                     str(self.__clinical_sig)

        return out_string


################################################################################
# Feature
#
# Contains feature name, location of source data
# Used for storing non-default features
class Feature:
    def __init__(self, name, fileName = "DEFAULT"):
        if fileName == "DEFAULT":
            fileName = name + '.txt'

        self.name = name
        self.fileName = fileName



################################################################################
# WekaData - Data Structure
#
# Contains a map of mutation objects that store information about features
# associated with each mutation
#


class WekaData:

    def __init__(self):
        self.__mutations = dict()
        self.__defaultFeatures = list()
        self.__defaultFeatureMap = {}
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
            self.__mutations[mutation.getId()] = mutation
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
