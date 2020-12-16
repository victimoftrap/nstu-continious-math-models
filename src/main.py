from math import sin
import sys

from src import spline, linsys_generator as gen, linear_equation
from src.utils import get_finite_elements

import numpy

from PySide2 import QtWidgets
import pyqtgraph as pg

q = []
finite_elems = []
xs = []
fs = []


def compute(x):
    return spline.compute_spline_in_point(
        x=x,
        finite_elems=finite_elems,
        qs=q
    )


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        spline_points = numpy.arange(0.0, 5.0, 0.05)
        y = list(map(compute, spline_points))

        # plot data: x, y values
        self.graphWidget.plot(spline_points, y)
        self.graphWidget.plot(xs, fs, pen=None, symbol='o')


def calculate():
    global q
    global finite_elems
    global xs
    global fs

    xs = [x * 0.5 for x in range(10)]
    xs_length = len(xs)
    fs = list(map(sin, xs))
    finite_elems = get_finite_elements([0, 3, 6])

    a = gen.generate_regularized_matrix_a(
        xs=xs,
        omega=[1 for i in range(xs_length)],
        finite_elems=finite_elems,
        alpha=lambda: 0,
        beta=lambda: 0.001
    )
    b = gen.generate_vector_b(
        xs=xs,
        fs=fs,
        omega=[1 for i in range(xs_length)],
        finite_elems=finite_elems
    )
    q = linear_equation.solve(
        system_coeffs=a,
        constants=b
    )


def main():
    calculate()
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
