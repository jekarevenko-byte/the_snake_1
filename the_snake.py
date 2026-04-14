from random import randint

import pygame as pg  # type: ignore

# --- Константы ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTER_POSITION = ((GRID_WIDTH // 2) * GRID_SIZE,
                   (GRID_HEIGHT // 2) * GRID_SIZE)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

INITIAL_DIRECTION = RIGHT
INITIAL_LENGTH = 1
INITIAL_SPEED = 8

BOARD_BACKGROUND_COLOR = (55, 75, 95)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (65, 155, 85)

# --- Инициализация Pygame ---
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Snake Game')
clock = pg.time.Clock()


# --- Базовый класс ---
class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self, body_color=SNAKE_COLOR, border_color=BORDER_COLOR):
        """Инициализация объекта: цвет тела и границы."""
        self.position = CENTER_POSITION
        self.body_color = body_color
        self.border_color = border_color

    def draw_cell(self, position):
        """Отрисовка одной клетки с границей на экране."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)

    def draw(self):
        """Отрисовка объекта на экране."""
        self.draw_cell(self.position)


# --- Яблоко ---
class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, body_color=APPLE_COLOR, border_color=BORDER_COLOR,
                 occupied_positions=(CENTER_POSITION,)):
        """Инициализация яблока."""
        super().__init__(body_color, border_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Генерация случайной позиции яблока, не занятой змейкой."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовка яблока на экране."""
        self.draw_cell(self.position)


# --- Змейка ---
class Snake(GameObject):
    """Класс змейки."""

    def __init__(self, body_color=SNAKE_COLOR, border_color=BORDER_COLOR):
        """Инициализация змейки: начальная позиция, направление и длина."""
        super().__init__(body_color, border_color)
        self.positions = [self.position]
        self.direction = INITIAL_DIRECTION
        self.next_direction = None
        self.length = INITIAL_LENGTH

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения после нажатия клавиши."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Двигает змейку по экрану с wrap-around (тороидальная геометрия)."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змейку в начальное положение и длину."""
        self.positions = [self.position]
        self.direction = INITIAL_DIRECTION
        self.next_direction = None
        self.length = INITIAL_LENGTH

    def draw(self):
        """Отрисовывает все сегменты змейки на экране."""
        for pos in self.positions:
            self.draw_cell(pos)


# --- Обработка клавиш ---
def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


# --- Главная функция ---
def main():
    """Главная функция игры: игровой цикл."""
    snake = Snake()
    apple = Apple()
    score = 0
    speed = INITIAL_SPEED

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        head_pos = snake.get_head_position()

        # Столкновение с собой
        if head_pos in snake.positions[1:]:
            snake.reset()
            score = 0
            speed = INITIAL_SPEED
            apple.randomize_position(snake.positions)

        # Съедено яблоко
        elif head_pos == apple.position:
            snake.length += 1
            score += 1
            apple.randomize_position(snake.positions)
            if score % 5 == 0:
                speed += 1

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()
        clock.tick(speed)


if __name__ == '__main__':
    main()
