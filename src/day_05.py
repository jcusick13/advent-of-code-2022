from collections import deque
from dataclasses import dataclass
from string import ascii_uppercase

from src.base import Solution


@dataclass
class Action:
    n: int
    current: int
    future: int


class Day05(Solution):
    name = "05"
    stacks: list[deque]

    def part_one(self, crane_instructions: list[str]) -> str:
        # Interpret instructions
        self.stacks = self.create_stacks(crane_instructions)
        actions = self.parse_instructions(crane_instructions)

        # Rearrange crates
        for action in actions:
            for _ in range(action.n):
                crate = self.stacks[action.current - 1].pop()
                self.stacks[action.future - 1].append(crate)

        # Determine top crate of each stack
        top_crates = ""
        for i in range(len(self.stacks)):
            top_crates += self.stacks[i].pop()

        return top_crates

    def part_two(self, crane_instructions: list[str]) -> str:
        # Interpret instructions
        self.stacks = self.create_stacks(crane_instructions)
        actions = self.parse_instructions(crane_instructions)

        # Rearrange crates, keeping multi-crate moves in order
        for action in actions:
            temp_crates: list[str] = []
            for _ in range(action.n):
                crate = self.stacks[action.current - 1].pop()
                temp_crates.append(crate)

            for crate in temp_crates[::-1]:
                self.stacks[action.future - 1].append(crate)

        # Determine top crate of each stack
        top_crates = ""
        for i in range(len(self.stacks)):
            top_crates += self.stacks[i].pop()

        return top_crates

    def create_stacks(self, crane_instructions: list[str]) -> list[deque]:
        """Generate a list of filled stacks from the original input"""

        # Find number of stacks needed
        for line in crane_instructions:
            if line.lstrip()[0] == "[":
                continue

            n_stacks = len(line.split())
            break

        # Fill stacks will input crates
        stacks: list[deque] = [deque() for _ in range(n_stacks)]
        stacks_filled = False
        for line in crane_instructions:
            if stacks_filled:
                break

            for stack in range(n_stacks):
                crate = line[stack * 4 + 1]
                if crate in ascii_uppercase:
                    stacks[stack].appendleft(crate)

                if crate == "1":
                    # We've hit the stack numbering; no more
                    # crates left to process
                    stacks_filled = True
                    break

        return stacks

    def parse_instructions(self, crane_instructions: list[str]) -> list[Action]:
        actions: list[Action] = []
        for line in crane_instructions:
            if line[:4] != "move":
                # Skip crate description overview
                continue

            parsed = line.split()
            actions.append(
                Action(
                    n=int(parsed[1].strip()),
                    current=int(parsed[3].strip()),
                    future=int(parsed[5].strip()),
                )
            )
        return actions


if __name__ == '__main__':
    Day05().solve()
