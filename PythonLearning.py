print("Game Start")
# generic maze
maze = [
    [1, 1, 3, 1, 1],
    [1, 1, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 2, 1, 1]
]

player_position = None
# finding our player start position
for y, row in enumerate(maze):
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
               
    T = input().lower()
    # movement logic
    dy, dx = 0, 0
    if (T == "left"):
        dx = -1
    if (T == "right"):
        dx = 1
    if (T == "up"):
        dy = -1
    if (T == "down"):
        dy = 1

    # boundary and wall check
    if (player_position_y + dy < 0 or player_position_y + dy >= len(maze) or player_position_x + dx < 0 or player_position_x + dx >= len(maze[player_position_y])):
        print("Out of Bounds")
        continue
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