################################################################################
# Gene Variant Interpretation Analysis
#
# Main python file that runs the VIA gui and event loop. This is where all the
# magic starts.
#

# Import required files
from VariantInterpretationAnalysis import Initializer
from VariantInterpretationAnalysis.Definitions import *


def run(argv):

    # Instantiate variables
    features = DEFAULT_FEATURES
    algorithms = DEFAULT_ALGORITHMS
    testMutation = ""
    loadFromCloud = False

    # Parse the arguments if there are any
    if argv:
        for i in range(len(argv)):
            if argv[i] == "-a":
                algorithms = argv[i+1].split(",")
                i += 1

            elif argv[i] == "-f":
                features = argv[i+1].split(",")
                i += 1

            elif argv[i] == "-m":
                testMutation = argv[i+1]
                i += 1

            elif argv[i] == "-l":
                loadFromCloud = True

    # Initialize the Weka Data
    mutationsFile = DATA_DIR + "mutations.txt"
    wekaData = Initializer.initWekaData(mutationsFile)
    for f in features:
        if f in AVAILABLE_FEATURES:
            wekaData.addFeature(f)
        else:
            print "Found unknown feature '" + f + "': excluding"

    for a in algorithms:
        if a in AVAILABLE_ALGORITHMS:
            wekaData.addAlgorithm(a)
        else:
            print "Found unknown algorithm '" + a + ""

    # Pass things off to the wrangler

    # Now have the WekaPrimer write the appropriate files

    # Pass things off to weka using the weka CLI

    # Get our return value


def printHelp():
    print """
      
    COMMANDS:-------------------------------------------------------------------
    
    run [-a] [-f] [-m] [-l] := Execute the program using the provided 
                               arguments
    
        -a algorithm
           Comma separated list of different Weka algorithms to run.
           Valid algorithms are:
               x
               y
               z
        
        -f features
           Comma separated list of features you want to use in training Weka.
           Valid features are:
               x
               y
               z
               
        -m mutation
           Determine the condition of the mutation based on the provided 
           features and Weka machine learning
           
        -l load
           Load new data from the cloud about features (default is to use 
           cached data if available) 
           
    ----------------------------------------------------------------------------
    
    help := display this help message
    
    ----------------------------------------------------------------------------
    
    exit := exit the program
    
    """


# Start program ----------------------------------------------------------------
# All this will be happening inside a terminal like event loop
while True:

    # Get the user inputted command
    command = raw_input("VIA >> ")
    argv = command.split()

    if argv[0] == "exit":
        break

    elif argv[0] == "run":
        run(argv[1:])

    elif argv[0] == "help":
        printHelp()

    else:
        print "Invalid command option, enter 'help' for a list of available" \
              "command options"
