################################################################################
# Initializer - Class
#
# Controls the initialization of the WekaData object used in the system.
#
import os


from Collections import WekaData,Mutation


# ------------------------------------------------------------------------------
# Initializes a WekaData object with the names of mutations to be used in this
# session of the program
#
def initWekaData(filename):
    if os.path.exists(filename):
        data = WekaData()
        with open(filename,"r") as mutationFile:
            for line in mutationFile:
                data = line.strip().split()

                mutation = Mutation()
                data.addMutation(mutation)
            file.close()
        return data
    else:
        return None


