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
#Цвет камня
ROCKET_COLOR = (0, 0, 255)
# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
Speed = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

count_eaten_apples = 0

class GameObject:
    """Родительский класс, от которого наследуются классы Apple и Snake.
    Содержит конструктор с общими атрибутами и метод заглушку,
    который переопределяется в дочерних классах.
    """

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

        # вынес метод draw в родительский класс, чтобы избежать повторения кода

    def draw(self, position: tuple) -> None:
        """Метод draw отрисовывает объект по переданным координатам"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс яблоко, содержит в себе конструктор и два метода.
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
            # заменил числа на константы
            (randrange(GRID_SIZE, SCREEN_WIDTH, GRID_SIZE)),
            (randrange(GRID_SIZE, SCREEN_HEIGHT, GRID_SIZE)),
        )

class Rock(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.body_color = ROCKET_COLOR
        self.rocks = list()
        self.last = None
        self.randomize_position()

    def spawn_rock(self) -> None:

        self.rocks.append(self.position)
        self.draw(self.position)

    def remove(self):
        for rock in self.rocks:
            last_rect = pygame.Rect(rock, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def randomize_position(self) -> None:
        """С помощью randrange выбирает случайное
        число из диапазона 20-SCREEN_WIDTH с шагом 20,
        чтобы координаты змейки и яблока всегда могли совпасть.
        """
        self.position = (
            # заменил числа на константы
            (randrange(GRID_SIZE, SCREEN_WIDTH, GRID_SIZE)),
            (randrange(GRID_SIZE, SCREEN_HEIGHT, GRID_SIZE)),
        )


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

    def get_param(self, direct):
        """Метод для упаковки параметров"""
        return (
            self.positions[0][0] + direct[0] * GRID_SIZE,
            self.positions[0][1] + direct[1] * GRID_SIZE,
        )

    def sub_move(self, direct, rock = None) -> None:
        """Метод sub_move уменьшает дублирование кода в методе move (DRY).
        Добавляет новую голову в направлении
        движения и удаляет хвост, реализуя перемещение.
        Если змейка сталкивается с собой - вызывает сброс (reset).
        """
        # Сделал распаковку значений.
        x_cord, y_cord = self.get_param(direct)
        # Убрал условный оператор, выполнив расчёт через %.
        x_cord %= SCREEN_WIDTH
        y_cord %= SCREEN_HEIGHT
        cords = (x_cord, y_cord)
        if self.length != 1 and cords in self.positions:
            self.reset(rock)
        else:
            self.positions.insert(0, cords)
            self.last = self.positions[-1]
            del self.positions[-1]

    def move(self, rock = None) -> None:
        """Метод move проверяет направление движения, в зависимости от этого,
        передаёт нужное направление в метод sub_move,
        в котором написана основная логика движения змейки.
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

    # Метод draw класса Snake
    def draw_snake(self) -> None:
        """Отрисовка змейки (Из прекода)"""
        for position in self.positions[:-1]:
            self.draw(position)

        # Отрисовка головы змейки
        self.draw(self.get_head_position())
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple:
        """Метод get_head_position возвращает
        координаты головы змеи в виде кортежа.
        """
        return self.positions[0]

    def reset(self, rock = None) -> None:
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
        global count_eaten_apples
        count_eaten_apples = 0
        if rock:
            rock.remove()
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
            elif event.key == pygame.K_w:
                global Speed
                if Speed < 30:
                    Speed += 5
            elif event.key == pygame.K_s:
                if Speed > 5:
                    Speed -= 5




def rock_conflict(snake, rock) -> None:
    if snake.get_head_position() in rock.rocks:
        rock.remove()
        rock.rocks.clear()
        snake.reset()
def chek_positions_between_rock_and_over(snake, apple, rock) -> None:
    if rock.position in snake.positions or rock.position in apple.position:
        while rock.position in snake.positions or rock.position in apple.position:
            rock.randomize_position()

def eat_and_check_position_and_spawn_rock(snake, apple, rock):
    """Проверяет и обрабатывает столкновение змейки с яблоком,
     а также генерирует камни на игровом поле.

    Если координаты головы змейки совпадают с положением яблока:
    1. Увеличивает змейку
    2. Генерирует новое положение яблока
    3. Генерирует 1 камень

    Убеждается, что новое яблоко не появляется внутри тела змейки.
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


if __name__ == '__main__':
    main()
