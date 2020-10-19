from polynomial import Polynomial
from finite_element import FiniteElement


def compute_phi_derivative(phi_number: int, x: float, finite_elem: FiniteElement) -> float:
    phi_second_derivative = [
        [-6, 12],
        [-4, 6],
        [6, -12],
        [-2, 6]
    ]

    deriv_phi_value = Polynomial(phi_second_derivative[phi_number]).calc(x)
    if phi_number % 2:
        return (1 / finite_elem.length()) * deriv_phi_value
    else:
        return (1 / (finite_elem.length() ** 2)) * deriv_phi_value
