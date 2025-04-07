#!/usr/bin/env python3
"""
Visualization script for Shor's Algorithm quantum circuits.

This script generates and visualizes the quantum circuits used in
Shor's algorithm for integer factorization.
"""

import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import QFT

def create_shor_circuit(N, a=2):
    """
    Create a quantum circuit for Shor's algorithm.
    
    Args:
        N: Number to factor
        a: Base for modular exponentiation
        
    Returns:
        QuantumCircuit: The created circuit
    """
    # Calculate register sizes
    n = N.bit_length()
    q = 2 * n  # Size of the control register
    
    # Create quantum registers
    control = QuantumRegister(q, 'control')
    target = QuantumRegister(n, 'target')
    classical = ClassicalRegister(q, 'classical')
    
    # Create the circuit
    circuit = QuantumCircuit(control, target, classical)
    
    # Initialize target register to |1⟩
    circuit.x(target[0])
    
    # Apply Hadamard gates to control register
    for i in range(q):
        circuit.h(control[i])
    
    # Apply controlled modular exponentiation
    # This is a simplified version - in a real implementation,
    # you would use a more efficient modular exponentiation
    for i in range(q):
        # Apply controlled-U operation
        # In a real implementation, this would be a modular exponentiation
        # Here we use a simplified version for visualization
        circuit.cx(control[i], target[0])
    
    # Apply inverse QFT
    qft = QFT(q, inverse=True)
    circuit.append(qft, control[:])
    
    # Measure the control register
    circuit.measure(control, classical)
    
    return circuit

def visualize_circuit(circuit, save_path=None):
    """
    Visualize a quantum circuit.
    
    Args:
        circuit: QuantumCircuit to visualize
        save_path: Path to save the visualization
    """
    # Draw the circuit
    fig = circuit.draw(output='mpl')
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def main():
    """Main function to visualize Shor's algorithm circuits."""
    # Numbers to visualize
    numbers = [15, 21, 35]
    
    for N in numbers:
        print(f"Creating circuit for N={N}...")
        circuit = create_shor_circuit(N)
        
        # Visualize the circuit
        save_path = f"shor_circuit_N{N}.png"
        visualize_circuit(circuit, save_path)
        print(f"Circuit visualization saved as '{save_path}'")
        
        # Print circuit information
        print(f"Circuit depth: {circuit.depth()}")
        print(f"Number of qubits: {circuit.num_qubits}")
        print(f"Number of classical bits: {circuit.num_clbits}")
        print(f"Number of operations: {circuit.size()}")
        print()

if __name__ == "__main__":
    main() 