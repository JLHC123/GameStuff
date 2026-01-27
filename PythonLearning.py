import random
import pygame

CELL_SIZE = 20

COLORS = {
    1: (0, 0, 0), # Wall - Black
    0: (255, 255, 255), # Path - White
    2: (0, 255, 0), # Start - Green
    3: (255, 0, 0), # End - Red
}

def startAndEndPoints(n):
    # select random starting point from the outer walls
    edges = ["top", "bottom", "left", "right"]
    starting_edge = random.choice(edges)
    if starting_edge == "top":
        starting_x = random.randint(1, n - 2)
        starting_y = 0
    elif starting_edge == "bottom": 
        starting_x = random.randint(1, n - 2)
        starting_y = n - 1
    elif starting_edge == "left": 
        starting_x = 0
        starting_y = random.randint(1, n - 2)
    elif starting_edge == "right": 
        starting_x = n - 1
        starting_y = random.randint(1, n - 2)
    
    # remove the starting edge from the list
    edges.remove(starting_edge)
    
    # select random ending point from the remaining outer walls
    ending_edge = random.choice(edges)
    if ending_edge == "top":
        ending_x = random.randint(1, n - 2)
        ending_y = 0
    elif ending_edge == "bottom": 
        ending_x = random.randint(1, n - 2)
        ending_y = n - 1
    elif ending_edge == "left": 
        ending_x = 0
        ending_y = random.randint(1, n - 2)
    elif ending_edge == "right": 
        ending_x = n - 1
        ending_y = random.randint(1, n - 2)
        
    # return starting and ending points
    return starting_x, starting_y, ending_x, ending_y

def moveAwayFromEdge(x, y, n):
    # move the point away from the edge
    if x == 0:
        x += 1
    elif x == n - 1:
        x -= 1
    elif y == 0:
        y += 1
    elif y == n - 1:
        y -= 1
    return x, y

def validPathGeneration(maze, starting_x, starting_y, ending_x, ending_y, n):
    sx, sy = starting_x, starting_y
    ex, ey = ending_x, ending_y
    
    # make sure to move away from edge before we make the paths
    sx, sy = moveAwayFromEdge(sx, sy, n)
    ex, ey = moveAwayFromEdge(ex, ey, n)
    while (sx, sy) != (ex, ey):
        if maze[sy][sx] == 1:
            maze[sy][sx] = 0
        # add curve to path
        directions = []
        if sx < ex: 
            directions.append((1, 0))
        if sx > ex: 
            directions.append((-1, 0))
        if sy < ey: 
            directions.append((0, 1))
        if sy > ey:
            directions.append((0, -1))
        dx, dy = random.choice(directions)
        sx += dx
        sy += dy
    if maze[ey][ex] == 1:
        maze[ey][ex] = 0
    return maze

def makeBendsInMaze(n, maze, starting_x, starting_y, ending_x, ending_y, n_points):
    max_n_points = n // 4
    
    # once we reach max number of points, we make path to the ending point
    if n_points >= max_n_points:
        maze = validPathGeneration(maze, starting_x, starting_y, ending_x, ending_y, n)
        return maze
    
    # otherwise we select a random point
    random_point = randomPoint(maze, n)
    random_point_x, random_point_y = random_point
    
    # and make a valid path to it
    maze = validPathGeneration(maze, starting_x, starting_y, random_point_x, random_point_y, n)
    maze[random_point_y][random_point_x] = 4
    n_points += 1
    return makeBendsInMaze(n, maze, random_point_x, random_point_y, ending_x, ending_y, n_points)
    
def makeMaze():
    n = 20
    maze = [[1] * n for _ in range(n)]
    
    # generate start and end points
    starting_x, starting_y, ending_x, ending_y = startAndEndPoints(n)
    
    # make bends in the maze
    n_points = 0    
    maze = makeBendsInMaze(n, maze, starting_x, starting_y, ending_x, ending_y, n_points)
    
    # make branching paths from main path
    maze = makeBranchingPaths(n, maze)
    
    # special markers for start, end, and random point
    maze[starting_y][starting_x] = 2
    maze[ending_y][ending_x] = 3
    
    return maze, starting_x, starting_y

def makeBranchingPaths(n, maze):
    # make n number of branching paths
    n_branches = n // 5
    
    # for each branching path we will selet a random starting point on main path and a random ending point
    for _ in range(n_branches):
        starting_branch = randomSpace(maze, n)
        starting_branch_x, starting_branch_y = starting_branch
        ending_branch = randomPoint(maze, n)
        ending_branch_x, ending_branch_y = ending_branch
        
        # we make a valid path from that starting point to the ending point, and mark the end as the branching path
        maze = validPathGeneration(maze, starting_branch_x, starting_branch_y, ending_branch_x, ending_branch_y, n)
        maze[ending_branch_y][ending_branch_x] = 5
        
        # we then try creating sub branching paths from that ending point
        sub_level_counter = 0
        maze = makeSubBranchingPaths(n, maze, ending_branch_x, ending_branch_y, sub_level_counter)
    return maze

