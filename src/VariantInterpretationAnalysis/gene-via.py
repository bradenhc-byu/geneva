################################################################################
# Gene Variant Interpretation Analysis
#
# Main python file that runs the VIA gui and event loop. This is where all the
# magic starts.
#

# Import required files
from VariantInterpretationAnalysis.Initializer import Initializer
from VariantInterpretationAnalysis.Definitions import DATA_DIR

# Start program
mutationsFile = DATA_DIR + "mutations.txt"
wekaData = Initializer.initWekaData(mutationsFile)