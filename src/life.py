import time
import os
import random

def create_grid(rows, cols):
    return [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

def get_neighbors(grid, r, c):
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nr, nc = (r + i) % rows, (c + j) % cols
            count += grid[nr][nc]
    return count

def next_generation(grid):
    rows = len(grid)
    cols = len(grid[0])
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            neighbors = get_neighbors(grid, r, c)
            if grid[r][c] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[r][c] = 0
                else:
                    new_grid[r][c] = 1
            else:
                if neighbors == 3:
                    new_grid[r][c] = 1
    return new_grid

def print_grid(grid):
    # os.system('clear')
    # print("\033[H", end="") # Move cursor home
    print("-" * 40)
    output = ""
    for row in grid:
        output += "".join([' 🦀 ' if cell else '  . ' for cell in row]) + "\n"
    print(output)

def main():
    rows, cols = 10, 10
    grid = create_grid(rows, cols)
    
    try:
        generations = 0
        while generations < 3:  # Run for 3 frames for demo
            print_grid(grid)
            print(f"Generation: {generations}")
            grid = next_generation(grid)
            time.sleep(0.5)
            generations += 1
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
