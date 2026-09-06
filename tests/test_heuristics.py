# -*- coding: utf-8 -*-
"""Pure-geometry heuristic invariants: determinism, validity, no-regress."""
import itertools

from opticore import nn2opt_open, two_opt, best_insert, worst_edge


def _km(seq, D):
    return sum(D[seq[k]][seq[k+1]] for k in range(len(seq) - 1))


def test_nn2opt_open_deterministic_and_permutation():
    D = [[(i - j) ** 2 + (i * j) % 3 for j in range(7)] for i in range(7)]
    r1 = nn2opt_open([5, 2, 6, 0, 3, 1, 4], D)
    r2 = nn2opt_open([5, 2, 6, 0, 3, 1, 4], D)
    assert r1 == r2                       # 同输入逐位复现
    assert sorted(r1) == list(range(7))   # 输出是输入的排列


def test_two_opt_never_increases_km():
    D = [[(i - j) ** 2 + ((i + 2 * j) % 5) for j in range(6)] for i in range(6)]
    seq = [3, 0, 5, 1, 4, 2]
    assert _km(two_opt(seq, D), D) <= _km(seq, D) + 1e-9

def test_best_insert_achieves_min_delta():
    D = [[abs(i - j) for j in range(4)] for i in range(4)]
    tour, node = [0, 3], 1
    new, delta = best_insert(tour, node, D)
    cands = [tour[:p] + [node] + tour[p:] for p in range(len(tour) + 1)]
    best = min(_km(t2, D) for t2 in cands)
    assert abs(delta - (best - _km(tour, D))) < 1e-9   # 返回的 delta 即最优增量
    assert abs(_km(new, D) - best) < 1e-9              # 放置达到最优


def test_worst_edge_returns_longest_edge_endpoint():
    D = [[0.0, 1.0, 9.0], [1.0, 0.0, 2.0], [9.0, 2.0, 0.0]]
    assert worst_edge([0, 1, 2], D) == 2            # 最长边 0-2 (9.0) 的端点 b
    assert worst_edge([0], D) is None
    zone_of = {0: "z", 1: "z", 2: "y"}
    assert worst_edge([0, 1, 2], D, zone_of, cross_pref=True) == 2
