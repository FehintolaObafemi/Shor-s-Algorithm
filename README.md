# Shor's Algorithm Implementation

This repository contains implementations of Shor's algorithm for integer factorization using both quantum and classical approaches. The algorithm demonstrates the potential of quantum computing to solve certain problems exponentially faster than classical computers.

## Overview

Shor's algorithm is a quantum algorithm for integer factorization. Given an integer N, it finds its prime factors. The algorithm consists of two parts:

1. A reduction, which can be done on a classical computer, of the factoring problem to the problem of order-finding.
2. A quantum algorithm to solve the order-finding problem.

## Implementations

This repository contains several implementations:

- **Python Implementations**:
  - `shor_2_0.py`: A comprehensive implementation with quantum state simulation
  - `shors.py`: A simpler implementation focusing on the classical parts
  - `491_final.py`: Implementation using Qiskit for IBM quantum computers
  - `main.py`: Main script to run the algorithm
  - `largeCircuits.py`: Utility for generating quantum circuits

- **C++ Implementations**:
  - `shor.C`: Main implementation
  - `qureg.C`: Quantum register implementation
  - `complex.C`: Complex number operations
  - `util.C`: Utility functions

## Requirements

### Python Dependencies
```
numpy>=1.20.0
qiskit>=0.30.0
matplotlib>=3.4.0
scipy>=1.7.0
```

### C++ Dependencies
- Standard C++ compiler
- Math library

## Usage

### Python Implementation

```bash
# Run the main implementation
python main.py

# Run the Qiskit implementation
python 491_final.py
```

### C++ Implementation

```bash
# Compile the C++ implementation
g++ -o shor shor.C qureg.C complex.C util.C -lm

# Run the compiled program
./shor
```

## License

This project is licensed under the terms included in the LICENSE file.

## References

- Shor, P. W. (1999). Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer. SIAM Review, 41(2), 303-332.
- Nielsen, M. A., & Chuang, I. L. (2010). Quantum Computation and Quantum Information. Cambridge University Press.