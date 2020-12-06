import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
array = np.array([0,2,1,3,7,8,1,8,3,9,7,13,1,9,6,3792,613,79,8,37,13,82,193,391,283,6,1,83,716,3,78])
sorted_array = []

local_n = round(len(array)/size)
recv_buffer = np.zeros(local_n)
local_start = (rank-1)*local_n
local_end = local_start+local_n-1

subarray = np.array(array[local_start:local_end])
#subarray.sort()

if(rank == 0):
    print("rank: 0: array size: {} size: {} ".format(len(array), size))
    
    for i in range(1, size):
        comm.Recv(recv_buffer, MPI.ANY_SOURCE)
        sorted_array.append(recv_buffer)
        
    print(sorted_array)        
else:
    print("rank: {}: n: {} start: {} end: {}".format(rank, local_n, local_start, local_end))
    print(rank, subarray)
    comm.Send(subarray)