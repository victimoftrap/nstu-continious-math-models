from typing import List


class Polynomial:

    def __init__(self, coeffs: List[float]):
        self.coeffs = coeffs
        self.deg = len(coeffs)

    def derivative(self):
        """Получить производную полинома.

        Returns:
            Полином, являющийся производной данного.
        """
        return Polynomial([deg * coeff for deg, coeff in enumerate(self.coeffs[1:], start=1)])

    def calc(self, x):
        """Вычислить полином в точке.

        Args:
            x: точка, в которой вычисляется значение полинома

        Returns:
            Значение данного полинома в точке x.
        """
        res = .0
        for i in range(self.deg):
            res += (x ** i) * self.coeffs[i]
        return res

    def integrate(self, x1, x2):
        """Вычисление интеграла Римана полинома по формуле Ньютона-Лейбница.

        Args:
            x1: нижний предел
            x2: верхний предел

        Returns:
            Значение интеграла.
        """
        new_coeffs = [coeff / (deg + 1) for deg, coeff in enumerate(self.coeffs)]
        new_coeffs.insert(0, .0)
        antiderivative = Polynomial(new_coeffs)
        return antiderivative.calc(x2) - antiderivative.calc(x1)
