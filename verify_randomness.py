import random

from constants import TOTAL_RUNS

def check_random_seed():
    print("Checking random seed...")

    versions = set()
    random.seed(42)

    for _ in range(TOTAL_RUNS):
        data_to_choose = ["blank", "blank", "live"]
        current = ""

        while len(data_to_choose) > 0:
            selected = random.choice(data_to_choose)
            data_to_choose.remove(selected)
            current += selected
            
        versions.add(current)

    print("results: ", versions)
    assert len(versions) > 1, "Failed on random seed, only one combination"

def check_static_seed():
    print("Checking static seed...")

    versions = set()
    for _ in range(TOTAL_RUNS):
        random.seed(42)
        data_to_choose = ["blank", "blank", "live"]
        current = ""

        while len(data_to_choose) > 0:
            selected = random.choice(data_to_choose)
            data_to_choose.remove(selected)
            current += selected
            
        versions.add(current)

    print("results: ", versions)
    assert len(versions) == 1, "Failed on static seed, more than one combination"




if __name__ == "__main__":
    check_random_seed()
    check_static_seed()
