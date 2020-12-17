from typing import List, Callable, Dict
import argparse
from math import sin, fabs
import statistics

from src import spline, linsys_generator as gen, linear_equation
from src.utils import get_finite_elements
from src.deviations import get_deviations, get_recompute_dict, recompute_omega

import matplotlib.pyplot as plt
from numpy import std


def compute_spline_points(xs: List[float], fs: List[float], fins: List[float],
                          beta_func: Callable, omega: List[float]) -> List[float]:
    finite_elems = get_finite_elements(fins)
    xs_length = len(xs)

    a = gen.generate_regularized_matrix_a(
        xs=xs,
        omega=omega,
        finite_elems=finite_elems,
        alpha=lambda: 0,
        # beta=lambda: 0.000001
        beta=beta_func
    )
    b = gen.generate_vector_b(
        xs=xs,
        fs=fs,
        omega=omega,
        finite_elems=finite_elems
    )
    q = linear_equation.solve(
        system_coeffs=a,
        constants=b
    )

    spline_dots = []
    for x in xs:
        spline_dot = spline.compute_spline_in_point(
            x=x,
            finite_elems=finite_elems,
            qs=q
        )
        spline_dots.append(spline_dot)

    return spline_dots


def spline_with_omega():
    # omega_param = 0.62
    omega_param = 1.61290322581

    xs = [x * 0.05 for x in range(200)]
    fs = list(map(lambda x: - 1 * (x ** 2) + 6 * x + 9, xs))
    # fs[4] += 0.9
    # fs = list(map(lambda x: x ** 2 + x - 3, xs))
    finite_elems = [0, 12]
    a_omega = [1 for i in range(len(xs))]

    spline_points_first = compute_spline_points(
        xs=xs, fs=fs, fins=finite_elems, beta_func=lambda: 0.001,
        omega=a_omega
    )
    plt.plot(xs, fs)
    plt.plot(xs, spline_points_first)
    plt.show()

    deviations = get_deviations(fs, spline_points_first)
    mean = statistics.mean(deviations)
    recompute = get_recompute_dict(mean, omega_param, deviations)

    tuned_spline_points = [0 for i in range(200)]
    while len(recompute.keys()) != 0:
        print(recompute.keys())
        recompute_omega(recompute, a_omega)
        tuned_spline_points = compute_spline_points(
            xs=xs, fs=fs, fins=finite_elems, beta_func=lambda: 0.001,
            omega=a_omega
        )
        next_deviations = get_deviations(fs, tuned_spline_points)
        next_mean = statistics.mean(next_deviations)
        recompute = get_recompute_dict(next_mean, omega_param, next_deviations)

    plt.plot(xs, fs)
    plt.plot(xs, tuned_spline_points)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--xs', dest='xs', nargs='+', help='список значений x, на которых будет строиться сплайн')
    parser.add_argument('--fs', dest='fs', nargs='+', help='список значений функции f, полученных на точках x')
    parser.add_argument('--fins', dest='finite_elems', nargs='+', help='список точек конечных элементов')
    parsed_args = parser.parse_args()

    xs = [x * 0.05 for x in range(200)]
    # fs = list(map(lambda x: - 1 * (x ** 2) + 6 * x + 9, xs))
    # finite_elems = [0, 7, 12]

    # fs = list(map(lambda x: sin(x), xs))
    # finite_elems = [0, 3, 6, 9, 12]

    # fs = list(map(lambda x: sin(x * 0.75), xs))
    # finite_elems = [0, 5, 12]

    # fs = list(map(lambda x: sin(x) * 0.75, xs))
    # finite_elems = [0, 3, 6, 9, 12]
    # finite_elems = [0, 5, 8, 12]

    # fs = list(map(lambda x: x ** 2 + x - 3, xs))
    # finite_elems = [0, 5, 12]

    # fs = list(map(lambda x: x ** 2 + 2 * x + 3, xs))
    # finite_elems = [0, 5, 12]

    # fs = list(map(lambda x: x ** 2 + 2 * x + 3, xs))
    # fs[4] = 4
    # fs[8] = 8
    # fs[15] = 15
    # fs[16] = 16
    # fs[16] = 16
    # fs[23] = 23
    # fs[42] = 42
    # fs[108] = 108
    # finite_elems = [0, 5, 12]

    # fs = list(map(lambda x: - 1 * (x ** 2) + 6 * x + 9, xs))
    # finite_elems = [0, 12]
    #
    # a_omega = [1 for i in range(len(xs))]
    #
    # spline_points1 = compute_spline_points(xs=xs, fs=fs, fins=finite_elems, beta_func=lambda: 0.001, omega=a_omega)
    # plt.plot(xs, fs)
    # plt.plot(xs, spline_points1)
    # plt.show()

    spline_with_omega()

    # converted_xs = list(map(float, parsed_args.xs))
    # converted_fs = list(map(float, parsed_args.fs))
    # converted_finite_elems = list(map(float, parsed_args.finite_elems))
    # spline_points = compute_spline_points(
    #     xs=converted_xs,
    #     fs=converted_fs,
    #     fins=converted_finite_elems
    # )
    # print(spline_points)
