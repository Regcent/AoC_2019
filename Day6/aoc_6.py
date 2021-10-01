import time
from typing import Union
from queue import PriorityQueue

class Object:

    def __init__(self, name: str):
        self.name = name
        self.orbiters = []
        self.master = None
        self.orbits = 0

    def add_orbiter(self, orbiter):
        self.orbiters.append(orbiter)
        orbiter.master = self
        orbiter.propagate_orbits(self.orbits + 1)

    def propagate_orbits(self, orbits: int):
        self.orbits = orbits
        for orbiter in self.orbiters:
            orbiter.propagate_orbits(self.orbits + 1)

class Node:

    def __init__(self, previous, distance, current):
        self.previous = previous
        self.distance = distance
        self.current = current
    
    def __lt__(self, other):
        return self.distance < other.distance

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
    objects = {}
    orbits = raw_data.split("\n")
    for orbit in orbits:
        a, b = orbit.split(")")
        if not a in objects:
            objects[a] = Object(a)
        if not b in objects:
            objects[b] = Object(b)
        objects[a].add_orbiter(objects[b])
    total_orbits = 0
    for name in objects:
        total_orbits += objects[name].orbits
    print(f"Part 1: {total_orbits}") 
    
    next_node = Node("", 0, objects["YOU"])
    pq = PriorityQueue()
    while next_node.current.name != "SAN":
        fill_queue(pq, next_node)
        next_node = pq.get()[1]
    print(f"Part 2: {next_node.distance - 2}")

def fill_queue(pq: PriorityQueue, node: Node):
    for orbiter in node.current.orbiters:
        if orbiter.name == node.previous:
            continue
        new = Node(node.current.name, node.distance + 1, orbiter)
        pq.put((new.distance, new))
    if node.current.master:
        if node.current.master.name == node.previous:
            return
        new = Node(node.current.master.name, node.distance + 1, node.current.master)
        pq.put((new.distance, new))

if __name__ == "__main__":
    print(run_script("example.txt"))