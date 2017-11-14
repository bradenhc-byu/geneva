################################################################################
#
# Parser for mutation information obtained via
#
import os
import re
from VariantInterpretationAnalysis.Collections import Mutation


# ------------------------------------------------------------------------------
#
def parse_mutation(line):
    """
    Parses a line of a file containing pre-formatted mutation information

    :param line: The line to parse
    :return: A mutation object constructed from the parsed information
    """
    data = line.strip().split()
    name = data[0]
    symbol = data[1]
    index = int(data[2])
    gene = data[3]
    sig_string = ' '.join(data[5:])
    if sig_string.find("benign") != -1:
        significance = Mutation.BENIGN
    elif sig_string.find("pathogenic") != -1:
        significance = Mutation.PATHOGENIC
    elif sig_string.find("conflict") != -1:
        significance = Mutation.CONFLICTING
    elif sig_string.find("risk") != -1:
        significance = Mutation.RISK
    else:
        significance = Mutation.UNKNOWN

    rs_num = int(data[4])

    # Create the mutation
    m = Mutation(name, symbol, index, gene, significance, rs_num)

    return m


# ------------------------------------------------------------------------------
# Pre-parser
#
def pre_parse(infile, outfile, use_all=False):
    """
    Takes a file formated as clinical variants and parses it, writing it to a
    file to be extracted later

    :param infile: The location and name of the file to read cleaned variant
                   data from
    :param outfile: The location and name of the file to write the newly
                    formatted mutation data to
    :param use_all: Default is false. If true, included all data regardless
                    of clinical significance. If false, only use ones classified
                    as 'benign' or 'pathogenic'
    """
    if os.path.exists(infile):
        output_file = open(outfile, "w")
        with open(infile, "r") as input_file:
            input_file.readline()
            for line in input_file:
                # Get the parts
                data = line.strip().split()

                # Get the mutation name
                name = data[0]

                # Get the mutation symbol and index
                pattern_symbol = re.compile("[a-zA-z][a-zA-Z][a-zA-Z]")
                symbol = ''.join(pattern_symbol.findall(data[1]))
                pattern_index = re.compile("[0-9]+")
                matches = pattern_index.findall(data[1])
                if matches:
                    index = int(matches[0])
                else:
                    index = -1

                # Get the gene
                gene = data[2]

                # Get the clinical significance
                significance = ' '.join(data[3:-1]).lower()
                if not use_all \
                    and (significance.find("conflicting") != -1
                         or (significance.find("pathogenic") == -1
                             and significance.find("benign") == -1)):
                    return None

                # Get the dbSNP number
                rs_num = int(data[-1])

                # Create the mutation
                m = Mutation(name, symbol, index, gene, significance, rs_num)

                output_file.write(str(m) + "\n")

            input_file.close()
        output_file.close()
