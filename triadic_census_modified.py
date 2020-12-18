import pandas as pd
import numpy as np
import time
import networkx as nx
from collections import Counter

TRICODES = (
    1,
    2,
    2,
    3,
    2,
    4,
    6,
    8,
    2,
    6,
    5,
    7,
    3,
    8,
    7,
    11,
    2,
    6,
    4,
    8,
    5,
    9,#
    9,#
    13,
    6,
    10,#
    9,#
    14,
    7,
    14,
    12,
    15,
    2,
    5,
    6,
    7,
    6,
    9,
    10,
    14,
    4,
    9,
    9,
    12,
    8,
    13,
    14,
    15,
    3,
    7,
    8,
    11,
    7,
    12,
    14,
    15,
    8,
    14,
    13,
    15,
    11,
    15,
    15,
    16,
)

#: The names of each type of triad. The order of the elements is
#: important: it corresponds to the tricodes given in :data:`TRICODES`.
TRIAD_NAMES = (
    "003",
    "012",
    "102",
    "021D",
    "021U",
    "021C",
    "111D",
    "111U",
    "030T",#9
    "030C",#10
    "201",
    "120D",#12
    "120U", #13
    "120C", #14
    "210", #15
    "300", #16
)

VALID_TRIAD_NAMES = (
    "030T",
    "030C",
    "120D",
    "120U",
    "120C",
    "210",
    "300",
)


#: A dictionary mapping triad code to triad name.
TRICODE_TO_NAME = {i: TRIAD_NAMES[code - 1] for i, code in enumerate(TRICODES)}


def _tricode(G, v, u, w):
    """Returns the integer code of the given triad.

    This is some fancy magic that comes from Batagelj and Mrvar's paper. It
    treats each edge joining a pair of `v`, `u`, and `w` as a bit in
    the binary representation of an integer.

    """
    return sum(x for u, v, x in combos if v in G[u])

def nodes_by_type(df):
    G = nx.DiGraph()
    G.add_weighted_edges_from(df)
    m = {v: i for i, v in enumerate(G)}
    result = []
    count = 0
    for v in G:
        vnbrs = set(G.pred[v]) | set(G.succ[v])
        for u in vnbrs:
            if m[u] <= m[v]:
                continue
            neighbors = (vnbrs | set(G.succ[u]) | set(G.pred[u])) - {u, v}

            for w in neighbors:
                combos = ((v, u, 1), (u, v, 2), (v, w, 4), (w, v, 8), (u, w, 16), (w, u, 32))
                combos_dict = {1:(v,u),2:(u,v),4:(v,w),8:(w,v),16:(u,w),32:(w,u)}

                if m[u] < m[w] or (
                    m[v] < m[w] < m[u] and v not in G.pred[w] and v not in G.succ[w]
                ):
                    code = sum(x for u, v, x in combos if v in G[u])
                    triadname = TRICODE_TO_NAME[code]

                    if triadname not in VALID_TRIAD_NAMES:
                        pass

                    else:
                        edges = {x: G.get_edge_data(u,v) for u, v, x in combos if v in G[u]}


                        e1 = [e for e in edges if e < 4]
                        e2 = [e for e in edges if (e < 16) and (e > 3)]
                        e3 = [e for e in edges if e > 15]

                        for e1_ in e1:
                            e1_weight = list(edges[e1_]['weight'])
                            e1_weight.append(combos_dict[e1_])
                            for e2_ in e2:
                                e2_weight = list(edges[e2_]['weight'])
                                e2_weight.append(combos_dict[e2_])
                                for e3_ in e3:
                                    e3_weight = list(edges[e3_]['weight'])
                                    e3_weight.append(combos_dict[e3_])

                                    _r = [e1_weight,e2_weight,e3_weight]
                                    _r.sort()


                                    (nodeA, nodeB) = _r[-1][-1]
                                    if nodeB  in _r[1][-1]:
                                        nodeX = list(set(_r[1][-1]) - set([nodeB]))[0]
                                        edge3 = _r[1][1:]
                                        edge2 = _r[0][1:]
                                    else:
                                        nodeX = list(set(_r[0][-1]) - set([nodeB]))[0]
                                        edge3 = _r[0][1:]
                                        edge2 = _r[1][1:]

                                    r = [nodeA, nodeB, nodeX, _r]

                                    if (nodeB, nodeX) == edge3[-1] and (nodeA, nodeX) == edge2[-1]:
                                        # B->X,A->X
                                        # ++ : 3 -+: 4 +-: 7 -- : 8

                                        if edge3[0] == 1 and edge2[0] == 1:
                                            r.append('type3')
                                        elif edge3[0] == -1 and edge2[0] == 1:
                                            r.append('type4')
                                        elif edge3[0] == 1 and edge2[0] == -1:
                                            r.append('type7')
                                        elif edge3[0] == -1 and edge2[0] == -1:
                                            r.append('type8')

                                        else:
                                            r.append('err1')


                                    elif (nodeB, nodeX) != edge3[-1] and (nodeA, nodeX) == edge2[-1]:
                                        # B<-X,A->X
                                        # ++ : 1 -+: 2 +-: 5 -- : 6

                                        if edge3[0] == 1 and edge2[0] == 1:
                                            r.append('type1')
                                        elif edge3[0] == -1 and edge2[0] == 1:
                                            r.append('type2')
                                        elif edge3[0] == 1 and edge2[0] == -1:
                                            r.append('type5')
                                        elif edge3[0] == -1 and edge2[0] == -1:
                                            r.append('type6')

                                        else:
                                            r.append('err2')


                                    elif (nodeB, nodeX) != edge3[-1] and (nodeA, nodeX) != edge2[-1]:
                                        # B<-X,A<-X
                                        # ++ : 9 -+: 10 +-: 13 -- : 14
                                        if edge3[0] == 1 and edge2[0] == 1:
                                            r.append('type9')
                                        elif edge3[0] == -1 and edge2[0] == 1:
                                            r.append('type10')
                                        elif edge3[0] == 1 and edge2[0] == -1:
                                            r.append('type13')
                                        elif edge3[0] == -1 and edge2[0] == -1:
                                            r.append('type14')

                                        else:
                                            r.append('err3')


                                    elif (nodeB, nodeX) == edge3[-1] and (nodeA, nodeX) != edge2[-1]:
                                        # B->X,A<-X
                                        # ++ : 11 -+: 12 +-: 15 -- : 16

                                        if edge3[0] == 1 and edge2[0] == 1:
                                            r.append('type11')
                                        elif edge3[0] == -1 and edge2[0] == 1:
                                            r.append('type12')
                                        elif edge3[0] == 1 and edge2[0] == -1:
                                            r.append('type15')
                                        elif edge3[0] == -1 and edge2[0] == -1:
                                            r.append('type16')

                                        else:
                                            r.append('err4')
                                    else:
                                        r.append('err5')

                                    result.append(r)

    e = int(time.time() - start)
    print('Counting Tridads of {} took {:02d}:{:02d}:{:02d}'.format('Epinions',e // 3600, (e % 3600 // 60), e % 60))
    triads_df = pd.DataFrame(result)
    triads_df = triads_df.rename(columns={0:'NodeA',1:'NodeB',2:'NodeX',3:'detail',4:'type'})
    triads_df['type'] = triads_df['type'].apply(lambda x: int(x[4:]))
    return triads_df[['NodeA', 'NodeB', 'type']]
