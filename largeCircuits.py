import datetime
from math import log2

def buildShorQP (N = None, a = 2, file = None, approach = '3nx1'):

    # Output file for Quantum Program
    if not file:
        file = 'Shor-N'+str(N)+'-a'+str(a)+'-'+approach+'.qp'
    
    # Timestamp the command generation.
    cmds = []
    cmds.append('#! '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    # Kitaev's circuit.
    if approach == 'nx2n':
        
        # Number of quantum and classical bits.
        nQ = N.bit_length()+1
        nC = int(log2(1<<((N**2)-1).bit_length()))
        
        # Add qubits and classical bits to circuit.
        cmds.append('\n#! Add Qubits and Cbits.')
        cmds.append('AddQubits '+str(nQ))
        cmds.append('AddCbits '+str(nC))
        
        # Initialization of work register.
        cmds.append('\n#! Initialize work register.')
        cmds.append('GateOp SigmaX '+str(nQ-1))

        # Loop over #stages in Keitev's approach.
        for e in range(nC):
 
            # At every stage, apply Hadamard and Quantum Modular Exponentiation.
            cmds.append('\n#! Stage '+str(e))
            cmds.append('GateOp Hadamard 0')
            cmds.append('GateOp QuModExpUaj 0:'+str(nQ)+' a='+str(a)+' j='+str((nC-e-1))+' N='+str(N))
 
            # Rotation and Hadamard after QuModExp.
            if e > 0: cmds.append("GateOp RPhase 0,"+','.join([str(i) for i in range(-e,0)]))
            cmds.append('GateOp Hadamard 0')
 
            # Measure and copy the qubit data to classical bit.
            cmds.append('Measure 0')
            cmds.append('GateOp Copy 0,-'+str(e+1))
 
            # Initialize before next stage.
            cmds.append('GateOp SigmaX 0,-'+str(e+1))
 
        # Measurement.
        cmds.append('\n#! Measure all qubits.')
        cmds.append('Measure 1:'+str(nQ))
    # Full Circuit
    elif approach =='3nx1':

        # Qubits in work register and control register
        nWQ = N.bit_length()
        nCQ = int(log2(1<<((N**2)-1).bit_length()))
        nTQ = nWQ+nCQ
 
        # Add qubits to circuit.
        cmds.append('\n#! Add Qubits.')
        cmds.append('AddQubits '+str(nTQ))
 
        # Initialization of work register.
        cmds.append('\n#! Initialize work register.')
        cmds.append('GateOp SigmaX '+str(nTQ - 1))
 
        # Hadamard on control register.
        cmds.append('\n#! Hadamard on control register.')
        cmds.append('GateOp Hadamard 0:'+str(nCQ - 1))
 
        # Quantum Modular Exponentiation.
        cmds.append('\n#! Modular Exponentiation of work register.')
        for c in range(nCQ):
            cmds.append('GateOp QuModExpUaj '+str(nCQ-c-1)+','+','.join([str(i) for i in range(nCQ,nTQ)])+' a='+str(a)+' j='+str(c)+' N='+str(N))

        # Measure work register.
        cmds.append('\n#! Measure work register.')
        cmds.append('Measure '+','.join([str(i) for i in range(nCQ,nTQ)]))
 
        # Quantum Fourier Transform.
        cmds.append('\n#! QFT.')
        for c in range(nCQ):
            cmds.append('GateOp Hadamard '+str(c))
            for i, d in enumerate(range(c+1,nCQ)):
                cmds.append('GateOp CPHASE '+str(d)+','+str(c)+' phi=PI/'+str(2**(i+1)))
 
        # Swap after QFT.
        cmds.append('\n#! SWAP.')
        for i in range(nCQ//2):
            cmds.append('GateOp SWAP '+str(i)+','+str(nCQ-i-1))
 
    # Write commands to .qp file to be loaded directly to Q-Kit.
    filePtr = open(file, 'w')
    filePtr.write('\n'.join(cmds))
    filePtr.close()

# Run function to build Shor's factorization QP with choice of N and a.
buildShorQP(N=15, a=2, approach='nx2n')
buildShorQP(N=15, a=2, approach='3nx1')