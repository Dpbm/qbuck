import pandas as pd

from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2

from quantum_utils import get_circuit_image,run_quantum_version
from constants import QUANTUM_DEFAULT_VERSION_FILE


if __name__ == "__main__":
    print("Getting circuit image...")
    get_circuit_image()

    df = pd.DataFrame(columns=("eval_i", "winner", "strategy", "total", "rounds"))
    print("Simulating...")
    run_quantum_version(df, QUANTUM_DEFAULT_VERSION_FILE, (AerSimulator(), SamplerV2()))
