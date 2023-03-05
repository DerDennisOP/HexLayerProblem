import random
from itertools import groupby

from numba import jit, cuda
import numpy as np

precalc = None
precalc_rev = None
available_template = []

for i in range(16):
        for j in range(16):
            for k in range(2):
                for l in range(2):
                    available_template.append([i, j, k, l])

def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

class Layer():
    def __init__(self, sfl: int, sfr: int, sbl: int, sbr: int, cl1: bool, cl2: bool, cr1: bool, cr2: bool, cm1: bool, cm2: bool, precalcuate: bool = True):
        self.precalc = precalcuate
        self.precalculate()

        self.sfl = sfl
        self.sfr = sfr
        self.sbl = sbl
        self.sbr = sbr
        self.cl1 = cl1
        self.cl2 = cl2
        self.cr1 = cr1
        self.cr2 = cr2
        self.cm1 = cm1
        self.cm2 = cm2
    
    def __str__(self):
        return f"{self.comperator_str(self.cl1)}{self.sfl}, {self.comperator_str(self.cl2)}{self.sbl}, {self.comperator_str(self.cr1)}{self.sfr}, {self.comperator_str(self.cr2)}{self.sbr}, {self.comperator_str(self.cm1)}-{self.comperator_str(self.cm2)};"
    
    def get_code(self):
        pass
        #return f"{self.s1:x}{self.s2:x}{int(self.c1)}{int(self.c2)}"
    
    def comperator_str(self, m: bool = False) -> str:
        return "*" if m else ""

    def comperator(self, x: int, s: int, m: bool = False) -> int:
            if s > x:
                return 0
            elif m:
                return x - s
            else:
                return x
            
    def comperator2(self, x: int, s1: int, s2: int, m: bool = False) -> int:
        s = s1 if s1 > s2 else s2
        if s > x:
            return 0
        elif m:
            return x - s
        else:
            return x
    
    def get_compid(self):
        return int(self.cl1) + int(self.cl2) * 2 + int(self.cr1) * 4 + int(self.cr2) * 8 + int(self.cm1) * 16 + int(self.cm2) * 32

    def run(self, x: int, y: int, z: int) -> int:
        global precalc_rev
        if self.precalc:
            return (x, y, precalc_rev[x][y][z][self.sfl][self.sfr][self.sbl][self.sbr][self.get_compid][0])
        else:
            cl1 = self.comperator(x, self.sfl, self.cl1)
            cl2 = self.comperator(self.sbl, x, self.cl2)
            cr1 = self.comperator(y, self.sfr, self.cr1)
            cr2 = self.comperator(self.sbr, y, self.cr2)
            cm1 = self.comperator2(z, cl1, cr1, self.cm1)
            cm2 = self.comperator2(cm1, cl2, cr2, self.cm2)
            return (x, y, cm2)
    
    def precalculate(self):
        global precalc, precalc_rev
        if self.precalc and precalc is None:
            precalc = [[] for i in range(16)]
            for i in range(16):
                precalc[i] = [[] for o in range(16)]
                for j in range(16):
                    precalc[i][j] = [[] for o in range(16)]
            
            precalc_rev = [[] for o in range(16)]
            for i in range(16):
                precalc_rev[i] = [[] for o in range(16)]
                for j in range(16):
                    precalc_rev[i][j] = [[] for o in range(16)]
                    for k in range(16):
                        precalc_rev[i][j][k] = [[] for o in range(16)]
                        for l in range(16):
                            precalc_rev[i][j][k][l] = [[] for o in range(16)]
                            for m in range(16):
                                precalc_rev[i][j][k][l][m] = [[] for o in range(16)]
                                for n in range(16):
                                    precalc_rev[i][j][k][l][m][n] = [[] for o in range(16)]
                                    for p in range(16):
                                        precalc_rev[i][j][k][l][m][n][p] = [[] for o in range(63)]


            for x in range(16):
                for y in range(16):
                    for z in range(16):
                        for i in range(16):
                            for j in range(16):
                                for k in range(16):
                                    for l in range(16):
                                        for m in range(63):
                                            n = bin(k)[2:].zfill(6)
                                            n = [bool(int(o)) for o in n]
                                            cl1 = self.comperator(x, i, n[0])
                                            cl2 = self.comperator(k, x, n[1])
                                            cr1 = self.comperator(y, j, n[2])
                                            cr2 = self.comperator(l, y, n[3])
                                            cm1 = self.comperator2(z, cl1, cr1, n[4])
                                            cm2 = self.comperator2(cm1, cl2, cr2, n[5])
                                            precalc[x][y][z][cm2].append([i, j, k, l, m])
                                            precalc_rev[x][y][z][i][j][k][l][m].append(cm2)

            precalc = np.array(precalc)
            precalc_rev = np.array(precalc_rev)

