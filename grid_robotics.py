import pygame
import random
import sys
from queue import PriorityQueue


WIDTH, HEIGHT = 600, 600
ROWS, COLS = 10, 10
OBSTACLES = 30
CELL_SIZE = WIDTH // COLS
DELAY = 50  


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Pathfinding Simulation")

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * CELL_SIZE
        self.y = col * CELL_SIZE
        self.color = WHITE
        self.neighbors = []
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(win, BLACK, (self.x, self.y, CELL_SIZE, CELL_SIZE), 1)
    
    def add_neighbors(self, grid):
        if not self.neighbors:  
            if self.row < ROWS - 1 and grid[self.row + 1][self.col].color != BLACK:  # Down
                self.neighbors.append(grid[self.row + 1][self.col])
            if self.row > 0 and grid[self.row - 1][self.col].color != BLACK:  # Up
                self.neighbors.append(grid[self.row - 1][self.col])
            if self.col < COLS - 1 and grid[self.row][self.col + 1].color != BLACK:  # Right
                self.neighbors.append(grid[self.row][self.col + 1])
            if self.col > 0 and grid[self.row][self.col - 1].color != BLACK:  # Left
                self.neighbors.append(grid[self.row][self.col - 1])

def heuristic(cell1, cell2):
    x1, y1 = cell1.row, cell1.col
    x2, y2 = cell2.row, cell2.col
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw, start, end):
    path = []
    while current in came_from:
        current = came_from[current]
        current.color = YELLOW
        path.append((current.row, current.col))
        draw()
        pygame.time.delay(DELAY)
    print("Start Coordinate:", (start.row, start.col))
    print("End Coordinate:", (end.row, end.col))
    return path

# A* Algorithm
def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue() #store nodes to be evaluated
    open_set.put((0, count, start))
    came_from = {} #track path where each node came from
    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0
    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = heuristic(start, end)
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path = reconstruct_path(came_from, end, draw, start, end)
            end.color = BLUE
            start.color = RED
            print("Shortest Path:", path)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, end)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.color = YELLOW
        
        draw()
        pygame.time.delay(DELAY)

    return False


def create_grid():
    grid = [[Cell(i, j) for j in range(COLS)] for i in range(ROWS)]
    return grid


def draw_grid(win, grid):
    win.fill(WHITE)  
    for row in grid:
        for cell in row:
            cell.draw(win)
    pygame.display.update()


def generate_obstacles(grid):
    obstacles = 0
    while obstacles < OBSTACLES:
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        if grid[row][col].color == WHITE:
            grid[row][col].color = BLACK
            obstacles += 1


def get_clicked_pos(pos):
    x, y = pos
    row = x // CELL_SIZE
    col = y // CELL_SIZE
    return row, col

def main():
    grid = create_grid()
    generate_obstacles(grid)

    start = None
    end = None

    run = True
    while run:
        draw_grid(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]:  # Left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                cell = grid[row][col]
                if not start and cell.color == WHITE:
                    start = cell
                    start.color = RED
                elif not end and cell.color == WHITE and cell != start:
                    end = cell
                    end.color = BLUE

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for cell in row:
                            cell.add_neighbors(grid)
                    if not a_star(lambda: draw_grid(win, grid), grid, start, end):
                        print("No path found!")
                    else:
                        print("path found!")
                
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()