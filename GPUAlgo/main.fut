def comperator (x:u8) (s:u8) (m:bool):u8 =
    if m then
        if x > s then x - s else 0
    else
        if x > s then x else 0

def layer (x:u8) (s1:u8) (s2:u8) (c1:bool) (c2:bool):u8 =
    let xc1 = comperator x s1 c1 in
    let xc2 = comperator s2 x c2 in
    if xc1 > xc2 then xc1 else xc2

--def layerp (precalc:[][][][][]u8) (s1:u8) (s2:u8) (c1:u8) (c2:u8) :[]u8 =
--    precalc[s1][s2][c1][c2]

def main: []u8 =
    let boolen = [0u8, 1u8]
    let input = [0u8, 1u8, 2u8, 3u8, 4u8, 5u8, 6u8, 7u8, 8u8, 9u8, 10u8, 11u8, 12u8, 13u8, 14u8, 15u8] in
    let target = [0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8, 0u8, 8u8] in


    let depth = 5000 in

    --let precalc =
    flatten (map (\(s1: u8) ->
        map (\(s2: u8) ->
            map (\(c1: u8) ->
                map (\(c2: u8) ->
                    map (\(inputx: u8) ->
                        layer inputx s1 s2 u8.bool c1 u8.bool c2
                    ) input
                ) boolen
            ) boolen
        ) input
    ) input)

    map (\(s1l3: u8) ->
        map (\(s2l3: u8) ->
            map (\(c1l3: bool) ->
                map (\(c2l3: bool) ->
                    map (\(s1l2: u8) ->
                        map (\(s2l2: u8) ->
                            map (\(c1l2: bool) ->
                                map (\(c2l2: bool) ->
                                    map (\(s1l1: u8) ->
                                        map (\(s2l1: u8) ->
                                            map (\(c1l1: bool) ->
                                                map (\(c2l1: bool) ->
                                                    (map (\(inputx: u8) ->
                                                        layer (layer (layer inputx s1l3 s2l3 c1l3 c2l3) s1l2 s2l2 c1l2 c2l2) s1l1 s2l1 c1l1 c2l1
                                                    ) input) == target
                                                ) boolen
                                            ) boolen
                                        ) input
                                    ) input
                                ) boolen
                            ) boolen
                        ) input
                    ) input
                ) boolen
            ) boolen
        ) input
    ) input

    --batch[0][0][0][0][0][0][0][0][0][0][0][0]
    -- loop () for i in batch
