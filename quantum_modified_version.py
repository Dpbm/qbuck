import sys

import pandas as pd

from quantum_utils import get_circuit_image, run_quantum_version
from constants import QUANTUM_MODIFIED_VERSION_FILE,MODIFIED_AER_VENV_LIB_PATH


if __name__ == "__main__":
    print("Updating libraries...")
    sys.path.insert(0, MODIFIED_AER_VENV_LIB_PATH)
    print("new path: ", sys.path)

    from qiskit_aer import AerSimulator
    from qiskit_aer.primitives import SamplerV2


    df = pd.DataFrame(columns=("eval_i", "winner", "strategy", "total", "rounds"))
    print("Simulating...")
    backend = AerSimulator()
    sampler = SamplerV2.from_backend(backend)
    run_quantum_version(df, QUANTUM_MODIFIED_VERSION_FILE, (backend,sampler))
