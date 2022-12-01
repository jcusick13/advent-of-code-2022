from src.base import Solution


class Day01(Solution):
    name = "01"

    def read(self, part: int) -> list[str]:
        with open(f"inputs/{self.name}_{part}.txt", encoding="utf-8") as f:
            puzzle_input = f.readlines()
        return puzzle_input

    def part_one(self, calorie_list: list[str]) -> int:
        max_calories: int = 0
        current_calories: int = 0

        for entry in calorie_list:
            try:
                current_calories += int(entry.strip())

            except ValueError:
                # Encountered empty entry in list, reset counter
                # for a new elf
                max_calories = max(max_calories, current_calories)
                current_calories = 0

        return max_calories

    def part_two(self, calorie_list: list[str]) -> int:
        elf_totals: list[int] = []
        current_calories: int = 0

        for entry in calorie_list:
            try:
                current_calories += int(entry.strip())

            except ValueError:
                # Encountered empty entry in list, reset counter
                # for a new elf
                elf_totals.append(current_calories)
                current_calories = 0

        # Total the three highest calorie counts
        return sum(sorted(elf_totals, reverse=True)[:3])


if __name__ == '__main__':
    Day01().solve()
