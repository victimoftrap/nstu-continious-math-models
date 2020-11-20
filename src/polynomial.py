from __future__ import annotations

from typing import List


class Polynomial:

    def __init__(self, coeffs: List[float]):
        self.coeffs = coeffs
        self.deg = len(coeffs)

    def __str__(self) -> str:
        output = ""
        for i in reversed(range(self.deg)):
            output += f"{self.coeffs[i]}x^{i} "
        return output

    def derivative(self) -> Polynomial:
        """Получить производную полинома.

        Returns:
            Полином, являющийся производной данного.
        """
        return Polynomial([deg * coeff for deg, coeff in enumerate(self.coeffs[1:], start=1)])

    def calc(self, x: float) -> float:
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

    def integrate(self, x1: float, x2: float) -> float:
        """Вычисление интеграла Римана полинома по формуле Ньютона-Лейбница.

        Args:
            x1 (float): нижний предел
            x2 (float): верхний предел

        Returns:
            Значение интеграла.
        """
        new_coeffs = [coeff / (deg + 1) for deg, coeff in enumerate(self.coeffs)]
        new_coeffs.insert(0, .0)
        antiderivative = Polynomial(new_coeffs)
        return antiderivative.calc(x2) - antiderivative.calc(x1)

    def multiply(self, poly: Polynomial) -> Polynomial:
        """Умножить этот полином на другой.

        Args:
            poly (Polynomial): полином, на который будет умножен текущий полином

        Returns:
            Новый полином, являющийся результатом умножения двух полиномов.
        """

        new_polynom = []
        size = max(self.deg, poly.deg)

        for i in range(size):
            new_polynom.append(self.coeffs[i] * poly.coeffs[i])
        return Polynomial(new_polynom)
