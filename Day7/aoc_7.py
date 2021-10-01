import time
from typing import Union
from copy import deepcopy
from itertools import permutations
from queue import Queue

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
    #print(f"Part 1 : {solve_part_1(program)}")
    print(f"Part 2 : {solve_part_2(program)}")

def solve_part_1(program: list) -> int:
    max_thrust = 0
    for combination in permutations(list(range(5))):
        amplifiers = [deepcopy(program) for i in range(5)]
        output = [0]
        ptrs = [0 for i in range(5)]
        for i in range(5):
            inputs = [combination[i], output[0]]
            ptrs[i] = execute_intcode_program(amplifiers[i], ptrs[i], inputs, output)
        if output[0] > max_thrust:
            max_thrust = output[0]
    return max_thrust

def solve_part_2(program: list) -> int:
    max_thrust = 0
    for combination in permutations(list(range(5, 10))):
        amplifiers = [deepcopy(program) for i in range(5)]
        output = [0]
        ptrs = [0 for i in range(5)]
        first_turn = True
        while program[ptrs[4]] != 99:
            for i in range(5):
                if first_turn:
                    inputs = [combination[i], output[0]]
                else:
                    inputs = [output[0]]
                print(ptrs[i])
                ptrs[i] = execute_intcode_program(amplifiers[i], ptrs[i], inputs, output)
                print(ptrs[i])
            first_turn = False
        print("Finished one")
        if output[0] > max_thrust:
            max_thrust = output[0]
    return max_thrust

def execute_intcode_program(program: list, ptr: int, inputs: list, output: list) -> int:
    while ptr < len(program):
        (pause, ptr) = perform_operation(program, ptr, inputs, output)
        if pause:
            break
    return ptr

def perform_operation(program: list, ptr: int, inputs: list, output: list) -> (bool, int):
    instruction = program[ptr]
    opcode = instruction % 100
    p1_mode = (instruction // 100) % 10
    p2_mode = (instruction // 1000) % 10
    p3_mode = instruction // 10000
    if opcode == 1:
        return (False, perform_add(program, ptr, p1_mode, p2_mode, p3_mode))
    elif opcode == 2:
        return (False, perform_multiply(program, ptr, p1_mode, p2_mode, p3_mode))
    elif opcode == 3:
        return (False, perform_input(program, ptr, p1_mode, inputs))
    elif opcode == 4:
        return (True, perform_output(program, ptr, p1_mode, output))
    elif opcode == 5:
        return (False, perform_jump_if_true(program, ptr, p1_mode, p2_mode))
    elif opcode == 6:
        return (False, perform_jump_if_false(program, ptr, p1_mode, p2_mode))
    elif opcode == 7:
        return (False, perform_less_than(program, ptr, p1_mode, p2_mode, p3_mode))
    elif opcode == 8:
        return (False, perform_equals(program, ptr, p1_mode, p2_mode, p3_mode))
    elif opcode == 99:
        print("Pausing")
        return (True, ptr)
    else: 
        print(f"Issue, unknown opcode {opcode} in instruction {instruction}")
    
def perform_add(program: list, ptr: int, p1_mode: int, p2_mode: int, p3_mode: int) -> None:
    p1 = parse_parameter(program, ptr + 1, p1_mode)
    p2 = parse_parameter(program, ptr + 2, p2_mode)
    p3 = parse_address(program, ptr + 3, p3_mode)
    program[p3] = p1 + p2
    return ptr + 4

def perform_multiply(program: list, ptr: int, p1_mode: int, p2_mode: int, p3_mode: int) -> None:
    p1 = parse_parameter(program, ptr + 1, p1_mode)
    p2 = parse_parameter(program, ptr + 2, p2_mode)
    p3 = parse_address(program, ptr + 3, p3_mode)
    program[p3] = p1 * p2
    return ptr + 4

def perform_input(program: list, ptr: int, p1_mode: int, inputs: int) -> None:
    p1 = parse_address(program, ptr + 1, p1_mode)
    program[p1] = inputs.pop(0)
    return ptr + 2

def perform_output(program: list, ptr: int, p1_mode: int, output: list) -> None:
    p1 = parse_address(program, ptr + 1, p1_mode)
    output[0] = program[p1]
    return ptr + 2

def perform_jump_if_true(program: list, ptr: int, p1_mode: int, p2_mode: int) -> None:
    p1 = parse_parameter(program, ptr + 1, p1_mode)
    p2 = parse_parameter(program, ptr + 2, p2_mode)
    if p1 != 0:
        return p2
    else:
        return ptr + 3

def perform_jump_if_false(program: list, ptr: int, p1_mode: int, p2_mode: int) -> None:
    p1 = parse_parameter(program, ptr + 1, p1_mode)
    p2 = parse_parameter(program, ptr + 2, p2_mode)
    if p1 == 0:
        return p2
    else:
        return ptr + 3

def perform_less_than(program: list, ptr: int, p1_mode: int, p2_mode: int, p3_mode: int) -> None:
    p1 = parse_parameter(program, ptr + 1, p1_mode)
    p2 = parse_parameter(program, ptr + 2, p2_mode)
    p3 = parse_address(program, ptr + 3, p3_mode)
    program[p3] = 1 if p1 < p2 else 0
    return ptr + 4

def perform_equals(program: list, ptr: int, p1_mode: int, p2_mode: int, p3_mode: int) -> None:
    p1 = parse_parameter(program, ptr + 1, p1_mode)
    p2 = parse_parameter(program, ptr + 2, p2_mode)
    p3 = parse_address(program, ptr + 3, p3_mode)
    program[p3] = 1 if p1 == p2 else 0
    return ptr + 4

def parse_parameter(program: list, ptr: int, mode: int) -> int:
    if mode == 0:
        return program[program[ptr]]
    elif mode == 1:
        return program[ptr]

def parse_address(program: list, ptr: int, mode: int) -> int:
    if mode == 0:
        return program[ptr]
    elif mode == 1:
        return ptr

if __name__ == "__main__":
    print(run_script("input.txt"))