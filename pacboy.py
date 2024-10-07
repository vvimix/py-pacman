import pygame
import math

class PacBoy:
    def __init__(self, maze):
        self.maze = maze
        self.grid_x, self.grid_y = maze.start_pos
        self.x, self.y = maze.grid_to_screen(self.grid_x, self.grid_y)
        self.size = maze.tile_size
        self.speed = 2  # Increased speed for smoother movement
        self.direction = (1, 0)
        self.next_direction = None
        self.score = 0
        self.mouth_angle = 0
        self.mouth_speed = 0.2
        self.power_mode = False
        self.power_timer = 0
        self.mouth_open_angle = 45  # Maximum mouth opening angle

    def draw(self, screen):
        color = (255, 255, 0) if not self.power_mode else (255, 0, 0)
        
        # Calculate mouth opening
        mouth_opening = abs(math.sin(self.mouth_angle)) * self.mouth_open_angle
        
        # Calculate the angle based on the direction
        angle = math.atan2(-self.direction[1], self.direction[0])
        
        # Draw Pac-Boy body
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size // 2)

        # Draw mouth
        start_angle = angle + math.radians(mouth_opening / 2)
        end_angle = angle - math.radians(mouth_opening / 2)
        
        mouth_points = [
            (self.x, self.y),
            (self.x + math.cos(start_angle) * self.size // 2, self.y - math.sin(start_angle) * self.size // 2),
            (self.x + math.cos(end_angle) * self.size // 2, self.y - math.sin(end_angle) * self.size // 2)
        ]
        pygame.draw.polygon(screen, (0, 0, 0), mouth_points)

        self.mouth_angle += self.mouth_speed

    def is_center_of_tile(self):
        return (abs(self.x - self.maze.offset_x - self.grid_x * self.maze.tile_size - self.maze.tile_size // 2) < self.speed and
                abs(self.y - self.maze.offset_y - self.grid_y * self.maze.tile_size - self.maze.tile_size // 2) < self.speed)

    def can_change_direction(self, new_direction):
        new_grid_x = self.grid_x + new_direction[0]
        new_grid_y = self.grid_y + new_direction[1]
        return not self.maze.is_wall(self.maze.grid_to_screen(new_grid_x, new_grid_y)[0],
                                     self.maze.grid_to_screen(new_grid_x, new_grid_y)[1])

    def move(self):
        if self.is_center_of_tile():
            self.x = self.maze.offset_x + self.grid_x * self.maze.tile_size + self.maze.tile_size // 2
            self.y = self.maze.offset_y + self.grid_y * self.maze.tile_size + self.maze.tile_size // 2
            
            if self.next_direction and self.can_change_direction(self.next_direction):
                self.direction = self.next_direction
                self.next_direction = None
            elif not self.can_change_direction(self.direction):
                return  # Stop if we can't move in the current direction

        next_x = self.x + self.direction[0] * self.speed
        next_y = self.y + self.direction[1] * self.speed

        next_grid_x = int((next_x - self.maze.offset_x) // self.maze.tile_size)
        next_grid_y = int((next_y - self.maze.offset_y) // self.maze.tile_size)

        if not self.maze.is_wall(next_x, next_y):
            self.x = next_x
            self.y = next_y
            self.grid_x = next_grid_x
            self.grid_y = next_grid_y

        if self.power_mode:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_mode = False

    def change_direction(self, key):
        if key == pygame.K_UP:
            self.next_direction = (0, -1)
        elif key == pygame.K_DOWN:
            self.next_direction = (0, 1)
        elif key == pygame.K_LEFT:
            self.next_direction = (-1, 0)
        elif key == pygame.K_RIGHT:
            self.next_direction = (1, 0)

    def eat_dot(self):
        dot_type = self.maze.eat_dot(self.x, self.y)
        if dot_type == 1:
            self.score += 10
        elif dot_type == 2:
            self.score += 50
            self.power_mode = True
            self.power_timer = 300  # 10 seconds at 30 FPS

    def check_ghost_collision(self, ghosts):
        for ghost in ghosts:
            if (abs(self.grid_x - ghost.grid_x) < 1 and
                abs(self.grid_y - ghost.grid_y) < 1):
                if self.power_mode:
                    ghost.reset()
                    self.score += 200
                else:
                    return True
        return False