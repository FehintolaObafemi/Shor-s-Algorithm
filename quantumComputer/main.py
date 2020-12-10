from qiskit import IBMQ, Aer
from qiskit.aqua import QuantumInstance
from helper import helper
import numpy as np

IBMQ.enable_account(
    '2c48804aa2f1d7c872f4cb2a37a4ec649f24241766d16c4b81061b00f62c2f0419dd04f260fe59be8a9550a93bea7692fa956cc6637565b593ae98e29c77331c')
provider = IBMQ.get_provider(hub='ibm-q')


backend = provider.get_backend('ibmq_16_melbourne')

print('\n Shors Algorithm')
print('--------------------')
print('\nExecuting...\n')

N = 899
a = 3

factors = helper(N, a)


xvals = factors.order()
yvals = [np.mod(a ** x, N) for x in xvals]

# getting possible period values
r = yvals[1:].index(1) + 1

check = a**(r/2) + 1

if check != 0:
    print("The prime factors of", N, "are", factors.gcd())
