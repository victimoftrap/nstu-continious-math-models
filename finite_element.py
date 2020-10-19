from dataclasses import dataclass


@dataclass(frozen=True)
class FiniteElement:
    """Класс, описывающий конечный элемент.

        left (float): левая граница конечного элемента
        right (float): правая граница конечного элемента
    """

    left: float
    right: float
