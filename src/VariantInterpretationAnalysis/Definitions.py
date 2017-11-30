################################################################################
# Project Definitions
#
#
import os


# Root directory of the program
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory of the data path
DATA_DIR = os.path.join(ROOT_DIR, "data/")

# List of available features to plug into Weka
# Format is "<key>": (<name>, <filepath>, <weka data type>)
AVAILABLE_FEATURES = {
    "gene-family": ("GENE_FAMILY",
                    DATA_DIR + "geneFamilyData.txt",
                    "real")
}

# List of available algorithms to use in Weka
# Format is "<key>": "string java class object"
AVAILABLE_ALGORITHMS = {
    "random-tree": "weka.classifiers.trees.RandomTree",
    "bayes-net": "weka.classifiers.bayes.BayesNet",
    "bayes-naive": "weka.classifiers.bayes.NaiveBayes",
    "bayes-naive-multinomial": "weka.classifiers.bayes"
                               ".NaiveBayesMultinomialText",
    "bayes-naive-updateable": "weka.classifiers.bayes.NaiveBayesUpdateable",
    "logistic": "weka.classifiers.functions.Logistic",
    "multilayer-perceptron": "weka.classifiers.functions.MultilayerPerceptron",
    "sgd": "weka.classifiers.functions.SGD",
    "sgd-text": "weka.classifiers.functions.SGDText",
    "smo": "weka.classifiers.functions.SMO",
    "simple-logistic": "weka.classifiers.functions.SimpleLogistic",
    "voted-perceptron": "weka.classifiers.functions.VotedPerceptron",
    "ibk": "weka.classifiers.lazy.IBk",
    "kstar": "weka.classifiers.lazy.KStar",
    "lwl": "weka.classifiers.lazy.LWL",
    "ada-boost-m1": "weka.classifiers.meta.AdaBoostM1",
    "attribute-selected": "weka.classifiers.meta.AttributeSelectedClassifier",
    "bagging": "weka.classifiers.meta.Bagging",
    "cv-parameter-selection": "weka.classifiers.meta.CVParameterSelection",
    "filtered-classifier": "weka.classifiers.meta.FilteredClassifier",
    "iterative-classifier-optimizer": "weka.classifiers.meta"
                                      ".IterativeClassifierOptimizer",
    "logitboost": "weka.classifiers.meta.LogitBoost",
    "multiclass-classifier": "weka.classifiers.meta.MultiClassClassifier",
    "multi-scheme": "weka.classifiers.meta.MultiScheme",
    "random-committee": "weka.classifiers.meta.RandomCommittee",
    "random-subspace": "weka.classifiers.meta.RandomSubSpace",
    "randomizable-filtered-classifier": "weka.classifiers.meta"
                                        ".RandomizableFilteredClassifier",
    "stacking": "weka.classifiers.meta.Stacking",
    "vote": "weka.classifiers.meta.Vote",
    "weighted-instance-handler-wrapper": "weka.classifiers.meta"
                                         ".WeightedInstancesHandlerWrapper",
    "input-mapped-classifier": "weka.classifiers.misc.InputMappedClassifier",
    "decision-table": "weka.classifiers.rules.DecisionTable",
    "jrip": "weka.classifiers.rules.JRip",
    "oner": "weka.classifiers.rules.OneR",
    "part": "weka.classifiers.rules.PART",
    "zeror": "weka.classifiers.rules.ZeroR",
    "decision-stump": "weka.classifiers.trees.DecisionStump",
    "hoeffding-tree": "weka.classifiers.trees.HoeffdingTree",
    "j48": "weka.classifiers.trees.J48",
    "lmt": "weka.classifiers.trees.LMT",
    "reptree": "weka.classifiers.trees.REPTree",
    "random-forest": "weka.classifiers.trees.RandomForest"
}

# Dictionary of Amino Acid conversions: 1 letter abbreviation to 3 letter
AMINO_ACIDS_1_3 = {
    "A": "Ala",
    "R": "Arg",
    "N": "Asn",
    "D": "Asp",
    "C": "Cys",
    "Q": "Gln",
    "E": "Glu",
    "G": "Gly",
    "H": "His",
    "I": "Ile",
    "L": "Leu",
    "K": "Lys",
    "M": "Met",
    "F": "Phe",
    "P": "Pro",
    "S": "Ser",
    "T": "Thr",
    "W": "Trp",
    "Y": "Tyr",
    "V": "Val",
    "B": "Asx",
    "Z": "Glx",
    "X": "Xaa",
    "*": "Ter"
}

# Dictionary of amino acid conversions: 3 letter abbreviations to 1 letter
AMINO_ACIDS_3_1 = dict((v, k) for k, v in AMINO_ACIDS_1_3.iteritems())



