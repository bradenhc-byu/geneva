#To reduce the features
#java -cp ./weka.jar weka.filters.supervised.attribute.AttributeSelection -E "weka.attributeSelection.CfsSubsetEval -M" -S "weka.attributeSelection.BestFirst -D 1 -N 5" -i data/soybean.arff -o data/soybean2.arff

# To run the tests

# java -cp ./weka.jar weka.classifiers.rules.ZeroR -t "data/weather.nominal.arff" -v | grep "Correctly"

# and it will get you back "Correctly Classified Instances <tab> 9 <tab> 99%"
# or try findstr if grep does not work
#
import Logger as Log
from Definitions import DATA_DIR, ROOT_DIR
import Configuration
import os


def run_weka(weka_data, weka_file):
    filepath = DATA_DIR + weka_file
    if os.path.exists(filepath):
        Log.info("Pushing data to weka...")
        results_file = open(DATA_DIR + "weka_results.txt", "w")
        results_file.write("WEKA RESULTS ================================\n\n")
        # Run the specified algorithms on the data and get the results
        # We write the output to a temporary file, from which we print the
        # results
        classifier_algorithms = weka_data.getAlgorithms()
        if classifier_algorithms:
            for algorithm in classifier_algorithms:
                Log.info("Running " + algorithm + "...")
                results_file.write(algorithm + "--------------\n")
                tmp_output = "./tmp_output"
                command = build_command(algorithm, filepath, tmp_output)
                if command is None:
                    return False
                os.system(command)
                with open(tmp_output, "r") as tmp_output_file:
                    for tmp_result_line in tmp_output_file:
                        results_file.write(tmp_result_line.rstrip() + "\n")

        else:
            Log.error("Unable to run weka: no specified algorithms")
    else:
        Log.error("Unable to run weka: file'" + filepath + "' does not exist")
    return True


def build_command(algorithm, weka_file, result_file="./tmp_output"):
    weka_path = Configuration.getConfig("weka_path")
    if weka_path is None:
        Log.error("Unable to build Weka command: weka path not set")
        return None
    return "java -cp {0} {1} -t {2} -v | grep Correctly > " \
           "{3}".format(weka_path, algorithm, weka_file, result_file)




################################################################################
# UNIT TESTING
#
from Collections import WekaData
import Initializer

def unit_test():
    weka_file = "genevia_default.arff"
    weka_data = WekaData()
    Initializer.init_weka_data(weka_data, filename=weka_file)

if __name__ == "__main__":
    Configuration.init("genevia.config")
    unit_test()

