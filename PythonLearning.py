import random

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

    edges.remove(starting_edge) # remove the starting edge from the list

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
        
    return starting_x, starting_y, ending_x, ending_y

def makeMaze():
    n = random.randint(5, 10)
    maze = [[1] * n for _ in range(n)]
    
    # generate start and end points
    starting_x, starting_y, ending_x, ending_y = startAndEndPoints(n)
    
    # turn all non edge cells into empty space 
    for y in range(1, n - 1):
        for x in range(1, n - 1):
            maze[y][x] = 0
            
    # random wall generation
    for y in range(1, n - 1):
        for x in range(1, n - 1):
            if random.randint(0, 10) < 11:
                maze[y][x] = 1

    # valid path generation
    sx, sy = starting_x, starting_y
    ex, ey = ending_x, ending_y
    # make sure to move away from edge before we make the paths
    if (sx == n - 1):
        sx -= 1
    elif (sx == 0):
        sx += 1
    elif (sy == n - 1):
        sy -= 1
    elif (sy == 0):
        sy += 1
    if (ex == n - 1):
        ex -= 1
    elif (ex == 0):
        ex += 1
    elif (ey == n - 1):
        ey -= 1
    elif (ey == 0):
        ey += 1
    while (sx, sy) != (ex, ey):
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
    maze[ey][ex] = 0
    maze[starting_y][starting_x] = 2
    maze[ending_y][ending_x] = 3
    
    return maze, starting_x, starting_y

def displayMaze(maze, player_position):
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
            print(" ".join(cells))   

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

        # boundary check
        if (
            player_position_y + dy < 0 or 
            player_position_y + dy >= len(maze) or 
            player_position_x + dx < 0 or 
            player_position_x + dx >= len(maze[player_position_y])
            ):
            print("Out of Bounds")
            continue
        # wall check
        if (maze[player_position_y + dy][player_position_x + dx] == 1):
            print("Wall")
            continue
        
        # position update
        player_position_x += dx
        player_position_y += dy
        player_position = (player_position_x, player_position_y)
        
        # special cells check
        if maze[player_position_y][player_position_x] == 2:
            print("You Can't Leave")
        if maze[player_position_y][player_position_x] == 3:
            print("You Found The Exit!")
            break

def main():
    print("Game Start")
    # make a random maze
    maze, starting_x, starting_y = makeMaze()
    player_position = starting_x, starting_y
    # play the maze
    playMaze(maze, player_position)

if __name__ == "__main__":
    main()