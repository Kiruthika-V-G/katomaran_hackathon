import pygame
import sys
import random

# Function to calculate the center point of the rectangular pillar
def calculate_center(vertices):
    x_coords = [v[0] for v in vertices]
    y_coords = [v[1] for v in vertices]
    center_x = sum(x_coords) / 4
    center_y = sum(y_coords) / 4
    return center_x, center_y

# Function to generate the navigation path avoiding the pillar
def navigate_to_center(robot_start, center, pillar_bounds):
    path = []
    x1, y1 = robot_start
    x2, y2 = center

    # Move along the x-axis
    if x1 != x2:
        path.append((x2, y1))
    
    # Move along the y-axis
    if y1 != y2:
        path.append((x2, y2))

    return path

# Function to check if a point is inside the rectangular pillar
def is_inside_pillar(x, y, pillar_bounds):
    x_min = min(p[0] for p in pillar_bounds)
    x_max = max(p[0] for p in pillar_bounds)
    y_min = min(p[1] for p in pillar_bounds)
    y_max = max(p[1] for p in pillar_bounds)
    return x_min <= x <= x_max and y_min <= y <= y_max

# Initialize the vertices of the rectangular pillar
vertices = [(200, 200), (200, 300), (400, 300), (400, 200)]

# Calculate the center point of the pillar
center = calculate_center(vertices)

# Randomly generate robot start position outside the pillar
width, height = 600, 400
while True:
    robot_start = (random.randint(0, width), random.randint(0, height))
    if not is_inside_pillar(robot_start[0], robot_start[1], vertices):
        break

# Generate the path to the center
path = navigate_to_center(robot_start, center, vertices)

# Initialize Pygame
pygame.init()

# Set up display
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Robot Navigation Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Draw the rectangular pillar
def draw_pillar(vertices):
    pygame.draw.polygon(window, BLUE, vertices, 0)

# Draw the robot
def draw_robot(position):
    pygame.draw.circle(window, RED, position, 5)

# Draw the path
def draw_path(path, progress):
    for i in range(progress):
        pygame.draw.line(window, GREEN, path[i], path[i + 1], 2)

# Simulation loop
running = True
robot_position = robot_start
path_index = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    window.fill(WHITE)
    
    draw_pillar(vertices)
    draw_robot(robot_position)
    if path_index > 0:
        draw_path([robot_start] + path, path_index)

    if path_index < len(path):
        target_position = path[path_index]
        if robot_position[0] != target_position[0]:
            robot_position = (robot_position[0] + 1 if robot_position[0] < target_position[0] else robot_position[0] - 1, robot_position[1])
        elif robot_position[1] != target_position[1]:
            robot_position = (robot_position[0], robot_position[1] + 1 if robot_position[1] < target_position[1] else robot_position[1] - 1)
        else:
            path_index += 1
    
    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()
sys.exit()
