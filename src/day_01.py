from src.base import Solution


class Day01(Solution):
    name = "01"

    def read(self, part: int) -> list[int]:
        with open(f"inputs/{self.name}_{part}.txt", encoding="utf-8") as f:
            puzzle_input = f.readlines()
        return puzzle_input

    def part_one(self, puzzle_input: list[int]) -> int:
        depth_increases: int = 0

        for i, depth in enumerate(puzzle_input):
            if i == 0:
                prev = depth
                continue

            if depth > prev:
                depth_increases += 1

            prev = depth

        return depth_increases


if __name__ == '__main__':
    Day01().solve(1)
