################################################################################
# Project Definitions
#
#
import os


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

MUTATION_SYMBOLS_2_3 = [
Ala     A       Alanine
        Arg     R       Arginine
        Asn     N       Asparagine
        Asp     D       Aspartic acid (Aspartate)
        Cys     C       Cysteine
        Gln     Q       Glutamine
        Glu     E       Glutamic acid (Glutamate)
        Gly     G       Glycine
        His     H       Histidine
        Ile     I       Isoleucine
        Leu     L       Leucine
        Lys     K       Lysine
        Met     M       Methionine
        Phe     F       Phenylalanine
        Pro     P       Proline
        Ser     S       Serine
        Thr     T       Threonine
        Trp     W       Tryptophan
        Tyr     Y       Tyrosine
        Val     V       Valine
        Asx     B       Aspartic acid or Asparagine
        Glx     Z       Glutamine or Glutamic acid.
        Xaa     X       Any amino acid.
        TERM            termination codon

]

MUTATION_SYMBOLS_3_2 = [

]
