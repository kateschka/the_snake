from random import randint, choice

import pygame

# Grid size and screen size.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Default position.
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Movement directions.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Black color for the board background color.
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Grid border color.
BORDER_COLOR = (93, 216, 228)

# Apple color.
APPLE_COLOR = (255, 0, 0)

# Snake color.
SNAKE_COLOR = (0, 255, 0)

# Snake speed.
SPEED = 10

# Game screen initialization.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Game screen title.
pygame.display.set_caption(
    'Змейка. Счет: 0. Нажмите Esc для выхода.')

# The clock object for controlling the game speed.
clock = pygame.time.Clock()


class GameObject:
    """This class is the base class for all game objects."""

    # Initialize the game object.
    def __init__(
            self,
            position: tuple[int, int] = SCREEN_CENTER,
            body_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self, position: tuple[int, int]) -> None:
        """Method for drawing the game object."""
        rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """This class represents an apple in the game."""

    # Initialize the apple object.
    def __init__(self) -> None:
        self.randomize_position()
        super().__init__(self.position, body_color=APPLE_COLOR)

    def draw(self) -> None:
        """Method for drawing the apple."""
        super().draw(self.position)

    def randomize_position(self) -> None:
        """Method for randomizing the position of the apple."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )


class Snake(GameObject):
    """This class represents a snake in the game."""

    # Initialize the snake object.
    def __init__(self) -> None:
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def draw(self) -> None:
        """Method for drawing the snake."""
        for position in self.positions:
            super().draw(position)

    def move(self) -> None:
        """Method for moving the snake."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_position = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_position)

        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop()

    def reset(self) -> None:
        """Method for resetting the snake."""
        self.positions = [SCREEN_CENTER]
        # Initially snake moves to the right.
        if '__name__' == '__init__':
            self.direction = RIGHT
        else:
            self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None
        self.length = 1

    def get_head_position(self) -> tuple[int, int]:
        """Method for getting the head position of the snake."""
        return self.positions[0]

    def update_direction(self) -> None:
        """Method for updating the direction of the snake."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object: GameObject) -> None:
    """Method for handling the keys."""
    for event in pygame.event.get():
        if (event.type == pygame.QUIT
            or (event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE)):
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
    """The main function of the game."""
    # PyGame initialization.
    pygame.init()

    # Create an apple and a snake object.
    apple = Apple()
    snake = Snake()

    # Fill the screen with the board background color.
    screen.fill(BOARD_BACKGROUND_COLOR)

    # Score counter
    score = 0

    # The main game loop.
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Check if the snake has collided with itself.
        if snake.get_head_position() in snake.positions[2:]:
            clock.tick(2)
            snake.reset()
            apple.randomize_position()
            score = 0

        # If the snake has eaten the apple.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            score += 1
            while apple.position in snake.positions:
                apple.randomize_position()

        # Draw the game objects.
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.set_caption(
            f'Змейка. Счет: {score}. Нажмите Esc для выхода.'
        )

        # Update the display.
        pygame.display.update()


if __name__ == '__main__':
    main()
