import pygame
import random

class Ghost:
    def __init__(self, maze, color):
        self.maze = maze
        self.color = color
        self.size = maze.tile_size
        self.speed = 1  # Whole number for easier grid alignment
        self.reset()

    def reset(self):
        self.grid_x, self.grid_y = self.maze.ghost_start_pos
        self.x, self.y = self.maze.grid_to_screen(self.grid_x, self.grid_y)
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

    def draw(self, screen, pac_boy_power_mode):
        color = self.color if not pac_boy_power_mode else (0, 0, 255)  # Blue when vulnerable
        
        # Draw ghost body
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size // 2)
        pygame.draw.rect(screen, color, (int(self.x - self.size // 2), int(self.y), self.size, self.size // 2))
        
        # Draw eyes
        eye_radius = self.size // 6
        left_eye = (int(self.x - self.size // 4), int(self.y - self.size // 4))
        right_eye = (int(self.x + self.size // 4), int(self.y - self.size // 4))
        
        pygame.draw.circle(screen, (255, 255, 255), left_eye, eye_radius)
        pygame.draw.circle(screen, (255, 255, 255), right_eye, eye_radius)
        
        pupil_radius = eye_radius // 2
        pygame.draw.circle(screen, (0, 0, 0), (left_eye[0] + self.direction[0] * pupil_radius, left_eye[1] + self.direction[1] * pupil_radius), pupil_radius)
        pygame.draw.circle(screen, (0, 0, 0), (right_eye[0] + self.direction[0] * pupil_radius, right_eye[1] + self.direction[1] * pupil_radius), pupil_radius)

    def is_center_of_tile(self):
        return (self.x - self.maze.offset_x) % self.maze.tile_size == self.maze.tile_size // 2 and \
               (self.y - self.maze.offset_y) % self.maze.tile_size == self.maze.tile_size // 2

    def move(self):
        if self.is_center_of_tile():
            self.choose_new_direction()
        
        next_x = self.x + self.direction[0] * self.speed
        next_y = self.y + self.direction[1] * self.speed

        if not self.maze.is_wall(next_x, next_y):
            self.x = next_x
            self.y = next_y
            self.grid_x = int((self.x - self.maze.offset_x) // self.maze.tile_size)
            self.grid_y = int((self.y - self.maze.offset_y) // self.maze.tile_size)

    def choose_new_direction(self):
        possible_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(possible_directions)

        for direction in possible_directions:
            next_x = self.x + direction[0] * self.maze.tile_size
            next_y = self.y + direction[1] * self.maze.tile_size
            if not self.maze.is_wall(next_x, next_y):
                self.direction = direction
                break