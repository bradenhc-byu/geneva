import sys
import re
sys.path.append('../..')
from VariantInterpretationAnalysis.Definitions import DATA_DIR
#######
#aaindex2parser.py
######
map={}
acid_abr = "ARNDCQEGHILKMFPSTWYV*"
#######
group_counter=-1
row_counter=0
with open(DATA_DIR+"aaindex2") as f:
    for line in f:
        #print(line)
        if "M rows = " in line:
            start = line.index("M rows =")+9
            end = line.index(",")
            acid_abr = line[start:end]
            #print("THIS" + acid_abr)
            group_counter = group_counter + 1
            row_counter = 0
        if group_counter > -1:
            if re.search('[a-zA-Z#]', line) or line.strip() == "": 
                ## Contains uppercase letters
                continue
            #print(line)
            items = line.split()
            if len(items) < 2:
                continue
            #print("ROW "+line)
            for item in range(len(items)):
                if item == 0:
                    continue
                col = item-1
                #print(str(col)+" r:"+str(row_counter)+" g:"+str(group_counter))
                
                forward = str(group_counter)+""+acid_abr[col]+" "+acid_abr[row_counter]
                backward = str(group_counter)+""+acid_abr[row_counter]+" "+acid_abr[col]
                
                map[forward] = str(items[item].strip())
                map[backward] = str(items[item].strip())
                print(str(group_counter)+" "+forward+ ": "+str(items[item].strip()))
            row_counter = row_counter + 1