from src.base import Solution


class Day08(Solution):
    name = "08"

    def part_one(self, heights_orig: list[str]) -> int:
        heights, heights_transpose = create_matrices(heights_orig)

        # Measure visibility for interior trees
        visible_trees = 0
        for row in range(1, len(heights) - 1):
            for col in range(1, len(heights[row]) - 1):
                if tree_visible(col, heights[row]) or tree_visible(
                    row, heights_transpose[col]
                ):
                    visible_trees += 1

        # Add trees visible from the grid edges, don't double count corners!
        visible_trees += 2 * len(heights[0])
        visible_trees += (2 * len(heights_transpose[0])) - 4

        return visible_trees

    def part_two(self, heights_orig: list[str]) -> int:
        heights, heights_transpose = create_matrices(heights_orig)

        best_scenic_score = 0
        for row in range(len(heights)):
            for col in range(len(heights[row])):
                score_orig = scenic_score(col, heights[row])
                score_transpose = scenic_score(row, heights_transpose[col])

                if (score := score_orig * score_transpose) > best_scenic_score:
                    best_scenic_score = score

        return best_scenic_score


def create_matrices(
    heights_orig: list[str],
) -> tuple[list[list[int]], list[list[int]]]:
    """Build 2-d matrices for both the input and transpose
    of the input
    """
    # Convert input to 2-d list
    heights: list[list[int]] = []
    for line in heights_orig:
        line = line.strip()

        row: list[int] = []
        for num in line:
            row.append(int(num))
        heights.append(row)

    # Transpose input; gross - wherefore art thou numpy?
    heights_transpose: list[list[int]] = list(map(list, zip(*heights)))

    return heights, heights_transpose


def tree_visible(tree_idx: int, row_heights: list[int]) -> bool:
    """Determine if a tree can be seen from within a
    single row of neighbors. `tree_idx` must be an index
    within the list of `row_heights`
    """
    visible_from_left = row_heights[tree_idx] > max(row_heights[:tree_idx])
    visible_from_right = row_heights[tree_idx] > max(row_heights[tree_idx + 1 :])
    return visible_from_left or visible_from_right


def scenic_score(tree_idx: int, row_heights: list[int]) -> int:
    """Calculate score based on number of trees viewable
    from `tree_idx`
    """
    score_right = 0
    if tree_idx < len(row_heights):
        for idx in range(tree_idx + 1, len(row_heights)):
            score_right += 1
            if not row_heights[tree_idx] > row_heights[idx]:
                break

    score_left = 0
    if tree_idx > 0:
        for idx in range(tree_idx - 1, -1, -1):
            score_left += 1
            if not row_heights[tree_idx] > row_heights[idx]:
                break

    return score_right * score_left


if __name__ == '__main__':
    Day08().solve()
