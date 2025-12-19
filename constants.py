import os

CLASSICAL_FILES = ('classical-results-no-seed.csv', 'classical-results-with-seed.csv', 'classical-results-cpp-random-seed.csv', 'classical-results-cpp-with-seed.csv')
QUANTUM_DEFAULT_VERSION_FILE = "quantum-results-regular.csv"
QUANTUM_MODIFIED_VERSION_FILE = "quantum-results-modified.csv"
QUANTUM_NOISY_VERSION_FILE_TORINO = "quantum-results-noisy-torino.csv"
QUANTUM_NOISY_VERSION_FILE_FEZ = "quantum-results-noisy-fez.csv"

QUANTUM_FILES = (QUANTUM_DEFAULT_VERSION_FILE, QUANTUM_MODIFIED_VERSION_FILE, QUANTUM_NOISY_VERSION_FILE_TORINO, QUANTUM_NOISY_VERSION_FILE_FEZ)
ALL_FILES = (*CLASSICAL_FILES, *QUANTUM_FILES)
LABELS = ("classical-random", "classical-random-seed", "cpp-random-seed", "cpp", "quantum-regular", "quantum-modified", "quantum-noisy-torino", "quantum-noisy-fez")

TOTAL_RUNS = 1000

MODIFIED_AER_VENV_LIB_PATH = os.path.join(os.getcwd(), "modified-aer-venv", "lib", "python3.12", "site-packages")

TARGET_ASSETS_FOLDER = os.path.join(os.getcwd(), "assets")
