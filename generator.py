from typing import List

from src.polynomial import Polynomial


def generate_matrix_a(xs: List[float], omega: List[float], finite_elems: List[List[float]]) -> List[List[float]]:
    """Сгенерировать глобальную матрицу A для СЛАУ сплайна.

    Args:
        xs (List[float]): точки, в которых взяты значения функции
        omega (List[float]): веса, регулирующие близость сплайна в точке x
        finite_elems (List[List[float]]): список конечных элементов

    Returns:
        Сгенерированная матрица A.
    """

    matrix_size = 2 * (len(finite_elems) + 1)
    global_a = [[0 for col in range(matrix_size)] for row in range(matrix_size)]
    matrix_a_offset = 0

    for elem in finite_elems:
        local_a = __generate_local_matrix_a__(xs, omega, elem)

        for i in range(len(local_a)):
            for j in range(len(local_a)):
                global_a[matrix_a_offset + i][matrix_a_offset + j] += local_a[i][j]
        matrix_a_offset += 2

    return global_a


def __generate_local_matrix_a__(xs: List[float], omega: List[float], finite_elem: List[float]) -> List[List[float]]:
    """Сгенерировать локальную матрицу A для конечного элемента.

    Args:
        xs (List[float]): точки, в которых взяты значения функции
        omega (List[float]): веса, регулирующие близость сплайна в точке x
        finite_elem (List[float]]): конечный элемент

    Returns:
        Сгенерированная локальная матрица A.
    """
    matrix_size = 4

    xs_in_finite_elem = list(filter(lambda x: finite_elem[0] <= x <= finite_elem[1], xs))

    local_a = [[0 for col in range(matrix_size)] for row in range(matrix_size)]

    for i in range(matrix_size):
        for j in range(matrix_size):
            component_value = 0

            for k in range(len(xs_in_finite_elem)):
                psi_first = calculate_psi(i + 1, xs_in_finite_elem[k], finite_elem)
                psi_second = calculate_psi(j + 1, xs_in_finite_elem[k], finite_elem)
                component_value += psi_first * psi_second * omega[k]

            local_a[i][j] = component_value

    return local_a


def calculate_psi(psi_number: int, point: float, finite_elem: List[float]) -> float:
    """Вычислить значение psi в точке относительно конечного элемента.

    Args:
        psi_number (int): номер функции psi, от 1 до 4
        point (float): точка, в которой будет вычисляться значение psi
        finite_elem (List[float]): конечный элемент

    Returns:
        Значение функции psi в точке.
    """
    phi_functions = [
        [1, 0, -3, 2],
        [0, 1, -2, 1],
        [0, 0, 3, -2],
        [0, 0, -1, 1]
    ]

    finite_elem_len = finite_elem[1] - finite_elem[0]
    normalized_point = (point - finite_elem[0]) / finite_elem_len

    psi_value = Polynomial(phi_functions[psi_number - 1]).calc(normalized_point)
    if psi_number % 2:
        return psi_value
    else:
        return finite_elem_len * psi_value


def generate_vector_b(xs: List[float], fs: List[float], omega: List[float], finite_elems: List[List[float]]) -> \
        List[float]:
    """Сгенерировать глобальный вектор b для СЛАУ сплайна.

    Args:
        xs (List[float]): точки, в которых взяты значения функции
        fs (List[float]): значения функции, по которым будет строиться сплайн
        omega (List[float]): веса, регулирующие близость сплайна в точке x
        finite_elems (List[List[float]]): список конечных элементов

    Returns:
        Сгенерированный вектор b.
    """

    vector_size = 2 * (len(finite_elems) + 1)
    global_b = [0 for i in range(vector_size)]
    vector_b_offset = 0

    for elem in finite_elems:
        local_b = __generate_local_vector_b__(xs, fs, omega, elem)

        for i in range(len(local_b)):
            global_b[vector_b_offset + i] += local_b[i]
        vector_b_offset += 2

    return global_b


def __generate_local_vector_b__(xs: List[float], fs: List[float], omega: List[float], finite_elem: List[float]) -> \
        List[float]:
    """Сгенерировать локальный вектор b для конечного элемента.

    Args:
        xs (List[float]): точки, в которых взяты значения функции
        fs (List[float]): значения функции, по которым будет строиться сплайн
        omega (List[float]): веса, регулирующие близость сплайна в точке x
        finite_elem (List[float]): список конечных элементов

    Returns:
        Сгенерированный локальный вектор b.
    """
    vector_size = 4

    xs_in_finite_elem = []
    fs_in_finite_elem = []
    for i in range(len(xs)):
        if finite_elem[0] <= xs[i] < finite_elem[1]:
            xs_in_finite_elem.append(xs[i])
            fs_in_finite_elem.append(fs[i])

    local_b = [0 for i in range(vector_size)]
    for b_index in range(vector_size):
        component_value = 0

        for i in range(len(xs_in_finite_elem)):
            psi = calculate_psi(b_index + 1, xs_in_finite_elem[i], finite_elem)
            component_value += psi * fs_in_finite_elem[i] * omega[i]
        local_b[b_index] = component_value

    return local_b
