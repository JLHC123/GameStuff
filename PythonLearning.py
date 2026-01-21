import random
import copy

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
        if maze[sy][sx] not in {2, 3, 4, 5}:
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
    if maze[ey][ex] not in {2, 3, 4, 5}:
        maze[ey][ex] = 0
    return maze

def makeMaze():
    n = 10
    maze = [[1] * n for _ in range(n)]
    
    # generate start and end points
    starting_x, starting_y, ending_x, ending_y = startAndEndPoints(n)
    
    # make a copy of maze that contains the start to end path
    tempMaze = copy.deepcopy(maze)
    tempMaze = validPathGeneration(tempMaze, starting_x, starting_y, ending_x, ending_y, n)
    
    # select a random point in the maze that is not on the path from start to end    
    random_point = randomPoint(tempMaze, n)
    random_point_x, random_point_y = random_point
    
    # generate paths from start to random point and from random point to end
    maze = validPathGeneration(maze, starting_x, starting_y, random_point_x, random_point_y, n)
    maze = validPathGeneration(maze, random_point_x, random_point_y, ending_x, ending_y, n)
    
    # make branching paths from main path
    maze = makeBranchingPaths(n, maze)
    
    # special markers for start, end, and random point
    maze[starting_y][starting_x] = 2
    maze[ending_y][ending_x] = 3
    maze[random_point_y][random_point_x] = 4
    
    return maze, starting_x, starting_y

def makeBranchingPaths(n, maze):
    n_branches = n // 2
    for _ in range(n_branches):
        starting_branch = randomSpace(maze, n)
        starting_branch_x, starting_branch_y = starting_branch
        ending_branch = randomPoint(maze, n)
        ending_branch_x, ending_branch_y = ending_branch
        maze = validPathGeneration(maze, starting_branch_x, starting_branch_y, ending_branch_x, ending_branch_y, n)
        maze[ending_branch_y][ending_branch_x] = 5
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
            print(" ".join(cells))   

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

def main():
    print("Game Start")
    # make a random maze
    maze, starting_x, starting_y = makeMaze()
    player_position = starting_x, starting_y
    # play the maze
    playMaze(maze, player_position)

if __name__ == "__main__":
    main()