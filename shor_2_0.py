import math
import random

class QuantumMapping:
    def __init__(self, state, amplitude):
        self.state = state
        self.amplitude = amplitude

class QuantumState:
    def __init__(self, amplitude, register):
        self.amplitude = amplitude
        self.register = register
        self.entangled = {}
    def SetEntangled(self, fromState, amplitude):
        register = fromState.register
        entanglement = QuantumMapping(fromState, amplitude)
        try:
            self.entangled[register].append(entanglement)
        except:
            self.entangled[register] = [entanglement]

def GetEntangles(self, register = None):
    entangles = 0
    if register is None:
        for states in self.entangled.values():
            entangles += len(states)
    else:
        entangles = len(self.entangled[register])
    return entangles

class QuantumRegister:
    def __init__(self, numBits):
        self.numBits = numBits
        self.numStates = 1 << numBits
        self.entangled = []
        self.states = [QuantumState(complex(0.0), self) for x in range(self.numStates)]
        self.states[0].amplitude = complex(1.0)
    def SetPropagate(self, fromRegister = None):
        if fromRegister is not None:
            for state in self.states:
                amplitude = complex(0.0)
                try:
                    entangles = state.entangled[fromRegister]
                    for entangle in entangles:
                        amplitude += entangle.state.amplitude * entangle.amplitude
                    state.amplitude = amplitude
                except KeyError:
                    state.amplitude = amplitude
        for register in self.entangled:
            if register is fromRegister:
                continue
            register.propagate(self)

def SetMap(self, toRegister, mapping, propagate = True):
        self.entangled.append(toRegister)
        toRegister.entangled.append(self)
        mapTensorX = {}
        mapTensorY = {}
        for x in range(self.numStates):
            mapTensorX[x] = {}
            codomain = mapping(x)
            for element in codomain:
                y = element.state
                mapTensorX[x][y] = element
                try:
                    mapTensorY[y][x] = element
                except KeyError:
                    mapTensorY[y] = { x: element }
        def SetNormalize(tensor, p = False):
            lSqrt = math.sqrt
            for vectors in tensor.values():
                sumProb = 0.0
                for element in vectors.values():
                    amplitude = element.amplitude
                    sumProb += (amplitude * amplitude.conjugate()).real
                normalized = lSqrt(sumProb)
                for element in vectors.values():
                    element.amplitude = element.amplitude / normalized
        SetNormalize(mapTensorX)
        SetNormalize(mapTensorY, True)
        for x, yStates in mapTensorX.items():
            for y, element in yStates.items():
                amplitude = element.amplitude
                toState = toRegister.states[y]
                fromState = self.states[x]
                toState.entangle(fromState, amplitude)
                fromState.entangle(toState, amplitude.conjugate())
        if propagate:
            toRegister.propagate(self)

def GetMeasure(self):
        measure = random.random()
        sumProb = 0.0
        finalXval = None
        finalState = None
        for x, state in enumerate(self.states):
            amplitude = state.amplitude
            sumProb += (amplitude * amplitude.conjugate()).real
            if sumProb > measure:
                finalState = state
                finalXval = x
                break
        if finalState is not None:
            for state in self.states:
                state.amplitude = complex(0.0)
            finalState.amplitude = complex(1.0)
            self.propagate()
        return finalXval

def GetEntangles(self, register = None):
    entanglevals = 0
    for state in self.states:
        entanglevals += state.entangles(None)
    return entanglevals

def GetAmplitudes(self):
    amplitudesarr = []
    for state in self.states:
        amplitudesarr.append(state.amplitude)
    return amplitudesarr

def ListEntangles(register):
    print("Entangles: " + str(register.entangles()))
def ListAmplitudes(register):
    amplitudes = register.amplitudes()
    for x, amplitude in enumerate(amplitudes):
        print('State #' + str(x) + '\'s Amplitude value: ' + str(amplitude))

def ApplyHadamard(x, Q):
    codomainarr = []
    for y in range(Q):
        amplitude = complex(pow(-1.0, GetBitCount(x & y) & 1))
        codomainarr.append(QuantumMapping(y, amplitude))
    return  codomainarr

def GetQModExp(aval, expval, modval):
    state = GetModExp(aval, expval, modval)
    amplitude = complex(1.0)
    return [QuantumMapping(state, amplitude)]

def ApplyQft(x, Q):
    fQ = float(Q)
    k = -2.0 * math.pi
    codomainarr = []
    for y in range(Q):
        theta = (k * float((x * y) % Q)) / fQ
        amplitude = complex(math.cos(theta), math.sin(theta))
        codomainarr.append(QuantumMapping(y, amplitude))
    return codomainarr

