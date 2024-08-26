from numba import jit, prange


@jit(fastmath=True)
def neighborhood_mur(field, x, y, val, radius):
    count = 0
    if field[x, y] == val:
        count -= 1
    for j in prange(y - radius, y + radius + 1):
        for i in prange(x - radius, x + radius + 1):
            if field[i, j] == val:
                count += 1
    return count


@jit(fastmath=True)
def neighbourhood_von_neumann(field, x, y, val, radius):
    count = 0
    if field[x, y] == val:
        count -= 1
    for i in prange(x - radius, x + radius + 1):
        for j in prange(y - radius, y + radius + 1):
            if abs(i - x) + abs(j - y) <= radius:
                if field[i, j] == val:
                    count += 1
    return count


@jit(fastmath=True)
def neighbourhood_von_neumann_external(field, x, y, val, radius):
    count = 0
    for i in prange(x - radius, x + radius + 1):
        for j in prange(y - radius, y + radius + 1):
            if abs(i - x) + abs(j - y) == radius:
                if field[i, j] == val:
                    count += 1
    return count


@jit(fastmath=True)
def neighborhood_mur_external(field, x, y, val, radius):
    count = 0

    for j in prange(y - radius, y + radius + 1):
        if field[x - radius, j] == val:
            count += 1
    for j in prange(y - radius, y + radius + 1):
        if field[x + radius, j] == val:
            count += 1

    for i in prange(x - radius, x + radius + 1):
        if field[i, y - radius + 1] == val:
            count += 1
    for i in prange(x - radius, x + radius + 1):
        if field[i, y + radius - 1] == val:
            count += 1

    return count


@jit(fastmath=True)
def neighborhood_diagonal(field, x, y, val, radius):
    count = 0

    for i in prange(x - radius, x):
        for j in prange(y + 1, y + radius + 1):
            if field[i, y + radius - 1] == val:
                count += 1

    for i in prange(x + 1, x + radius + 1):
        for j in prange(y - radius, y):
            if field[i, j] == val:
                count += 1

    return count


@jit(fastmath=True)
def neighborhood_lines(field, x, y, val, radius):
    count = 0

    for j in prange(y + 1, y + radius + 1):
        if field[x - radius, j] == val:
            count += 1
    for j in prange(y + 1, y + radius + 1):
        if field[x, j] == val:
            count += 1
    for j in prange(y - radius, y):
        if field[x, j] == val:
            count += 1
    for j in prange(y - radius, y):
        if field[x + radius, j] == val:
            count += 1

    return count


@jit(fastmath=True)
def neighbourhood_euclid(field, x, y, val, radius):
    count = 0
    if field[x, y] == val:
        count -= 1
    for i in prange(x - radius, x + radius + 1):
        for j in prange(y - radius, y + radius + 1):
            if ((i - x) ** 2 + (j - y) ** 2) ** 0.5 <= radius:
                if field[i, j] == val:
                    count += 1
    return count


@jit(fastmath=True)
def neighbourhood_circle(field, x, y, val, radius):
    count = 0
    if field[x, y] == val:
        count -= 1
    for i in prange(x - radius, x + radius + 1):
        for j in prange(y - radius, y + radius + 1):
            if ((i - x) ** 2 + (j - y) ** 2) ** 0.5 <= radius + 0.5:
                if field[i, j] == val:
                    count += 1
    return count


@jit(fastmath=True)
def neighbourhood_chess(field, x, y, val, radius):
    count = 0

    for i in prange(x - radius, x + radius + 1):
        for j in prange(y - radius, y + radius + 1):
            if (abs(x - i) + abs(y - j)) % 2:
                if field[i, j] == val:
                    count += 1
    return count


@jit(fastmath=True)
def neighbourhood_chess_inverse(field, x, y, val, radius):
    count = 0
    if field[x, y] == val:
        count -= 1

    for i in prange(x - radius, x + radius + 1):
        for j in prange(y - radius, y + radius + 1):
            if (abs(x - i) + abs(y - j)) % 2 == 0:
                if field[i, j] == val:
                    count += 1
    return count


@jit(fastmath=True)
def neighbourhood_lattice(field, x, y, val, radius):
    count = 0

    for i in prange(x - radius, x + radius + 1):
        for j in prange(y - radius, y + radius + 1):
            if (abs(x - i) == 1) or (abs(y - j) == 1):
                if field[i, j] == val:
                    count += 1
    return count


@jit(fastmath=True)
def neighbourhood_plus(field, x, y, val, radius):
    count = 0
    if field[x, y] == val:
        count -= 1

    for i in prange(x - radius, x + radius + 1):
        for j in prange(y - radius, y + radius + 1):
            if (abs(x - i) == 0) or (abs(y - j) == 0):
                if field[i, j] == val:
                    count += 1
    return count


@jit(fastmath=True)
def neighbourhood_cross(field, x, y, val, radius):
    count = 0
    if field[x, y] == val:
        count -= 1

    for i in prange(x - radius, x + radius + 1):
        for j in prange(y - radius, y + radius + 1):
            if abs(x - i) == abs(y - j):
                if field[i, j] == val:
                    count += 1
    return count


@jit(fastmath=True)
def neighbourhood_star(field, x, y, val, radius):
    count = 0
    if field[x, y] == val:
        count -= 1

    for i in prange(x - radius, x + radius + 1):
        for j in prange(y - radius, y + radius + 1):
            if (abs(x - i) == abs(y - j)) or (x - i == 0) or (y - j == 0):
                if field[i, j] == val:
                    count += 1
    return count


neighborhood_funcs = {
    'M': neighborhood_mur,
    'N': neighbourhood_von_neumann,
    'NR': neighbourhood_von_neumann_external,
    'MR': neighborhood_mur_external,
    'D': neighborhood_diagonal,
    'L': neighborhood_lines,
    '2': neighbourhood_euclid,
    'C': neighbourhood_circle,
    'B': neighbourhood_chess,
    'Bi': neighbourhood_chess_inverse,
    '#': neighbourhood_lattice,
    '+': neighbourhood_plus,
    'X': neighbourhood_cross,
    '*': neighbourhood_star
}
