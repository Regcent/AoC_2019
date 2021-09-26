import time
import math
from typing import Union

def run_script(filepath: str) -> Union[int, str, float, bool]:
    with open(filepath, "r") as f:
        raw_data = f.read()
    return main_function(raw_data)

def main_function(raw_data: str) -> Union[int, str, float, bool]:
    start_time = time.time()
    
    result = your_script(raw_data)

    elapsed_time = time.time() - start_time
    print(f"Time elapsed : {elapsed_time}s")
    return result

def your_script(raw_data: str) -> Union[int, str, float, bool]:
    modules = [int(i) for i in raw_data.split("\n")]
    total = 0
    for val in modules:
        total += calculate_fuel_part_1(int(val))
    print(f"Part 1 : {total}")
    total = 0
    for val in modules:
        total += calculate_fuel_part_2(int(val))
    return total

def calculate_fuel_part_1(mass: int) -> int:
    return mass // 3 - 2

def calculate_fuel_part_2(mass: int) -> int:
    total = 0
    fuel_mass = mass // 3 - 2
    while fuel_mass > 0:
        total += fuel_mass
        fuel_mass = fuel_mass // 3 - 2
    return total

if __name__ == "__main__":
    print(run_script("input.txt"))