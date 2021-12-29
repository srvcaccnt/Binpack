import os
from datetime import datetime

def get_indices(name):
    return [int(digs) for digs in name.split('_') if digs.isdigit()]

def gettime():
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d %H%M%S")
    dt_string = dt_string + " " +str(now.microsecond) 
    return dt_string

def computeBinPack(inputfileName,weights, bin_capacity):
    #print(weights)
    #print(bin_capacity)
    #print(inputfileName)
    timelimit=5 
    f=open("knapsack-master/binpackdata/results/test.txt","a")
    f.write(str(inputfileName))
    f.write("|")
    f.write(str(bin_capacity))
    f.write("|")
    f.write(str(weights))
    f.write("|")
    num_items=len(weights)

    f.write(str(num_items))
    f.write("|")
    f.write(str(sum(weights)))
    f.write("|")
    f.write(str(timelimit))
    f.write("|")
    
    from dimod import ConstrainedQuadraticModel
    cqm = ConstrainedQuadraticModel()
    from dimod import Binary
    bin_used = [Binary(f'bin_used_{j}') for j in range(num_items)]
    cqm.set_objective(sum(bin_used))

    item_in_bin = [[Binary(f'item_{i}_in_bin_{j}') for j in range(num_items)]
        for i in range(num_items)]

    for i in range(num_items):
        one_bin_per_item = cqm.add_constraint(sum(item_in_bin[i]) == 1, label=f'item_placing_{i}')

    for j in range(num_items):
        bin_up_to_capacity = cqm.add_constraint(
            sum(weights[i] * item_in_bin[i][j] for i in range(num_items)) - bin_used[j] * bin_capacity <= 0,
            label=f'capacity_bin_{j}')

    len(cqm.variables)

    from dwave.system import LeapHybridCQMSampler
    sampler = LeapHybridCQMSampler() 
    f.write(gettime())
    f.write("|")
    sampleset = sampler.sample_cqm(cqm,
    time_limit=timelimit, label="SDK Examples - Bin Packing")  
    f.write(gettime())
    f.write("|")
    feasible_sampleset = sampleset.filter(lambda row: row.is_feasible)  
    
    if len(feasible_sampleset):      
        f.write("{} of {}|".format(
            len(feasible_sampleset), len(sampleset)))
        f.write("Start Test ".format(len(selected_bins)))
        iter=0
        for trial in feasible_sampleset:
            iter=iter+1
            sel_bins = [key for key, val in trial.sample.items() if 'bin_used' in key and val]
            f.write("{} bins in {}|".format(len(sel_bins),str(iter)))
        f.write("End Test|".format(len(sel_bins)))
        best = feasible_sampleset.first

    selected_bins = [key for key, val in best.sample.items() if 'bin_used' in key and val]   
    #print("{} bins are used.".format(len(selected_bins)))
    f.write("{} bins|".format(len(selected_bins)))

    for bin in selected_bins:                        
        in_bin = [key for key, val in best.sample.items() if
            "_in_bin" in key and
            get_indices(key)[1] == get_indices(bin)[0]
            and val]
        b = get_indices(in_bin[0])[1]
        w = [weights[get_indices(item)[0]] for item in in_bin]
        #print("Bin {} has weights {} for a total of {}.".format(b, w, sum(w)))
        f.write("{}:{}:{};".format(b, w, sum(w)))

    f.write("|")
    f.write("\n")    
    f.close()


your_path = 'knapsack-master/binpackdata/test'
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
        a_file.close()
        if file[3]=='1':
            capac =100
        elif file[3]=='2':
            capac =120
        elif file[3]=='3':
            capac=150
        else:
            capac=100
        print("{}|{}|{}|{}".format(file,file[3],capac,len(line_list)))
        computeBinPack(file,line_list,capac)
        



