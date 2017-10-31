################################################################################
#
#
#
#

# Import required files
from VariantInterpretationAnalysis.Initializer import Initializer
from VariantInterpretationAnalysis.Definitions import DATA_DIR

# Start program
mutationsFile = DATA_DIR + "mutations.txt"
wekaData = Initializer.initWekaData(mutationsFile)