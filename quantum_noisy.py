import os
from enum import Enum

import pandas as pd

from qiskit_ibm_runtime import QiskitRuntimeService

from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2

from quantum_utils import run_quantum_version
from constants import QUANTUM_NOISY_VERSION_FILE_TORINO, QUANTUM_NOISY_VERSION_FILE_FEZ, IBM_BACKEND_FEZ, IBM_BACKEND_TORINO

class Backends(Enum):
    FEZ=IBM_BACKEND_FEZ
    TORINO=IBM_BACKEND_TORINO

backends_mapping ={
        Backends.FEZ:QUANTUM_NOISY_VERSION_FILE_FEZ,
        Backends.TORINO:QUANTUM_NOISY_VERSION_FILE_TORINO
}

def run_noisy_experiment(selected_backend:Backends):
    print("Logging into IBM platform...")
    service = QiskitRuntimeService(channel="ibm_quantum_platform", token=os.getenv("IBM_KEY"), instance=os.getenv("CRN"))

    backend = service.backend(selected_backend.value)
    print("USING BACKEND: ", backend.name)

    df = pd.DataFrame(columns=("eval_i", "winner", "strategy", "total", "rounds"))
    file = backends_mapping[selected_backend]
    sim = AerSimulator.from_backend(backend)
    sampler = SamplerV2.from_backend(backend)

    run_quantum_version(df, file, (sim,sampler))
        
    print("Finished noisy experiment!")



