import time
from typing import Union

class Wire:

    def __init__(self):
        self.horizontal = {}
        self.vertical = {}
        self.steps = [(0, 0)]
        self.distances = []
        self.x = 0
        self.y = 0
        
    def add_segment(self, target: str):
        direction = target[0]
        distance = int(target[1:])
        if direction == "R":
            self.add_horizontal(distance)
            self.x += distance
        elif direction == "L":
            self.add_horizontal(-distance)
            self.x -= distance
        elif direction == "U":
            self.add_vertical(distance)
            self.y += distance
        elif direction == "D":
            self.add_vertical(-distance)
            self.y -= distance
        else:
            print(f"Unexpected direction {direction}")
        self.steps.append((self.x, self.y))
        self.distances.append(distance)

    def add_horizontal(self, distance: int):
        if self.y not in self.horizontal:
            self.horizontal[self.y] = []
        if distance < 0:
            self.horizontal[self.y].append((self.x + distance, self.x))
        else:
            self.horizontal[self.y].append((self.x, self.x + distance))

    def add_vertical(self, distance: int):
        if self.x not in self.vertical:
            self.vertical[self.x] = []
        if distance < 0:
            self.vertical[self.x].append((self.y + distance, self.y))
        else:
            self.vertical[self.x].append((self.y, self.y + distance))

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
    raw_wire_1, raw_wire_2 = raw_data.split("\n")
    wire_1 = create_wire(raw_wire_1)
    wire_2 = create_wire(raw_wire_2)
    intersections = calculate_intersections(wire_1, wire_2)
    if (0,0) in intersections:
        intersections.remove((0,0))
    print(f"Part 1: {find_min_part_1(intersections)}")
    print(f"Part 2: {find_min_part_2(intersections, wire_1, wire_2)}")

def create_wire(raw_wire: str) -> Wire:
    wire = Wire()
    for target in raw_wire.split(","):
        wire.add_segment(target)
    return wire

def calculate_intersections(wire_1: Wire, wire_2: Wire) -> list:
    intersections = []
    for x in wire_1.vertical:
        for v_segment in wire_1.vertical[x]:
            for y in range(v_segment[0], v_segment[1] + 1):
                if y in wire_2.horizontal:
                    for h_segment in wire_2.horizontal[y]:
                        if x >= h_segment[0] and x <= h_segment[1]:
                            intersections.append((x, y))
    for y in wire_1.horizontal:
        for h_segment in wire_1.horizontal[y]:
            for x in range(h_segment[0], h_segment[1] + 1):
                if x in wire_2.vertical:
                    for v_segment in wire_2.vertical[x]:
                        if y >= v_segment[0] and y <= v_segment[1]:
                            intersections.append((x, y))
    return intersections

def find_min_part_1(intersections: list) -> int:
    min_dist = abs(intersections[0][0]) + abs(intersections[0][1])
    for inter in intersections:
        distance = abs(inter[0]) + abs(inter[1])
        if distance < min_dist:
            min_dist = distance
    return min_dist

def find_min_part_2(intersections: list, wire_1: Wire, wire_2: Wire) -> int:
    min_dist = calculate_delay(intersections[0], wire_1) + calculate_delay(intersections[0], wire_2)
    for inter in intersections:
        delay_1 = calculate_delay(inter, wire_1)
        delay_2 = calculate_delay(inter, wire_2)
        distance = delay_1 + delay_2
        if distance < min_dist:
            min_dist = distance
    return min_dist

def calculate_delay(position: tuple, wire: Wire) -> int:
    delay = 0
    for i in range(len(wire.steps)):
        current_x = wire.steps[i][0]
        current_y = wire.steps[i][1]
        if position[0] == current_x:
            if position[1] <= current_y and wire.steps[i +1][1] < current_y:
                delay += current_y - position[1]
                return delay
            elif position[1] >= current_y and wire.steps[i + 1][1] > current_y:
                delay += position[1] - current_y   
                return delay
        if position[1] == current_y:
            if position[0] <= current_x and wire.steps[i +1][0] < current_x:
                delay += current_x - position[0]
                return delay
            elif position[0] >= current_x and wire.steps[i + 1][0] > current_x:
                delay += position[0] - current_x
                return delay
        delay += wire.distances[i]
    return delay

if __name__ == "__main__":
    print(run_script("input.txt"))