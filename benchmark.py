#!/usr/bin/env python3
"""
Benchmark script for Shor's Algorithm implementations.

This script compares the performance of different implementations
of Shor's algorithm for integer factorization.
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from shors import Shors
from shor_2_0 import execute_shors

def benchmark_shors_class(numbers, max_time=60):
    """
    Benchmark the Shors class implementation.
    
    Args:
        numbers: List of numbers to factor
        max_time: Maximum time in seconds to spend on each number
        
    Returns:
        List of tuples (number, time_taken, success)
    """
    results = []
    
    for N in numbers:
        print(f"Benchmarking Shors class with N={N}...")
        start_time = time.time()
        
        try:
            shor = Shors(N, 3)
            factors = shor.find_prime_factors(N)
            
            end_time = time.time()
            elapsed = end_time - start_time
            
            success = len(factors) > 1
            results.append((N, elapsed, success))
            
            print(f"  Time: {elapsed:.4f}s, Success: {success}")
            
            if elapsed > max_time:
                print(f"  Exceeded maximum time of {max_time}s, stopping benchmark")
                break
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            results.append((N, time.time() - start_time, False))
            
    return results

def benchmark_shor_2_0(numbers, attempts=5, max_time=60):
    """
    Benchmark the shor_2_0 implementation.
    
    Args:
        numbers: List of numbers to factor
        attempts: Number of attempts for each number
        max_time: Maximum time in seconds to spend on each number
        
    Returns:
        List of tuples (number, time_taken, success)
    """
    results = []
    
    for N in numbers:
        print(f"Benchmarking shor_2_0 with N={N}...")
        start_time = time.time()
        
        try:
            result = execute_shors(N, attempts=attempts)
            
            end_time = time.time()
            elapsed = end_time - start_time
            
            success = result is not None
            results.append((N, elapsed, success))
            
            print(f"  Time: {elapsed:.4f}s, Success: {success}")
            
            if elapsed > max_time:
                print(f"  Exceeded maximum time of {max_time}s, stopping benchmark")
                break
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            results.append((N, time.time() - start_time, False))
            
    return results

def plot_results(shors_results, shor_2_0_results):
    """
    Plot the benchmark results.
    
    Args:
        shors_results: Results from the Shors class benchmark
        shor_2_0_results: Results from the shor_2_0 benchmark
    """
    plt.figure(figsize=(10, 6))
    
    # Extract data
    shors_numbers = [r[0] for r in shors_results]
    shors_times = [r[1] for r in shors_results]
    shor_2_0_numbers = [r[0] for r in shor_2_0_results]
    shor_2_0_times = [r[1] for r in shor_2_0_results]
    
    # Plot
    plt.plot(shors_numbers, shors_times, 'o-', label='Shors Class')
    plt.plot(shor_2_0_numbers, shor_2_0_times, 's-', label='shor_2_0')
    
    plt.xlabel('Number to Factor')
    plt.ylabel('Time (seconds)')
    plt.title('Shor\'s Algorithm Benchmark')
    plt.legend()
    plt.grid(True)
    
    # Save the plot
    plt.savefig('shor_benchmark.png')
    plt.close()

def main():
    """Main function to run the benchmarks."""
    # Numbers to test
    numbers = [15, 21, 35, 55, 77, 91, 119, 143, 187, 221]
    
    print("Starting benchmarks...")
    
    # Run benchmarks
    shors_results = benchmark_shors_class(numbers)
    shor_2_0_results = benchmark_shor_2_0(numbers)
    
    # Plot results
    plot_results(shors_results, shor_2_0_results)
    
    print("\nBenchmark results:")
    print("Number | Shors Class (s) | shor_2_0 (s)")
    print("-------|----------------|-------------")
    
    for i, N in enumerate(numbers):
        if i < len(shors_results) and i < len(shor_2_0_results):
            shors_time = shors_results[i][1]
            shor_2_0_time = shor_2_0_results[i][1]
            print(f"{N:6d} | {shors_time:14.4f} | {shor_2_0_time:11.4f}")
        elif i < len(shors_results):
            shors_time = shors_results[i][1]
            print(f"{N:6d} | {shors_time:14.4f} | N/A")
        elif i < len(shor_2_0_results):
            shor_2_0_time = shor_2_0_results[i][1]
            print(f"{N:6d} | N/A            | {shor_2_0_time:11.4f}")
        else:
            print(f"{N:6d} | N/A            | N/A")
            
    print("\nBenchmark plot saved as 'shor_benchmark.png'")

if __name__ == "__main__":
    main() 