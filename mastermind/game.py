import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass
import random
from typing import Any


class Color(enum.Enum):
    (
        RED,
        YELLOW,
        ORANGE,
        GREEN,
        BLUE,
        PURPLE,
    ) = range(1, 7)


@dataclass
class History:
    colors: 'list[Color]'
    correct_position: int
    correct_color: int

    @classmethod
    def from_saved_state(cls, state: dict[str, Any]) -> 'History':
        return cls(
            colors=[Color._value2member_map_[i] for i in state['colors']],
            correct_color=state['correct_color'],
            correct_position=state['correct_position'],
        )

    def save_state(self) -> dict[str, Any]:
        return {
            'colors': [i.value for i in self.colors],
            'correct_color': self.correct_color,
            'correct_position': self.correct_position,
        }


def get_correct(original: 'list[Color]', guess: 'list[Color]') -> 'tuple[int, int]':
    correct_position, correct_color = 0, 0
    remaining_current = []
    remaining_thought = []

    for i, color in enumerate(guess):
        if original[i] == color:
            correct_position += 1
        else:
            remaining_current.append(color)
            remaining_thought.append(original[i])

    for i in remaining_current:
        if i in remaining_thought:
            correct_color += 1
            del remaining_thought[remaining_thought.index(i)]

    return correct_position, correct_color


class MasterMind:
    def __init__(self):
        self.thought = [Color._value2member_map_[random.randrange(1, 7)] for _ in range(4)]
        self.current = [Color.RED] * 4
        self.history: 'list[History]' = []
        self.won = False

    @classmethod
    def from_saved_state(cls, state: dict[str, Any]):
        obj = cls()
        obj.thought = state['thought']
        obj.current = [Color._value2member_map_[i] for i in state['current']]
        obj.history = [History.from_saved_state(i) for i in state['history']]
        obj.won = state['won']

    def save_state(self) -> dict[str, Any]:
        return {
            'thought': self.thought,
            'current': [i.value for i in self.current],
            'history': [i.save_state() for i in self.history],
            'won': self.won,
        }

    def select_color(self, position: int, color: 'Color') -> None:
        assert not self.won
        self.current[position] = color

    def commit(self) -> None:
        self.history.append(History(self.current[:], *get_correct(self.thought, self.current)))
        self.won = self.current == self.thought
