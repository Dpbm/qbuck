import os

from dotenv import load_dotenv
import pandas as pd

from qiskit_ibm_runtime import QiskitRuntimeService

from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2

from quantum_utils import run_quantum_version
from constants import QUANTUM_NOISY_VERSION_FILE

if __name__ == "__main__":
    load_dotenv()
    
    print("Logging into IBM platform...")
    QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token=os.getenv("IBM_KEY"), instance=os.getenv("CRN"), overwrite=True, set_as_default=True)
    service = QiskitRuntimeService()

    print("finding best backend...")
    backend = service.least_busy(filters= lambda b : not b.simulator and b.num_qubits >= 9)
    print("found: ",backend.name)

    sim = AerSimulator.from_backend(backend)

    df = pd.DataFrame(columns=("eval_i", "winner", "strategy", "total", "rounds"))
    print("Simulating...")
    run_quantum_version(df, QUANTUM_NOISY_VERSION_FILE, (sim, SamplerV2()))


