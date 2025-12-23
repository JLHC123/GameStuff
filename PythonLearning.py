import random

print("Game Start")
# # generic maze
# maze = [
#     [1, 1, 3, 1, 1],
#     [1, 1, 0, 0, 1],
#     [1, 0, 1, 0, 1],
#     [1, 0, 0, 0, 1],
#     [1, 1, 2, 1, 1]
# ]

# make random maze
n = random.randint(5, 10)
random_maze = [[1] * n for _ in range(n)]

# select random starting point from just the outer walls
edges = ["top", "bottom", "left", "right"]
starting_edge = random.choice(edges)
if starting_edge == "top":
    random_starting_x = random.randint(1, n - 2)
    random_starting_y = 0
elif starting_edge == "bottom": 
    random_starting_x = random.randint(1, n - 2)
    random_starting_y = n - 1
elif starting_edge == "left": 
    random_starting_x = 0
    random_starting_y = random.randint(1, n - 2)
elif starting_edge == "right": 
    random_starting_x = n - 1
    random_starting_y = random.randint(1, n - 2)
random_maze[random_starting_y][random_starting_x] = 2

edges.remove(starting_edge) # remove the starting edge from the list

# select random ending point from the remaining outer walls
ending_edge = random.choice(edges)
if ending_edge == "top":
    random_ending_x = random.randint(1, n - 2)
    random_ending_y = 0
elif ending_edge == "bottom": 
    random_ending_x = random.randint(1, n - 2)
    random_ending_y = n - 1
elif ending_edge == "left": 
    random_ending_x = 0
    random_ending_y = random.randint(1, n - 2)
elif ending_edge == "right": 
    random_ending_x = n - 1
    random_ending_y = random.randint(1, n - 2)
random_maze[random_ending_y][random_ending_x] = 3

# turn all non edge cells into empty space 
for y in range(1, n - 1):
    for x in range(1, n - 1):
        random_maze[y][x] = 0
        
# random wall generation
for y in range(1, n - 1):
    for x in range(1, n - 1):
        if random.randint(0, 10) < 3:
            random_maze[y][x] = 1

# print random maze
for y, row in enumerate(random_maze):
    cells = []
    for x, cell in enumerate(row):
        cells.append(f"{cell}")
    print(" ".join(cells))

player_position = None
# finding our player start position
for y, row in enumerate(random_maze):
    for x, cell in enumerate(row):
        if cell == 2:
            player_position = (x, y)
            break
    if player_position is not None:
        break
    
player_position_x, player_position_y = player_position
isInput = True

while (isInput):
    # map display
    for y, row in enumerate(random_maze):
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
        player_position_y + dy >= len(random_maze) or 
        player_position_x + dx < 0 or 
        player_position_x + dx >= len(random_maze[player_position_y])
        ):
        print("Out of Bounds")
        continue
    # wall check
    if (random_maze[player_position_y + dy][player_position_x + dx] == 1):
        print("Wall")
        continue
    
    # position update
    player_position_x += dx
    player_position_y += dy
    player_position = (player_position_x, player_position_y)
    
    # special cells check
    if random_maze[player_position_y][player_position_x] == 2:
        print("You Can't Leave")
    if random_maze[player_position_y][player_position_x] == 3:
        print("You Found The Exit!")
        break