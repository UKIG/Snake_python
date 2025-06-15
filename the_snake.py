from random import choice, randrange
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

FLAG = False
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
# Цвет камня
ROCKET_COLOR = (0, 0, 255)
# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
Speed = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()

count_eaten_apples = 0


class GameObject:
    """Базовый класс для всех игровых объектов.

    Attributes:
        position (tuple): Текущая позиция объекта на экране (x, y).
        body_color (tuple): Цвет объекта в формате RGB.
    """

    def __init__(self) -> None:
        """Инициализирует игровой объект с позицией по центру экрана."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self, position: tuple) -> None:
        """Отрисовывает объект на указанной позиции.

        Args:
            position (tuple): Координаты (x, y) для отрисовки объекта.
        """
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, представляющий яблоко в игре.

    Attributes:
        body_color (tuple): Цвет яблока (красный).
    """

    def __init__(self) -> None:
        """Инициализирует яблоко со случайной позицией."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self) -> None:
        """Генерирует случайную позицию для яблока на игровом поле."""
        self.position = (
            randrange(GRID_SIZE, SCREEN_WIDTH, GRID_SIZE),
            randrange(GRID_SIZE, SCREEN_HEIGHT, GRID_SIZE),
        )


class Rock(GameObject):
    """Класс, представляющий препятствия (камни) в игре.

    Attributes:
        body_color (tuple): Цвет камня (синий).
        rocks (list): Список позиций всех камней на поле.
        last (tuple): Последняя позиция камня.
    """

    def __init__(self) -> None:
        """Инициализирует камень со случайной позицией."""
        super().__init__()
        self.body_color = ROCKET_COLOR
        self.rocks = list()
        self.last = None
        self.randomize_position()

    def spawn_rock(self) -> None:
        """Добавляет новый камень в список и отрисовывает его."""
        self.rocks.append(self.position)
        self.draw(self.position)

    def remove(self) -> None:
        """Удаляет все камни с игрового поля."""
        for rock in self.rocks:
            last_rect = pygame.Rect(rock, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def randomize_position(self) -> None:
        """Генерирует случайную позицию для камня на игровом поле."""
        self.position = (
            randrange(GRID_SIZE, SCREEN_WIDTH, GRID_SIZE),
            randrange(GRID_SIZE, SCREEN_HEIGHT, GRID_SIZE),
        )


class Snake(GameObject):
    """Класс, представляющий змейку в игре.

    Attributes:
        body_color (tuple): Цвет змейки (зеленый).
        length (int): Текущая длина змейки.
        positions (list): Список позиций всех сегментов змейки.
        direction (tuple): Текущее направление движения.
        next_direction (tuple): Следующее направление движения.
        last (tuple): Позиция последнего сегмента змейки.
    """

    def __init__(self) -> None:
        """Инициализирует змейку в центре экрана."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self) -> None:
        """Обновляет текущее направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_param(self, direct: tuple) -> tuple:
        """Вычисляет новые координаты на основе направления.

        Args:
            direct (tuple): Направление движения (x, y).

        Returns:
            tuple: Новые координаты головы змейки.
        """
        return (
            self.positions[0][0] + direct[0] * GRID_SIZE,
            self.positions[0][1] + direct[1] * GRID_SIZE,
        )

    def sub_move(self, direct: tuple, rock=None) -> None:
        """Обрабатывает движение змейки в указанном направлении.

        Args:
            direct (tuple): Направление движения.
            rock (Rock, optional): Объект камня для обработки столкновений.
        """
        x_cord, y_cord = self.get_param(direct)
        x_cord %= SCREEN_WIDTH
        y_cord %= SCREEN_HEIGHT
        cords = (x_cord, y_cord)
        if self.length != 1 and cords in self.positions:
            self.reset(rock)
        else:
            self.positions.insert(0, cords)
            self.last = self.positions[-1]
            del self.positions[-1]

    def move(self, rock=None) -> None:
        """Обновляет позицию змейки в зависимости от текущего направления.

        Args:
            rock (Rock, optional): Объект камня для обработки столкновений.
        """
        self.update_direction()
        if self.direction == LEFT:
            self.sub_move(LEFT, rock)
        elif self.direction == RIGHT:
            self.sub_move(RIGHT, rock)
        elif self.direction == UP:
            self.sub_move(UP, rock)
        elif self.direction == DOWN:
            self.sub_move(DOWN, rock)

    def draw_snake(self) -> None:
        """Отрисовывает змейку на игровом поле."""
        for position in self.positions[:-1]:
            self.draw(position)
        self.draw(self.get_head_position())
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple:
        """Возвращает позицию головы змейки.

        Returns:
            tuple: Координаты (x, y) головы змейки.
        """
        return self.positions[0]

    def reset(self, rock=None) -> None:
        """Сбрасывает змейку в начальное состояние.

        Args:
            rock (Rock, optional): Объект камня для очистки при сбросе.
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
        global count_eaten_apples
        count_eaten_apples = 0
        if rock:
            rock.remove()


def handle_keys(game_object) -> None:
    """Обрабатывает нажатия клавиш для управления змейкой.

    Args:
        game_object (Snake): Объект змейки, которым управляет игрок.
    """
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
            elif event.key == pygame.K_w:
                global Speed
                if Speed < 30:
                    Speed += 5
            elif event.key == pygame.K_s:
                if Speed > 5:
                    Speed -= 5


def rock_conflict(snake: Snake, rock: Rock) -> None:
    """Обрабатывает столкновение змейки с камнями.

    Args:
        snake (Snake): Объект змейки.
        rock (Rock): Объект камней.
    """
    if snake.get_head_position() in rock.rocks:
        rock.remove()
        rock.rocks.clear()
        snake.reset()


def chek_positions_between_rock_and_over(
    snake: Snake, apple: Apple, rock: Rock
) -> None:
    """Проверяет и корректирует позиции камня,
    чтобы он не появлялся на змейке или яблоке.

    Args:
        snake (Snake): Объект змейки.
        apple (Apple): Объект яблока.
        rock (Rock): Объект камней.
    """
    if rock.position in snake.positions or rock.position == apple.position:
        while rock.position in snake.positions or rock.position == apple.position:
            rock.randomize_position()


def eat_and_check_position_and_spawn_rock(
    snake: Snake, apple: Apple, rock: Rock
) -> None:
    """Обрабатывает поедание яблока и генерацию камней.

    Args:
        snake (Snake): Объект змейки.
        apple (Apple): Объект яблока.
        rock (Rock): Объект камней.
    """
    if snake.get_head_position() == apple.position:
        snake.positions.append(apple.position)
        snake.length += 1
        global count_eaten_apples
        count_eaten_apples += 1
        apple.randomize_position()
        if count_eaten_apples % 3 == 0:
            rock.randomize_position()
            chek_positions_between_rock_and_over(snake, apple, rock)
            rock.spawn_rock()
    if apple.position in snake.positions:
        while apple.position in snake.positions:
            apple.randomize_position()


def main() -> None:
    """Главная функция, запускающая и управляющая игровым циклом."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    rock = Rock()

    while True:
        clock.tick(Speed)
        handle_keys(snake)
        snake.move(rock)
        snake.draw_snake()
        apple.draw(apple.position)
        eat_and_check_position_and_spawn_rock(snake, apple, rock)
        rock_conflict(snake, rock)
        pygame.display.update()


if __name__ == "__main__":
    main()
