import numpy as np
num_items = 12
#item_weight_range = [1, 100]
#weights = list(np.random.randint(*item_weight_range, num_items))
weights = [99,99,96,96,92,92,91,88,87,86,85,76,74,72,69,67,67,62,61,56,52,51,49,46,44,42,40,40,33,33,30,30,29,28,28,27,25,24,23,22,21,20,17,14,13,11,10,7,7,3]
#bin_capacity = int(10 * np.mean(weights))
bin_capacity = 100
num_items = len(weights)

f=open("test.txt","a")

print("Problem: pack a total weight of {} into bins of capacity {} and total number of items {}.".format(sum(weights), bin_capacity,num_items)) 
f.write("Problem: pack a total weight of {} into bins of capacity {} and total number of items {}.|".format(sum(weights), bin_capacity,num_items))

from dimod import ConstrainedQuadraticModel
cqm = ConstrainedQuadraticModel()

from dimod import Binary
bin_used = [Binary(f'bin_used_{j}') for j in range(num_items)]

cqm.set_objective(sum(bin_used))

bin_used[0]
2*bin_used[0]
bin_used[0]*bin_used[1] 


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

sampleset = sampler.sample_cqm(cqm,
   time_limit=10, label="SDK Examples - Bin Packing")  
feasible_sampleset = sampleset.filter(lambda row: row.is_feasible)  
if len(feasible_sampleset):      
    best = feasible_sampleset.first
    print("{} feasible solutions of {}.".format(
       len(feasible_sampleset), len(sampleset)))
    f.write("{} feasible solutions of {}.|".format(
       len(feasible_sampleset), len(sampleset)))

selected_bins = [key for key, val in best.sample.items() if 'bin_used' in key and val]   
print("{} bins are used.".format(len(selected_bins)))
f.write("{} bins are used.|".format(len(selected_bins)))
def get_indices(name):
    return [int(digs) for digs in name.split('_') if digs.isdigit()]


for bin in selected_bins:                        
     in_bin = [key for key, val in best.sample.items() if
        "_in_bin" in key and
        get_indices(key)[1] == get_indices(bin)[0]
        and val]
     b = get_indices(in_bin[0])[1]
     w = [weights[get_indices(item)[0]] for item in in_bin]
     print("Bin {} has weights {} for a total of {}.".format(b, w, sum(w)))
     f.write("Bin {} has weights {} for a total of {}.".format(b, w, sum(w)))
     
f.write("\n")