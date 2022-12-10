from dataclasses import dataclass, field
import re

from src.base import Solution


@dataclass
class CPU:
    clock: int = 0
    x_register: int = 1
    compiled_instructions: list[str] = field(default_factory=list)
    addx: re.Pattern = re.compile("addx -*[0-9]+")

    def compile_instructions(self, instructions: list[str]):
        """Read through and update the passed instructions
        such that each entry can be accomplished in a single
        clock cycle by adding noops for instructions previously
        taking multiple cycles"""
        for instruction in instructions:
            instruction = instruction.rstrip()

            if self.addx.match(instruction):
                self.compiled_instructions.append("noop")
                self.compiled_instructions.append(instruction)

            else:
                self.compiled_instructions.append(instruction)

    def make_empty_screen(self):
        screen = []
        for _ in range(6):
            screen.append(["."] * 40)
        return screen

    def run_program(self, draw=False):
        signal_strength: int = 0
        screen: list[list[str]] = self.make_empty_screen()

        for instruction in self.compiled_instructions:
            self.clock += 1

            if draw:
                curr_pixel_col = (self.clock - 1) % 40
                curr_pixel_row = self.clock // 40

                if abs(self.x_register - curr_pixel_col) < 2:
                    screen[curr_pixel_row][curr_pixel_col] = "#"

            if (self.clock == 20) or ((self.clock - 20) % 40 == 0):
                if self.clock <= 220:
                    strength = self.clock * self.x_register
                    signal_strength += self.clock * self.x_register

            if self.addx.match(instruction):
                val_change = instruction.split()[-1]
                self.x_register += int(val_change)

        if draw:
            for row in screen:
                print("".join(row))

        return signal_strength


class Day10(Solution):
    name = "10"

    def part_one(self, instructions: list[str]) -> int:
        cpu = CPU()
        cpu.compile_instructions(instructions)
        strength = cpu.run_program()

        return strength

    def part_two(self, instructions: list[str]):
        cpu = CPU()
        cpu.compile_instructions(instructions)
        cpu.run_program(draw=True)


if __name__ == '__main__':
    Day10().solve()
