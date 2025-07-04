***# 🔐 MPI Brute-Force Password Cracker***

This project is a \*\*parallel brute-force password cracker\*\* implemented in \*\*Python\*\* using \*\*MPI (Message Passing Interface)\*\* via the `mpi4py` library. It distributes the password search space across multiple processes to significantly speed up the cracking time compared to a sequential approach.


***## 🚀 Project Overview***

The goal is to crack a given target password by brute-forcing all possible combinations from a defined character set. The program utilizes MPI to split the total workload evenly across available processes, making use of all CPU cores.



**### ✅ Features**

1\- Parallelized brute-force cracking using `mpi4py`

2\- Customizable character set and password length

3\- Distributed workload across MPI processes

4\- Real-time progress tracking and timing

5\- Displays the process that cracked the password

6\- Efficient early termination of all processes when the password is found



***## 📌 Technologies Used***

1\. *Python 3*

2\. *mpi4py*

3\. *MPI (OpenMPI or MPICH)*

4\. *itertools*

5\. *time*



***## 🧠 How It Works***

1\. \*\*Character Set \& Password Length\*\* are defined at the top.

2\. The total number of combinations is calculated.

3\. The space is divided across all MPI ranks.

4\. Each process attempts to brute-force its assigned chunk.

5\. Once any process finds the password, it:

6\. Notifies all other processes to stop.

7\. Outputs who found it, what the password was, and how long it took.



\## ⚙️ Setup \& Installation

***### Prerequisites:***

1\- Python 3

2\- `mpi4py` library

3\- MPI implementation (e.g., OpenMPI or MPICH)



&nbsp;					------------------------------HOW TO EXECUTE------------------------------



***### Install Dependencies:***

---  pip install mpi4py


***### Run Command*** 

---  mpiexec -n 4 python mpi\_password\_cracker.py 

**#### NOTE:** 4 is the number of processor/Ranks used for this program this number can be changed

&nbsp;					
			------------------------------PERFORMANCE------------------------------

**Tested on:** Intel Core i5 8th Gen, 16 GB RAM

6 billion combinations completed in ~6.5 hours

Average speed: ~243,000 combinations/second





