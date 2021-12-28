import os
your_path = 'knapsack-master/binpackdata/bin1data'
files = os.listdir(your_path)

for file in files:
    if os.path.isfile(os.path.join(your_path, file)):
        a_file = open(os.path.join(your_path, file),'r')
        print("FileName is {}".format(file))
        line_list =[]
        for line in a_file:
            stripped_line = line.strip()
            line_list.append(int(stripped_line))
        print(line_list)
        print(len(line_list))
        a_file.close()

