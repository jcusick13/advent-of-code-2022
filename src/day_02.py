from enum import Enum

from src.base import Solution


class ActionOne(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class ActionZero(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


class Outcome(Enum):
    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"


class Day02(Solution):
    name = "02"

    def part_one(self, game_rounds: list[str]) -> int:
        total_score: int = 0
        my_map = {"X": ActionOne.ROCK, "Y": ActionOne.PAPER, "Z": ActionOne.SCISSORS}
        opponent_map = {
            "A": ActionOne.ROCK,
            "B": ActionOne.PAPER,
            "C": ActionOne.SCISSORS,
        }

        for single_round in game_rounds:
            entries = single_round.split()
            opponent_action = opponent_map[entries[0].strip()]
            my_action = my_map[entries[1].strip()]

            outcome = self.score_single_round(my_action, opponent_action)
            total_score += outcome + my_action.value

        return total_score

    def part_two(self, game_rounds: list[str]) -> int:
        total_score: int = 0
        outcome_map = {Outcome.WIN: 6, Outcome.DRAW: 3, Outcome.LOSE: 0}
        opponent_map = {
            "A": ActionZero.ROCK,
            "B": ActionZero.PAPER,
            "C": ActionZero.SCISSORS,
        }

        for single_round in game_rounds:
            entries = single_round.split()
            opponent_action = opponent_map[entries[0].strip()]
            outcome = Outcome(entries[1].strip())

            my_action = self.determine_round_action(opponent_action, outcome)
            # Need to add one at the end b/c zero-index action values
            total_score += outcome_map[outcome] + my_action.value + 1

        return total_score

    def score_single_round(self, a: ActionOne, b: ActionOne) -> int:
        """Play a single round of rock, paper, scissors between
        players `a` and `b`, returning the score from player a's
        perspective
        """
        if a.value == b.value:
            return 3  # draw

        if (a.value - b.value) % 3 == 1:
            return 6  # player a wins

        if (b.value - a.value) % 3 == 1:
            return 0  # player a loses

    def determine_round_action(
        self, action: ActionZero, outcome: Outcome
    ) -> ActionZero:
        """Given the `action` of player a and the `outcome`
        of the round, return the action that player b would
        have to have chosen
        """
        if outcome == Outcome.DRAW:
            return action

        if outcome == Outcome.WIN:
            return ActionZero((action.value + 1) % 3)

        if outcome == Outcome.LOSE:
            return ActionZero((action.value - 1) % 3)


if __name__ == '__main__':
    Day02().solve()
