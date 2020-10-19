import generator as gen
import linear_equation
import spline as spl

if __name__ == "__main__":
    xs = [0., 0.5, 1.1, 1.5, 2., 2.5, 3., 4., 4.5, 4.8, 5.]
    fs = [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.3, 1.2, 0.8, 0.]
    finite_elems = [[0, 2], [2, 5]]
    spline_point = 0.8

    a = gen.generate_matrix_a(
        xs=xs,
        omega=[1 for i in range(11)],
        finite_elems=finite_elems
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

    res = spl.compute_spline_in_point(
        x=spline_point,
        finite_elems=finite_elems,
        qs=q
    )
    print("Spline in point", spline_point, "is", res)
