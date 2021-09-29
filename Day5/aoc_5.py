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
    program = [int(i) for i in raw_data.split(",")]
    execute_intcode_program(program)
    return 0    
    
def execute_intcode_program(program: list):
    ptr = 0
    while ptr < len(program):
        ptr = perform_operation(program, ptr)
        if ptr == -1:
            break

def perform_operation(program: list, ptr: int) -> int:
    instruction = program[ptr]
    opcode = instruction % 100
    p1_mode = (instruction // 100) % 10
    p2_mode = (instruction // 1000) % 10
    p3_mode = instruction // 10000
    if opcode == 1:
        return perform_add(program, ptr, p1_mode, p2_mode, p3_mode)
    elif opcode == 2:
        return perform_multiply(program, ptr, p1_mode, p2_mode, p3_mode)
    elif opcode == 3:
        return perform_input(program, ptr, p1_mode)
    elif opcode == 4:
        return perform_print(program, ptr, p1_mode)
    elif opcode == 5:
        return perform_jump_if_true(program, ptr, p1_mode, p2_mode)
    elif opcode == 6:
        return perform_jump_if_false(program, ptr, p1_mode, p2_mode)
    elif opcode == 7:
        return perform_less_than(program, ptr, p1_mode, p2_mode, p3_mode)
    elif opcode == 8:
        return perform_equals(program, ptr, p1_mode, p2_mode, p3_mode)
    elif opcode == 99:
        return -1
    else: 
        print(f"Issue, unknown opcode {opcode} in instruction {instruction}")
    
def perform_add(program: list, ptr: int, p1_mode: int, p2_mode: int, p3_mode: int) -> None:
    print(f"Add with modes {p1_mode}, {p2_mode}, {p3_mode}")
    p1 = parse_parameter(program, ptr + 1, p1_mode)
    p2 = parse_parameter(program, ptr + 2, p2_mode)
    p3 = parse_address(program, ptr + 3, p3_mode)
    program[p3] = p1 + p2
    return ptr + 4

def perform_multiply(program: list, ptr: int, p1_mode: int, p2_mode: int, p3_mode: int) -> None:
    print(f"Multiply with modes {p1_mode}, {p2_mode}, {p3_mode}")
    p1 = parse_parameter(program, ptr + 1, p1_mode)
    p2 = parse_parameter(program, ptr + 2, p2_mode)
    p3 = parse_address(program, ptr + 3, p3_mode)
    program[p3] = p1 * p2
    return ptr + 4

def perform_input(program: list, ptr: int, p1_mode: int) -> None:
    print(f"Input with mode {p1_mode}")
    p1 = parse_address(program, ptr + 1, p1_mode)
    program[p1] = int(input())
    return ptr + 2

def perform_print(program: list, ptr: int, p1_mode: int) -> None:
    print(f"Print with mode {p1_mode}")
    p1 = parse_address(program, ptr + 1, p1_mode)
    print(program[p1])
    return ptr + 2

def perform_jump_if_true(program: list, ptr: int, p1_mode: int, p2_mode: int) -> None:
    print(f"Jump if True with modes {p1_mode}, {p2_mode}")
    p1 = parse_parameter(program, ptr + 1, p1_mode)
    p2 = parse_parameter(program, ptr + 2, p2_mode)
    if p1 != 0:
        return p2
    else:
        return ptr + 3

def perform_jump_if_false(program: list, ptr: int, p1_mode: int, p2_mode: int) -> None:
    print(f"Jump if False with modes {p1_mode}, {p2_mode}")
    p1 = parse_parameter(program, ptr + 1, p1_mode)
    p2 = parse_parameter(program, ptr + 2, p2_mode)
    if p1 == 0:
        return p2
    else:
        return ptr + 3

def perform_less_than(program: list, ptr: int, p1_mode: int, p2_mode: int, p3_mode: int) -> None:
    print(f"Less than with modes {p1_mode}, {p2_mode}, {p3_mode}")
    p1 = parse_parameter(program, ptr + 1, p1_mode)
    p2 = parse_parameter(program, ptr + 2, p2_mode)
    p3 = parse_address(program, ptr + 3, p3_mode)
    program[p3] = 1 if p1 < p2 else 0
    return ptr + 4

def perform_equals(program: list, ptr: int, p1_mode: int, p2_mode: int, p3_mode: int) -> None:
    print(f"Equals with modes {p1_mode}, {p2_mode}, {p3_mode}")
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