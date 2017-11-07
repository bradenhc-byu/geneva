################################################################################
# Project Definitions
#
#
import os

amnio_acids = {"Ala", "Arg", "Asn", "Asp", "Cys", "Gln", "Glu", "Gly", "His", "Ile", "Leu", "Lys", "Met", "Phe", "Pro", "Ser", "Thr", "Trp", "Tyr", "Val", "Ter"}
acid_abr = "ARNDCQEGHILKMFPSTWYV*"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(ROOT_DIR, "data/")

AVAILABLE_FEATURES = [
    "x",
    "y",
    "z"
]

DEFAULT_FEATURES = [
    "x",
    "y",
    "x"
]

AVAILABLE_ALGORITHMS = [
    "x",
    "y",
    "z"
]

DEFAULT_ALGORITHMS = AVAILABLE_ALGORITHMS


