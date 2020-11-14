from typing import Callable


def integrate(func: Callable, bound_a: float, bound_b: float, subintervals: int) -> float:
    """Выислить значение интеграла функции f(x) на интервале [a, b]  метожом средних прямоугольников.

    Args:
        func (Callable): функция, от которой будет браться интеграл
        bound_a (float): левая граница интервала
        bound_b (float): правая граница интервала
        subintervals (int): количество подинтервалов, на которых будет браться значение функци

    Returns:
        Значение интеграла на интервале.
    """
    subinterval_length = (bound_b - bound_a) / subintervals

    integral_value = 0
    for i in range(subintervals):
        x = bound_a + (i * subinterval_length)
        integral_value += func(x)

    return integral_value * subinterval_length
