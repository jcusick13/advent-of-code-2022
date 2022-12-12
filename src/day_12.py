from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
from typing import Union

from src.base import Solution

Numeric = Union[float, int]


@dataclass
class Cell:
    x: int
    y: int

    def __hash__(self) -> int:
        s = f"{self.x}-{self.y}"
        return int(hashlib.sha256(bytearray(s, encoding="utf-8")).hexdigest(), 16)

    @property
    def neighbors(self) -> set[Cell]:
        return {
            Cell(self.x, self.y - 1),
            Cell(self.x, self.y + 1),
            Cell(self.x - 1, self.y),
            Cell(self.x + 1, self.y),
        }


@dataclass
class HeightMap:
    location: Cell
    starts: list[Cell]
    end: Cell
    elev: list[list[int]] = field(default_factory=list)

    @classmethod
    def new(cls, input: list[str], multi_start=False) -> HeightMap:
        elev: list[list[int]] = []
        starts: list[Cell] = []
        end = Cell(x=-1, y=-1)

        for row_idx in range(len(input)):
            elev_row: list[int] = []
            for col_idx, char in enumerate(input[row_idx].rstrip()):
                value = ord(char)
                if char == "S":
                    value = ord("a")
                    start = Cell(x=col_idx, y=row_idx)
                    starts.append(start)

                if char == "E":
                    value = ord("z")
                    end.x = col_idx
                    end.y = row_idx

                if multi_start and char == "a":
                    value = ord("a")
                    start = Cell(x=col_idx, y=row_idx)
                    starts.append(start)

                elev_row.append(value)
            elev.append(elev_row)

        return HeightMap(
            location=start,
            starts=starts,
            end=end,
            elev=elev,
        )


def shortest_path(grid: list[list[int]], start: Cell, end: Cell) -> int:
    unvisited_set: set[Cell] = set()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            cell = Cell(x, y)
            unvisited_set.add(cell)

    cost: list[list[Numeric]] = []
    for i in range(len(grid)):
        cost.append([float("inf") for _ in range(len(grid[i]))])
    cost[start.y][start.x] = 0

    while unvisited_set:
        lowest_cost = float("inf")
        for cell in unvisited_set:
            if cost[cell.y][cell.x] < lowest_cost:
                curr = cell
                lowest_cost = cost[cell.y][cell.x]

        if lowest_cost == float("inf"):
            # No more reachable cells remain
            break

        unvisited_set.remove(curr)
        curr_elev = grid[curr.y][curr.x]

        unvisited_neighbors = curr.neighbors & unvisited_set
        for neighbor in unvisited_neighbors:
            neighbor_elev = grid[neighbor.y][neighbor.x]
            if neighbor_elev - curr_elev < 2:
                # Able to get there without climbing gear
                cost[neighbor.y][neighbor.x] = min(
                    cost[neighbor.y][neighbor.x], cost[curr.y][curr.x] + 1
                )

    return cost[end.y][end.x]


class Day12(Solution):
    name = "12"

    def part_one(self, input_map: list[str]) -> int:
        heightmap = HeightMap.new(input_map)
        dist = shortest_path(heightmap.elev, heightmap.starts[0], heightmap.end)
        return dist

    def part_two(self, input_map: list[str]):
        heightmap = HeightMap.new(input_map, multi_start=True)
        shortest_dist = float("inf")
        for start in heightmap.starts:
            dist = shortest_path(heightmap.elev, start, heightmap.end)
            shortest_dist = min(shortest_dist, dist)

        return shortest_dist


if __name__ == '__main__':
    Day12().solve()
