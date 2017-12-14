"""
WekaPrimer Module

This module takes a fully populated WekaData object and writes it to a file
that the Weka machine learning program can use
"""
from Collections import WekaData, Mutation, Feature
from Definitions import DATA_DIR
import Logger as Log


def write_to_file(weka_data, out_filename):
    """
    Takes a populated WekaData object and writes the contents to a file in
    ARFF format. This is the file format used by Weka when using machine
    learning.

    :param weka_data: A fully populated WekaData object
    :param out_filename: The name of the ARFF file to write to
    :return: True on success, False otherwise
    """
    Log.info("Writing WekaData object to file in ARFF format")
    # Initialize the file
    out_file = open(DATA_DIR + out_filename, "w")

    # Write the relation
    relation = "@relation mutationvariants\n\n"
    out_file.write(relation)

    # Write the attributes
    for f in weka_data.getDefaultFeatures():
        out_file.write("@attribute " + f + " " + "real" + "\n")
    for f in weka_data.getFeatures():
        out_file.write("@attribute " + f.get_name() + " " + f.get_datatype() +
                       "\n")
    out_file.write("@attribute class {" + ",".join(Mutation.CLASSES) + "}\n")

    # Write the data
    out_file.writelines("\n@data\n")
    for mutation in weka_data.getMutations():
        data_line = []
        for feature in weka_data.getDefaultFeatures():
            value = mutation.get_feature(feature)
            if value is None or value == "?":
                value = "0"
            data_line.append(str(value))
        for feature in weka_data.getFeatures():
            value = mutation.get_feature(feature.get_name())
            if value is None:
                value = "0" if feature.get_datatype() == Feature.NUMERIC_TYPE \
                    else "?"
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
        m.add_feature('feature_d', "ab" * ((i % 6) + 1))
        m.add_feature('feature_e', random.random() * i * 7)
        m.add_feature('feature_f', 'NM_' + 'HelloWorld!'[i%10:])
        data.addMutation(m)
    write_to_file(data, DATA_DIR + "test_weka_output.arff")
    return None

if __name__ == "__main__":
    unit_test()