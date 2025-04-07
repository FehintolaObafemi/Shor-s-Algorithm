"""
Main script for running Shor's Algorithm using Qiskit and custom implementation.

This script demonstrates both the Qiskit implementation and a custom implementation
of Shor's algorithm for integer factorization.
"""

from typing import List, Optional, Tuple
import os
import numpy as np
from qiskit import IBMQ
from qiskit.aqua import QuantumInstance
from qiskit.providers.ibmq import IBMQBackend
from shors import Shors

def setup_quantum_backend(api_token: Optional[str] = None) -> IBMQBackend:
    """
    Set up connection to IBM Quantum backend.
    
    Args:
        api_token: IBM Quantum API token. If None, tries to get from environment.
        
    Returns:
        IBMQBackend: Configured quantum backend
        
    Raises:
        ValueError: If API token is not provided and not found in environment
    """
    if api_token is None:
        api_token = os.getenv('IBMQ_API_TOKEN')
        if api_token is None:
            raise ValueError("IBMQ API token not provided and IBMQ_API_TOKEN environment variable not set")
            
    IBMQ.enable_account(api_token)
    provider = IBMQ.get_provider(hub='ibm-q')
    return provider.get_backend('ibmq_qasm_simulator')

def find_period(a: int, N: int, factors: Shors) -> Optional[int]:
    """
    Find the period of a^x mod N.
    
    Args:
        a: Base number
        N: Modulus
        factors: Shors instance
        
    Returns:
        Optional[int]: Period if found, None otherwise
    """
    try:
        xvals = factors.find_coprimes()
        yvals = [np.mod(a ** x, N) for x in xvals]
        
        # Find first occurrence of 1 after index 0
        try:
            r = yvals[1:].index(1) + 1
            return r
        except ValueError:
            return None
            
    except Exception as e:
        print(f"Error finding period: {str(e)}")
        return None

def factor_number(N: int, a: int = 3) -> Optional[List[int]]:
    """
    Factor a number using Shor's algorithm.
    
    Args:
        N: Number to factor
        a: Base number for modular exponentiation
        
    Returns:
        Optional[List[int]]: List of factors if found, None otherwise
    """
    try:
        if N < 2:
            raise ValueError("Number to factor must be greater than 1")
            
        factors = Shors(N, a)
        r = find_period(a, N, factors)
        
        if r is None:
            print(f"Could not find period for {N}")
            return None
            
        check = a**(r/2) + 1
        if check != 0:
            return factors.find_prime_factors()
            
        return None
        
    except Exception as e:
        print(f"Error factoring {N}: {str(e)}")
        return None

def main() -> None:
    """Main function to demonstrate Shor's algorithm."""
    try:
        print('\nShor\'s Algorithm')
        print('--------------------')
        print('\nExecuting...\n')
        
        # Get input numbers
        N = int(input("Enter a number to factor: "))
        N2 = int(input("Enter another number to factor: "))
        
        # Factor first number
        print(f"\nFactoring {N}...")
        factors = factor_number(N)
        if factors:
            print(f"The prime factors of {N} are: {factors}")
            
        # Factor second number if it's large enough
        if N2 > 15:
            print(f"\nFactoring {N2}...")
            factors2 = factor_number(N2)
            if factors2:
                print(f"The prime factors of {N2} are: {factors2}")
                
    except ValueError as e:
        print(f"Invalid input: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")
        
if __name__ == "__main__":
    main()
