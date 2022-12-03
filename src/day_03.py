from functools import cached_property
from string import ascii_lowercase

from src.base import Solution


class Day03(Solution):
    name = "03"

    @cached_property
    def priorities(self) -> dict[str, int]:
        lowercase_priorities = {
            letter: (priority + 1) for priority, letter in enumerate(ascii_lowercase)
        }
        uppercase_priorities = {
            letter.upper(): (priority + 27)
            for priority, letter in enumerate(ascii_lowercase)
        }
        return lowercase_priorities | uppercase_priorities

    def part_one(self, rucksacks: list[str]) -> int:
        priority_total: int = 0
        for rucksack in rucksacks:
            rucksack = rucksack.strip()
            split = int(len(rucksack) / 2)

            compartment_a = set(rucksack[:split])
            compartment_b = set(rucksack[split:])

            duplicate = compartment_a.intersection(compartment_b)
            priority = self.priorities[duplicate.pop()]

            priority_total += priority

        return priority_total

    def part_two(self, rucksacks: list[str]) -> int:
        priority_total: int = 0
        for i in range(0, len(rucksacks), 3):
            rucksack_a = set(rucksacks[i].strip())
            rucksack_b = set(rucksacks[i + 1].strip())
            rucksack_c = set(rucksacks[i + 2].strip())

            badge = rucksack_a & rucksack_b & rucksack_c
            priority = self.priorities[badge.pop()]

            priority_total += priority

        return priority_total


if __name__ == '__main__':
    Day03().solve()
