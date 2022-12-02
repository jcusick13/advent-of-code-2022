from dataclasses import dataclass
from typing import Optional


@dataclass
class Solution:
    @property
    def name(self) -> str:
        # Two digit day, e.g. "04"
        raise NotImplementedError

    def read(self):
        with open(f"inputs/{self.name}.txt", encoding="utf-8") as f:
            puzzle_input = f.readlines()
        return puzzle_input

    def part_one(self, puzzle_input):
        raise NotImplementedError

    def part_two(self, puzzle_input):
        raise NotImplementedError

    def solve(self, part: Optional[int] = None):
        """Run the implemented solution for a given day and
        print computed answer
        """
        part_one = (part == 1) or (part is None)
        part_two = (part == 2) or (part is None)

        if part_one:
            input_one = self.read()
            solution_one = self.part_one(input_one)
            print(f"Soln part one: {solution_one}")

        if part_two:
            input_two = self.read()
            solution_two = self.part_two(input_two)
            print(f"Soln part two: {solution_two}")
