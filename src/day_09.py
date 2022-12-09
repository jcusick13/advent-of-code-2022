from __future__ import annotations

from dataclasses import dataclass
import hashlib

from src.base import Solution


@dataclass
class Location:
    x: int
    y: int

    def __hash__(self) -> int:
        s = f"{self.x}-{self.y}"
        return int(hashlib.sha256(bytearray(s, encoding="utf-8")).hexdigest(), 16)

    def _is_adjacent(self, other: Location) -> bool:
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if (self.x == other.x + x) and (self.y == other.y + y):
                    return True
        return False

    def _in_same_row_or_col(self, other: Location) -> bool:
        return (self.x == other.x) ^ (self.y == other.y)

    def _move_towards_other_along_row_or_col(self, other: Location):
        if (x_diff := other.x - self.x) != 0:
            self.x += 1 if x_diff > 0 else -1

        else:
            y_diff = other.y - self.y
            self.y += 1 if y_diff > 0 else -1

    def _move_towards_other_along_diagonal(self, other: Location):
        x_diff = other.x - self.x
        y_diff = other.y - self.y

        self.x += 1 if x_diff > 0 else -1
        self.y += 1 if y_diff > 0 else -1

    def move_one(self, direction: str):
        if direction == "U":
            self.y += 1

        elif direction == "D":
            self.y -= 1

        elif direction == "L":
            self.x -= 1

        elif direction == "R":
            self.x += 1

    def move_towards_other(self, other: Location):
        if self._is_adjacent(other):
            return

        if self._in_same_row_or_col(other):
            self._move_towards_other_along_row_or_col(other)

        else:
            self._move_towards_other_along_diagonal(other)


class Day09(Solution):
    name = "09"

    def part_one(self, motions: list[str]) -> int:
        head = Location(x=0, y=0)
        tail = Location(x=0, y=0)
        visited: set[Location] = {tail}

        for motion in motions:
            direction, distance = motion.strip().split()[:2]

            for _ in range(int(distance)):
                head.move_one(direction)
                tail.move_towards_other(head)
                visited.add(tail)

        return len(visited)

    def part_two(self, motions: list[str]) -> int:
        head = Location(x=0, y=0)
        tails = [Location(x=0, y=0) for _ in range(9)]
        visited: set[Location] = {tails[-1]}

        for motion in motions:
            direction, distance = motion.strip().split()[:2]

            for _ in range(int(distance)):
                head.move_one(direction)
                tails[0].move_towards_other(head)

                other = tails[0]
                for tail in tails[1:]:
                    tail.move_towards_other(other)
                    other = tail

                visited.add(tails[-1])

        return len(visited)


if __name__ == '__main__':
    Day09().solve()
