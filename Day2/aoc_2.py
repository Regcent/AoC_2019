import time
from typing import Union
from copy import deepcopy

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
    program = [int(i) for i in raw_data.split(",")]
    part1_prog = deepcopy(program)
    execute_program_part_1(part1_prog)
    print(f"Part 1 : {part1_prog[0]}")
    print(f"Part 2 : {execute_program_part_2(program)}")
    return

def execute_program_part_1(program: list):
    program[1] = 12
    program[2] = 2
    execute_intcode_program(program)

def execute_program_part_2(program: list):
    for i in range(100):
        for j in range(100):
            test_prog = deepcopy(program)
            test_prog[1] = i
            test_prog[2] = j
            execute_intcode_program(test_prog)
            if test_prog[0] == 19690720:
                return 100 * i + j

def execute_intcode_program(program: list):
    for i in range(0, len(program), 4):
        if program[i] == 1:
            program[program[i + 3]] = program[program[i + 1]] + program[program[i + 2]]
        elif program[i] == 2:
            program[program[i + 3]] = program[program[i + 1]] * program[program[i + 2]]
        elif program[i] == 99:
            return
        else:
            print(f"Unexpected value {program[i]}")
            
if __name__ == "__main__":
    print(run_script("input.txt"))