class Function():
    def __init__(self, *args):

        if len(args) == 1:
            if isinstance(args[0], list):
                self.layers = args[0]
            elif isinstance(args[0], str):
                code = args[0].replace(" ", "")
                self.layers = []
                for i in range(0, len(code), 4):
                    self.layers.append(Layer(int(code[i], 16), int(code[i+1], 16), bool(int(code[i+2])), bool(int(code[i+3]))))
            else:
                raise Exception("Invalid argument")
        else:
            raise Exception("Invalid argument")
    
    def __str__(self):
        return " ".join([str(layer) for layer in self.layers])
    
    def get_code(self):
        return " ".join([str(layer.get_code()) for layer in self.layers])
    
    def add_layer(self, layer: Layer, infront: bool = False):
        if infront:
            self.layers.insert(0, layer)
        else:
            self.layers.append(layer)
    
    def remove_layer(self, layer_index: int):
        self.layers.pop(layer_index)
    
    def get_layer(self, layer_index: int) -> Layer:
        return self.layers[layer_index]
    
    def set_layer(self, layer_index: int, layer: Layer):
        self.layers[layer_index] = layer
    
    def set_precalculate(self, precalc: bool):
        for layer in self.layers:
            layer.precalc = precalc

    def run(self, x: int, y: int, z: int) -> int:
        for i in range(len(self.layers)):
            x, y, z = self.layers[i].run(x, y, z)
        return z
    
    def run_all(self) -> list:
        out = []
        for x in range(16):
            out.append([])
        for x in range(16):
            for y in range(16):
                    out[x].append(self.run(x, y, 15))
        return out

def get_random_layer(precalc = True) -> Layer:
    cs = [random.randint(0, 1) == 1 for x in range(6)]
    return Layer(random.randint(0, 15), random.randint(0, 15), random.randint(0, 15), random.randint(0, 15), cs[0], cs[1], cs[2], cs[3], True, True, precalc)

def get_random_function(depth = 7, pass_check = False, non_zero = False, precalc = True) -> Function:
    if pass_check or non_zero:
        while True:
            func = Function([get_random_layer(precalc) for x in range(depth)])
            out = func.run_all()
            
            if (([not 0 in x for x in out].count(False) <= 2) or not non_zero) and ((not all_equal(out)) or not pass_check):
                return func
    else:
        return Function([get_random_layer(precalc) for x in range(depth)])

# get_random_layer()
# print(precalc.shape)

func = get_random_function(depth=5, pass_check=True, precalc=False)
# func = Function("6411 5911 da11")
#func = Function()
#func = Function("8000 1e01 1c01 7f11 0e01")
# func.set_precalculate(False)
print(func)
[print(x) for x in func.run_all()]
exit()

def find_function_dep(output: list):
    global precalc, precalc_rev, available_template
    for o in range(16):
        available_1 = available_template.copy()
        available_1 = [x for x in available_1 if x in precalc[o][output[o]]]
        for t in available_1:
            available_2 = available_template.copy()
            for p in range(16):
                available_2 = [x for x in available_2 if x in precalc[p][precalc_rev[output[p]][t[0]][t[1]][t[2]][t[3]][0]]]
            if len(available_2) > 0:
                return (t, available_2)

