from math import sin

import numpy

from finite_element import FiniteElement
import linsys_generator as gen
import linear_equation
import spline

from PySide2 import QtWidgets
import pyqtgraph as pg
import sys

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

    xs = [0., 0.5, 1.1, 1.5, 2., 2.5, 2.7, 3., 4., 4.5, 4.8, 5.]
    fs = list(map(sin, xs))
    # fs[2] = -0.5
    finite_elems = [FiniteElement(0, 2), FiniteElement(1, 2), FiniteElement(2, 3),
                    FiniteElement(3, 3.5), FiniteElement(2, 5)]
    # spline_point = 0.8

    a = gen.generate_regularized_matrix_a(
        xs=xs,
        omega=[1 for i in range(11)],
        finite_elems=finite_elems,
        alpha=lambda: 0,
        beta=lambda: 0.001
    )

    b = gen.generate_vector_b(
        xs=xs,
        fs=fs,
        omega=[1 for i in range(11)],
        finite_elems=finite_elems
    )
    q = linear_equation.solve(
        system_coeffs=a,
        constants=b
    )
    # print("Got solution of linear system: ", q)

    # res = spline.compute_spline_in_point(
    #     x=spline_point,
    #    finite_elems=finite_elems,
    #     qs=q
    # )
    # print("Spline in point", spline_point, "is", res)


def main():
    calculate()
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
