import time
from typing import Union

class Layer:

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.data = []

def fill_layer(layer: Layer, raw_data: list, start: int) -> int:
    end = start + layer.width * layer.height
    for i in range(start, end):
        if raw_data[i] == "0":
            layer.counts[0] += 1
        elif raw_data[i] == "1":
            layer.counts[1] += 1
        elif raw_data[i] == "2":
            layer.counts[2] += 1
        elif raw_data[i] == "3":
            layer.counts[3] += 1
        elif raw_data[i] == "4":
            layer.counts[4] += 1
        elif raw_data[i] == "5":
            layer.counts[5] += 1
        elif raw_data[i] == "6":
            layer.counts[6] += 1
        elif raw_data[i] == "7":
            layer.counts[7] += 1
        elif raw_data[i] == "8":
            layer.counts[8] += 1
        elif raw_data[i] == "9":
            layer.counts[9] += 1
        layer.data.append(raw_data[i])    
    return end

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
    width = 25
    height = 6
    layers = parse_image(raw_data, width, height)
    print(len(layers))
    fewest_zero = find_fewest_zero(layers)
    print(f"Part 1: {fewest_zero.counts[1] * fewest_zero.counts[2]}")
    image = decode_image(layers, width, height)
    for i in range(6):
        print(''.join(["  " if image[j] == "0" else "##" for j in range(25*i, 25*(i + 1))]))

def parse_image(raw_data: int, width: int, height: int) -> list:
    ptr = 0
    layers = []
    while ptr < len(raw_data):
        new_layer = Layer(width, height)
        ptr = fill_layer(new_layer, raw_data, ptr)
        layers.append(new_layer)
    return layers

def find_fewest_zero(layers: list) -> Layer:
    min_zero = layers[0].counts[0]
    candidate_layer = layers[0]
    for i in range(1, len(layers)):
        if layers[i].counts[0] < min_zero:
            print("Coucou")
            min_zero = layers[i].counts[0]
            candidate_layer = layers[i]
    return candidate_layer

def decode_image(layers: list, width: int, height: int) -> list:
    image = []
    for i in range(width * height):
        j = 0
        while layers[j].data[i] == "2":
            j += 1
        image.append(layers[j].data[i])
    return image

if __name__ == "__main__":
    print(run_script("input.txt"))