from random import choice, randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс, от которого наследуются классы Apple и Snake.
    Содержит конструктор с общими атрибутами и метод заглушку,
    который переопределяется в дочерних классах.
    """

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Заглушка для переопределения в дочках"""
        pass


class Apple(GameObject):
    """Класс яблоко, содржащий в себе конструктор и два метода.
    Метод randomize_position случайным
    образом задаёт положение яблока на экране.
    Метод draw рисует яблоко на экране.
    """

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self) -> None:
        """С помощью randrange выбирает случайное
        число из диапазона 20-SCREEN_WIDTH с шагом 20,
        чтобы координаты змейки и яблока всегда могли совпасть.
        """
        self.position = (
            (randrange(20, SCREEN_WIDTH, 20)),
            (randrange(20, SCREEN_HEIGHT, 20)),
        )

    def draw(self) -> None:
        """Отрисовка яблока по заданным параметрам"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Объект класса Snake"""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления координат в зависимости от направления движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def sub_move(self, direct) -> None:
        """Метод sub_move уменьшает дублирование кода в методе move (DRY).
        Добавляет новую голову в направлении
        движения и удаляет хвост, реализуя перемещение.
        Если змейка сталкивается с собой - вызывает сброс (reset).
        """
        x_cord = self.positions[0][0] + direct[0] * GRID_SIZE
        y_cord = self.positions[0][1] + direct[1] * GRID_SIZE
        if x_cord >= SCREEN_WIDTH:
            x_cord = 20
        elif x_cord < 1:
            x_cord = SCREEN_WIDTH - 20
        if y_cord >= SCREEN_HEIGHT:
            y_cord = 20
        elif y_cord < 1:
            y_cord = SCREEN_HEIGHT - 20
        cords = (x_cord, y_cord)
        if self.length != 1 and cords in self.positions:
            self.reset()
        else:
            self.positions.insert(0, cords)
            self.last = self.positions[-1]
            del self.positions[-1]

    def move(self) -> None:
        """Метод move проверяет направление движения, в зависимости от этого,
        передаёт нужное направление в метод sub_move,
        в котором написана основная логика движения змейки.
        """
        self.update_direction()
        if self.direction == LEFT:
            self.sub_move(LEFT)

        elif self.direction == RIGHT:
            self.sub_move(RIGHT)

        elif self.direction == UP:
            self.sub_move(UP)

        elif self.direction == DOWN:
            self.sub_move(DOWN)

    # Метод draw класса Snake
    def draw(self) -> None:
        """Отрисовка змейки (Из прекода)"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple:
        """Метод get_head_position возвращает
        координаты головы змеи в виде кортежа.
        """
        return self.positions[0]

    def reset(self) -> None:
        """Метод reset возвращает змейку к начальному положению.
        В цикле закрашиваем тело змейки в цвет фона, После чего обнуляем массив
        координат змейки и задаём начальное значение.
        Рандомно выбираем направление движения
        """
        for i in range(len(self.positions)):
            self.last = self.positions[i]
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        self.last = None
        self.positions.clear()
        self.positions.append(self.position)
        self.direction = choice(DIRECTIONS)
        self.length = 1


def handle_keys(game_object) -> None:
    """Обработка нажатий пользователя (Из прекода)"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главный игровой цикл программы 'Змейка'.
    Инициализирует игру, создает объекты змейки

    и яблока, обрабатывает следующие события:
    - Управление змейкой с клавиатуры
    - Движение змейки
    - Отрисовка игровых объектов
    - Проверка столкновений
    - Обновление игрового поля

    Игра:
        - Змейка растет при поедании яблок
        - Игра продолжается бесконечно (без системы очков)
        - При столкновении с собой
        змейка сбрасывается (реализовано в классе Snake)
    """
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        snake.draw()
        apple.draw()
        if snake.get_head_position() == apple.position:
            snake.positions.append(apple.position)
            snake.length += 1
            apple.randomize_position()

        pygame.display.update()


if __name__ == '__main__':
    main()
