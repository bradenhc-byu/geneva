import sys
#######
#aaindex2parser.py old new group
#
#Where old is the old acid, new is what the acid changed into.
#Group is what group you want (0-99)
######

old=int(sys.argv[1]) # eg 0
new=int(sys.argv[2]) # eg 1
group=int(sys.argv[3]) # eg 4

#print( old )
#print( new )
#print( group )
#######
acid_abbreviations = "ARNDCQEGHILKMFPSTWYV*"
min=min(old,new)
max=max(old,new)
group_counter=-1
row_counter=0;
with open("C:\\aaindex2") as f:
    for line in f:
        #print(line)
        if group_counter == group:
            #print(line)
            if row_counter == max:
                #print(line)
                items = line.split("    ")
                print(items[min+1].strip())
            row_counter = row_counter + 1
        if "M rows = ARNDCQEGHILKMFPSTWYV" in line:
            group_counter = group_counter + 1
        