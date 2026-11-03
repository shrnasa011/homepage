"""A tiny exact graph-isomorphism checker for small simple graphs.

Run: python examples/isomorphism_tester.py

This is an educational backtracking example, not a replacement for optimized
libraries such as nauty or bliss.
"""
from __future__ import annotations

from collections import Counter
from typing import Hashable, Mapping, Set

Vertex = Hashable
Graph = Mapping[Vertex, Set[Vertex]]


def is_isomorphic(left: Graph, right: Graph) -> bool:
    """Return whether two undirected simple graphs are exactly isomorphic."""
    if len(left) != len(right):
        return False
    if sum(map(len, left.values())) != sum(map(len, right.values())):
        return False

    def signatures(graph: Graph) -> dict[Vertex, tuple[int, tuple[int, ...]]]:
        return {
            v: (len(graph[v]), tuple(sorted(len(graph[n]) for n in graph[v])))
            for v in graph
        }

    sig_left, sig_right = signatures(left), signatures(right)
    if Counter(sig_left.values()) != Counter(sig_right.values()):
        return False

    # Match the most constrained vertices first.
    order = sorted(left, key=lambda v: (-len(left[v]), v.__repr__()))
    candidates = {
        v: [w for w in right if sig_left[v] == sig_right[w]]
        for v in left
    }
    mapping: dict[Vertex, Vertex] = {}
    used: set[Vertex] = set()

    def search(i: int) -> bool:
        if i == len(order):
            return True
        v = order[i]
        for w in candidates[v]:
            if w in used:
                continue
            # Preserve both edges and non-edges to every assigned vertex.
            if any(
                ((u in left[v]) != (mapping[u] in right[w]))
                for u in mapping
            ):
                continue
            mapping[v] = w
            used.add(w)
            if search(i + 1):
                return True
            used.remove(w)
            del mapping[v]
        return False

    return search(0)


def cycle(vertices: tuple[str, ...]) -> dict[str, set[str]]:
    graph = {v: set() for v in vertices}
    for i, v in enumerate(vertices):
        w = vertices[(i + 1) % len(vertices)]
        graph[v].add(w)
        graph[w].add(v)
    return graph


if __name__ == "__main__":
    six_cycle = cycle(("a", "b", "c", "d", "e", "f"))
    relabeled_six_cycle = cycle(("u", "w", "x", "y", "z", "v"))
    two_triangles = {
        "a": {"b", "c"}, "b": {"a", "c"}, "c": {"a", "b"},
        "d": {"e", "f"}, "e": {"d", "f"}, "f": {"d", "e"},
    }

    print("C6 vs relabeled C6:", is_isomorphic(six_cycle, relabeled_six_cycle))
    print("C6 vs two triangles:", is_isomorphic(six_cycle, two_triangles))
