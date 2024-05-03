from random import randint

import pygame

# Grid size and screen size:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Default position:
DEFAULT_POSITION = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

# Movement directions:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Black color for the board background color:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Grid border color:
BORDER_COLOR = (93, 216, 228)

# Apple color:
APPLE_COLOR = (255, 0, 0)

# Snake color:
SNAKE_COLOR = (0, 255, 0)

# Snake speed:
SPEED = 20

# Game screen initialization:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Game screen title:
pygame.display.set_caption('Змейка')

# The clock object for controlling the game speed:
clock = pygame.time.Clock()


class GameObject:
    """
    This class is the base class for all game objects.
    """

    # Initialize the game object
    def __init__(self,
                 position=DEFAULT_POSITION,
                 body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    # Draw the game object (this method should be overridden in subclasses)
    def draw(self):
        pass


class Apple(GameObject):
    """
    This class represents an apple in the game.
    """

    # Initialize the apple object
    def __init__(self):
        position = self.randomize_position()
        super().__init__(position, body_color=APPLE_COLOR)

    # Draw the apple
    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Randomize the apple position
    def randomize_position(self):
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


class Snake(GameObject):
    """
    This class represents a snake in the game.
    """

    # Initialize the snake object
    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    # Draw the snake
    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Draw snake head
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Erase last segment of snake
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    # Move the snake
    def move(self):
        head_x, head_y = self.get_head_position()
        new_position = (head_x + self.direction[0] * GRID_SIZE,
                        head_y + self.direction[1] * GRID_SIZE)
        self.positions = [new_position] + self.positions[:-1]

    # Check if the snake has eaten the apple
    def reset(self):
        self.positions = DEFAULT_POSITION
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    # Get the position of the snake's head
    def get_head_position(self):
        return self.positions[0]

    # Update the direction of the snake
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


# Handle the user's actions
def handle_keys(game_object):
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
    # PyGame initialization:
    pygame.init()
    # Create an apple and a snake object:
    apple = Apple()
    snake = Snake()
    ...

    # while True:
    #     clock.tick(SPEED)

    # Тут опишите основную логику игры.
    # ...


if __name__ == '__main__':
    main()
