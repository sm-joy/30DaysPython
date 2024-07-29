from random import randint, choice
import pygame
from typing import Tuple, List

sand_colors = [
    (194, 178, 128),  # Light Sand
    (207, 192, 141),  # Pale Beige
    (220, 205, 155),  # Soft Desert Sand
    (235, 220, 180),  # Warm Beige
    (245, 230, 200)   # Light Tan
]


class Block:
    def __init__(self, row: int, col: int, size: int) -> None:
        self.rect: pygame.rect.Rect = pygame.rect.Rect(col * size, row * size, size, size)
        self.state: bool = False
        self.visited: bool = False
        self.settled: bool = False
        self.color: Tuple[int, int, int] = (-1, -1, -1)  # no color

    def render(self, surface: pygame.surface) -> None:
        if self.state:
            pygame.draw.rect(surface=surface,
                             color=self.color,
                             rect=self.rect)

    def make_sand(self):
        self.state = True
        self.color = choice(seq=sand_colors)

    def make_air(self):
        self.state: bool = False
        self.visited: bool = False
        self.settled: bool = False
        self.color: Tuple[int, int, int] = (-1, -1, -1) # no color

    @staticmethod
    def reset(cells: List[List['Block']]):
        for cell_row in cells:
            for cell in cell_row:
                cell.make_air()

    @staticmethod
    def move(cells: List[List['Block']], current_pos: Tuple[int, int], next_pos: Tuple[int, int]) -> None:
        current_cell = cells[current_pos[0]][current_pos[1]]
        next_cell = cells[next_pos[0]][next_pos[1]]
        current_cell.state = False  # current cells current position
        next_cell.state = True  # current cells next position
        next_cell.color = current_cell.color
        current_cell.color = (-1, -1, -1)
        cells[next_pos[0]][next_pos[1]].visited = True

    @staticmethod
    def update(cells: List[List['Block']], row: int, col: int, rows: int, cols: int) -> None:
        current_cell = cells[row][col]
        if current_cell.settled:
            return
        if current_cell.state and row == rows - 1:
            current_cell.settled = True
            return

        if current_cell.state:
            if current_cell.visited:
                current_cell.visited = False
            else:
                if not cells[row + 1][col].state:
                    Block.move(cells=cells,
                               current_pos=(row, col),
                               next_pos=(row + 1, col))
                elif cells[row + 1][col].state and not cells[row + 1][col].settled:
                    pass
                elif randint(a=1, b=2) == 1:
                    if col != cols - 1 and not cells[row + 1][col + 1].state:
                        Block.move(cells=cells,
                                   current_pos=(row, col),
                                   next_pos=(row + 1, col + 1))
                    elif col != 0 and not cells[row + 1][col - 1].state:
                        Block.move(cells=cells,
                                   current_pos=(row, col),
                                   next_pos=(row + 1, col - 1))
                    else:
                        current_cell.settled = True
                else:
                    if col != 0 and not cells[row + 1][col - 1].state:
                        Block.move(cells=cells,
                                   current_pos=(row, col),
                                   next_pos=(row + 1, col - 1))
                    elif col != cols - 1 and not cells[row + 1][col + 1].state:
                        Block.move(cells=cells,
                                   current_pos=(row, col),
                                   next_pos=(row + 1, col + 1))
                    else:
                        current_cell.settled = True


def pygame_run(window_size: Tuple[int, int]) -> Tuple[pygame.surface, pygame.time.Clock]:
    pygame.init()
    pygame.display.set_caption("Falling Sand")
    return (pygame.display.set_mode(window_size),
            pygame.time.Clock())


def main() -> int:
    width: int = 600
    height: int = 600
    block_size: int = 4
    rows: int = int(width / block_size)
    cols: int = int(height / block_size)
    fps: int = 80
    run: bool = True

    cells: List[List[Block]] = [[
        Block(row=row, col=col, size=block_size)
        for col in range(cols)]
        for row in range(rows)]

    window, clock = pygame_run(window_size=(width, height))

    while run:

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // block_size
                row = mouse_pos[1] // block_size
                if 0 <= row < rows and 0 <= col < cols:  # efficiently checking the pressed cell
                    cells[row][col].make_sand()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Block.reset(cells)

        # testing
        cells[0][60].make_sand()

        # Update
        for row in range(rows-1, -1, -1):  # in reverse order
            for col in range(cols-1, -1, -1):  # in reverse order
                cells[row][col].update(cells=cells, row=row, col=col, rows=rows, cols=cols)

        # Render
        window.fill((0, 200, 255))
        for cell_row in cells:
            for cell in cell_row:
                cell.render(surface=window)

        pygame.display.flip()
        clock.tick(fps)
        print(f"\rFPS: {clock.get_fps():.2f}", end="")

    pygame.quit()
    return 0


if __name__ == "__main__":
    main()
