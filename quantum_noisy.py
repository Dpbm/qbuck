import os

from dotenv import load_dotenv
import pandas as pd

from qiskit_ibm_runtime import QiskitRuntimeService

from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2

from quantum_utils import run_quantum_version
from constants import QUANTUM_NOISY_VERSION_FILE_TORINO, QUANTUM_NOISY_VERSION_FILE_FEZ

if __name__ == "__main__":
    load_dotenv()
    
    print("Logging into IBM platform...")
    QiskitRuntimeService.save_account(channel="ibm_quantum_platform", token=os.getenv("IBM_KEY"), instance=os.getenv("CRN"), overwrite=True, set_as_default=True)
    service = QiskitRuntimeService()

    torino_backend = service.backend('ibm_torino')
    fez_backend = service.backend('ibm_fez')

    print("BACKENDS: ", torino_backend.name, " ", fez_backend.name)

    for backend,file in zip((torino_backend,fez_backend), (QUANTUM_NOISY_VERSION_FILE_TORINO, QUANTUM_NOISY_VERSION_FILE_FEZ)):
        sim = AerSimulator.from_backend(backend)
        sampler = SamplerV2.from_backend(backend)

        df = pd.DataFrame(columns=("eval_i", "winner", "strategy", "total", "rounds"))
        print("Simulating ", backend.name, "...")
        run_quantum_version(df, file, (sim, sampler))


