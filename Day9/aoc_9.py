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
    computer = IntcodeComputer()
    computer.execute_program(program)
    return 0    

class IntcodeComputer:

    def __init__(self):
        self.memory = {}
        self.relative_base = 0

    def execute_program(self, program: list):
        self.memory = {}
        self.relative_base = 0
        self.program = program
        ptr = 0
        while ptr < len(program):
            ptr = self.perform_operation(ptr)
            if ptr == -1:
                break

    def perform_operation(self, ptr: int) -> int:
        instruction = self.program[ptr]
        opcode = instruction % 100
        p1_mode = (instruction // 100) % 10
        p2_mode = (instruction // 1000) % 10
        p3_mode = instruction // 10000
        if opcode == 1:
            return self.perform_add(ptr, p1_mode, p2_mode, p3_mode)
        elif opcode == 2:
            return self.perform_multiply(ptr, p1_mode, p2_mode, p3_mode)
        elif opcode == 3:
            return self.perform_input(ptr, p1_mode)
        elif opcode == 4:
            return self.perform_print(ptr, p1_mode)
        elif opcode == 5:
            return self.perform_jump_if_true(ptr, p1_mode, p2_mode)
        elif opcode == 6:
            return self.perform_jump_if_false(ptr, p1_mode, p2_mode)
        elif opcode == 7:
            return self.perform_less_than(ptr, p1_mode, p2_mode, p3_mode)
        elif opcode == 8:
            return self.perform_equals(ptr, p1_mode, p2_mode, p3_mode)
        elif opcode == 9:
            return self.perform_adjust_base(ptr, p1_mode)
        elif opcode == 99:
            return -1
        else: 
            print(f"Issue, unknown opcode {opcode} in instruction {instruction}")
        
    def perform_add(self, ptr: int, p1_mode: int, p2_mode: int, p3_mode: int) -> int:
        print(f"Add with modes {p1_mode}, {p2_mode}, {p3_mode}")
        p1 = self.parse_parameter(ptr + 1, p1_mode)
        p2 = self.parse_parameter(ptr + 2, p2_mode)
        p3 = self.parse_address(ptr + 3, p3_mode)
        self.write_memory(p3, p1 + p2)
        return ptr + 4

    def perform_multiply(self, ptr: int, p1_mode: int, p2_mode: int, p3_mode: int) -> int:
        print(f"Multiply with modes {p1_mode}, {p2_mode}, {p3_mode}")
        p1 = self.parse_parameter(ptr + 1, p1_mode)
        p2 = self.parse_parameter(ptr + 2, p2_mode)
        p3 = self.parse_address(ptr + 3, p3_mode)
        self.write_memory(p3, p1 * p2)
        return ptr + 4

    def perform_input(self, ptr: int, p1_mode: int) -> int:
        print(f"Input with mode {p1_mode}")
        p1 = self.parse_address(ptr + 1, p1_mode)
        self.write_memory(p1, int(input()))
        return ptr + 2

    def perform_print(self, ptr: int, p1_mode: int) -> int:
        print(f"Print with mode {p1_mode}")
        p1 = self.parse_address(ptr + 1, p1_mode)
        print(self.read_memory(p1))
        return ptr + 2

    def perform_jump_if_true(self, ptr: int, p1_mode: int, p2_mode: int) -> int:
        print(f"Jump if True with modes {p1_mode}, {p2_mode}")
        p1 = self.parse_parameter(ptr + 1, p1_mode)
        p2 = self.parse_parameter(ptr + 2, p2_mode)
        if p1 != 0:
            return p2
        else:
            return ptr + 3

    def perform_jump_if_false(self, ptr: int, p1_mode: int, p2_mode: int) -> int:
        print(f"Jump if False with modes {p1_mode}, {p2_mode}")
        p1 = self.parse_parameter(ptr + 1, p1_mode)
        p2 = self.parse_parameter(ptr + 2, p2_mode)
        if p1 == 0:
            return p2
        else:
            return ptr + 3

    def perform_less_than(self, ptr: int, p1_mode: int, p2_mode: int, p3_mode: int) -> int:
        print(f"Less than with modes {p1_mode}, {p2_mode}, {p3_mode}")
        p1 = self.parse_parameter(ptr + 1, p1_mode)
        p2 = self.parse_parameter(ptr + 2, p2_mode)
        p3 = self.parse_address(ptr + 3, p3_mode)
        self.write_memory(p3, 1 if p1 < p2 else 0)
        return ptr + 4

    def perform_equals(self, ptr: int, p1_mode: int, p2_mode: int, p3_mode: int) -> int:
        print(f"Equals with modes {p1_mode}, {p2_mode}, {p3_mode}")
        p1 = self.parse_parameter(ptr + 1, p1_mode)
        p2 = self.parse_parameter(ptr + 2, p2_mode)
        p3 = self.parse_address(ptr + 3, p3_mode)
        self.write_memory(p3, 1 if p1 == p2 else 0)
        return ptr + 4

    def perform_adjust_base(self, ptr: int, p1_mode: int) -> int:
        print(f"Adjust base with mode {p1_mode}")
        p1 = self.parse_parameter(ptr + 1, p1_mode)
        self.relative_base = parameter

    def parse_parameter(self, ptr: int, mode: int) -> int:
        if mode == 0:
            return self.read_memory(self.read_memory(ptr))
        elif mode == 1:
            return self.read_memory(ptr)
        elif mode == 2:
            return self.read_memory(self.read_memory(ptr + self.relative_base))

    def parse_address(self, ptr: int, mode: int) -> int:
        if mode == 0:
            return self.read_memory(ptr)
        elif mode == 1:
            return ptr
        elif mode == 2:
            return self.read_memory(ptr + self.relative_base)
    
    def read_memory(self, ptr: int) -> int:
        if ptr < len(self.program):
            return self.program[ptr]
        if ptr not in self.memory:
            print("UNDEFINED")
        return self.memory[ptr]
        
    def write_memory(self, ptr: int, value: int) -> int:
        if ptr < len(self.program):
            self.program[ptr] = value
            return
        if ptr not in self.memory:
            print("UNDEFINED")
            return
        self.memory[ptr] = value

if __name__ == "__main__":
    print(run_script("input_5.txt"))