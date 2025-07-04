from mpi4py import MPI
import itertools
import time 

# ---------- Configuration ----------
charset = "abc123def456"
password_length = 11
target_password = "face416c3df"

# ---------- MPI Setup ----------
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

total = len(charset) ** password_length
chunk_size = total // size
start = rank * chunk_size
end = total if rank == size - 1 else (rank + 1) * chunk_size

found_flag = 0
found_password = None
found_by_rank = -1

# ---------- Brute Force Function ----------
def attempt_passwords(start_index, end_index):
    index = 0
    check_interval = 1000
    start_time = time.time()

    for combo in itertools.product(charset, repeat=password_length):
        if index < start_index:
            index += 1
            continue
        if index >= end_index:
            break

        password = ''.join(combo)

        if password == target_password:
            return password

        # Show time every N steps
        if index % check_interval == 0:
            elapsed = time.time() - start_time
            print(f"[Rank {rank}]  Elapsed time: {elapsed:.2f}s — Checked {index - start_index} combinations", flush=True)

        index += 1

    return None

# ---------- Start ----------
start_time = time.time()
result = attempt_passwords(start, end)
end_time = time.time()

# If password is found
if result:
    found_flag = 1
    found_password = result
    found_by_rank = rank
    print(f"[Rank {rank}]  Found the password: '{found_password}' in {end_time - start_time:.2f} seconds", flush=True)

# ---------- Notify All ----------
# Allreduce to check if anyone found it
any_found = comm.allreduce(found_flag, op=MPI.SUM)

# Broadcast who found it and what password
found_password = comm.bcast(found_password if found_flag else None, root=rank if found_flag else 0)
found_by_rank = comm.bcast(found_by_rank if found_flag else None, root=rank if found_flag else 0)

comm.Barrier()

# ---------- Final Result ----------
# Step 1: Gather results from all processes
local_result = {
    'found_flag': found_flag,
    'found_password': found_password,
    'found_by_rank': rank if found_flag else -1,
    'time_taken': end_time - start_time
}

# Rank 0 gathers all results
all_results = comm.gather(local_result, root=0)

# Step 2: Rank 0 decides the final result
if rank == 0:
    final_found_flag = 0
    final_password = None
    found_by_rank = None
    time_taken = None

    for res in all_results:
        if res['found_flag'] == 1:
            final_found_flag = 1
            final_password = res['found_password']
            found_by_rank = res['found_by_rank']
            time_taken = res['time_taken']
            break  # stop after first match

else:
    final_found_flag = None
    final_password = None
    found_by_rank = None
    time_taken = None

# Step 3: Broadcast the final result to all processes
final_found_flag = comm.bcast(final_found_flag, root=0)
final_password = comm.bcast(final_password, root=0)
found_by_rank = comm.bcast(found_by_rank, root=0)
time_taken = comm.bcast(time_taken, root=0)

comm.Barrier()

if final_found_flag:
    if rank == found_by_rank:
        print(f"[Rank {rank}]  I cracked the password: '{final_password}' in {time_taken:.2f} seconds", flush=True)
    else:
        print(f"[Rank {rank}]  Terminated: did not find the password.", flush=True)

    if rank == 0:
        print(f"\n Password cracked by Rank {found_by_rank}: '{final_password}' in {time_taken:.2f} seconds", flush=True)
else:
    print(f"[Rank {rank}]  All ranks failed to find the password.", flush=True)


