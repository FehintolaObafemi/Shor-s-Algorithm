# -*- coding: utf-8 -*-
"""
Shor's Algorithm Implementation using Qiskit

This script demonstrates the use of Shor's algorithm for integer factorization
using IBM's quantum computing platform through Qiskit.

Author: Taofeek Obafemi-Babatunde
Course: Computer Science 491 - Quantum Computing
Fall 2020 - Final Project
"""

from typing import Dict, List, Optional, Tuple
import os
from qiskit import IBMQ
from qiskit.aqua import QuantumInstance
from qiskit.aqua.algorithms import Shor
from qiskit.providers.ibmq import IBMQBackend

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

def factor_number(number: int, backend: IBMQBackend, shots: int = 1) -> List[int]:
    """
    Factor a number using Shor's algorithm.
    
    Args:
        number: The number to factor
        backend: Quantum backend to use
        shots: Number of shots to run
        
    Returns:
        List[int]: List of factors found
        
    Raises:
        ValueError: If number is less than 2
    """
    if number < 2:
        raise ValueError("Number to factor must be greater than 1")
        
    shor = Shor(number)
    quantum_instance = QuantumInstance(
        backend,
        shots=shots,
        skip_qobj_validation=False
    )
    
    result = shor.run(quantum_instance)
    return result['factors']

def main() -> None:
    """Main function to demonstrate Shor's algorithm."""
    try:
        # Set up quantum backend
        backend = setup_quantum_backend()
        
        # Numbers to factor
        numbers = [571, 757]
        
        # Factor each number
        for num in numbers:
            print(f"\nFactoring {num}...")
            factors = factor_number(num, backend)
            print(f"Factors of {num}: {factors}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        
if __name__ == "__main__":
    main()