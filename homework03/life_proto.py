import copy

import pygame
import random

from pygame.locals import *
from typing import List, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        # Создание списка клеток
        self.grid = self.create_grid(True)

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid: Grid
        grid = []
        for y in range(0, self.cell_height):
            grid.append([])
            for x in range(0, self.cell_width):
                if randomize:
                    grid[y].append(random.randint(0, 1))
                else:
                    grid[y].append(0)

        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for y in range(0, self.cell_height):
            for x in range(0, self.cell_width):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color(
                            random.randint(150, 240),
                            random.randint(150, 240),
                            random.randint(150, 240),
                        ),
                        (
                            x * self.cell_size + 1,
                            y * self.cell_size + 1,
                            self.cell_size - 1,
                            self.cell_size - 1,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color(255, 255, 255),
                        (
                            x * self.cell_size + 1,
                            y * self.cell_size + 1,
                            self.cell_size - 1,
                            self.cell_size - 1,
                        ),
                    )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        high_border = max(0, cell[0] - 1)
        down_border = min(self.cell_height, cell[0] + 2)
        left_border = max(0, cell[1] - 1)
        right_border = min(self.cell_width, cell[1] + 2)
        for row in range(high_border, down_border):
            for col in range(left_border, right_border):
                if cell[0] != row or cell[1] != col:
                    neighbours.append(self.grid[row][col])

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = copy.deepcopy(self.grid)

        for y in range(0, self.cell_height):
            for x in range(0, self.cell_width):
                cell_sum = sum(self.get_neighbours((y, x)))
                if self.grid[y][x] == 1 and (cell_sum < 2 or cell_sum > 3):
                    new_grid[y][x] = 0
                    continue
                if self.grid[y][x] == 0 and cell_sum == 3:
                    new_grid[y][x] = 1
                    continue

        return new_grid


def main():
    game = GameOfLife(1000, 500, 25, 5)
    game.run()


if __name__ == "__main__":
    main()
