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
        
print(player_position)
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
               
    # Movement
    T = input().lower()
    if (T == "left"):
        if player_position_x - 1 < 0:
            print("Out of Bounds")
        elif maze[player_position_y][player_position_x - 1] == 1:
            print("Wall")
        else:
            player_position_x = player_position_x - 1
            player_position = (player_position_x, player_position_y)
            print(player_position)
    if (T == "right"):
        if player_position_x + 1 >= len(maze[player_position_y]):
            print("Out of Bounds")
        elif maze[player_position_y][player_position_x + 1] == 1:
            print("Wall")
        else:
            player_position_x = player_position_x + 1
            player_position = (player_position_x, player_position_y)
            print(player_position)
    if (T == "up"):
        if player_position_y - 1 < 0:
            print("Out of Bounds")
        elif maze[player_position_y - 1][player_position_x] == 1:
            print("Wall")
        else:
            player_position_y = player_position_y - 1
            player_position = (player_position_x, player_position_y)
            print(player_position)
    if (T == "down"):
        if player_position_y + 1 >= len(maze):
            print("Out of Bounds")
        elif maze[player_position_y + 1][player_position_x] == 1:
            print("Wall")
        else:
            player_position_y = player_position_y + 1
            player_position = (player_position_x, player_position_y)
            print(player_position)
    # Special Cells
    if maze[player_position_y][player_position_x] == 2:
        print("You Can't Leave")
    if maze[player_position_y][player_position_x] == 3:
        print("You Found The Exit!")
        break