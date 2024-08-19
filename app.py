import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 20
PLAYER_SIZE = 15
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'GRAY': (128, 128, 128)
}

# Difficulty settings
DIFFICULTIES = {
    'EASY': (4, 4),
    'MEDIUM': (6, 6),
    'HARD': (10, 10)
}

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self.generate()

    def generate(self):
        stack = []
        current = self.grid[0][0]
        current.visited = True

        while True:
            unvisited = self.get_unvisited_neighbors(current)
            if unvisited:
                next_cell = random.choice(unvisited)
                stack.append(current)
                self.remove_walls(current, next_cell)
                current = next_cell
                current.visited = True
            elif stack:
                current = stack.pop()
            else:
                break

    def get_unvisited_neighbors(self, cell):
        neighbors = []
        x, y = cell.x, cell.y

        if x > 0 and not self.grid[x-1][y].visited:
            neighbors.append(self.grid[x-1][y])
        if x < self.width - 1 and not self.grid[x+1][y].visited:
            neighbors.append(self.grid[x+1][y])
        if y > 0 and not self.grid[x][y-1].visited:
            neighbors.append(self.grid[x][y-1])
        if y < self.height - 1 and not self.grid[x][y+1].visited:
            neighbors.append(self.grid[x][y+1])

        return neighbors

    def remove_walls(self, current, next_cell):
        dx = current.x - next_cell.x
        dy = current.y - next_cell.y

        if dx == 1:
            current.walls['left'] = False
            next_cell.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next_cell.walls['left'] = False
        elif dy == 1:
            current.walls['top'] = False
            next_cell.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            next_cell.walls['top'] = False

class Game:
    def __init__(self):
        self.difficulty = 'EASY'
        self.maze = None
        self.player_pos = [0, 0]
        self.start_time = None
        self.moves = 0
        self.zoom_factor = 3
        self.restart()

    def restart(self):
    
        width, height = DIFFICULTIES[self.difficulty]
        self.maze = Maze(width, height)
        self.player_pos = [0, 0]
        self.start_time = time.time()
        self.moves = 0

    def move_player(self, dx, dy):
        x, y = self.player_pos
        new_x, new_y = x + dx, y + dy

        if 0 <= new_x < self.maze.width and 0 <= new_y < self.maze.height:
            current_cell = self.maze.grid[x][y]
            if dx == 1 and not current_cell.walls['right']:
                self.player_pos = [new_x, new_y]
                self.moves += 1
            elif dx == -1 and not current_cell.walls['left']:
                self.player_pos = [new_x, new_y]
                self.moves += 1
            elif dy == 1 and not current_cell.walls['bottom']:
                self.player_pos = [new_x, new_y]
                self.moves += 1
            elif dy == -1 and not current_cell.walls['top']:
                self.player_pos = [new_x, new_y]
                self.moves += 1

    def check_win(self):
        return self.player_pos == [self.maze.width - 1, self.maze.height - 1]

