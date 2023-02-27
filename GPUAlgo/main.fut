def comperator (x:u8) (s:u8) (m:bool):u8 =
    if m then
        if x > s then x - s else 0
    else
        if x > s then x else 0

def layer (x:u8) (s1:u8) (s2:u8) (c1:bool) (c2:bool):u8 =
    let xc1 = comperator x s1 c1 in
    let xc2 = comperator s2 x c2 in
    if xc1 > xc2 then xc1 else xc2

def main: []u8 =
    let x = [1u8,6u8] in
    let s1 = [3u8,10u8] in
    let s2 = [7u8,15u8] in
    let c1 = [false, true] in
    let c2 = [true, true] in
    map5 (layer) x s1 s2 c1 c2
