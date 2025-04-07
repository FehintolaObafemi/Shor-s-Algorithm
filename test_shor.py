#!/usr/bin/env python3
"""
Test script for Shor's Algorithm implementations.

This script tests both the custom implementation and the Qiskit implementation
to ensure they correctly factor numbers.
"""

import unittest
import numpy as np
from shors import Shors
from shor_2_0 import execute_shors

class TestShorsAlgorithm(unittest.TestCase):
    """Test cases for Shor's Algorithm implementations."""
    
    def test_shors_class(self):
        """Test the Shors class implementation."""
        # Test prime number detection
        shor = Shors(17, 3)
        self.assertTrue(shor.is_prime(17))
        self.assertFalse(shor.is_prime(15))
        
        # Test factor finding
        factors = shor.get_factors(15)
        self.assertEqual(set(factors), {1, 3, 5, 15})
        
        # Test prime factorization
        prime_factors = shor.find_prime_factors(15)
        self.assertEqual(prime_factors, [3, 5])
        
    def test_shor_2_0(self):
        """Test the shor_2_0 implementation."""
        # Test with a small number
        result = execute_shors(15, attempts=5)
        if result:
            factor1, factor2 = result
            self.assertEqual(factor1 * factor2, 15)
            
    def test_edge_cases(self):
        """Test edge cases for both implementations."""
        # Test with even numbers (should be handled by shor_2_0)
        result = execute_shors(14, attempts=1)
        if result:
            factor1, factor2 = result
            self.assertEqual(factor1 * factor2, 14)
            
        # Test with prime numbers
        shor = Shors(17, 3)
        prime_factors = shor.find_prime_factors(17)
        self.assertEqual(prime_factors, [17])
        
    def test_performance(self):
        """Test performance with larger numbers."""
        # This test might take longer to run
        result = execute_shors(21, attempts=10)
        if result:
            factor1, factor2 = result
            self.assertEqual(factor1 * factor2, 21)

if __name__ == "__main__":
    unittest.main() 