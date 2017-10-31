old=0
new=5
group=3

#######
acid_abbreviations = "ARNDCQEGHILKMFPSTWYV*"
min=min(old,new)
max=max(old,new)
group_counter=-1
row_counter=0;
with open("C:\\aaindex2") as f:
    for line in f:
        if group_counter == group:
            if row_counter == max:
                #print(line)
                items = line.split("    ")
                print(items[min+1].strip())
            row_counter = row_counter + 1
        if "M rows = ARNDCQEGHILKMFPSTWYV" in line:
            group_counter = group_counter + 1
        