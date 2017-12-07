################################################################################
# Gene Variant Interpretation Analysis
#
# Main python file that runs the VIA gui and event loop. This is where all the
# magic starts.
#

# Import the required files
import VariantInterpretationAnalysis.CommandLine as cmd
import VariantInterpretationAnalysis.Logger as Log
from VariantInterpretationAnalysis.Definitions import *
from VariantInterpretationAnalysis.Collections import WekaData, Feature
# Import the components/classes
from VariantInterpretationAnalysis import Initializer
from VariantInterpretationAnalysis import Wrangler
from VariantInterpretationAnalysis import WekaPrimer
from VariantInterpretationAnalysis import WekaController
from VariantInterpretationAnalysis import Configuration


class GeneVIA(cmd.Cmd):
    """
    This class inherits from the cmd module, which makes it easy to execute
    commands from a simple bash shell prompt.
    """

    prompt = "VIA>> "

    def do_run(self, line):
        """
        \rrun [-a <agorithms>] [-f <features>] [-m <mutation>] [-s <file>] [-l] [-d]
        \r
        \r:= Use the Weka machine learning tool to analyze mutation feature
        \r   using the provided arguments
        \r
        \r-a algorithm
        \r   Comma separated list of different Weka algorithms to run.
        \r
        \r-f features
        \r   Comma separated list of features you want to use in training Weka.
        \r       
        \r-m mutation [currently not implemented]
        \r   Determine the condition of the mutation based on the provided 
        \r   features and Weka machine learning
        \r   
        \r-l load
        \r   Load new data from the cloud about features (default is to use 
        \r   cached data if available)
        \r
        \r-s save
        \r   Name of the file to save the ARFF formatted data to before executing
        \r   Weka. The default value is 'genevia_default.arff'
        """

        argv = line.split()

        # Instantiate variables
        features = AVAILABLE_FEATURES.keys()
        algorithms = AVAILABLE_ALGORITHMS.keys()
        testMutation = ""
        loadFromCloud = False
        saveFile = "genevia_default.arff"

        # Parse the arguments if there are any
        try:
            if argv:
                for i in range(len(argv)):
                    if argv[i] == "-a":
                        algorithms = argv[i + 1].split(",")
                        i += 1

                    elif argv[i] == "-f":
                        features = argv[i + 1].split(",")
                        i += 1

                    elif argv[i] == "-m":
                        testMutation = argv[i + 1]
                        i += 1

                    elif argv[i] == "-l":
                        loadFromCloud = True
                        i += 1

                    elif argv[i] == "-s":
                        saveFile = argv[i + 1]
                        i += 1

        except:
            Log.error("Unable to execute incorrectly formatted command")
            return False

        # Initialize the Weka Data
        wekaData = WekaData()
        Initializer.init_weka_data(wekaData)

        for f in features:
            if f in AVAILABLE_FEATURES.keys():
                f_args = AVAILABLE_FEATURES[f]
                f_obj = Feature(f_args[0], f_args[1], f_args[2])
                wekaData.addFeature(f_obj)
            else:
                Log.info("Found unknown feature '" + f + "': excluding")

        for a in algorithms:
            if a in AVAILABLE_ALGORITHMS.keys():
                wekaData.addAlgorithm(AVAILABLE_ALGORITHMS[a])
            else:
                Log.info("Found unknown algorithm '" + a + "': excluding")

        # Pass things off to the wrangler
        w = Wrangler.Wrangler(wekaData)
        w.populateWekaData(loadFromCloud)

        # Now have the WekaPrimer write the appropriate files
        WekaPrimer.write_to_file(wekaData, saveFile)

        # Pass things off to weka using the weka CLI
        WekaController.run_weka(wekaData, saveFile)

        # Get our return value
        result_filename = DATA_DIR + "weka_results.txt"
        with open(result_filename, "r") as result_file:
            for line in result_file:
                print line.rstrip()

    def complete_run(self, text, line, begidx, endidx):
        if begidx > 2:
            # Auto complete for algorithms
            if line.find("-a") != -1 and \
                (line.find("-a") > line.find("-f")
                and line.find("-a") > line.find("-l")
                and line.find("-a") > line.find("-d"))\
                and line.find("-a") > line.find("-m"):
                    if not text:
                        return AVAILABLE_ALGORITHMS.keys()[:]
                    return [a for a in AVAILABLE_ALGORITHMS.keys()
                            if a.startswith(text)]

            # Auto complete for features
            if line.find("-f") != -1 and \
                (line.find("-f") > line.find("-a")
                and line.find("-f") > line.find("-l")
                and line.find("-f") > line.find("-d"))\
                and line.find("-f") > line.find("-m"):
                    if not text:
                        return AVAILABLE_FEATURES.keys()[:]
                    return [f for f in AVAILABLE_FEATURES.keys()
                            if f.startswith(text)]
        return []


    def do_log(self, line):
        """
        \rlog := Change log settings for the running application. Available commands
        \r       are as follows:
           
        \r  Enable log:       log enable
        \r  Disable log:      log disable
        \r  Change log level: log set level [debug, info, warn, error]
        \r  Change output:    log set output [stdout, file]
        \r  Change log file:  log set file <filename.log>
        """
        argv = line.split()
        command = argv[0]

        if command == "set":
            option = argv[1]
            if option == "level":
                Log.set_log_level(argv[2].lower())
            elif option == "output":
                Log.set_destination(argv[2].lower())
            elif option == "file":
                Log.set_file(argv[2].lower())

        if command == "enable":
            Log.enable()

        elif command == "disable":
            Log.disable()

    def complete_log(self, text, line, begidx, endidx):
        if begidx == 4:
            options = ["enable", "disable", "set"]
            if endidx == 4:
                return options
            return [o for o in options if o.startswith(text)]
        if line.find("enable") != -1 or line.find("disable") != -1:
            return []
        if line.find("set") != -1:
            if line.find("level") != -1 \
            and line.find("level") > line.find("set"):
                level_options = ["debug", "info", "warn", "error"]
                if not text:
                    return level_options
                return [o for o in level_options if o.startswith(text)]
            if line.find("output") != -1 \
            and line.find("output") > line.find("set"):
                file_options = ["stdout", "file"]
                if not text:
                    return file_options
                return [o for o in file_options if o.startswith(text)]
            set_options = ["level", "output", "file"]
            if not text:
                return set_options
            return [o for o in set_options if o.startswith(text)]
        return []

    def do_exit(self, line):
        """
        \rexit := exit the program
        """
        return True

# Start program ----------------------------------------------------------------
# All this will be happening inside a terminal like event loop


if __name__ == "__main__":

    # Initialize configuration
    Configuration.init("genevia.config")

    # Start the command prompt
    GeneVIA().cmdloop("Welcome to the Gene Variant Interpretation Analyzer")



