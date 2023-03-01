def findidx [n] (e:bool) (xs:[n]bool) : i64 =
    let es = map2 (\(x: bool) (i: i64) -> if x==e then i else n) xs (iota n)
    let res = reduce i64.min n es
    in if res == n then -1i64 else res

def comperator (x:u8) (s:u8) (m:bool):u8 =
    if s > x then 0 else
    if m then x - s
    else x

def layer (x:u8) (s1:u8) (s2:u8) (c1:bool) (c2:bool):u8 =
    let xc1 = comperator x s1 c1 in
    let xc2 = comperator s2 x c2 in
    if xc1 > xc2 then xc1 else xc2

def layerp (precalc:[][]u8) (precalcid:i64) (x:[]u8):[]u8 =
    map (\(inputx: u8) ->
        precalc[precalcid, (i64.u8 inputx)]
    ) x

def main: (bool, i16, i16, i16) =
    let boolen = [0u8, 1u8] in
    let input = [0u8, 1u8, 2u8, 3u8, 4u8, 5u8, 6u8, 7u8, 8u8, 9u8, 10u8, 11u8, 12u8, 13u8, 14u8, 15u8] in
    let target = [0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8] in
    --let target = [10u8, 10u8, 10u8, 10u8, 10u8, 10u8, 10u8, 10u8, 5u8, 5u8, 5u8, 5u8, 5u8, 5u8, 6u8, 7u8] in
    --let target = [0u8, 1u8, 2u8, 3u8, 0u8, 5u8, 6u8, 7u8, 8u8, 9u8, 10u8, 11u8, 12u8, 13u8, 14u8, 15u8] in

    let depth = 5000i32 in

    let precalc =
    (flatten (flatten (flatten (map (\(s1: u8) ->
        map (\(s2: u8) ->
            map (\(c1: u8) ->
                map (\(c2: u8) ->
                    map (\(inputx: u8) ->
                        layer inputx s1 s2 (bool.u8 c1) (bool.u8 c2)
                    ) input
                ) boolen
            ) boolen
        ) input
    ) input)))) in

    let precalcindc = (indices precalc) in

    let (triplayer1, triplayer2, triplayer3, triplayer4) =
    --loop (depth, res, found) = (3u8, [0u8, 0u8, 0u8], false) while found == false do
    loop (res1, res2, res3, res4) = (false, 0i16, 0i16, 0i16) for i < 1 do
        let (triplayer1, triplayer2, triplayer3, triplayer4) =
        (unzip4 (flatten (flatten (map (\(l1: i64) ->
            map (\(l2: i64) ->
                map (\(l3: i64) ->
                    ((layerp precalc l1 (layerp precalc l2 (layerp precalc l3 input)) == target), i16.i64 l1, i16.i64 l2, i16.i64 l3)
                ) precalcindc
            ) precalcindc
        ) precalcindc)))) in

        let getidx = (findidx true triplayer1) in

        (triplayer1[getidx], triplayer2[getidx], triplayer3[getidx], triplayer4[getidx]) in
        --(unzip4(triplayer))[0] in
        --(3u8, [0u8, 0u8, 0u8], true) in

    (triplayer1, triplayer2, triplayer3, triplayer4)
    --batch[0][0][0][0][0][0][0][0][0][0][0][0]
    -- loop () for i in batch