def find_function(output: list):
    global precalc, precalc_rev, available_template

    # find output blocks (increment, decrement, set)
    direction = None
    blocks = [[]]
    for i in range(15):
        if output[i] == output[i+1] + 1 and direction != 0:
            direction = 0
            blocks[-1].append(i)
            blocks.append([direction, i])
        elif output[i] == output[i+1] - 1 and direction != 1:
            direction = 1
            blocks[-1].append(i)
            blocks.append([direction, i])
        elif output[i] == output[i+1] and direction != 2:
            direction = 2
            blocks[-1].append(i)
            blocks.append([direction, i])
        elif output[i] != output[i+1] and output[i] != output[i+1] + 1 and output[i] != output[i+1] - 1:
            direction = 3
            blocks[-1].append(i)
            blocks.append([direction, i])
    blocks[-1].append(15)
    blocks.pop(0)

    blocks_cleaned = [blocks[0]]
    for i in range(len(blocks) - 1):
        if abs(output[blocks[i][2]] - output[blocks[i+1][1] + 1]) == 1:
            blocks_cleaned.pop()
            blocks_cleaned.append([blocks[i], blocks[i+1]])
        else:
            blocks_cleaned.append(blocks[i+1])
    print(blocks_cleaned, len(blocks_cleaned))
    return len(blocks_cleaned)

    func = Function([])
    for i in range(len(blocks_cleaned)):
        block = blocks_cleaned[i]
        if isinstance(block[0], list):
            if block[1][0] == 0:
                if i+1 < len(blocks_cleaned) and blocks_cleaned[i+1][0] == 3:
                    func.add_offset_invert_max(block[0][2], 16 - (blocks_cleaned[i+1][2] - blocks_cleaned[i+1][2]))
                # func.add_overwrite_min(output[block[0][1]] - 1, output[block[0][1]] + (block[0][2] - block[0][1]) - 1)
    
    # return func

unit_layer_len = [[13, 13, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 15],      # 2 layers     0,2; 15,*15;
                    [10, 10, 10, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5, 5, 6, 7],   # 3 layers     8,0; *7,*11; *1,5;
                    [5, 5, 4, 2, 2, 2, 2, 2, 8, 9, 10, 11, 12, 13, 14, 15],     # 4 layers     0,1; 8,*6; 0,3; 4,*5;
                    [3, 3, 2, 2, 12, 13, 11, 10, 9, 8, 3, 2, 1, 0, 0, 1],       # 5 layers     4,1; 10,*11; 8,*7; 2,*1; *14,*13;
                    [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0],           # 5 layers     9,*8; *2,*15; 10,*9; 13,*15; *13,*5;
                    [7, 7, 2, 3, 9, 10, 11, 3, 4, 5, 6, 7, 8, 7, 7, 14],        # 6 layers     0,1; 4,*3; 7,*7; 15,*13; *1,*1; 7,*8;
                    [0, 1, 0, 1, 4, 5, 4, 5, 0, 1, 0, 1, 4, 5, 4, 5],           # 5 layers
                    [0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8],           # 5 layers
                    [0, 0, 0, 2, 0, 5, 0, 2, 0, 0, 5, 0, 0, 2, 2, 0],           # 6 layers
                    [0, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1],     # 3 layers
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]]     # 2 layers
unit_layer_len_res = [2, 3, 4, 5, 5, 6, 5, 5, 6, 3, 2]	

func = [find_function(unit_layer_len[x]) == unit_layer_len_res[x] for x in range(len(unit_layer_len))]

if False in func:
    print("UNIT TEST FAILED...")
else:
    print("UNIT TEST PASSED! PARTATADFSDAFXYFSEADFSDFASDFDSFSDFDSFSDSDFADSFADSFSGJPRWETGK!°°°!!")

#func = find_function([13, 13, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 15])
# print(func.run_all())
print(func)
# print(func.get_code())


test_list = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            [14, 13, 12, 11, 10, 9, 8, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            [7, 6, 5, 4, 5, 6, 7, 8, 7, 6, 5, 4, 5, 6, 7, 8],
            [7, 6, 7, 8, 7, 6, 7, 8, 7, 6, 7, 8, 7, 6, 7, 8],
            [7, 8, 7, 8, 7, 8, 7, 8, 7, 8, 7, 8, 7, 8, 7, 8],
            [0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8]]

func = [find_function(test_list[x]) for x in range(len(test_list))]
print(func)