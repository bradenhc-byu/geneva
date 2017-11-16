################################################################################
#
# Parser for mutation information obtained via
#
import os
import re
from VariantInterpretationAnalysis.Definitions import DATA_DIR
from VariantInterpretationAnalysis.Collections import Mutation
from VariantInterpretationAnalysis.Definitions import AMINO_ACIDS_1_3
import VariantInterpretationAnalysis.Logger as Logger


# ------------------------------------------------------------------------------
#
def parse_mutation(line):
    """
    Parses a line of a file containing pre-formatted mutation information

    :param line: The line to parse
    :return: A mutation object constructed from the parsed information
    """
    data = line.strip().split("\t")
    name = data[0]
    symbol = data[1]
    index = int(data[2])
    gene = data[3]
    rs_num = int(data[4])
    significance = int(data[5])

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
        with open(infile, "r") as input_file:
            parsed_mutations = dict()
            input_file.readline()
            Logger.info("Starting parser")
            for line in input_file:
                # Get the parts
                data = line.strip().split()

                # Get the mutation name
                name = data[0]

                # Get the mutation symbol and index
                pattern_symbol = re.compile("[a-zA-z][a-zA-Z][a-zA-Z]")
                symbol = ''.join(pattern_symbol.findall(data[1]))
                if not symbol:
                    # Try the single letter abbreviation
                    pattern_symbol = re.compile("[a-zA-z]+")
                    symbol = ''.join(pattern_symbol.findall(data[1])[1:])
                    if not symbol or len(symbol) < 2:
                        continue
                    symbol = AMINO_ACIDS_1_3[symbol[0]] + \
                             AMINO_ACIDS_1_3[symbol[1]]
                if len(symbol) < 6:
                    continue
                pattern_index = re.compile("[0-9]+")
                matches = pattern_index.findall(data[1])
                if matches:
                    index = int(matches[0])
                else:
                    index = -1

                # Get the gene
                gene = data[2]

                # Get the clinical significance
                sig_string = ' '.join(data[3:-1]).lower()
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

                if not use_all \
                    and (significance == Mutation.CONFLICTING
                         or significance == Mutation.RISK
                         or significance == Mutation.UNKNOWN):
                    continue

                # Get the dbSNP number
                rs_num = int(data[-1])

                if rs_num in parsed_mutations.keys():
                    if parsed_mutations[rs_num][-1] != significance:
                        parsed_mutations.pop(rs_num, None)
                    continue

                parsed_mutations[rs_num] = [name, symbol, index, gene, rs_num,
                                            significance]

            input_file.close()
        output_file = open(outfile, "w")
        Logger.info("Writing formatted data to file")
        for key in parsed_mutations.keys():
            m = parsed_mutations[key]
            line = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(m[0],
                                                           m[1],
                                                           m[2],
                                                           m[3],
                                                           m[4],
                                                           m[5])
            output_file.write(line)
        output_file.close()
    else:
        print Logger.error("Unable to open file")


def main():
    in_file = DATA_DIR + "cleaned_variants"
    out_file = DATA_DIR + "mutations_certain"
    print "Input file:", in_file
    print "Output file:", out_file
    pre_parse(in_file, out_file)


if __name__ == "__main__":
    main()
