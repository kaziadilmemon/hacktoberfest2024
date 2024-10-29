import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the Game of Life class
class GameOfLife:
    def __init__(self, size, initial_state=None):
        self.size = size
        # If initial state is provided, use it; otherwise, start with a random grid
        if initial_state is None:
            self.grid = np.random.choice([0, 1], size=(size, size))
        else:
            self.grid = np.array(initial_state)

    def get_neighbors(self, row, col):
        # Get coordinates of neighbors with wrap-around (toroidal boundary conditions)
        neighbors = [
            ((row-1) % self.size, (col-1) % self.size),
            ((row-1) % self.size, col),
            ((row-1) % self.size, (col+1) % self.size),
            (row, (col-1) % self.size),
            (row, (col+1) % self.size),
            ((row+1) % self.size, (col-1) % self.size),
            ((row+1) % self.size, col),
            ((row+1) % self.size, (col+1) % self.size)
        ]
        return neighbors

    def update_cell(self, row, col):
        # Get the state of the cell and its neighbors
        cell_state = self.grid[row, col]
        neighbors = self.get_neighbors(row, col)
        live_neighbors = sum(self.grid[n[0], n[1]] for n in neighbors)
        
        # Apply the rules of the Game of Life
        if cell_state == 1:  # Cell is alive
            if live_neighbors < 2 or live_neighbors > 3:
                return 0  # Cell dies
            else:
                return 1  # Cell survives
        else:  # Cell is dead
            if live_neighbors == 3:
                return 1  # Cell becomes alive
            else:
                return 0  # Cell remains dead

    def update_grid(self):
        # Create a copy of the grid to update cells without interfering with current states
        new_grid = np.copy(self.grid)
        for row in range(self.size):
            for col in range(self.size):
                new_grid[row, col] = self.update_cell(row, col)
        self.grid = new_grid

    def animate(self, generations=100, interval=200):
        # Set up the figure and axis for animation
        fig, ax = plt.subplots()
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Initialize the image
        img = ax.imshow(self.grid, cmap='binary')
        
        # Define update function for animation
        def update(*args):
            self.update_grid()
            img.set_array(self.grid)
            return img,
        
        # Run animation
        ani = animation.FuncAnimation(fig, update, frames=generations, interval=interval, blit=True)
        plt.show()

# Initialize and run the game
size = 50  # Define grid size
initial_state = np.random.choice([0, 1], size=(size, size), p=[0.8, 0.2])  # Sparse initial state

game = GameOfLife(size=size, initial_state=initial_state)
game.animate(generations=200, interval=100)
