import itertools
import numpy as np
from itertools import permutations

from qiskit import Aer, QuantumCircuit, QuantumRegister, ClassicalRegister, execute
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.circuit.library import PhaseOracle, GroverOperator, Permutation
from qiskit.tools.visualization import plot_histogram
from qiskit_ibm_runtime import QiskitRuntimeService, Session, Options, Sampler
import matplotlib.pyplot as plt

xor_lut = np.array([
    # [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
    # [15, 14, 15, 14, 15, 14, 15, 14, 15, 14, 15, 14, 15, 14, 15, 14],
    # [15, 15, 13, 13, 15, 15, 13, 13, 15, 15, 13, 13, 15, 15, 13, 13],
    # [15, 14, 13, 12, 15, 14, 13, 12, 15, 14, 13, 12, 15, 14, 13, 12],
    # [15, 15, 15, 15, 11, 11, 11, 11, 15, 15, 15, 15, 11, 11, 11, 11],
    # [15, 14, 15, 14, 11, 10, 11, 10, 15, 14, 15, 14, 11, 10, 11, 10],
    # [15, 15, 13, 13, 11, 11,  9,  9, 15, 15, 13, 13, 11, 11,  9,  9],
    # [15, 14, 13, 12, 11, 10,  9,  8, 15, 14, 13, 12, 11, 10,  9,  8],
    [15, 15, 15, 15, 15, 15, 15, 15,  7,  7,  7,  7,  7,  7,  7,  7],
    # [15, 14, 15, 14, 15, 14, 15, 14,  7,  6,  7,  6,  7,  6,  7,  6],
    # [15, 15, 13, 13, 15, 15, 13, 13,  7,  7,  5,  5,  7,  7,  5,  5],
    # [15, 14, 13, 12, 15, 14, 13, 12,  7,  6,  5,  4,  7,  6,  5,  4],
    # [15, 15, 15, 15, 11, 11, 11, 11,  7,  7,  7,  7,  3,  3,  3,  3],
    # [15, 14, 15, 14, 11, 10, 11, 10,  7,  6,  7,  6,  3,  2,  3,  2],
    # [15, 15, 13, 13, 11, 11,  9,  9,  7,  7,  5,  5,  3,  3,  1,  1],
    # [15, 14, 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0]
    ], dtype=np.uint8)

xor_len = (xor_lut.shape[0], xor_lut.shape[1])

def dec_xor(a, b):
    return xor_lut[a][b]

def a(x):
    return 15 if x > 0 else 0

def b(x):
    return 0 if x > 0 else 15

def c(a, b):
    x = a - b
    return 0 if x < 0 else x

def d(a, b):
    return a if a >= b else 0

def e(x):
    x = x - 1
    return 0 if x < 0 else x

def f(a, b):
    return a if a >= b else b

def check(logic):
    vala = 0
    for i in range(xor_lut.shape[0]):
        for j in range(xor_lut.shape[1]):
            vala = i
            valb = j

            for l in logic:
                log = l[0]
                if log <= 14:
                    if l[1] == 0:
                        vala = c(vala, log + 1)
                    elif l[1] == 1:
                        valb = c(valb, log + 1)
                if log == 15:
                    if l[1] == 0:
                        vala = a(vala)
                    elif l[1] == 1:
                        valb = a(valb)
                if log == 16:
                    if l[1] == 0:
                        vala = b(vala)
                    elif l[1] == 1:
                        valb = b(valb)
                if log == 17:
                    if l[1] == 0:
                        vala = c(vala, valb)
                    elif l[1] == 1:
                        valb = c(valb, vala)
                if log == 18:
                    if l[1] == 0:
                        vala = d(vala, valb)
                    elif l[1] == 1:
                        valb = d(valb, vala)
                if log == 19:
                    if l[1] == 0:
                        vala = e(vala)
                    elif l[1] == 1:
                        valb = e(valb)
                if log == 20:
                    if l[1] == 0:
                        vala = f(vala, valb)
                    elif l[1] == 1:
                        valb = f(valb, vala)
            
            if xor_lut[i][j] != vala:
                return False
    return True

def brute():
    length = 21
    for i in range(200):
        print("Iteration: " + str(i))
        for j in itertools.permutations(range(length*2), i):
            logic = []
            for x in j:
                logic.append([x-length if (x-length) >= 0 else x, 0 if x < length else 1])
            if check(logic):
                print("=============== Found! ===============")
                print(logic)
                return logic

# brute()
service = QiskitRuntimeService()
options = Options(optimization_level=1)
options.execution.shots = 1024

log_expr = '(Aa ^ Ba) & (Ab ^ Bb) & (Ac ^ Bc) & (Ad ^ Bd)'
oracle = PhaseOracle(log_expr)
#print(oracle.draw(output="text"))

problem = AmplificationProblem(oracle=oracle, is_good_state=0)
#print(problem.grover_operator.decompose().draw(output='text'))

permutation = Permutation(oracle.num_qubits).to_gate()
grover = GroverOperator(oracle=oracle, state_preparation=problem.state_preparation).to_gate()

#backend = Aer.get_backend('qasm_simulator')
circuit = QuantumCircuit(oracle.num_qubits, 2)
circuit.h(range(oracle.num_qubits))
circuit.append(permutation, range(oracle.num_qubits))
circuit.append(oracle, range(oracle.num_qubits))
for i in range(1):
    circuit.append(grover, range(oracle.num_qubits))

#circuit = grover.construct_circuit(problem, measurement=True)
circuit.measure_all()
print(circuit.draw(output='text'))

with Session(service=service, backend="ibmq_qasm_simulator") as session:
    sampler = Sampler(session=session, options=options)
    job = sampler.run(circuits=circuit)
    print(f"Job ID is {job.job_id()}")
    print(f"Job result is {job.result()}")