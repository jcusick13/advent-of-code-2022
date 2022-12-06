from collections import deque

from src.base import Solution


class Day06(Solution):
    name = "06"

    def read(self) -> str:
        with open(f"inputs/{self.name}.txt", encoding="utf-8") as f:
            puzzle_input = f.readline().strip()
        return puzzle_input

    def part_one(self, signal: str) -> int:
        marker_check: deque[str] = deque()

        for i in range(3):
            marker_check.append(signal[i])

        for i in range(3, len(signal)):
            marker_check.append(signal[i])
            if len(set(marker_check)) == 4:
                return i + 1

            marker_check.popleft()

        return -1

    def part_two(self, signal: str) -> int:
        marker_check: deque[str] = deque()

        for i in range(13):
            marker_check.append(signal[i])

        for i in range(13, len(signal)):
            marker_check.append(signal[i])
            if len(set(marker_check)) == 14:
                return i + 1

            marker_check.popleft()

        return -1


if __name__ == '__main__':
    Day06().solve()
