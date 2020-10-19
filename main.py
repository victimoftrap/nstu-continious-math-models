import generator as gen
import linear_equation
import spline as spl

if __name__ == "__main__":
    # a = gen.generate_matrix_a(
    #     xs=[0., 0.5, 1.1, 1.5, 2., 2.5, 3., 4., 4.5, 4.8, 5.],
    #     omega=[1 for i in range(11)],
    #     finite_elems=[[0, 2], [2, 5]]
    # )
    # b = gen.generate_vector_b(
    #     xs=[0., 0.5, 1.1, 1.5, 2., 2.5, 3., 4., 4.5, 4.8, 5.],
    #     fs=[2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.3, 1.2, 0.8, 0.],
    #     omega=[1 for i in range(11)],
    #     finite_elems=[[0, 2], [2, 5]]
    # )
    # q = linear_equation.solve(
    #     system_coeffs=a,
    #     constants=b
    # )
    # print(q)

    res = spl.compute_spline_in_point(
        0.8,
        [[0, .5], [.5, 1], [1, 1.5], [1.5, 2], [2, 2.5]],
        [10.01, -0.228, 9.885, -0.085, 7.811, -8.826, 3.348, -8.923, 1.076, -0.434, 0.939, -0.129]
    )
    print(res)
