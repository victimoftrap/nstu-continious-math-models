import generator as gen
import linear_equation

if __name__ == "__main__":
    a = gen.generate_matrix_a(
        xs=[0., 0.5, 1.1, 1.5, 2., 2.5, 3., 4., 4.5, 4.8, 5.],
        omega=[1 for i in range(11)],
        finite_elems=[[0, 2], [2, 5]]
    )
    b = gen.generate_vector_b(
        xs=[0., 0.5, 1.1, 1.5, 2., 2.5, 3., 4., 4.5, 4.8, 5.], 
        fs=[2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.3, 1.2, 0.8, 0.],
        omega=[1 for i in range(11)],
        finite_elems=[[0, 2], [2, 5]]
    )
    q = linear_equation.solve(
        system_coeffs=a,
        constants=b
    )
    print(q)
