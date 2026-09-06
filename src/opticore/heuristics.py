# -*- coding: utf-8 -*-
"""Domain-free route-geometry heuristics (no visit/contract/domain vocabulary).

Verbatim moves from the mainline app (visit-scheduling-optimizer):
- nn2opt_open  <- algos/tsp_engine._nn2opt_open   (NN construction + bounded 2-opt)
- two_opt      <- algos/alns_v3.two_opt           (open-path 2-opt, bounded passes)
- best_insert  <- algos/alns_v3.best_insert       (cheapest-insertion delta)
- worst_edge   <- algos/alns_v3.worst_edge        (removal candidate: longest edge)

All operate on (sequence, distance matrix) only; deterministic.
"""


def nn2opt_open(stores, D):
    """NN construction from input head + bounded 2-opt. Open path (no return depot)."""
    seq = list(stores); n = len(seq)
    if n <= 3: return seq
    unv = set(range(1, n)); out = [0]
    while unv:
        l = out[-1]; out.append(min(unv, key=lambda j: D[seq[l]][seq[j]])); unv.discard(out[-1])
    route = [seq[t] for t in out]
    for _ in range(30):
        imp = False
        for a in range(1, n - 2):
            for b in range(a + 1, n - 1):
                if D[route[a-1]][route[b]] + D[route[a]][route[b+1]] < D[route[a-1]][route[a]] + D[route[b]][route[b+1]] - 1e-9:
                    route[a:b+1] = route[a:b+1][::-1]; imp = True
        if not imp: break
    return route


def best_insert(tour, node, D):
    """node 插入 tour 最优位置 -> (新tour, delta). 增量 O(n), 不重建."""
    n = len(tour)
    if n == 0: return [node], 0.0
    best = float('inf'); pos = n
    # 端点插入
    d0 = D[node][tour[0]]
    if d0 < best: best = d0; pos = 0
    dl = D[tour[-1]][node]
    if dl < best: best = dl; pos = n
    for k in range(n - 1):
        delta = D[tour[k]][node] + D[node][tour[k+1]] - D[tour[k]][tour[k+1]]
        if delta < best: best = delta; pos = k + 1
    return tour[:pos] + [node] + tour[pos:], best


def two_opt(tour, D, max_pass=20):
    """开放路径 2-opt, 有限轮. 返回改进后 tour."""
    seq = list(tour); n = len(seq)
    if n <= 3: return seq
    improved = True; p = 0
    while improved and p < max_pass:
        improved = False; p += 1
        for a in range(1, n - 1):
            for b in range(a + 1, n):
                before = D[seq[a-1]][seq[a]] + (D[seq[b]][seq[b+1]] if b < n-1 else 0.0)
                after  = D[seq[a-1]][seq[b]] + (D[seq[a]][seq[b+1]] if b < n-1 else 0.0)
                if after < before - 1e-9:
                    seq[a:b+1] = seq[a:b+1][::-1]; improved = True
    return seq


def worst_edge(tour, D, zone_of=None, cross_pref=False):
    """当前 tour 里最"该拆"的边: 距离最大; cross_pref 时跨区边加权. 返回端点b."""
    if len(tour) < 2: return None
    best_s = -1; vb = None
    for k in range(len(tour)-1):
        a, b = tour[k], tour[k+1]
        d = D[a][b]
        if cross_pref and zone_of is not None and zone_of.get(a) == zone_of.get(b):
            d *= 0.25
        if d > best_s: best_s = d; vb = b
    return vb


__all__ = ["nn2opt_open", "two_opt", "best_insert", "worst_edge"]
