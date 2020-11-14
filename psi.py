from finite_element import FiniteElement
from polynomial import Polynomial


def calculate_psi(psi_number: int, point: float, finite_elem: FiniteElement) -> float:
    """Вычислить значение psi в точке относительно конечного элемента.

    Args:
        psi_number (int): номер функции psi, от 1 до 4
        point (float): точка, в которой будет вычисляться значение psi
        finite_elem (FiniteElement): конечный элемент

    Returns:
        Значение функции psi в точке.
    """
    phi_functions = [
        [1, 0, -3, 2],
        [0, 1, -2, 1],
        [0, 0, 3, -2],
        [0, 0, -1, 1]
    ]

    finite_elem_len = finite_elem.right - finite_elem.left
    normalized_point = (point - finite_elem.left) / finite_elem_len

    psi_value = Polynomial(phi_functions[psi_number - 1]).calc(normalized_point)
    if psi_number % 2:
        return psi_value
    else:
        return finite_elem_len * psi_value
