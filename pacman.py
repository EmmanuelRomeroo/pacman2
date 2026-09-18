"""Pacman con fantasmas que buscan el camino más corto."""

from collections import deque
from random import choice
from turtle import *

from freegames import floor, vector


state = {'score': 0}

path = Turtle(visible=False)
writer = Turtle(visible=False)

aim = vector(5, 0)
pacman = vector(-40, -80)

ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

# 0 = pared, 1 = camino con comida, 2 = camino sin comida.
# 0 = pared, 1 = camino con comida, 2 = camino sin comida.
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]


def square(x, y):
    """Dibuja una casilla del camino."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """Convierte una posición en un índice del tablero."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    return int(x + y * 20)


def valid(point):
    """Comprueba que el personaje cabe en el camino."""
    if not (-200 <= point.x <= 180 and -200 <= point.y <= 180):
        return False

    if tiles[offset(point)] == 0:
        return False

    if tiles[offset(point + 19)] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Dibuja el laberinto y la comida."""
    bgcolor('black')
    path.color('blue')

    for index, tile in enumerate(tiles):
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')


def chase(point, course):
    """Busca con BFS el camino más corto hacia Pacman."""
    start = offset(point)
    target = offset(pacman)

    # Guarda la casilla y el primer paso para llegar a ella.
    pending = deque([(start, None)])
    visited = {start}

    directions = [
        (0, 1, vector(5, 0)),
        (0, -1, vector(-5, 0)),
        (-1, 0, vector(0, 5)),
        (1, 0, vector(0, -5)),
    ]

    while pending:
        current, first_step = pending.popleft()

        if current == target:
            if first_step is not None:
                return first_step
            break

        row, col = divmod(current, 20)

        for dr, dc, direction in directions:
            next_row = row + dr
            next_col = col + dc

            if not (0 <= next_row < 20 and 0 <= next_col < 20):
                continue

            neighbor = next_row * 20 + next_col

            if tiles[neighbor] == 0 or neighbor in visited:
                continue

            visited.add(neighbor)

            step = direction if first_step is None else first_step
            pending.append((neighbor, step))

    # Si no hay ruta o comparte casilla con Pacman, sigue avanzando.
    if valid(point + course):
        return course.copy()

    options = [
        direction
        for _, _, direction in directions
        if valid(point + direction)
    ]

    return choice(options) if options else vector(0, 0)


def move():
    """Mueve a Pacman y a los fantasmas."""
    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1

        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    writer.clear()
    writer.write(state['score'])

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for point, course in ghosts:
        # Decide la ruta cuando está alineado con una casilla.
        if point.x % 20 == 0 and point.y % 20 == 0:
            plan = chase(point, course)
            course.x = plan.x
            course.y = plan.y

        if valid(point + course):
            point.move(course)

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            print('¡Fin del juego! Puntuación:', state['score'])
            return

    ontimer(move, 100)


def change(x, y):
    """Cambia la dirección de Pacman si el movimiento es válido."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


setup(420, 420, 370, 0)
hideturtle()
tracer(False)

writer.up()
writer.goto(160, 160)
writer.color('white')

listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')

world()
move()
done()