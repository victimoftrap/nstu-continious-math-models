from typing import List
from operator import mul

from finite_element import FiniteElement
from linsys_generator import calculate_psi


def compute_spline_in_point(x: float, finite_elems: List[FiniteElement], qs: List[float]) -> float:
    """Вычислить значение сплайна в выбранной точке.

    Args:
        x (float): точка, в которой вычисляется сплайн
        finite_elems (List[FiniteElement]): конечные элемены
        qs (List[float]): решение СЛАУ Aq=b

    Returns:
        значение сплайна в точке.
    """

    working_finite_elem = []
    working_finite_elem_index = 0

    for i in range(len(finite_elems)):
        if finite_elems[i].left <= x < finite_elems[i].right:
            working_finite_elem = finite_elems[i]
            working_finite_elem_index = i + 1

    working_qs = qs[2 * working_finite_elem_index - 2: 2 * working_finite_elem_index + 2]
    psi_in_x = map(lambda psi_num: calculate_psi(psi_num, x, working_finite_elem), range(1, 5))
    return sum(map(mul, working_qs, psi_in_x))
