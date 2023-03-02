from queue import Queue

def solve_hex_layer(start, target, layers):
    # start and target are lists of integers representing the starting and target output
    # layers is a list of tuples representing the possible layers, each tuple contains:
    # - the ss of the left barrel
    # - the ss of the right barrel
    # - the mode of the right comparator (0 or 1)
    
    # create a set to store visited states
    visited = []
    
    # create a queue to store states to explore
    queue = Queue()
    
    # add the starting state to the queue
    queue.put((start, []))
    
    while not queue.empty():
        # get the next state to explore
        state, path = queue.get()
        
        # check if we reached the target state
        if state == target:
            return path
        
        # explore all possible next states
        for layer in layers:
            next_state = apply_layer(state, layer)
            
            # check if the next state is valid and not visited before
            if next_state is not None and next_state not in visited:
                visited.append(next_state)
                next_path = path + [layer]
                queue.put((next_state, next_path))
    
    # if we didn't find a solution, return None
    return None

def comperator(x: int, s: int, m: bool = False) -> int:
    if s > x:
        return 0
    elif m:
        return x - s
    else:
        return x

def apply_layer(state, layer):
    # apply a single layer to the state
    left_ss, right_ss, mode1, mode2 = layer
    next_state = []
    for x in state:
        xc1 = comperator(x, left_ss, mode1)
        xc2 = comperator(right_ss, x, mode2)
        next_state.append(xc1 if xc1 >= xc2 else xc2)
    return next_state

start = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
target = [10, 10, 10, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5, 5, 6, 7]
layers = []
for i in range(16):
    for j in range(16):
        for k in range(2):
            for l in range(2):
                layers.append((i, j, k, l))

path = solve_hex_layer(start, target, layers)
print(path)