import time
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
    minimum, maximum = [int(i) for i in raw_data.split("-")]
    part_1_pwds = find_eligible_part_1_passwords(minimum, maximum)
    print(f"Part 1: {len(part_1_pwds)}")
    part_2_pwds = find_eligible_part_2_passwords(part_1_pwds)
    print(f"Part 2: {len(part_2_pwds)}")

def find_eligible_part_1_passwords(minimum: int, maximum: int) -> list:
    pwds = []
    for candidate in range(minimum, maximum + 1):
        if is_eligible(candidate):
            pwds.append(candidate)
    return pwds

def is_eligible(candidate_pwd: int) -> bool:
    str_pwd = str(candidate_pwd)
    return check_growing(str_pwd) and check_duplicate(str_pwd)

def check_duplicate(str_pwd: str) -> bool:
    # Due to growing check, no need to check if the duplicates are adjacent
    for char in str_pwd:
        if str_pwd.count(char) > 1:
            return True
    return False

def check_growing(str_pwd: str) -> bool:
    for i in range(len(str_pwd) - 1):
        if str_pwd[i] > str_pwd[i + 1]: # Use ASCII Ordering here.
            return False
    return True

def find_eligible_part_2_passwords(part_1_pwds: list) -> list:
    pwds = []
    for pwd in part_1_pwds:
        if exactly_two_duplicates(str(pwd)):
            print(pwd)
            pwds.append(pwd)
    return pwds

def exactly_two_duplicates(str_pwd: str) -> bool:
    # The exercise explanation is slightly unclear : what matters is that one group of duplicate is exactly 2-long
    for char in str_pwd:
        if str_pwd.count(char) == 2:
            return True
    return False

if __name__ == "__main__":
    print(run_script("input.txt"))