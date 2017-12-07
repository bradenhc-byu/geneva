################################################################################
# Weka Controller Module
#
# Takes a fully populated WekaData object and the location of a fully populated
# ARFF file containing mutation information from the WekaData object
# and runs various machine learning algorithms on a filtered subset of the
# data to determine which features are most effective in correctly classifying
# mutation classifications.
#
import Logger as Log
from Definitions import DATA_DIR
import Configuration
import os
import platform


def run_weka(weka_data, weka_file):
    filepath = DATA_DIR + weka_file
    if os.path.exists(filepath):
        Log.info("Converting any strings to nominal values...")
        converted_weka_filepath = convert_arff_to_all_nominal(filepath)
        Log.info("Filtering mutation ARFF file...")
        filtered_weka_filepath = filter_mutations(converted_weka_filepath)
        
        
        # Run the specified algorithms on the data and get the results
        # We write the output to a temporary file, from which we print the
        # results
        classifier_algorithms = weka_data.getAlgorithms()
        results_file = open(DATA_DIR + "weka_results.txt", "w")
        results_file.write("WEKA RESULTS ================================\n\n")
        results_file.close()
        if classifier_algorithms:
            for algorithm in classifier_algorithms:
                results_file = open(DATA_DIR + "weka_results.txt", "a")
                Log.info("Running " + algorithm + "...")
                results_file.write(algorithm + "--------------\n")
                tmp_output = "./tmp_output"
                command = build_command(algorithm, filtered_weka_filepath,
                                        tmp_output)
                #print(command)
                if command is None:
                    return False
                os.system(command)
                with open(tmp_output, "r") as tmp_output_file:
                    for tmp_result_line in tmp_output_file:
                        results_file.write(tmp_result_line.rstrip() + "\n\n")
                        print(tmp_result_line.rstrip())
                results_file.close()

        else:
            Log.error("Unable to run weka: no specified algorithms")
            return False
        
    else:
        Log.error("Unable to run weka: file'" + filepath + "' does not exist")
        return False
    Log.debug("Removing temporary output file")
    try:
        os.remove(tmp_output)
    except OSError as e:
        Log.error("Failed with:", e.strerror)
        print Log.error("Error code:", e.code)
    return True

def convert_arff_to_all_nominal(weka_filepath):
    #weka_path = Configuration.getConfig("weka_path") #+ '"'
    weka_path = '"' + Configuration.getConfig("weka_path") + '"'
    converted_filepath = weka_filepath.replace(".arff", "_converted.arff")
    convert_command = "java -cp {0} " \
                      "weka.filters.unsupervised.attribute.StringToNominal " \
                      "-R first -i \"{1}\" -o \"{2}\"".format(weka_path,
                                                     weka_filepath,
                                                     converted_filepath)
    os.system(convert_command)
    return converted_filepath

def filter_mutations(weka_filepath):
    #weka_path = Configuration.getConfig("weka_path") #+ '"'
    weka_path = '"' + Configuration.getConfig("weka_path") + '"'
    filtered_weka_filepath = weka_filepath.replace(".arff","_filtered.arff")
    filter_command = "java -cp {0} " \
                     "weka.filters.supervised.attribute.AttributeSelection -E " \
                     "\"weka.attributeSelection.CfsSubsetEval -M\" -S " \
                     "\"weka.attributeSelection.BestFirst -P 95,96,97 -D 1 -N 5\" -i " \
                     "\"{1}\" -o \"{2}\"".format(weka_path,
                                         weka_filepath,
                                         filtered_weka_filepath)
    os.system(filter_command)
    return filtered_weka_filepath


def build_command(algorithm, weka_file, result_file="./tmp_output"):
    #weka_path = Configuration.getConfig("weka_path") #+ '"'
    weka_path = '"' + Configuration.getConfig("weka_path") + '"'
    grep_command = "grep" if platform.system().lower() != "windows" else \
        "findstr"
    if weka_path is None:
        Log.error("Unable to build Weka command: weka path not set")
        return None
    #return "java -Xms512m -Xmx1024m -cp {0} {1} -t \"{2}\" -v | findstr Correctly > " \
    return "java -Xms512m -Xmx1024m -cp {0} {1} -t \"{2}\" -v | {3} Correctly > " \
           "{4}".format(weka_path,
                        algorithm,
                        weka_file,
                        grep_command,
                        result_file)




################################################################################
# UNIT TESTING
#
from Collections import WekaData
import Initializer
import WekaPrimer
from Definitions import AVAILABLE_ALGORITHMS

def unit_test():
    weka_file = "genevia_default.arff"
    weka_data = WekaData()
    Initializer.init_weka_data(weka_data)
    for a in AVAILABLE_ALGORITHMS.keys():
        weka_data.addAlgorithm(AVAILABLE_ALGORITHMS[a])
    WekaPrimer.write_to_file(weka_data, weka_file)
    run_weka(weka_data, weka_file=weka_file)

if __name__ == "__main__":
    Configuration.init("genevia.config")
    unit_test()

