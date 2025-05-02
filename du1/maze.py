import sys

def check_maze(maze):
    # 1. Check if rectangular
    width = len(maze[0])
    for row in maze:
        if len(row) != width:
            sys.stderr.write("Error: Bludiste neni obdelnikove!\n")
            return False

    # 2. Check entrance (second char in first row)
    if maze[0][1] != ".":
        sys.stderr.write("Error: Vstup neni vlevo nahore!\n")
        return False

    # 3. Check exit (second-to-last char in last row)
    height = len(maze)
    if maze[height - 1][width - 2] != ".":
        sys.stderr.write("Error: Vystup neni vpravo dole!\n")
        return False

    # 4. Check width (5 to 100)
    if width < 5 or width > 100:
        sys.stderr.write("Error: Sirka bludiste je mimo rozsah!\n")
        return False

    # 5. Check height (5 to 50)
    if height < 5 or height > 50:
        sys.stderr.write("Error: Delka bludiste je mimo rozsah!\n")
        return False

    # 6. Check characters (only # or .)
    for i in range(height):
        for j in range(width):
            if maze[i][j] != "#" and maze[i][j] != ".":
                sys.stderr.write("Error: Bludiste obsahuje nezname znaky!\n")
                return False

    # 7. Check borders
    # Top row (all # except j=1)
    for j in range(width):
        if j != 1 and maze[0][j] != "#":
            sys.stderr.write("Error: Bludiste neni oplocene!\n")
            return False
    # Bottom row (all # except j=width-2)
    for j in range(width):
        if j != width - 2 and maze[height - 1][j] != "#":
            sys.stderr.write("Error: Bludiste neni oplocene!\n")
            return False
    # Left and right columns (all #)
    for i in range(height):
        if maze[i][0] != "#":
            sys.stderr.write("Error: Bludiste neni oplocene!\n")
            return False
        if maze[i][width - 1] != "#":
            sys.stderr.write("Error: Bludiste neni oplocene!\n")
            return False

    return True

def find_key_points(maze):
    changed = []

    # DFS to find a path
    def search_path(x, y):
        # Check bounds and if passable
        if (y < 0 or y >= len(maze) or x < 0 or x >= len(maze[0]) or 
            maze[y][x] != "."):
            return None

        # Found exit
        if x == len(maze[0]) - 2 and y == len(maze) - 1:
            return [(x, y)]

        # Mark as visited
        maze[y][x] = "X"
        changed.append((x, y))

        # Try directions: down, right, up, left
        path = search_path(x, y + 1)  # Down
        if path:
            return [(x, y)] + path
        path = search_path(x + 1, y)  # Right
        if path:
            return [(x, y)] + path
        path = search_path(x, y - 1)  # Up
        if path:
            return [(x, y)] + path
        path = search_path(x - 1, y)  # Left
        if path:
            return [(x, y)] + path

        return None

    # Add temporary walls in open areas
    temp_walls = []
    for i in range(2, len(maze) - 1):
        for j in range(2, len(maze[0]) - 2):
            if maze[i][j] == ".":
                # Check if surrounded by dots
                all_dots = True
                for r in range(i - 1, i + 2):
                    for c in range(j - 1, j + 2):
                        if maze[r][c] != ".":
                            all_dots = False
                if all_dots:
                    maze[i][j] = "#"
                    temp_walls.append((j, i))

    # Find first path
    first_path = search_path(1, 0)

    # Reset maze
    for x, y in changed:
        maze[y][x] = "."
    changed = []

    # Check if path exists
    if not first_path:
        sys.stderr.write("Error: Cesta neexistuje!\n")
        return None

    # Start with entrance and exit as key points
    key_points = [first_path[0], first_path[1], first_path[-2], first_path[-1]]

    # Test each point in the path
    for i in range(2, len(first_path) - 2):
        x, y = first_path[i]
        maze[y][x] = "#"  # Block this point
        test_path = search_path(1, 0)

        # Reset maze
        for cx, cy in changed:
            maze[cy][cx] = "."
        changed = []

        if not test_path:  # No path means this is a key point
            key_points.append((x, y))

        maze[y][x] = "."  # Restore it

    # Remove temporary walls
    for x, y in temp_walls:
        maze[y][x] = "."

    return key_points

# Read the maze
maze = []
while True:
    try:
        line = input()
        if line == "":
            break
        maze.append(list(line))
    except EOFError:
        break

# Validate and solve
if check_maze(maze):
    key_points = find_key_points(maze)
    if key_points is None:  # No path exists
        sys.exit(1)

    # Mark key points with !
    for x, y in key_points:
        maze[y][x] = "!"

    # Print the maze
    for row in maze:
        print("".join(row))
else:
    sys.exit(1)