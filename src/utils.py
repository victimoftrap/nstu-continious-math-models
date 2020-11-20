from typing import List

from src.finite_element import FiniteElement


def get_finite_elements(points: List[float]) -> List[FiniteElement]:
    """Создать список конечных элементов по списку точек.
    К примеру, по списку точек [0; 2; 5] будут получены конечные элементы [0; 2] и [2; 5].
    
    Args:
        points (List[float]): список точек, по которым будет построен список конечных элементов 

    Returns:
        список конечных элементов.
    """

    finite_elems = []
    for i in range(len(points) - 1):
        finite_elems.append(FiniteElement(points[i], points[i + 1]))
    return finite_elems
