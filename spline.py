from typing import List
from generator import calculate_psi
from operator import mul


def compute_spline_in_point(x: float, finite_elems: List[List[float]], qs: List[float]) -> float:
    """Вычислить значение сплайна в выбранной точке.

    Args:
        x (float): точка, в которой вычисляется сплайн
        finite_elems (List[List[float]]): конечные элемены
        qs (List[float]): решение СЛАУ Aq=b

    Returns:
        значение сплайна в точке.
    """

    working_finite_elem = []
    working_finite_elem_index = 0

    for i in range(len(finite_elems)):
        if finite_elems[i][0] <= x <= finite_elems[i][1]:
            working_finite_elem = finite_elems[i]
            working_finite_elem_index = i + 1

    working_qs = qs[2 * working_finite_elem_index - 2: 2 * working_finite_elem_index + 2]
    psi_in_x = map(lambda psi_num: calculate_psi(psi_num, x, working_finite_elem), range(1, 5))
    return sum(map(mul, working_qs, psi_in_x))
