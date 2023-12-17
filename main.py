import plotly.figure_factory as ff
from math import sin, cos, pi


def multiply_matrices(matrix1, matrix2):
    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix2[0])):
            sum = 0
            for k in range(len(matrix2)):
                sum += matrix1[i][k] * matrix2[k][j]
            row.append(sum)
        result.append(row)
    return result


def shift(x, y, z, shift_x=0.0, shift_y=0.0, shift_z=0.0):
    xn = [val + shift_x for val in x]
    yn = [val + shift_y for val in y]
    zn = [val + shift_z for val in z]

    return xn, yn, zn


def resize(x, y, z, k = 1.0):
    return [val * k for val in x], [val * k for val in y], [val * k for val in z]


def rotate_ox(angle, x, y, z):
    m1 = [x, y, z]
    m2 = [[1, 0, 0],
          [0, cos(angle), -sin(angle)],
          [0, sin(angle), cos(angle)]]

    return multiply_matrices(m2, m1)


def rotate_oz(angle, x, y, z):
    m1 = [x, y, z]
    m2 = [[cos(angle), -sin(angle), 0],
          [sin(angle), cos(angle), 0],
          [0, 0, 1]]

    return multiply_matrices(m2, m1)


def rotate_oy(angle, x, y, z):
    m1 = [x, y, z]
    m2 = [[cos(angle), 0, sin(angle)],
          [0, 1, 0],
          [-sin(angle), 0, cos(angle)]]

    return multiply_matrices(m2, m1)


points = [[0, 0, 0], [1, 0, 0], [3, 0, 6], [4, 0, 6], [3, 0, 0], [4, 0, 0], [0, 0, 6], [1, 0, 6],
          [2, 0, 4],
          [1.5, 0, 3],
          [2.5, 0, 3],
          [2, 0, 2]]

points.extend([[point[0], point[1] + 0.3, point[2]] for point in points])

x = [a[0] for a in points]
y = [a[1] for a in points]
z = [a[2] for a in points]

run = True

while run:
    command = input("enter command, to break enter b, for help enter h:\n")
    if command.strip().startswith("rotate"):
        command = command.split()
        if command[1] == "x":
            x, y, z = rotate_ox(float(command[2]) * pi / 180, x, y, z)
        elif command[1] == "y":
            x, y, z = rotate_oy(float(command[2]) * pi / 180, x, y, z)
        elif command[1] == "z":
            x, y, z = rotate_oz(float(command[2]) * pi / 180, x, y, z)
        else:
            print("incorrect command")
    elif command.strip().startswith("shift"):
        command = command.split()
        x, y, z = shift(x, y, z, float(command[1]), float(command[2]), float(command[3]))
    elif command.strip().startswith("resize"):
        command = command.split()
        x, y, z = resize(x, y, z, float(command[1]))
    elif command.strip() == "b":
        run = False
    elif command.strip() == "h":
        print("to rotate an object around ox/oy/oz angle degrees enter:"
              "rotate {x/y/z} {angle}"
              "to shift coordinate x by val1 coordinate y by val2 coordinate z by val3 enter:"
              "shift {val1}, {val2}, {val3}"
              "to resize object by val enter:"
              "resize {val}", sep='\n')
    else:
        print("unknown command, enter h for help")

x.append(-10)
x.append(10)
y.append(-10)
y.append(10)
z.append(-10)
z.append(10)

simplices = [[0, 1, 2], [1, 2, 3], [6, 7, 9], [7, 9, 8], [10, 11, 4], [10, 4, 5]]

simplices.extend([list(map(lambda x: x + 12, s)) for s in simplices])

simplices.extend([[0, 12, 9], [12, 9, 21], [6, 9, 18], [9, 18, 21], [6, 7, 18], [7, 18, 19], [2, 3, 14], [3, 14, 15],
                  [0, 1, 12], [1, 12, 13],
                  [4, 5, 16], [5, 16, 17],
                  [7, 8, 19], [8, 20, 19],
                  [2, 8, 14], [8, 20, 14],
                  [3, 10, 15], [10, 15, 22],
                  [5, 10, 17], [10, 17, 22],
                  [1, 11, 13], [11, 13, 23],
                  [4, 11, 16], [11, 16, 23]])

colors = ["rgb(0, 0, 0)" for i in range(len(simplices))]

fig = ff.create_trisurf(x=x, y=y, z=z,
                        simplices=simplices,
                        color_func=colors,
                        plot_edges=False,
                        title="Torus", aspectratio=dict(x=1, y=1, z=1))
fig.show()
