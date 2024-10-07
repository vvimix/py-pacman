import pygame
import sys
from pacboy import PacBoy
from ghost import Ghost
from maze import Maze

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 672
SCREEN_HEIGHT = 744
TILE_SIZE = 24
FONT_SIZE = 24
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac Boy")

# Create font
font = pygame.font.Font(None, FONT_SIZE)

# Create game objects
maze = Maze(SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)
pac_boy = PacBoy(maze)
ghosts = [
    Ghost(maze, (255, 0, 0)),
    Ghost(maze, (255, 192, 203)),
    Ghost(maze, (0, 255, 255)),
    Ghost(maze, (255, 165, 0))
]

clock = pygame.time.Clock()

def reset_game():
    global pac_boy, ghosts
    pac_boy = PacBoy(maze)
    for ghost in ghosts:
        ghost.reset()
    maze.reset_dots()

def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                pac_boy.change_direction(event.key)

        # Update game objects
        pac_boy.move()
        pac_boy.eat_dot()
        for ghost in ghosts:
            ghost.move()

        # Check collisions
        if pac_boy.check_ghost_collision(ghosts):
            reset_game()

        if maze.all_dots_eaten():
            reset_game()

        # Draw everything
        screen.fill(BLACK)
        maze.draw(screen)
        pac_boy.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen, pac_boy.power_mode)

        # Draw score and Pac-Boy location
        score_text = font.render(f"Score: {pac_boy.score}", True, WHITE)
        location_text = font.render(f"Loc: ({pac_boy.grid_x}, {pac_boy.grid_y})", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))
        screen.blit(location_text, (SCREEN_WIDTH - location_text.get_width() - 10, 40))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    game_loop()