from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

print("Setup circuit...")
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0,1)
qc.measure_all()

print("Setup simulator...")
sim = AerSimulator()

print("Run job...")
job = sim.run(qc, shots=1000)

print("Getting results...")
result = job.result().get_counts()
print(result)

