from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from src.base import Solution


class CellType(Enum):
    AIR = "."
    ROCK = "#"
    SAND = "O"


@dataclass
class Location:
    x: int
    y: int


@dataclass
class Cell:
    contents: CellType


class Day14(Solution):
    name = "14"

    def part_one(self, scan: list[str]) -> int:
        cave, x_offset = create_empty_cave(scan)
        cave = add_rocks_to_cave(cave, x_offset, scan)

        sand_counter: int = 0
        cave_full: bool = False
        while not cave_full:
            try:
                cave = add_grain_of_sand(cave, x_offset)
                sand_counter += 1

            except IndexError:
                cave_full = True

        return sand_counter

    def part_two(self, scan: list[str]) -> int:
        cave, x_offset = create_empty_cave(scan, part_two=True)
        cave = add_rocks_to_cave(cave, x_offset, scan)

        sand_counter: int = 0
        cave_full: bool = False
        while not cave_full:
            try:
                cave = add_grain_of_sand(cave, x_offset)
                sand_counter += 1

                if cave[0][500 - x_offset].contents == CellType.SAND:
                    cave_full = True

            except IndexError as err:
                continue

        return sand_counter


def create_empty_cave(
    scan: list[str], part_two: bool = False
) -> tuple[list[list[Cell]], int]:
    """Return a cave of unoccupied cells along with
    an x-offset value"""
    min_x: int = 1_000_000
    max_x: int = -1
    max_y: int = -1

    for trace in scan:
        trace = trace.rstrip()
        for coords in trace.split(" -> "):
            x, y = coords.split(",")[:2]
            min_x = min(int(x), min_x)
            max_x = max(int(x), max_x)
            max_y = max(int(y), max_y)

    if part_two:
        # Expand cave to allow for full pyramid creation
        max_y += 2
        width_of_pyramid_base = 2 * max_y - 1
        min_x = 500 - (width_of_pyramid_base // 2) - 1
        max_x = 500 + (width_of_pyramid_base // 2) + 1

    cave: list[list[Cell]] = []
    for _ in range(max_y + 1):
        cave.append([Cell(contents=CellType.AIR) for _ in range(min_x, max_x + 1)])

    if part_two:
        # Add an additional layer of rocks along the bottom row
        for cell in cave[-1]:
            cell.contents = CellType.ROCK

    return cave, min_x


def add_rocks_to_cave(
    cave: list[list[Cell]], x_offset: int, scan: list[str]
) -> list[list[Cell]]:
    for trace in scan:
        trace = trace.rstrip()

        rock_points: list[Location] = []
        for coords in trace.split(" -> "):
            x, y = coords.split(",")[:2]
            rock_points.append(
                Location(
                    x=int(x) - x_offset,
                    y=int(y),
                )
            )

        curr: Location = rock_points[0]
        cave[curr.y][curr.x].contents = CellType.ROCK

        for new_point in rock_points[1:]:
            if (x_diff := new_point.x - curr.x) != 0:
                direction = 1 if x_diff > 0 else -1

                for x in range(1, abs(x_diff) + 1):
                    cave[curr.y][curr.x + (x * direction)].contents = CellType.ROCK

            else:
                y_diff = new_point.y - curr.y
                direction = 1 if y_diff > 0 else -1

                for y in range(1, abs(y_diff) + 1):
                    cave[curr.y + (y * direction)][curr.x].contents = CellType.ROCK

            curr = new_point

    return cave


def add_grain_of_sand(
    cave: list[list[Cell]], x_offset: int
) -> tuple[list[list[Cell]], bool]:
    """Adds a single grain of sand into the cave if possible.
    Returns the updated cave and a boolean denoted if the
    cave is full or not.
    """
    done: bool = False
    sand: Location = Location(x=500 - x_offset, y=0)

    max_x = len(cave[0])
    max_y = len(cave)
    while not done:

        if cave[sand.y + 1][sand.x].contents == CellType.AIR:
            sand.y += 1

        elif cave[sand.y + 1][sand.x - 1].contents == CellType.AIR:
            sand.y += 1
            sand.x -= 1

        elif cave[sand.y + 1][sand.x + 1].contents == CellType.AIR:
            sand.y += 1
            sand.x += 1

        else:
            done = True

    cave[sand.y][sand.x].contents = CellType.SAND
    return cave


def draw_cave(cave: list[list[Cell]]):
    for y, row in enumerate(cave):
        print([cave[y][x].contents.value for x in range(len(row))])


if __name__ == '__main__':
    Day14().solve()
