import random
from collections import defaultdict

from constants import TOTAL_RUNS

DEFAULT_SEED = 42

def check_random_seed() -> defaultdict :
    print("Checking random seed...")

    results = defaultdict(int)
    random.seed(DEFAULT_SEED)

    for _ in range(TOTAL_RUNS):
        data_to_choose = ["blank", "blank", "live"]
        current = ""

        while len(data_to_choose) > 0:
            selected = random.choice(data_to_choose)
            data_to_choose.remove(selected)
            current += selected
        results[current] += 1

    print("Results: ", results)
    assert len(results.keys()) > 1, "Failed on random seed, only one combination"
    return results

def check_static_seed() -> defaultdict:
    print("Checking static seed...")

    results = defaultdict(int)
    for _ in range(TOTAL_RUNS):
        random.seed(DEFAULT_SEED)
        data_to_choose = ["blank", "blank", "live"]
        current = ""

        while len(data_to_choose) > 0:
            selected = random.choice(data_to_choose)
            data_to_choose.remove(selected)
            current += selected
        results[current] += 1

    print("Results: ", results)
    assert len(results.keys()) == 1, "Failed on static seed, more than one combination"
    return results

def check_random_seed_compare() -> defaultdict:
    print("Checking random seed but randomizing in the middle...")

    results = defaultdict(int)
    random.seed(DEFAULT_SEED)

    for _ in range(TOTAL_RUNS):
        data_to_choose = ["blank", "blank", "live"]
        current = ""

        while len(data_to_choose) > 0:
            selected = random.choice(data_to_choose)
            data_to_choose.remove(selected)
            current += selected
            random.random()
        results[current] += 1

    previous_results = check_random_seed()
    print("Previous Results: ", previous_results)
    print("New Results: ", results)
    assert len(results.keys()) > 1, "Failed on random seed with randomization, only one combination"
    assert results != previous_results, "Failed on random seed with randomization, both dictionaries are the same"
    return results



if __name__ == "__main__":
    check_random_seed()
    print("-"*30)
    check_static_seed()
    print("-"*30)
    check_random_seed_compare()