def makeSubBranchingPaths(n, maze, ending_branch_x, ending_branch_y, sub_level_counter):
    # each sub branching path has a chance to create another sub branching path
    sub_level_counter += 1
    
    # max limit of sub branching paths
    if sub_level_counter > n // 5:
        return maze
    
    # roll chance to create another sub branching path
    sub_branch_chance = random.randint(0, 10)
    if sub_branch_chance > 1:
        # create a ending point for the sub branching path
        sub_branch_ending = randomPoint(maze, n)
        sub_branch_ending_x, sub_branch_ending_y = sub_branch_ending
        
        # we make a path from the starting to ending point
        maze = validPathGeneration(maze, ending_branch_x, ending_branch_y, sub_branch_ending_x, sub_branch_ending_y, n)
        
        # mark the end of the sub branching path
        maze[sub_branch_ending_y][sub_branch_ending_x] = 5 + sub_level_counter
        
        # and then we try to make another sub branching path over and over again until either we reach the limit or fail the chance roll
        maze = makeSubBranchingPaths(n, maze, sub_branch_ending_x, sub_branch_ending_y, sub_level_counter)
    return maze

def randomSpace(maze, n):
    # select a random point in the maze that isn't on a already open space
    x = random.randint(1, n - 2)
    y = random.randint(1, n - 2)
    if (maze[y][x] != 0):
        return randomSpace(maze, n)
    return (x, y)

def randomPoint(maze, n):
    # select a random point in the maze that isn't on a already open space
    x = random.randint(1, n - 2)
    y = random.randint(1, n - 2)
    if (maze[y][x] == 0):
        return randomPoint(maze, n)
    return (x, y)

def displayMaze(maze, player_position):
    # displays the maze
    for y, row in enumerate(maze):
            cells = []
            for x, cell in enumerate(row):
                if (x, y) == player_position:
                    cells.append("P")
                elif cell == 1:
                    cells.append("#")
                elif cell == 0:
                    cells.append(".")
                elif cell == 2:
                    cells.append("S")
                elif cell == 3:
                    cells.append("E")
                elif cell == 4:
                    cells.append("I")
                elif cell == 5:
                    cells.append("B")
                elif cell == 6:
                    cells.append("b")
                elif cell >= 7:
                    cells.append(f"{cell}")
            print(" ".join(cells))
            
def drawMaze(screen, maze, player_position):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = COLORS.get(cell, (255, 255, 255))
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
    
    # draw player
    player_x, player_y = player_position
    player_position_rect = pygame.draw.rect(
        screen, 
        (0, 0, 255), 
        pygame.Rect(player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    ) 

def isValidMove(maze, x, y):
    # checks if the move is valid
    if y < 0 or y >= len(maze):
        return False
    if x < 0 or x >= len(maze[y]):
        return False
    if maze[y][x] == 1:
        return False
    return True

def playMaze(maze, player_position):
    player_position_x, player_position_y = player_position
    isInput = True

    while (isInput):
        # display maze
        displayMaze(maze, player_position)     
        T = input().lower()
        
        # movement logic
        dy, dx = 0, 0
        if (T == "left"):
            dx = -1
        elif (T == "right"):
            dx = 1
        elif (T == "up"):
            dy = -1
        elif (T == "down"):
            dy = 1

        # valid move check
        new_dx, new_dy = player_position_x + dx, player_position_y + dy
        if not isValidMove(maze, new_dx, new_dy):
            print("Invalid Move")
            continue
        
        # check if player tries to return to start point
        if maze[new_dy][new_dx] == 2:
            print("You Can't Leave")
            continue
        
        # position update
        player_position_x += dx
        player_position_y += dy
        player_position = (player_position_x, player_position_y)
        
        # check if player reaches exits
        if maze[player_position_y][player_position_x] == 3:
            print("You Found The Exit!")
            break

def keyMovement(maze, player_position, keys):
    player_position_x, player_position_y = player_position
    dx, dy = 0, 0
    if (keys[pygame.K_LEFT]):
        dx = -1
    elif (keys[pygame.K_RIGHT]):
        dx = 1
    elif (keys[pygame.K_UP]):
        dy = -1
    elif (keys[pygame.K_DOWN]):
        dy = 1
        
    # valid move check
    new_dx, new_dy = player_position_x + dx, player_position_y + dy
    if isValidMove(maze, new_dx, new_dy):
        return (new_dx, new_dy)
    
    return (player_position_x, player_position_y)
    

def main():
    # test if pygame works
    print(pygame.ver)
    pygame.init()
    
    # make a random maze
    maze, starting_x, starting_y = makeMaze()
    player_position = (starting_x, starting_y)
    
    # maze dimensions
    rows = len(maze)
    columns = len(maze[0])
    
    # set up pygame window
    screen = pygame.display.set_mode((columns * CELL_SIZE, rows * CELL_SIZE))
    pygame.display.set_caption("Maze Game")
    
    # main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        player_position = keyMovement(maze, player_position, keys)
                
        if maze[player_position[1]][player_position[0]] == 3:
            print("You Found The Exit!")
            running = False
        
        screen.fill((0, 0, 0))
        drawMaze(screen, maze, player_position)
        pygame.display.flip()
    
    # we don't need the old playMaze or displayMaze function for pygame version
    # player_position = starting_x, starting_y
    # play the maze
    # playMaze(maze, player_position)
    # test to see if it would close when maze is done
    pygame.quit()

if __name__ == "__main__":
    main()