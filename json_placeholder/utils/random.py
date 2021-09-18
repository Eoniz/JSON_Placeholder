import random
from typing import Iterable, TypeVar

T = TypeVar("T")

def one_of(values: Iterable[T]) -> T:
    return random.choice(values)

def int_bewteen(min: int = 0, max: int = 10) -> int:
    return random.randint(min, max)

def float_between(start: float = 0.0, end: float = 1.0) -> float:
    min_ = min(start, end)
    max_ = max(start, end)
    return min_ + (random.random() * (max_ - min_))
