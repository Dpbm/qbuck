import os

from dotenv import load_dotenv

from qiskit_ibm_runtime import QiskitRuntimeService

if __name__ == "__main__":
    load_dotenv()

    QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token=os.getenv("IBM_KEY"), instance=os.getenv("CRN"), overwrite=True, set_as_default=True)
    service = QiskitRuntimeService()

    print(service.least_busy(filters= lambda b : not b.simulator and b.num_qubits >= 9))
