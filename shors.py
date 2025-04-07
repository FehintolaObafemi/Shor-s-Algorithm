import math
from typing import List, Optional, Set

class Shors:
    def __init__(self, num: int, divisor: int):
        """
        Initialize Shor's algorithm implementation.
        
        Args:
            num: The number to factor
            divisor: Initial divisor to try
        """
        self.num = num
        self.div = divisor
        self._prime_cache: Set[int] = {2, 3}  # Cache of known primes
        
    def is_prime(self, number: int) -> bool:
        """
        Check if a number is prime using optimized trial division.
        
        Args:
            number: The number to check
            
        Returns:
            bool: True if the number is prime, False otherwise
        """
        if number < 2:
            return False
        if number in self._prime_cache:
            return True
        if number % 2 == 0:
            return number == 2
            
        # Only check up to square root of number
        sqrt_num = int(math.sqrt(number))
        for i in range(3, sqrt_num + 1, 2):
            if number % i == 0:
                return False
                
        self._prime_cache.add(number)
        return True

    def get_factors(self, number: int) -> List[int]:
        """
        Get all factors of a number efficiently.
        
        Args:
            number: The number to factor
            
        Returns:
            List[int]: List of all factors
        """
        factors = set()
        sqrt_num = int(math.sqrt(number))
        
        for i in range(1, sqrt_num + 1):
            if number % i == 0:
                factors.add(i)
                factors.add(number // i)
                
        return sorted(list(factors))

    def find_coprimes(self) -> List[int]:
        """
        Find all numbers coprime to self.num.
        
        Returns:
            List[int]: List of numbers coprime to self.num
        """
        coprimes = []
        num_factors = set(self.get_factors(self.num))
        
        for a in range(3, self.num):
            a_factors = set(self.get_factors(a))
            if len(num_factors.intersection(a_factors)) == 1:  # Only 1 is shared
                coprimes.append(a)
                
        return coprimes

    def find_prime_factors(self) -> List[int]:
        """
        Find all prime factors of self.num.
        
        Returns:
            List[int]: List of prime factors
        """
        if self.is_prime(self.num):
            return [self.num]
            
        factors = []
        num = self.num
        
        # Handle 2 separately
        while num % 2 == 0:
            factors.append(2)
            num //= 2
            
        # Check odd numbers up to square root
        sqrt_num = int(math.sqrt(num))
        for i in range(3, sqrt_num + 1, 2):
            while num % i == 0:
                if self.is_prime(i):
                    factors.append(i)
                num //= i
                
        # If num is still greater than 2, it must be prime
        if num > 2:
            factors.append(num)
            
        return factors

    def order(self):
        # checking all possible factors that only share 1 as a prime number
        all_coprimes = []
        a = 3
        factor_a = self.get_factors(a)
        factor_num = self.get_factors(self.num)
        shared_factors = 0
        while a < self.num:
            for num in factor_a:
                if num in factor_num:
                    shared_factors += 1
            if shared_factors == 1:
                all_coprimes.append(a)
            a += 1
            factor_a = self.get_factors(a)
            shared_factors = 0
        return all_coprimes

    def gcd(self):
        factors = []
        if self.is_prime(self.num):
            return self.num
        # getting all the prime factors of N
        for num in range(3, self.num, 2):
            if self.num % num == 0:
                if self.is_prime(num):
                    factors.append(num)
        return factors

