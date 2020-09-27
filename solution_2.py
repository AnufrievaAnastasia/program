import pygame
from random import random

SCREEN_SIZE = (1280, 720)

class Vector:
    def __init__(self, x, y=None):
        if y is None:
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y


    def __sub__(self, vec):
        return Vector(self.x - vec.x, self.y - vec.y)

    def __add__(self, vec):
        return Vector(self.x + vec.x, self.y + vec.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self * scalar

    def len(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


    def int_pair(self):
        return int(self.x), int(self.y)

class Line:
    def __init__(self, points=[], speeds=[]):
        self.points = points or []
        self.speeds = speeds or []

    def add(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)


    def set_points(self):
        for point_ in range(len(self.points)):
            self.points[point_] = self.points[point_] + self.speeds[point_]
            if self.points[point_][0] > SCREEN_SIZE[0] or self.points[point_][0] < 0:
                self.speeds[point_] = Vector(- self.speeds[point_][0], self.speeds[point_][1])
            if self.points[point_][1] > SCREEN_SIZE[1] or self.points[point_][1] < 0:
                self.speeds[point_] = Vector(self.speeds[point_][0], -self.speeds[point_][1])


    def draw_points(self, points, width=4, color=(255, 255, 255)):
        for point in points:
            pygame.draw.circle(gameDisplay, color, point.int_pair(), width)


class Joint(Line):
    def __init__(self, count):
        super().__init__()
        self.count = count


    def add(self, point, speed):
        super().add(point, speed)
        self.get_joint()

    def set_points(self):
        super().set_points()
        self.get_joint()


    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        alpha = 1 / self.count
        result = []
        for i in range(self.count):
            result.append(self.get_point(base_points, i * alpha))
        return result

    def get_joint(self):
        if len(self.points) < 3:
            return []
        result = []
        for i in range(-2, len(self.points) - 2):
            pnt = []
            pnt.append((self.points[i] + self.points[i + 1]) * 0.5)
            pnt.append(self.points[i + 1])
            pnt.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            result.extend(self.get_points(pnt))
        return result

    def draw_points(self, points, style="points", width=4, color=(255, 255, 255)):
        if style == "line":
            for point_number in range(-1, len(points) - 1):
                pygame.draw.line(gameDisplay, color, (int(points[point_number][0]), int(points[point_number][1])),
                             (int(points[point_number + 1][0]), int(points[point_number + 1][1])), width)

        elif style == "points":
            for point in points:
                pygame.draw.circle(gameDisplay, color,
                               (int(point[0]), int(point[1])), width)



def display_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("arial", 30)
    font2 = pygame.font.SysFont("serif", 30)
    data = []
    data.append(["F1", "Помощь"])
    data.append(["R", "Перезапуск"])
    data.append(["P", "Воспроизвести / Пауза"])
    data.append(["Num+", "Добавить точку"])
    data.append(["Num-", "Удалить точку"])
    data.append(["", ""])
    data.append([str(steps), "текущих точек"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    steps = 20
    working = True
    line = Line()
    joint = Joint(steps)
    show_help = False
    pause = False
    color_param = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    line.points = []
                    line.speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                line.points.append(Vector(event.pos[0], event.pos[1]))
                joint.speeds.append(Vector(random() * 2, random() * 2))

        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)
        line.draw_points(line.points)
        joint.draw_points(joint.get_joint(), "line", 4, color)
        if not pause:
            joint.set_points()
            line.set_points()
        if show_help:
            display_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)









