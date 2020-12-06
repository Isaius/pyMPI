import numpy as np
from mpi4py import MPI
import random
import timeit

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
LENGTH = 10

if(rank == 0):
    array = np.linspace(1, size*LENGTH, size*LENGTH)
    random.shuffle(array)
else:
    array = None

start = timeit.default_timer()

local_array = np.zeros(LENGTH)
comm.Scatter(array, local_array, root=0)

# array to put the numbers in the right places, fill with 0 as blank spaces
ordened = np.zeros(size*LENGTH)

# sorting the local array by placind the number in the equivalent index
for i in local_array:
    ordened[i-1] = i

if rank == 0:
    # pre acolating the final array
    sorted_array = np.zeros(size*LENGTH)
    
    # joining the rank0 part to the result
    for i in list(ordened):
        if i != 0:
            sorted_array[i-1] = i

    # receiving the result from another process
    for i in range(1, size):
        rcvbuffer = np.zeros(size*LENGTH)
        comm.Recv(rcvbuffer, MPI.ANY_SOURCE)
        
        # joining the array to the solution
        for i in list(rcvbuffer):
            if i != 0:
                sorted_array[i-1] = i
    
    end = timeit.default_timer()
    
    if len(sorted_array) > 750:
        # printing the first 40 items
        print(sorted_array[:40])
        # printing the last 60 items
        print(sorted_array[len(sorted_array)-60:])
    else:
        print(sorted_array)
    
    print("Took {}s in parallel".format(end - start))

    start = timeit.default_timer()
    array.sort()
    end = timeit.default_timer()
    print("Took {}s in serial".format(end - start))

else:    
    comm.Send(ordened)