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

def main: (bool, []u8, []u8, []u8, []u8, []u8, []u8) =
    let batchsize = 64i64
    let boolen = [0u8, 1u8] in
    let input = [0u8, 1u8, 2u8, 3u8, 4u8, 5u8, 6u8, 7u8, 8u8, 9u8, 10u8, 11u8, 12u8, 13u8, 14u8, 15u8] in
    --let target = [0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8] in
    let target = [10u8, 10u8, 10u8, 10u8, 10u8, 10u8, 10u8, 10u8, 5u8, 5u8, 5u8, 5u8, 5u8, 5u8, 6u8, 7u8] in
    --let target = [0u8, 1u8, 2u8, 3u8, 0u8, 5u8, 6u8, 7u8, 8u8, 9u8, 10u8, 11u8, 12u8, 13u8, 14u8, 15u8] in

    let depth = 5000i32 in

    let (precalc, idconv) =
    (unzip2 (flatten (flatten (flatten (map (\(s1: u8) ->
        map (\(s2: u8) ->
            map (\(c1: u8) ->
                map (\(c2: u8) ->
                    ((map (\(inputx: u8) ->
                        (layer inputx s1 s2 (bool.u8 c1) (bool.u8 c2))
                    ) input), [s1, s2, c1, c2])
                ) boolen
            ) boolen
        ) input
    ) input))))) in

    --let iotalen = (iota (1024/batchsize)) in

    --let precalcindc = (indices precalc) in

    --let indcpre = map (\(l: i64) -> (map (\(i: i64) -> (i+(batchsize*l))) (iota batchsize))) iotalen

    --let indc = (flatten (flatten (flatten (flatten (flatten (map (\(l1: i64) ->
    --    map (\(l2: i64) ->
    --        map (\(l3: i64) ->
    --            map (\(l4: i64) ->
    --                map (\(l5: i64) ->
    --                    map (\(l6: i64) ->
    --                        [indcpre[l1], indcpre[l2], indcpre[l3], indcpre[l4], indcpre[l5], indcpre[l6]]
    --                    ) iotalen
    --                ) iotalen
    --            ) iotalen
    --        ) iotalen
    --    ) iotalen
    --) iotalen)))))) in
    let (i1, i2, i3, i4, i5, i6, triplayer1, triplayer2, triplayer3, triplayer4, triplayer5, triplayer6, triplayer7) =
    loop (i1, i2, i3, i4, i5, i6, res1, res2, res3, res4, res5, res6, res7) = (0i64, 0i64, 0i64, 0i64, 0i64, 0i64, false, 0i16, 0i16, 0i16, 0i16, 0i16, 0i16) while ((i1 < batchsize) || res1) do
    let (i2, i3, i4, i5, i6, triplayer1, triplayer2, triplayer3, triplayer4, triplayer5, triplayer6, triplayer7) =
    loop (i2, i3, i4, i5, i6, res1, res2, res3, res4, res5, res6, res7) = (0i64, 0i64, 0i64, 0i64, 0i64, false, 0i16, 0i16, 0i16, 0i16, 0i16, 0i16) while ((i2 < batchsize) || res1) do
    let (i3, i4, i5, i6, triplayer1, triplayer2, triplayer3, triplayer4, triplayer5, triplayer6, triplayer7) =
    loop (i3, i4, i5, i6, res1, res2, res3, res4, res5, res6, res7) = (0i64, 0i64, 0i64, 0i64, false, 0i16, 0i16, 0i16, 0i16, 0i16, 0i16) while ((i3 < batchsize) || res1) do
    let (i4, i5, i6, triplayer1, triplayer2, triplayer3, triplayer4, triplayer5, triplayer6, triplayer7) =
    loop (i4, i5, i6, res1, res2, res3, res4, res5, res6, res7) = (0i64, 0i64, 0i64, false, 0i16, 0i16, 0i16, 0i16, 0i16, 0i16) while ((i4 < batchsize) || res1) do
    let (i5, i6, triplayer1, triplayer2, triplayer3, triplayer4, triplayer5, triplayer6, triplayer7) =
    loop (i5, i6, res1, res2, res3, res4, res5, res6, res7) = (0i64, 0i64, false, 0i16, 0i16, 0i16, 0i16, 0i16, 0i16) while ((i5 < batchsize) || res1) do
        let (i6, triplayer1, triplayer2, triplayer3, triplayer4, triplayer5, triplayer6, triplayer7) =
        loop (i6, res1, res2, res3, res4, res5, res6, res7) = (0i64, false, 0i16, 0i16, 0i16, 0i16, 0i16, 0i16) while ((i6 < batchsize) || res1) do
            let (triplayer1, triplayer2) =
            (unzip (flatten (flatten (flatten (flatten (flatten (map (\(l1: i64) ->
                map (\(l2: i64) ->
                    map (\(l3: i64) ->
                        map (\(l4: i64) ->
                            map (\(l5: i64) ->
                                map (\(l6: i64) ->
                                    ((layerp precalc l1 (layerp precalc l2 (layerp precalc l3 (layerp precalc l4 (layerp precalc l5 (layerp precalc l6 input))))) == target), [i16.i64 l1, i16.i64 l2, i16.i64 l3, i16.i64 l4, i16.i64 l5, i16.i64 l6])
                                ) (map (\(i: i64) -> (i+(batchsize*i6))) (iota batchsize))
                            ) (map (\(i: i64) -> (i+(batchsize*i5))) (iota batchsize))
                        ) (map (\(i: i64) -> (i+(batchsize*i4))) (iota batchsize))
                    ) (map (\(i: i64) -> (i+(batchsize*i3))) (iota batchsize))
                ) (map (\(i: i64) -> (i+(batchsize*i2))) (iota batchsize))
            ) (map (\(i: i64) -> (i+(batchsize*i1))) (iota batchsize))))))))) in

            let getidx = (findidx true triplayer1) in

            (i6+1, triplayer1[getidx], triplayer2[getidx, 0], triplayer2[getidx, 1], triplayer2[getidx, 2], triplayer2[getidx, 3], triplayer2[getidx, 4], triplayer2[getidx, 5]) in
        (i5+1, i6, triplayer1, triplayer2, triplayer3, triplayer4, triplayer5, triplayer6, triplayer7) in
        (i4+1, i5, i6, triplayer1, triplayer2, triplayer3, triplayer4, triplayer5, triplayer6, triplayer7) in
        (i3+1, i4, i5, i6, triplayer1, triplayer2, triplayer3, triplayer4, triplayer5, triplayer6, triplayer7) in
        (i2+1, i3, i4, i5, i6, triplayer1, triplayer2, triplayer3, triplayer4, triplayer5, triplayer6, triplayer7) in
        (i1+1, i2, i3, i4, i5, i6, triplayer1, triplayer2, triplayer3, triplayer4, triplayer5, triplayer6, triplayer7) in
        --(unzip4(triplayer))[0] in
        --(3u8, [0u8, 0u8, 0u8], true) in

    (triplayer1, idconv[triplayer2], idconv[triplayer3], idconv[triplayer4], idconv[triplayer5], idconv[triplayer6], idconv[triplayer7])
    --batch[0][0][0][0][0][0][0][0][0][0][0][0]
    -- loop () for i in batch
