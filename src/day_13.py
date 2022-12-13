from ast import literal_eval
from src.base import Solution


class Pass(Exception):
    ...


class Fail(Exception):
    ...


class Day13(Solution):
    name = "13"

    def part_one(self, radio_packets: list[str]) -> int:
        sum_of_correct_indicies: int = 0

        for i, packet in enumerate(radio_packets):
            if i % 3 == 0:
                left_packet = literal_eval(packet.rstrip())
            elif i % 3 == 1:
                right_packet = literal_eval(packet.rstrip())

            else:
                group_idx = (i // 3) + 1
                if packets_are_correctly_ordered(
                    left_packet,
                    right_packet,
                ):
                    sum_of_correct_indicies += group_idx

        return sum_of_correct_indicies

    def part_two(self, radio_packets: list[str]) -> int:
        return -1


def packets_are_correctly_ordered(left: list, right: list) -> bool:
    try:
        answer = _packets_are_correctly_ordered(left, right)
    except Pass:
        answer = True
    except Fail:
        answer = False

    return answer


def _packets_are_correctly_ordered(left: list, right: list) -> bool:
    for i in range(len(left)):
        if len(right) < i + 1:
            # Right list is exhausted before the left
            raise Fail

        if isinstance(left[i], int) and isinstance(right[i], int):
            if left[i] < right[i]:
                raise Pass
            elif left[i] > right[i]:
                raise Fail
            else:
                continue

        # Avoid mixed integer and list comparisons
        if isinstance(left[i], int):
            left[i] = [left[i]]

        if isinstance(right[i], int):
            right[i] = [right[i]]

        _packets_are_correctly_ordered(left[i], right[i])

    if len(right) > len(left):
        # Left list is exhausted before the right
        raise Pass

    # Completed comparisons
    return True


def assert_tests():
    l = [1, 1, 3, 1, 1]
    r = [1, 1, 5, 1, 1]
    assert packets_are_correctly_ordered(l, r)

    l = [[1], [2, 3, 4]]
    r = [[1], 4]
    assert packets_are_correctly_ordered(l, r)

    l = [9]
    r = [[8, 7, 6]]
    assert not packets_are_correctly_ordered(l, r)

    l = [[4, 4], 4, 4]
    r = [[4, 4], 4, 4, 4]
    assert packets_are_correctly_ordered(l, r)

    l = [7, 7, 7, 7]
    r = [7, 7, 7]
    assert not packets_are_correctly_ordered(l, r)

    l = []
    r = [3]
    assert packets_are_correctly_ordered(l, r)

    l = [[[]]]
    r = [[]]
    assert not packets_are_correctly_ordered(l, r)

    l = [1, [2, [3, [4, [5, 6, 7]]]], 8, 9]
    r = [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
    assert not packets_are_correctly_ordered(l, r)


if __name__ == '__main__':
    # l = [[], [2], [9]]
    # r = [[7, [[5, 2, 2], 7, 9, [3, 9, 0]], [], [[], 5]]]
    l = [[], []]
    r = [[], [[[4, 2, 3], 5, [2, 7, 8], 5]]]
    # print(packets_are_correctly_ordered(l, r))
    # assert_tests()
    Day13().solve(1)
