import os
your_path = 'knapsack-master/binpackdata/test'

def computeBinPack(weights, capacity):
    print(weights)
    print(capacity)

files = os.listdir(your_path)

for file in files:
    if os.path.isfile(os.path.join(your_path, file)):
        a_file = open(os.path.join(your_path, file),'r')
        #print("FileName is {}".format(file))
        #print(file)
        line_list =[]
        cnt=0
        for line in a_file:
            cnt=cnt+1
            if cnt > 2:
                stripped_line = line.strip()
                line_list.append(int(stripped_line))
        #print(line_list)
        if file[3]=='1':
            capac =100
        elif file[3]=='2':
            capac =120
        elif file[3]=='3':
            capac=150
        print("{}|{}|{}|{}".format(file,file[3],capac,len(line_list)))
        computeBinPack(line_list,capac)
        a_file.close()



