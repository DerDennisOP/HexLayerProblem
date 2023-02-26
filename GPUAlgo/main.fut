def maina (a: []i32): i32 = reduce (+) 0 a

def main () =
    let x = 0...5 in
    let y = 5...10 in
    reduce (+) 0 (map2 (*) x y)