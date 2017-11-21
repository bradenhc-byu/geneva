################################################################################
# Project Definitions
#
#
import os
#from Collections import Feature


# Root directory of the program
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory of the data path
DATA_DIR = os.path.join(ROOT_DIR, "data/")

# List of available features to plug into Weka
AVAILABLE_FEATURES = [
    "GENE_FAMILY"
]
AVAILABLE_FEATURES_MAP = dict([
    ("GENE_FAMILY","geneFamilyData.txt")])


# List of default features the program will use if additional features aren't
#  specified
DEFAULT_FEATURES = [
    "GENE_FAMILY"
]

# List of available algorithms to use in Weka
AVAILABLE_ALGORITHMS = [
    "x",
    "y",
    "z"
]

# Default algorithms to use in Weka
DEFAULT_ALGORITHMS = []

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



