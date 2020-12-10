import math

class Shors:
    def __init__(self, num, divisor):
        self.num = num
        self.div = divisor
        self.true_prime = 3

    # checking if the number is already prime
    def isprime(self, number):
        if number % 2 == 0:
            return False
        for i in range(self.true_prime, number, 2):
            if number % i == 0:
                return False
        self.true_prime = number
        return True

    # getting all possible factors of each number
    def getfactor(self, number):
        factors = []
        for num in range(1, number+1):
            if number % num == 0:
                factors.append(num)
        return factors

    def order(self):
        # checking all possible factors that only share 1 as a prime number
        all_coprimes = []
        a = 3
        factor_a = self.getfactor(a)
        factor_num = self.getfactor(self.num)
        shared_factors = 0
        while a < self.num:
            for num in factor_a:
                if num in factor_num:
                    shared_factors += 1
            if shared_factors == 1:
                all_coprimes.append(a)
            a += 1
            factor_a = self.getfactor(a)
            shared_factors = 0
        return all_coprimes

    def gcd(self):
        factors = []
        if self.isprime(self.num):
            return self.num
        # getting all the prime factors of N
        for num in range(3, self.num, 2):
            if self.num % num == 0:
                if self.isprime(num):
                    factors.append(num)
        return factors

