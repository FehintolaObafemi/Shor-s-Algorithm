import math
import random
from typing import List, Dict, Optional, Tuple, Union
import numpy as np

class QuantumMapping:
    def __init__(self, state: int, amplitude: complex):
        self.state = state
        self.amplitude = amplitude

class QuantumState:
    def __init__(self, amplitude: complex, register: 'QuantumRegister'):
        self.amplitude = amplitude
        self.register = register
        self.entangled: Dict['QuantumRegister', List[QuantumMapping]] = {}
    
    def set_entangled(self, from_state: 'QuantumState', amplitude: complex) -> None:
        register = from_state.register
        entanglement = QuantumMapping(from_state, amplitude)
        if register not in self.entangled:
            self.entangled[register] = []
        self.entangled[register].append(entanglement)

    def get_entangles(self, register: Optional['QuantumRegister'] = None) -> int:
        if register is None:
            return sum(len(states) for states in self.entangled.values())
        return len(self.entangled.get(register, []))

class QuantumRegister:
    def __init__(self, num_bits: int):
        self.num_bits = num_bits
        self.num_states = 1 << num_bits
        self.entangled: List['QuantumRegister'] = []
        self.states = [QuantumState(complex(0.0), self) for _ in range(self.num_states)]
        self.states[0].amplitude = complex(1.0)
    
    def set_propagate(self, from_register: Optional['QuantumRegister'] = None) -> None:
        if from_register is not None:
            for state in self.states:
                amplitude = complex(0.0)
                try:
                    entangles = state.entangled[from_register]
                    amplitude = sum(entangle.state.amplitude * entangle.amplitude 
                                  for entangle in entangles)
                except KeyError:
                    pass
                state.amplitude = amplitude
        
        for register in self.entangled:
            if register is from_register:
                continue
            register.propagate(self)

    def set_map(self, to_register: 'QuantumRegister', mapping: callable, propagate: bool = True) -> None:
        self.entangled.append(to_register)
        to_register.entangled.append(self)
        
        # Use numpy for better performance in tensor operations
        map_tensor_x: Dict[int, Dict[int, QuantumMapping]] = {}
        map_tensor_y: Dict[int, Dict[int, QuantumMapping]] = {}
        
        for x in range(self.num_states):
            map_tensor_x[x] = {}
            codomain = mapping(x)
            for element in codomain:
                y = element.state
                map_tensor_x[x][y] = element
                if y not in map_tensor_y:
                    map_tensor_y[y] = {}
                map_tensor_y[y][x] = element

        def normalize_tensor(tensor: Dict[int, Dict[int, QuantumMapping]], p: bool = False) -> None:
            for vectors in tensor.values():
                sum_prob = sum((element.amplitude * element.amplitude.conjugate()).real 
                             for element in vectors.values())
                normalized = math.sqrt(sum_prob)
                for element in vectors.values():
                    element.amplitude /= normalized

        normalize_tensor(map_tensor_x)
        normalize_tensor(map_tensor_y, True)

        # Vectorized operations for better performance
        for x, y_states in map_tensor_x.items():
            for y, element in y_states.items():
                amplitude = element.amplitude
                to_state = to_register.states[y]
                from_state = self.states[x]
                to_state.set_entangled(from_state, amplitude)
                from_state.set_entangled(to_state, amplitude.conjugate())

        if propagate:
            to_register.propagate(self)

    def get_measure(self) -> Optional[int]:
        measure = random.random()
        sum_prob = 0.0
        final_xval = None
        final_state = None
        
        # Vectorized probability calculation
        probabilities = np.array([(state.amplitude * state.amplitude.conjugate()).real 
                                for state in self.states])
        cumulative_prob = np.cumsum(probabilities)
        
        idx = np.searchsorted(cumulative_prob, measure)
        if idx < len(self.states):
            final_state = self.states[idx]
            final_xval = idx
            
            # Collapse the state
            for state in self.states:
                state.amplitude = complex(0.0)
            final_state.amplitude = complex(1.0)
            self.propagate()
            
        return final_xval

    def get_entangles(self, register: Optional['QuantumRegister'] = None) -> int:
        return sum(state.get_entangles(register) for state in self.states)

    def get_amplitudes(self) -> List[complex]:
        return [state.amplitude for state in self.states]

def apply_hadamard(x: int, Q: int) -> List[QuantumMapping]:
    return [QuantumMapping(y, complex(pow(-1.0, bin(x & y).count('1') & 1)))
            for y in range(Q)]

def get_q_mod_exp(a_val: int, exp_val: int, mod_val: int) -> List[QuantumMapping]:
    state = get_mod_exp(a_val, exp_val, mod_val)
    return [QuantumMapping(state, complex(1.0))]

