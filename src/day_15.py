from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re

from src.base import Solution


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        s = f"{self.x}-{self.y}"
        return int(hashlib.sha256(bytearray(s, encoding="utf-8")).hexdigest(), 16)


@dataclass
class NumericRange:
    min: int
    max: int

    @property
    def n(self) -> int:
        """Count total using inclusive bounds"""
        return self.max - self.min + 1

    def merge_other(self, other: NumericRange):
        self.min = min(self.min, other.min)
        self.max = max(self.max, other.max)


@dataclass
class ExclusionZone:
    center: Point
    top: Point
    left: Point
    right: Point
    bottom: Point
    beacon: Point
    dist: int

    @classmethod
    def create(cls, center: Point, beacon: Point) -> ExclusionZone:
        dist = distance(center, beacon)
        return ExclusionZone(
            center=center,
            top=Point(x=center.x, y=center.y + dist),
            left=Point(x=center.x - dist, y=center.y),
            right=Point(x=center.x + dist, y=center.y),
            bottom=Point(x=center.x, y=center.y - dist),
            beacon=beacon,
            dist=dist,
        )

    def contains(self, point: Point) -> bool:
        # Attempt loose check for early return
        if (
            point.y > self.top.y
            or point.y < self.bottom.y
            or point.x > self.right.x
            or point.x < self.left.x
        ):
            return False

        row_intersection = self.intersection_of_row(row=point.y)
        return row_intersection.min <= point.x <= row_intersection.max

    def intersection_of_row(self, row: int) -> NumericRange:
        if self.top.y < row or self.bottom.y > row:
            return NumericRange(min=0, max=0)

        dist_from_y_extreme = min((row - self.bottom.y), (self.top.y - row))
        total_width = 2 * dist_from_y_extreme + 1

        return NumericRange(
            min=self.center.x - (total_width // 2),
            max=self.center.x + (total_width // 2),
        )


def count_non_beacon_points(zones: list[ExclusionZone], row: int) -> int:
    beacons_to_remove: set[Point] = set()

    points_along_row = zones[0].intersection_of_row(row)
    if zones[0].beacon.y == row:
        beacons_to_remove.add(zones[0].beacon)

    for zone in zones[1:]:
        new_range = zone.intersection_of_row(row)
        points_along_row.merge_other(new_range)

        if zone.beacon.y == row:
            beacons_to_remove.add(zone.beacon)

    return points_along_row.n - len(beacons_to_remove)


def distance(a: Point, b: Point) -> int:
    """Return Manhattan distance"""
    return abs(a.x - b.x) + abs(a.y - b.y)


def parse_line(line: str) -> tuple[Point, Point]:
    num = "-*[0-9]+"
    r = re.compile(f".* x=({num}), y=({num}): .* x=({num}), y=({num})$")
    match = r.match(line)

    sensor = Point(x=int(match.group(1)), y=int(match.group(2)))
    beacon = Point(x=int(match.group(3)), y=int(match.group(4)))
    return sensor, beacon


class Day15(Solution):
    name = "15"

    def part_one(self, position_report: list[str]) -> int:
        exclusion_zones: list[ExclusionZone] = []
        for line in position_report:
            sensor, beacon = parse_line(line.rstrip())
            exclusion_zones.append(ExclusionZone.create(sensor, beacon))

        return count_non_beacon_points(exclusion_zones, row=10)

    def part_two(self, position_report: list[str]) -> int:
        exclusion_zones: list[ExclusionZone] = []
        for line in position_report:
            sensor, beacon = parse_line(line.rstrip())
            exclusion_zones.append(ExclusionZone.create(sensor, beacon))

        # shame...
        max_size = 20
        point_found: bool = False
        for x in range(max_size):
            if point_found:
                break

            for y in range(max_size):
                point = Point(x, y)
                if any(zone.contains(point) for zone in exclusion_zones):
                    continue

                # Point doesn't intersect any exclusions, this is our spot!
                point_found = True
                break

        tuning_freq = (4_000_000 * point.x) + point.y
        return tuning_freq


if __name__ == '__main__':
    Day15().solve()
