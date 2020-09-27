from typing import List

def solve(system_coeffs: List[List[float]], constants: List[float]) -> List[float]:
    """Решить систему линейных уравнений.

    Args:
        system_coeffs (List[List[float]]): матрица системы
        constants (List[float]): вектор постоянных

    Results:
        Вектор решения системы.
    """

    size = len(system_coeffs)
    a = [[system_coeffs[i][j] for j in range(size)] for i in range(size)]
    b = [constants[i] for i in range(size)]

    for column in range(size):
        swapped_row = __find_row_with_max_element__(a, column)
        a[column], a[swapped_row] = a[swapped_row], a[column]
        b[column], b[swapped_row] = b[swapped_row], b[column]

    for row in range(size - 1):
        inverse_diagonal_el = 1 / a[row][row]

        for row_under in range(row + 1, size):
            coefficient = a[row_under][row] * inverse_diagonal_el

            a[row_under][row] = 0
            for col in range(row + 1, size):
                a[row_under][col] -=  a[row][col] * coefficient

            b[row_under] -= b[row] * coefficient


    solution = [0 for i in range(size)]

    for row in reversed(range(size)):
        inverse_diagonal_el = 1 / a[row][row]
        s = 0
        for col in range(row + 1, size):
            s += a[row][col] * solution[col]

        solution[row] = (b[row] - s) * inverse_diagonal_el

    return solution

def __find_row_with_max_element__(matrix: List[List[float]], start_row: int) -> int:
    """Найти строку в матрице с элементом большим по модулю, чем на диагонали.

    Args:
        matrix (List[List[float]]): квадратная матрица 
        start_row (int): номер строки, содержащей текущий диагональный элемент

    Returns:
        Номер строки, в которой находится элемент больший, чем на диагонали.
    """

    diagonal_element = matrix[start_row][start_row]
    row_with_max_element = start_row

    for row in range(start_row, len(matrix)):
        if abs(matrix[row][start_row]) > abs(diagonal_element):
            diagonal_element = matrix[row][start_row]
            row_with_max_element = row

    return row_with_max_element
