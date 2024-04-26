import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for i in range(height)]

        self.left_start = 10
        self.top_start = 10
        self.cell_size = 50

        self.game_on = False

    def set_view(self, left, top, cell_size):
        self.left_start = left
        self.top_start = top
        self.cell_size = cell_size

    def render(self, screen):
        screen.fill((0, 0, 0))
        colors = ['black', 'green']
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(colors[self.board[y][x]]),
                                 (self.cell_size * x + self.left_start, self.cell_size * y + self.top_start,
                                  self.cell_size, self.cell_size))

                pygame.draw.rect(screen, pygame.Color('white'),
                                 (self.cell_size * x + self.left_start, self.cell_size * y + self.top_start,
                                  self.cell_size, self.cell_size), width=1)
        clock.tick(fps)

    def on_click(self, cell):
        if not self.game_on:
            x, y = cell
            self.board[y][x] = (self.board[y][x] + 1) % 2

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left_start) // self.cell_size
        y = (mouse_pos[1] - self.top_start) // self.cell_size
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None
        return x, y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


class Life(Board):

    def check_lives_cells(self, y_n, x_n):
        cnt_life_cells = 0
        for y in range(y_n - 1, y_n + 2):
            for x in range(x_n - 1, x_n + 2):
                if y_n != y or x_n != x:
                    if y >= self.height:
                        y = 0
                    if x >= self.width:
                        x = 0
                    if self.board[y][x] == 1 or self.board[y][x] == 2:
                        cnt_life_cells += 1
        return cnt_life_cells

    def next_move(self):
        for y in range(self.height):
            for x in range(self.width):
                cnt_life_cells = self.check_lives_cells(y, x)
                if self.board[y][x] == 1:
                    if not (2 <= cnt_life_cells <= 3):
                        self.board[y][x] = 2  # клетка потом умрет
                else:
                    if cnt_life_cells == 3:
                        self.board[y][x] = 3  # клетка потом оживет
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 2:
                    self.board[y][x] = 0
                elif self.board[y][x] == 3:
                    self.board[y][x] = 1


life = Life(30, 30)
running = True
pygame.init()
pygame.display.set_caption('Игра "Жизнь"')
screen = pygame.display.set_mode((940, 940))
screen.fill((0, 0, 0))
life.set_view(17, 17, 30)
clock = pygame.time.Clock()
fps = 15
check_fps = fps  # фпс для расстановки клеток, чтобы не лагало
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            life.get_click(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            life.game_on = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            if fps < 120:
                fps += 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            if fps > 2:
                fps -= 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if life.game_on:
                life.game_on = False
                check_fps = fps
                fps = 30
            else:
                life.game_on = True
                fps = check_fps
    if life.game_on:
        life.next_move()
    life.render(screen)
    pygame.display.flip()