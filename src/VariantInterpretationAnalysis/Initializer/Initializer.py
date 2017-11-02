################################################################################
# Initializer - Class
#
# Controls the initialization of the WekaData object used in the system.
#
from VariantInterpretationAnalysis.Collections.WekaData import WekaData
from os import path


# ------------------------------------------------------------------------------
# Initializes a WekaData object with the names of mutations to be used in this
# session of the program
#
def initWekaData(filename):
    if path.exists(filename):
        data = WekaData()
        with open(filename,"r") as mutationFile:
            for line in mutationFile:
                mutation = line.rstrip()
                data.addMutation(mutation)
            file.close()
        return data
    else:
        return None