def apply_qft(x: int, Q: int) -> List[QuantumMapping]:
    fQ = float(Q)
    k = -2.0 * math.pi
    return [QuantumMapping(y, complex(math.cos(k * float((x * y) % Q) / fQ),
                                    math.sin(k * float((x * y) % Q) / fQ)))
            for y in range(Q)]

def get_period(a: int, N: int) -> Optional[int]:
    n_num_bits = N.bit_length()
    input_num_bits = (2 * n_num_bits) - 1
    input_num_bits += 1 if ((1 << input_num_bits) < (N * N)) else 0
    Q = 1 << input_num_bits
    
    print(f"Finding the period...\nQ = {Q}\ta = {a}")
    
    input_register = QuantumRegister(input_num_bits)
    hmd_input_register = QuantumRegister(input_num_bits)
    qft_input_register = QuantumRegister(input_num_bits)
    output_register = QuantumRegister(input_num_bits)
    
    print("Registers generated")
    print("Performing Hadamard on input register")
    input_register.set_map(hmd_input_register, lambda x: apply_hadamard(x, Q), False)
    
    print("Mapping input register to output register, where f(x) is a^x mod N")
    hmd_input_register.set_map(output_register, lambda x: get_q_mod_exp(a, x, N), False)
    
    print("Performing quantum Fourier transform on output register")
    hmd_input_register.set_map(qft_input_register, lambda x: apply_qft(x, Q), False)
    input_register.set_propagate()
    
    print("Performing measurements")
    y = output_register.get_measure()
    x = qft_input_register.get_measure()
    
    if x is None:
        return None
        
    print(f"Measurements: x = {x}, y = {y}")
    print("Finding the period via continued fractions")
    
    r_period = get_continued_fraction(x, Q, N)
    print(f"Candidate period r = {r_period}")
    return r_period

def get_bit_count(x_val: int) -> int:
    return bin(x_val).count('1')

def get_gcd(a_val: int, b_val: int) -> int:
    while b_val:
        a_val, b_val = b_val, a_val % b_val
    return a_val

def get_extended_gcd(a: int, b: int) -> List[int]:
    fractions = []
    while b:
        fractions.append(a // b)
        a, b = b, a % b
    return fractions

def get_continued_fraction(y: int, Q: int, N: int) -> int:
    fractions = get_extended_gcd(y, Q)
    depth = 2
    
    def partial(fractions: List[int], depth: int) -> int:
        c, r = 0, 1
        for i in reversed(range(depth)):
            c, r = r, fractions[i] * r + c
        return r
    
    r_cf = 0
    for d in range(depth, len(fractions) + 1):
        t_r = partial(fractions, d)
        if t_r == r_cf or t_r >= N:
            return r_cf
        r_cf = t_r
    return r_cf

def get_mod_exp(a_val: int, exp_val: int, mod_val: int) -> int:
    result = 1
    a_val %= mod_val
    while exp_val:
        if exp_val & 1:
            result = (result * a_val) % mod_val
        a_val = (a_val * a_val) % mod_val
        exp_val >>= 1
    return result

def random_pick(N_val: int) -> int:
    return math.floor(random.random() * (N_val - 1) + 0.5)

def get_candidates(a: int, r: Optional[int], N: int, neighborhood: float) -> Optional[int]:
    if r is None:
        return None
        
    # Check multiples of r
    for k in range(1, int(neighborhood) + 2):
        t_r = k * r
        if get_mod_exp(a, a, N) == get_mod_exp(a, a + t_r, N):
            return t_r
            
    # Check values around r
    for t_r in range(max(1, r - int(neighborhood)), r):
        if get_mod_exp(a, a, N) == get_mod_exp(a, a + t_r, N):
            return t_r
            
    return None

def execute_shors(N: int, attempts: int = 1, neighborhood: float = 0.0, num_periods: int = 1) -> Optional[Tuple[int, int]]:
    if N < 2:
        return None
        
    if N % 2 == 0:
        return (2, N // 2)
        
    for _ in range(attempts):
        a = random_pick(N)
        if get_gcd(a, N) != 1:
            continue
            
        r = get_period(a, N)
        if r is None:
            continue
            
        candidates = get_candidates(a, r, N, neighborhood)
        if candidates is not None:
            factor1 = get_gcd(pow(a, candidates // 2, N) + 1, N)
            factor2 = get_gcd(pow(a, candidates // 2, N) - 1, N)
            if factor1 != 1 and factor1 != N:
                return (factor1, N // factor1)
            if factor2 != 1 and factor2 != N:
                return (factor2, N // factor2)
                
    return None

results_algo = execute_shors(35, 20, 0.01, 2)
print("Results from the algorithm:\t" + str(results_algo[0]) + ", " + str(results_algo[1]))