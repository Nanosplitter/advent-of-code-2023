from collections import defaultdict, Counter
from functools import cache
import sys

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

def node_default():
    return None

class Node:
    def __init__(self, position, symbol):
        self.position = position
        self.symbol = symbol
        self.dist_from_start = None
        self.neighbors = []
        
    def find_neighbors(self, board):
        if len(self.neighbors) > 0:
            return self.neighbors
        
        neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None}
        
        for direction in [UP, DOWN, LEFT, RIGHT]:
            check_position = (self.position[0] + direction[0], self.position[1] + direction[1])
            if check_position in board.nodes:
                check_node = board.nodes[check_position]
                if check_node is not None and check_node.symbol != "#":
                    neighbors[direction] = check_node
        
        self.neighbors = neighbors
        return neighbors
    
    
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.start_position = None
        self.end_position = None
        self.nodes = defaultdict(node_default)
    
    def set_node(self, node):
        self.nodes[node.position] = node
    
    def set_start_position(self, position):
        self.start_position = position
        self.nodes[position].symbol = "S"
    
    def set_end_position(self, position):
        self.end_position = position
        self.nodes[position].symbol = "E"
    
    def find_path(self):
        path = []
        current_node = self.nodes[self.start_position]
        while current_node.position != self.end_position:
            current_node.dist_from_start = len(path)
            path.append(current_node)
            for direction, neighbor in current_node.find_neighbors(self).items():
                if neighbor is not None and neighbor.dist_from_start is None:
                    current_node = neighbor
                    break
                
        current_node.dist_from_start = len(path)
        path.append(current_node)
        return path

def part1(board):
    
    path = board.find_path()
    
    shortcuts = []
    
    counter = 0
    
    for node in path:
        counter += 1
        print(f"[{counter}/{len(path)}] {node.position}")
        for target_node in path:
            distance = abs(node.position[0] - target_node.position[0]) + abs(node.position[1] - target_node.position[1])
            if distance <= 20 and target_node.dist_from_start > node.dist_from_start + distance:
                shortcuts.append(target_node.dist_from_start - node.dist_from_start - distance)
    
    shortcuts = sorted(shortcuts, reverse=True)
    
    shortcut_counter = sorted(Counter(shortcuts).items(), key=lambda x: x[0], reverse=True)
    
    return sum([shortcut[1] for shortcut in shortcut_counter if shortcut[0] >= 100])

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            sys.exit(1)

        input_file = sys.argv[1]

        with open(input_file) as f:
            instructions = [line.strip() for line in f.readlines()]

            sys.setrecursionlimit(1000000)

            board = Board(len(instructions[0]), len(instructions))
            for row in range(len(instructions)):
                for col in range(len(instructions[row])):
                    board.set_node(Node((row, col), instructions[row][col]))
                    if instructions[row][col] == "S":
                        board.set_start_position((row, col))
                    elif instructions[row][col] == "E":
                        board.set_end_position((row, col))
            
            print(part1(board))
    except KeyboardInterrupt:
        print("Execution interrupted by user.")
        sys.exit(1)