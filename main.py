from finite_element import FiniteElement
import linsys_generator as gen
import linear_equation
import spline

if __name__ == "__main__":
    xs = [0., 0.5, 1.1, 1.5, 2., 2.5, 3., 4., 4.5, 4.8, 5.]
    fs = [2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.3, 1.2, 0.8, 0.]
    finite_elems = [FiniteElement(0, 2), FiniteElement(2, 5)]
    spline_point = 0.8

    a = gen.generate_regularized_matrix_a(
        xs=xs,
        omega=[1 for i in range(11)],
        finite_elems=finite_elems,
        alpha=lambda: 0,
        beta=lambda: 0.000001
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

    res = spline.compute_spline_in_point(
        x=spline_point,
        finite_elems=finite_elems,
        qs=q
    )
    print("Spline in point", spline_point, "is", res)
