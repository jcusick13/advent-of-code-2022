from src.base import Solution


class Day04(Solution):
    name = "04"

    def part_one(self, section_assignments: list[str]) -> int:
        fully_contained: int = 0
        for assignment in section_assignments:
            range_a = assignment.strip().split(",")[0]
            range_b = assignment.strip().split(",")[1]

            elf_a = self.calculate_elf_sections(range_a)
            elf_b = self.calculate_elf_sections(range_b)

            if not elf_a.difference(elf_b) or not elf_b.difference(elf_a):
                fully_contained += 1

        return fully_contained

    def part_two(self, section_assignments: list[str]) -> int:
        overlaps: int = 0
        for assignment in section_assignments:
            range_a = assignment.strip().split(",")[0]
            range_b = assignment.strip().split(",")[1]

            elf_a = self.calculate_elf_sections(range_a)
            elf_b = self.calculate_elf_sections(range_b)

            if elf_a.intersection(elf_b):
                overlaps += 1

        return overlaps

    def calculate_elf_sections(self, ranges: str) -> set[int]:
        """Create a set of all sections assigned to an elf"""
        start = int(ranges.split("-")[0])
        stop = int(ranges.split("-")[1])
        return {x for x in range(start, stop + 1)}


if __name__ == '__main__':
    Day04().solve()
