import os
from pathlib import Path

DEFAULT_RANDOM_FILE = 'classical-results-no-seed.csv' # default python's random setup
DEFAULT_RANDOM_SEED_FILE = 'classical-results-with-seed.csv' # python's random setting a fixed seed
CPP_FILE = 'classical-results-cpp-with-seed.csv' # cpp with a fixed seed
CPP_RANDOM_FILE = 'classical-results-cpp-random-seed.csv' # cpp random engine with a random seed each time (not the default)

CLASSICAL_FILES = (DEFAULT_RANDOM_FILE, DEFAULT_RANDOM_SEED_FILE, CPP_RANDOM_FILE, CPP_FILE)
QUANTUM_DEFAULT_VERSION_FILE = "quantum-results-regular.csv"
QUANTUM_MODIFIED_VERSION_FILE = "quantum-results-modified.csv"
QUANTUM_NOISY_VERSION_FILE_TORINO = "quantum-results-noisy-torino.csv"
QUANTUM_NOISY_VERSION_FILE_FEZ = "quantum-results-noisy-fez.csv"

QUANTUM_FILES = (QUANTUM_DEFAULT_VERSION_FILE, QUANTUM_MODIFIED_VERSION_FILE, QUANTUM_NOISY_VERSION_FILE_TORINO, QUANTUM_NOISY_VERSION_FILE_FEZ)
ALL_FILES = (*CLASSICAL_FILES, *QUANTUM_FILES)
LABELS = ("python random (random seed)", "python random (static seed)", "cpp (random seed)", "cpp (static seed)", "quantum regular (default AER)", "quantum modified (modified AER - random seed)", "quantum noisy (IBM torino)", "quantum noisy (IBM Fez)")

STRATEGIES_DESCRIPTION = ("Probability Based", "Always Shoot", "50/50", "Always Himself")
TOTAL_STRATEGIES = len(STRATEGIES_DESCRIPTION)

CLASSICAL_PORTION = LABELS[:4]
QUANTUM_PORTION = LABELS[4:]

TOTAL_RUNS = 1000

IBM_BACKEND_FEZ = "ibm_fez"
IBM_BACKEND_TORINO = "ibm_torino"

__CONSTANTS_FILE_FOLDER = Path(__file__).resolve().parents[0]
MODIFIED_AER_VENV_LIB_PATH = os.path.join(__CONSTANTS_FILE_FOLDER, "modified-aer-venv", "lib", "python3.12", "site-packages")
TARGET_ASSETS_FOLDER = os.path.join(__CONSTANTS_FILE_FOLDER, "assets")
