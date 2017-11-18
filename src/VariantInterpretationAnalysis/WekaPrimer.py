################################################################################
# Weka Primer
#
# This module takes a fully populated WekaData object and writes it to a file
# that the Weka machine learning program can use
#
from Collections import WekaData, Mutation, Feature
from Definitions import DATA_DIR
import Logger as Log


def write_to_file(weka_data, out_filename):
    Log.info("Writing WekaData object to file in ARFF format")
    # Initialize the file
    out_file = open(out_filename, "w")

    # Write the relation
    relation = "@relation mutationvariants\n\n"
    out_file.write(relation)

    # Write the attributes
    for f in weka_data.getFeatures():
        out_file.write("@attribute " + f.name + " " + f.dataType + "\n")
    out_file.write("@attribute class {" + ",".join(Mutation.CLASSES) + "}\n")

    # Write the data
    out_file.writelines("\n@data\n")
    for mutation in weka_data.getMutations():
        data_line = []
        for key, value in mutation.get_features().iteritems():
            data_line.append(str(value))
        out_file.write(",".join(data_line) + "," +
                       mutation.get_clinical_significance() + "\n")

    Log.info("Write completed successfully!")
    return True


################################################################################
# Unit Testing
import random
def unit_test():
    Log.set_log_level("debug")
    data = WekaData()
    data.addFeature(Feature('feature_a'))
    data.addFeature(Feature('feature_b'))
    data.addFeature(Feature('feature_c'))
    data.addFeature(Feature('feature_d',dataType=Feature.STRING_TYPE))
    data.addFeature(Feature('feature_e'))
    data.addFeature(Feature('feature_f',dataType=Feature.STRING_TYPE))
    for i in range(10000):
        mutation_class = Mutation.BENIGN if random.random() > 0.5 else \
            Mutation.PATHOGENIC
        m = Mutation("Test", "RR", i + 1, "ABC", mutation_class, i * 2)
        m.add_feature('feature_a', random.random() * i * 3)
        m.add_feature('feature_b', random.random() * i * 4)
        m.add_feature('feature_c', random.random() * i * 5)
        m.add_feature('feature_d', "ab" * ((i + 1) % 6))
        m.add_feature('feature_e', random.random() * i * 7)
        m.add_feature('feature_f', 'HelloWorld!'[i%11:])
        data.addMutation(m)
    write_to_file(data, DATA_DIR + "test_weka_output.arff")
    return None

if __name__ == "__main__":
    unit_test()