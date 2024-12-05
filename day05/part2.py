from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

import pytest

FILE = Path(__file__)
TEST_RESULT = 123
TEST_INPUT = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


class Edge(NamedTuple):
    source: int
    to: int

    @classmethod
    def from_rule(cls, rule: str) -> "Edge":
        source, to = map(int, rule.split("|"))
        return cls(source=source, to=to)


class Graph(NamedTuple):
    edges: tuple[Edge, ...]

    @classmethod
    def from_rules(cls, rules: str) -> "Graph":
        return cls(edges=tuple(Edge.from_rule(rule) for rule in rules.splitlines()))

    def valid(self, operation: str) -> bool:
        nodes = tuple(map(int, operation.split(",")))
        for node, next_node in zip(nodes, nodes[1:]):
            reachable = reachable_nodes(graph=self, source=node, allowed=nodes)
            if next_node not in reachable:
                return False
        return True

    def sort(self, operation: str) -> list[int]:
        allowed = tuple(map(int, operation.split(",")))
        unsorted = set(allowed)
        current = unsorted.pop()
        sorted = [current]
        while unsorted:
            current = unsorted.pop()
            for idx in range(len(sorted)):
                node = sorted[idx]
                if node in reachable_nodes(self, current, allowed=allowed):
                    sorted.insert(idx, current)
                    break
            else:
                sorted.append(current)
        return sorted


@lru_cache
def children(graph: Graph, source: int) -> tuple[int, ...]:
    children: tuple[int, ...] = tuple()
    for edge in graph.edges:
        if edge.source == source:
            children += (edge.to,)
    return children


@lru_cache
def reachable_nodes(graph: Graph, source: int, allowed: tuple[int, ...]) -> set[int]:
    seen = set()
    unseen = {source}
    while unseen:
        current = unseen.pop()
        seen.add(current)
        unseen |= set(children(graph, current)).difference(seen) & set(allowed)
    return seen


def solve(puzzle_input: str) -> int:
    rules, operations = puzzle_input.split("\n\n")
    graph = Graph.from_rules(rules)
    count = 0
    for operation in operations.splitlines():
        if not graph.valid(operation):
            result = graph.sort(operation)
            count += result[len(result) // 2]
    return count


@pytest.mark.parametrize(
    ("test_input", "expected"),
    ((TEST_INPUT, TEST_RESULT),),
)
def test(test_input: str, expected: int) -> None:
    assert solve(test_input) == expected


if __name__ == "__main__":
    test_answer = solve(puzzle_input=TEST_INPUT)
    print(test_answer)
    if test_answer == TEST_RESULT:
        with open(FILE.parent / "input.txt") as file:
            answer = solve(puzzle_input=file.read())
        print(answer)
