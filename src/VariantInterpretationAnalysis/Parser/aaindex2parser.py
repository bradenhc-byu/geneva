import sys
sys.path.append('../..')
from VariantInterpretationAnalysis.Definitions import DATA_DIR
#######
#aaindex2parser.py old new group
#
#Where old is the old acid, new is what the acid changed into.
#Group is what group you want (0-99)
######

#static String[] amnio_acids = {"Ala", "Arg", "Asn", "Asp", "Cys", "Gln", "Glu", "Gly", "His", "Ile", "Leu", "Lys", "Met", "Phe", "Pro", "Ser", "Thr", "Trp", "Tyr", "Val", "Ter"};
#static String acid_abbreviations = "ARNDCQEGHILKMFPSTWYV*";

#old,new,and group are 0 indexed
acid_abr = "ARNDCQEGHILKMFPSTWYV*"

old=int(acid_abr.index(sys.argv[1]))
new=int(acid_abr.index(sys.argv[2]))
#group=int(acid_abr.index(sys.argv[3]))
#old=int(sys.argv[1]) # eg 0
#new=int(sys.argv[2]) # eg 1
group=int(sys.argv[3]) # eg 4

#print( old )
#print( new )
#print( group )
#######
min=min(old,new)
max=max(old,new)
group_counter=-1
row_counter=0
with open(DATA_DIR+"aaindex2") as f:
    for line in f:
        #print(line)
        if group_counter > -1:
            #print(line)
            if row_counter == max:
                #print(line)
                items = line.split("    ")
                print(items[min+1].strip())
            row_counter = row_counter + 1
        if "M rows = ARNDCQEGHILKMFPSTWYV" in line:
            group_counter = group_counter + 1
            row_counter = 0

#with open(DATA_DIR+"aaindex2") as f:
#    for line in f:
#        #print(line)
##        if group_counter == group:
#           #print(line)
#            if row_counter == max:
#                #print(line)
#                items = line.split("    ")
#                print(items[min+1].strip())
#            row_counter = row_counter + 1
#        if "M rows = ARNDCQEGHILKMFPSTWYV" in line:
#            group_counter = group_counter + 1
#            row_counter = 0
        