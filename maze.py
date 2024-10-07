import pygame

class Maze:
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.layout = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W............WW............W",
            "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
            "WoWWWW.WWWWW.WW.WWWWW.WWWWoW",
            "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
            "W..........................W",
            "W.WWWW.WW.WWWWWWWW.WW.WWWW.W",
            "W.WWWW.WW.WWWWWWWW.WW.WWWW.W",
            "W......WW....WW....WW......W",
            "WWWWWW.WWWWW WW WWWWW.WWWWWW",
            "WWWWWW.WWWWW WW WWWWW.WWWWWW",
            "WWWWWW.WW          WW.WWWWWW",
            "WWWWWW.WW WWWWWWWW WW.WWWWWW",
            "WWWWWW.WW W      W WW.WWWWWW",
            "      .   W      W   .      ",
            "WWWWWW.WW W      W WW.WWWWWW",
            "WWWWWW.WW WWWWWWWW WW.WWWWWW",
            "WWWWWW.WW          WW.WWWWWW",
            "WWWWWW.WW WWWWWWWW WW.WWWWWW",
            "WWWWWW.WW WWWWWWWW WW.WWWWWW",
            "W............WW............W",
            "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
            "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
            "Wo..WW................WW..oW",
            "WWW.WW.WW.WWWWWWWW.WW.WW.WWW",
            "WWW.WW.WW.WWWWWWWW.WW.WW.WWW",
            "W......WW....WW....WW......W",
            "W.WWWWWWWWWW.WW.WWWWWWWWWW.W",
            "W.WWWWWWWWWW.WW.WWWWWWWWWW.W",
            "W..........................W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]
        self.dots = set()
        self.power_dots = set()
        self.start_pos = None
        self.ghost_start_pos = None
        self.offset_x = (width - len(self.layout[0]) * tile_size) // 2
        self.offset_y = (height - len(self.layout) * tile_size) // 2
        self.initialize_maze()

    def initialize_maze(self):
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                if cell == '.':
                    self.dots.add((x, y))
                elif cell == 'o':
                    self.power_dots.add((x, y))

        # Set start positions
        self.start_pos = (1, 23)  # Pac-Boy start position
        self.ghost_start_pos = (14, 11)  # Ghost start position

    def draw(self, screen):
        for y, row in enumerate(self.layout):
            for x, cell in enumerate(row):
                screen_x = x * self.tile_size + self.offset_x
                screen_y = y * self.tile_size + self.offset_y
                if cell == 'W':
                    pygame.draw.rect(screen, (0, 0, 255),
                                     (screen_x, screen_y, self.tile_size, self.tile_size))
                elif (x, y) in self.dots:
                    pygame.draw.circle(screen, (255, 255, 255),
                                       (screen_x + self.tile_size // 2, screen_y + self.tile_size // 2), 2)
                elif (x, y) in self.power_dots:
                    pygame.draw.circle(screen, (255, 255, 255),
                                       (screen_x + self.tile_size // 2, screen_y + self.tile_size // 2), 6)

    def is_wall(self, x, y):
        grid_x = int((x - self.offset_x) // self.tile_size)
        grid_y = int((y - self.offset_y) // self.tile_size)
        if 0 <= grid_y < len(self.layout) and 0 <= grid_x < len(self.layout[0]):
            return self.layout[grid_y][grid_x] == 'W'
        return True

    def eat_dot(self, x, y):
        grid_x = int((x - self.offset_x) // self.tile_size)
        grid_y = int((y - self.offset_y) // self.tile_size)
        pos = (grid_x, grid_y)
        if pos in self.dots:
            self.dots.remove(pos)
            return 1
        if pos in self.power_dots:
            self.power_dots.remove(pos)
            return 2
        return 0

    def all_dots_eaten(self):
        return len(self.dots) == 0 and len(self.power_dots) == 0

    def reset_dots(self):
        self.dots = set()
        self.power_dots = set()
        self.initialize_maze()

    def grid_to_screen(self, grid_x, grid_y):
        return (grid_x * self.tile_size + self.offset_x + self.tile_size // 2,
                grid_y * self.tile_size + self.offset_y + self.tile_size // 2)