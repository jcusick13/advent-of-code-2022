from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
import hashlib
import re
from typing import Optional

from src.base import Solution


@dataclass
class Node:
    name: str
    is_dir: bool
    parent: Optional[Node]
    size: int = 0

    def __hash__(self):
        s = f"{self.name}-none"
        if self.parent:
            s = f"{self.name}-{self.parent.name}"
        return int(hashlib.sha256(bytearray(s, encoding="utf-8")).hexdigest(), 16)


@dataclass
class FileSystem:
    root: Node
    nodes: dict[Node, list[Node]] = field(default_factory=dict)

    @classmethod
    def new(cls) -> FileSystem:
        root = Node(name="/", is_dir=True, parent=None)
        return FileSystem(root=root, nodes={root: []})


def get_directory_sizes(
    nodes: dict[Node, list[Node]],
    start_node: Node,
    visited: set[Node],
) -> list[int]:
    """Perform depth-first traversal of nodes, accumulating
    the size underneath a node as it's traversed back on the
    way up. Returns a list of total size for all nodes that
    are a directory.
    """
    if start_node not in visited:
        visited.add(start_node)

        for child_node in nodes[start_node]:
            if child_node not in visited:
                get_directory_sizes(nodes, child_node, visited)

            child_node.parent.size += child_node.size

    return [node.size for node in nodes.keys() if node.is_dir]


class Day07(Solution):
    name = "07"

    def part_one(self, display: list[str]) -> int:
        fs = self.build_filesystem(display)

        visited: set[Node] = set()
        sizes = get_directory_sizes(
            nodes=fs.nodes,
            start_node=fs.root,
            visited=visited,
        )
        return sum(size for size in sizes if size <= 100_000)

    def part_two(self, display: list[str]) -> int:
        total_disk_size = 70_000_000
        space_for_update = 30_000_000

        fs = self.build_filesystem(display)
        visited: set[Node] = set()
        sizes = get_directory_sizes(
            nodes=fs.nodes,
            start_node=fs.root,
            visited=visited,
        )

        current_usage = total_disk_size - max(sizes)
        needed_space = space_for_update - current_usage

        return min([size for size in sizes if size >= needed_space])

    def build_filesystem(self, display: list[str]) -> FileSystem:
        fs = FileSystem.new()
        curr_node: Node = fs.root

        change_dir_in = re.compile("\$ cd [a-z]+")
        change_dir_out = re.compile("\$ cd \.\.")
        change_dir_root = re.compile("\$ cd /")
        directory = re.compile("dir [a-z]+")
        file = re.compile("[0-9]+ [a-z]+")

        for entry in display[2:]:
            entry = entry.strip()

            if change_dir_in.match(entry):
                to_dir = entry.split()[-1]
                for child in fs.nodes[curr_node]:
                    if child.name != to_dir:
                        continue
                    curr_node = child

            elif change_dir_out.match(entry):
                curr_node = curr_node.parent

            elif change_dir_root.match(entry):
                curr_node = fs.root

            elif directory.match(entry):
                name = entry.split()[1]
                new_node = Node(name=name, is_dir=True, parent=curr_node)
                fs.nodes[new_node] = []
                fs.nodes[curr_node].append(new_node)

            elif file.match(entry):
                size, name = entry.split()[:2]
                new_node = Node(
                    name=name, is_dir=False, parent=curr_node, size=int(size)
                )
                fs.nodes[new_node] = []
                fs.nodes[curr_node].append(new_node)

            elif entry != "$ ls":
                raise ValueError(f"Failed to parse {entry=}")

        return fs


if __name__ == '__main__':
    Day07().solve()