def GetPeriod(a, N):
    nNumBits = N.bit_length()
    inputNumBits = (2 * nNumBits) - 1
    inputNumBits += 1 if ((1 << inputNumBits) < (N * N)) else 0
    Q = 1 << inputNumBits
    print("Finding the period...")
    print("Q = " + str(Q) + "\ta = " + str(a))
    inputRegister = QuantumRegister(inputNumBits)
    hmdInputRegister = QuantumRegister(inputNumBits)
    qftInputRegister = QuantumRegister(inputNumBits)
    outputRegister = QuantumRegister(inputNumBits)
    print("Registers generated")
    print("Performing Hadamard on input register")
    inputRegister.map(hmdInputRegister, lambda x: hadamard(x, Q), False)
    print("Hadamard complete")
    print("Mapping input register to output register, where f(x) is a^x mod N")
    hmdInputRegister.map(outputRegister, lambda x: GetQModExp(a, x, N), False)
    print("Modular exponentiation complete")
    print("Performing quantum Fourier transform on output register")
    hmdInputRegister.map(qftInputRegister, lambda x: qft(x, Q), False)
    inputRegister.propagate()
    print("Quantum Fourier transform complete")
    print("Performing a measurement on the output register")
    y = outputRegister.measure()
    print("Output register measured\ty = " + str(y))
    print("Performing a measurement on the periodicity register")
    x = qftInputRegister.measure()
    print("QFT register measured\tx = " + str(x))
    if x is None:
        return None
    print("Finding the period via continued fractions")
    rperiod = cf(x, Q, N)
    print("Candidate period\tr = " + str(rperiod))
    return rperiod

def GetBitCount(xval):
    sumBitvals = 0
    while xval > 0:
        sumBitvals += xval & 1
        xval >>= 1
    return sumBitvals

def GetGcd(aval, bval):
    while bval != 0:
        tA = aval % bval
        aval = bval
        bval = tA
    return aval

def GetExtendedGCD(a, b):
    fractionvals = []
    while b != 0:
        fractionvals.append(a // b)
        tA = a % b
        a = b
        b = tA
    return fractionvals

def GetContinuedFraction(y, Q, N):
    fractions = GetExtendedGCD(y, Q)
    depth = 2
    def partial(fractions, depth):
        c = 0
        r = 1
        for i in reversed(range(depth)):
            tR = fractions[i] * r + c
            c = r
            r = tR
        return c
    rcf = 0
    for d in range(depth, len(fractions) + 1):
        tR = partial(fractions, d)
        if tR == rcf or tR >= N:
            return rcf
        rcf = tR
    return rcf

def GetModExp(aval, expval, modval):
    fxval = 1
    while exp > 0:
        if (exp & 1) == 1:
            fxval = fxval * aval % modval
        aval = (aval * aval) % modval
        expval = expval >> 1
    return fxval

def RandomPick(Nval):
    aval = math.floor((random.random() * (Nval - 1)) + 0.5)
    return aval

def GetCandidates(a, r, N, neighborhood):
    if r is None:
        return None
    for k in range(1, neighborhood + 2):
        tR = k * r
        if GetModExp(a, a, N) == GetModExp(a, a + tR, N):
            return tR
    for tR in range(r - neighborhood, r):
        if GetModExp(a, a, N) == GetModExp(a, a + tR, N):
            return tR
    for tR in range(r + 1, r + neighborhood + 1):
        if GetModExp(a, a, N) == GetModExp(a, a + tR, N):
            return tR
    return None

def ExecuteShors(N, attempts = 1, neighborhood = 0.0, numPeriods = 1):
    periods = []
    neighborhood = math.floor(N * neighborhood) + 1
    print("N = " + str(N))
    print("Neighborhood = " + str(neighborhood))
    print("Number of periods = " + str(numPeriods))
    for attempt in range(attempts):
        print("\nAttempt #" + str(attempt))
        a = pick(N)
        while a < 2:
            a = pick(N)
        d = GetGcd(a, N)
        if d > 1:
            print("Found factors classically, re-attempt")
            continue
        r = findPeriod(a, N)
        print("Checking candidate period, nearby values, and multiples")
        r = GetCandidates(a, r, N, neighborhood)
        if r is None:
            print("Period was not found, re-attempt")
            continue
        if (r % 2) > 0:
            print("Period was odd, re-attempt")
            continue
        d = GetModExp(a, (r // 2), N)
        if r == 0 or d == (N - 1):
            print("Period was trivial, re-attempt")
            continue
        print("Period found\tr = " + str(r))
        periods.append(r)
        if(len(periods) < numPeriods):
            continue
        print("\nFinding least common multiple of all periods")
        r = 1
        for period in periods:
            d = GetGcd(period, r)
            r = (r * period) // d
        b = GetModExp(a, (r // 2), N)
        f1 = GetGcd(N, b + 1)
        f2 = GetGcd(N, b - 1)
        return [f1, f2]
    return None

results_algo = ExecuteShors(35, 20, 0.01, 2)
print("Results from the algorithm:\t" + str(results_algo[0]) + ", " + str(results_algo[1]))