import os

CLASSICAL_FILES = ('classical-results-no-seed.csv', 'classical-results-with-seed.csv', 'classical-results-cpp-random-seed.csv', 'classical-results-cpp-with-seed.csv')
QUANTUM_DEFAULT_VERSION_FILE = "quantum-results-regular.csv"
QUANTUM_MODIFIED_VERSION_FILE = "quantum-results-modified.csv"
QUANTUM_NOISY_VERSION_FILE = "quantum-results-noisy.csv"
QUANTUM_FILES = (QUANTUM_DEFAULT_VERSION_FILE, QUANTUM_MODIFIED_VERSION_FILE, QUANTUM_NOISY_VERSION_FILE)
ALL_FILES = (*CLASSICAL_FILES, *QUANTUM_FILES)
LABELS = ("classical-random", "classical-random-seed", "cpp-random-seed", "cpp", "quantum-regular", "quantum-modified", "quanutm-noisy")

TOTAL_RUNS = 1000

MODIFIED_AER_VENV_LIB_PATH = os.path.join(os.getcwd(), "modified-aer-venv", "lib", "python3.12", "site-packages")

TARGET_ASSETS_FOLDER = os.path.join(os.getcwd(), "assets")