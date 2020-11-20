from typing import List, Callable

from src.polynomial import Polynomial
from src.finite_element import FiniteElement
from src import riemann_sum


def generate_beta_regularization_matrix(beta: Callable, finite_elems: List[FiniteElement]) -> List[List[float]]:
    """Вычилить матрицу регуляризации, состоящую из определённых интегралов
       вторых производных функций phi, умноженных на параметр beta.

    Args:
        beta (Callable): параметр beta, "подкручивающий" значение вторых производных
        finite_elems: список конечных элементов

    Returns:
        Матрица регуляризации.
    """
    matrix_size = 2 * (len(finite_elems) + 1)
    global_beta_reg = [[0 for c in range(matrix_size)] for r in range(matrix_size)]
    matrix_offset = 0

    for elem in finite_elems:
        local_reg = __generate_local_beta_regularization_matrix__(beta, elem)

        for i in range(len(local_reg)):
            for j in range(len(local_reg)):
                global_beta_reg[matrix_offset + i][matrix_offset + j] += local_reg[i][j]
        matrix_offset += 2

    return global_beta_reg


def __generate_local_beta_regularization_matrix__(beta: Callable, finite_elem: FiniteElement) -> List[List[float]]:
    """Вычислить локальную матрицу регуляризации beta.

    Args:
        beta (Callable): параметр beta, "подкручивающий" значение вторых производных
        finite_elem (FiniteElement): конечный элемент, на котором будет вычисляться матрица

    Returns:
        Локальная матрица регуляризации.
    """
    matrix_size = 4
    local_beta_reg = [[0 for c in range(matrix_size)] for r in range(matrix_size)]

    for i in range(matrix_size):
        for j in range(matrix_size):
            local_beta_reg[i][j] = __compute_beta_matrix_element__(
                phi_1_number=i + 1,
                phi_2_number=j + 1,
                beta=beta,
                finite_elem=finite_elem
            )
    return local_beta_reg


def __compute_beta_matrix_element__(phi_1_number: int, phi_2_number: int,
                                    beta: Callable, finite_elem: FiniteElement) -> float:
    """Вычислить элемент регуляризирующей матрицы.
    Для этого вычислится интеграл от произведения вторых производных функций phi и beta-параметра.
    integral ( beta * (d2/dx^2 phi[phi_1_number](x)) * (d2/dx^2 phi[phi_2_number](x)) ) dx, x=0..1

    Args:
        phi_1_number (int): номер первой функции phi
        phi_2_number (int): номер второй функции phi
        beta (Callable): параметр beta, "подкручивающий" значение вторых производных
        finite_elem (FiniteElement): конечный элемент

    Returns:

    """
    def integrating_function(x: float) -> float:
        """Вычислить значение подынтегральной функции.
        Подинтегральная функция: beta * (d2/dx^2 phi[phi_1_number](x)) * (d2/dx^2 phi[phi_2_number](x))

        Args:
            x (float): точка, в которой будет вычисляться значение производных

        Returns:
            Значение функции.
        """

        return beta() * __compute_second_phi_derivative__(phi_1_number, x, finite_elem)\
            * __compute_second_phi_derivative__(phi_2_number, x, finite_elem)

    return riemann_sum.integrate(
        func=integrating_function,
        bound_a=finite_elem.left,
        bound_b=finite_elem.right,
        subintervals=1000
    )


def __compute_first_phi_derivative__(phi_number: int, x: float, finite_elem: FiniteElement) -> float:
    """Численно вычислить первую производную phi.

    Args:
        phi_number (int): номер локальной функции phi, от 1 до 4
        x (float): точка, в которой вычисляется значение производной
        finite_elem (FiniteElement): конечный элемент, на котором определена функция phi

    Returns:
        Значение первой производой в точке.
    """
    phi_first_derivative = [
        [0, -6, 6],
        [0, -4, 3],
        [0, 6, -6],
        [0, -2, 3],
    ]
    deriv_phi_value = Polynomial(phi_first_derivative[phi_number - 1]).calc(x)
    if phi_number % 2:
        return deriv_phi_value
    else:
        return (1 / finite_elem.length()) * deriv_phi_value


def __compute_second_phi_derivative__(phi_number: int, x: float, finite_elem: FiniteElement) -> float:
    """Численно вычислить вторую производную phi.

    Args:
        phi_number (int): номер локальной функции phi, от 1 до 4
        x (float): точка, в которой вычисляется значение производной
        finite_elem (FiniteElement): конечный элемент, на котором определена функция phi

    Returns:
        Значение второй производой в точке.
    """
    phi_second_derivative = [
        [-6, 12],
        [-4, 6],
        [6, -12],
        [-2, 6]
    ]
    deriv_phi_value = Polynomial(phi_second_derivative[phi_number - 1]).calc(x)
    if phi_number % 2:
        return (1 / finite_elem.length()) * deriv_phi_value
    else:
        return (1 / (finite_elem.length() ** 2)) * deriv_phi_value