class MazeGame:
    def __init__(self):
        self.game = Game()
        self.main_screen = pygame.display.set_mode((900, 800))
        pygame.display.set_caption("Maze Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24) 
        
        # Ask for difficulty at startup
        difficulty = self.ask_difficulty()
        self.game.difficulty = difficulty
        self.game.restart()

    def show_full_map(self):
        full_map_surface = pygame.Surface((self.game.maze.width * CELL_SIZE, self.game.maze.height * CELL_SIZE))
        full_map_surface.fill(COLORS['WHITE'])
        self.draw_maze(full_map_surface)
        self.draw_player(full_map_surface)
        
        # Scale the surface to fit the screen if it's too large
        max_width = self.main_screen.get_width() - 20
        max_height = self.main_screen.get_height() - 20
        surface_width = min(full_map_surface.get_width(), max_width)
        surface_height = min(full_map_surface.get_height(), max_height)
        scaled_surface = pygame.transform.scale(full_map_surface, (surface_width, surface_height))
        
        # Center the map on the screen
        x = (self.main_screen.get_width() - surface_width) // 2
        y = (self.main_screen.get_height() - surface_height) // 2
        
        self.main_screen.blit(scaled_surface, (x, y))
        pygame.display.flip()
        
        # Wait for a click to close the full map
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    waiting = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def ask_difficulty(self):
        difficulties = ['EASY', 'MEDIUM', 'HARD']
        selected = 0
        
        while True:
            self.main_screen.fill(COLORS['WHITE'])
            text = self.font.render("Select Difficulty:", True, COLORS['BLACK'])
            self.main_screen.blit(text, (300, 200))
            
            for i, diff in enumerate(difficulties):
                color = COLORS['GREEN'] if i == selected else COLORS['GRAY']
                pygame.draw.rect(self.main_screen, color, (300 + i * 100, 250, 80, 40), 1)  # Thinner border
                text = self.font.render(diff, True, COLORS['BLACK'])
                self.main_screen.blit(text, (310 + i * 100, 260))
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selected = (selected - 1) % 3
                    elif event.key == pygame.K_RIGHT:
                        selected = (selected + 1) % 3
                    elif event.key == pygame.K_RETURN:
                        return difficulties[selected]
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def draw_maze(self, surface, zoom=False):
        cell_size = CELL_SIZE if not zoom else CELL_SIZE * self.game.zoom_factor
        for x in range(self.game.maze.width):
            for y in range(self.game.maze.height):
                cell = self.game.maze.grid[x][y]
                px, py = x * cell_size, y * cell_size

                if cell.walls['top']:
                    pygame.draw.line(surface, COLORS['BLACK'], (px, py), (px + cell_size, py))
                if cell.walls['right']:
                    pygame.draw.line(surface, COLORS['BLACK'], (px + cell_size, py), (px + cell_size, py + cell_size))
                if cell.walls['bottom']:
                    pygame.draw.line(surface, COLORS['BLACK'], (px, py + cell_size), (px + cell_size, py + cell_size))
                if cell.walls['left']:
                    pygame.draw.line(surface, COLORS['BLACK'], (px, py), (px, py + cell_size))

        # Draw start and end points
        pygame.draw.rect(surface, COLORS['GREEN'], (0, 0, cell_size, cell_size))
        pygame.draw.rect(surface, COLORS['RED'], ((self.game.maze.width - 1) * cell_size, (self.game.maze.height - 1) * cell_size, cell_size, cell_size))

    def draw_player(self, surface, zoom=False):
        cell_size = CELL_SIZE if not zoom else CELL_SIZE * self.game.zoom_factor
        player_size = PLAYER_SIZE if not zoom else PLAYER_SIZE * self.game.zoom_factor
        x, y = self.game.player_pos
        px = x * cell_size + (cell_size - player_size) // 2
        py = y * cell_size + (cell_size - player_size) // 2
        pygame.draw.rect(surface, COLORS['BLUE'], (px, py, player_size, player_size))

    def draw_ui(self):
        # Draw restart button
        pygame.draw.rect(self.main_screen, COLORS['GRAY'], (10, 10, 90, 30), 1)  # Thinner border
        text = self.font.render('Restart', True, COLORS['BLACK'])
        self.main_screen.blit(text, (15, 15))

        # Draw show map button
        pygame.draw.rect(self.main_screen, COLORS['GRAY'], (110, 10, 90, 30), 1)  # Thinner border
        text = self.font.render('Show Map', True, COLORS['BLACK'])
        self.main_screen.blit(text, (115, 15))

        # Draw timer and move counter
        elapsed_time = int(time.time() - self.game.start_time)
        timer_text = self.font.render(f'Time: {elapsed_time}s', True, COLORS['BLACK'])
        self.main_screen.blit(timer_text, (10, 50))

        moves_text = self.font.render(f'Moves: {self.game.moves}', True, COLORS['BLACK'])
        self.main_screen.blit(moves_text, (10, 80))

    def show_win_screen(self):
        self.main_screen.fill(COLORS['WHITE'])

        elapsed_time = int(time.time() - self.game.start_time)
        time_text = self.font.render(f'Time: {elapsed_time}s', True, COLORS['BLACK'])
        moves_text = self.font.render(f'Moves: {self.game.moves}', True, COLORS['BLACK'])
        win_text = self.font.render('You Won!', True, COLORS['GREEN'])
        restart_text = self.font.render('Press SPACE to restart', True, COLORS['BLUE'])

        self.main_screen.blit(time_text, (350, 200))
        self.main_screen.blit(moves_text, (350, 240))
        self.main_screen.blit(win_text, (350, 280))
        self.main_screen.blit(restart_text, (300, 320))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
                    # Instead of setting difficulty to None, simply call restart later
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        # After pressing SPACE, restart the game
        self.game.restart()

    def run(self):
        running = True
        game_won = False
        while running:
            if self.game.difficulty is None:  # If difficulty is not set, prompt for it
                difficulty = self.ask_difficulty()
                self.game.difficulty = difficulty
                self.game.restart()
                game_won = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and not game_won:
                    if event.key == pygame.K_LEFT:
                        self.game.move_player(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.game.move_player(1, 0)
                    elif event.key == pygame.K_UP:
                        self.game.move_player(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.game.move_player(0, 1)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 10 <= y <= 50:
                        if 10 <= x <= 100:
                            self.game.difficulty = None  # Reset difficulty to trigger selection
                        elif 110 <= x <= 230:
                            self.show_full_map()

            if not game_won:
                self.main_screen.fill(COLORS['WHITE'])

                # Draw zoomed maze
                zoom_size = 5 * CELL_SIZE * self.game.zoom_factor
                zoomed_maze_surface = pygame.Surface((zoom_size, zoom_size))
                zoomed_maze_surface.fill(COLORS['WHITE'])

                player_x, player_y = self.game.player_pos
                offset_x = max(0, min(player_x - 2, self.game.maze.width - 5))
                offset_y = max(0, min(player_y - 2, self.game.maze.height - 5))

                for x in range(5):
                    for y in range(5):
                        cell_x, cell_y = offset_x + x, offset_y + y
                        if 0 <= cell_x < self.game.maze.width and 0 <= cell_y < self.game.maze.height:
                            cell = self.game.maze.grid[cell_x][cell_y]
                            px, py = x * CELL_SIZE * self.game.zoom_factor, y * CELL_SIZE * self.game.zoom_factor
                            
                            # Draw exit cell in green
                            if cell_x == self.game.maze.width - 1 and cell_y == self.game.maze.height - 1:
                                pygame.draw.rect(zoomed_maze_surface, COLORS['GREEN'], 
                                                (px, py, CELL_SIZE * self.game.zoom_factor, CELL_SIZE * self.game.zoom_factor))
                            
                            if cell.walls['top']:
                                pygame.draw.line(zoomed_maze_surface, COLORS['BLACK'], (px, py), (px + CELL_SIZE * self.game.zoom_factor, py), 2)
                            if cell.walls['right']:
                                pygame.draw.line(zoomed_maze_surface, COLORS['BLACK'], (px + CELL_SIZE * self.game.zoom_factor, py), (px + CELL_SIZE * self.game.zoom_factor, py + CELL_SIZE * self.game.zoom_factor), 2)
                            if cell.walls['bottom']:
                                pygame.draw.line(zoomed_maze_surface, COLORS['BLACK'], (px, py + CELL_SIZE * self.game.zoom_factor), (px + CELL_SIZE * self.game.zoom_factor, py + CELL_SIZE * self.game.zoom_factor), 2)
                            if cell.walls['left']:
                                pygame.draw.line(zoomed_maze_surface, COLORS['BLACK'], (px, py), (px, py + CELL_SIZE * self.game.zoom_factor), 2)

                # Draw player on zoomed maze
                player_zoom_x = (player_x - offset_x) * CELL_SIZE * self.game.zoom_factor
                player_zoom_y = (player_y - offset_y) * CELL_SIZE * self.game.zoom_factor
                pygame.draw.rect(zoomed_maze_surface, COLORS['BLUE'], (player_zoom_x + CELL_SIZE * self.game.zoom_factor // 4, player_zoom_y + CELL_SIZE * self.game.zoom_factor // 4, CELL_SIZE * self.game.zoom_factor // 2, CELL_SIZE * self.game.zoom_factor // 2))

                self.main_screen.blit(zoomed_maze_surface, (10, 150))

                self.draw_ui()

                if self.game.check_win():
                    game_won = True

                pygame.display.flip()

            if game_won:
                self.show_win_screen()
                game_won = False

            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = MazeGame()
    game.run()