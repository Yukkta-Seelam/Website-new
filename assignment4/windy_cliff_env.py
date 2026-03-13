"""
Windy Cliff Environment
A gridworld with upward wind in specified columns and a cliff along the start-goal row.
"""
import numpy as np


class WindyCliffEnv:
    """
    Windy Cliff Walking Environment
    
    Gridworld with:
    - Upward wind in specified columns (pushes agent up)
    - Cliff along the start-goal row (bottom row)
    - Start position: bottom-left
    - Goal position: bottom-right
    - Rewards: -1 per step, -100 for cliff, 0 on goal
    """
    
    def __init__(self, height=7, width=10, wind_strength=[0, 0, 0, 1, 1, 1, 2, 2, 1, 0], max_steps=1000):
        """
        Initialize the environment.
        
        Args:
            height: Height of the grid (default 7)
            width: Width of the grid (default 10)
            wind_strength: List of wind strength for each column (pushes agent up by this amount)
            max_steps: Maximum steps per episode
        """
        self.height = height
        self.width = width
        self.wind_strength = wind_strength
        self.max_steps = max_steps
        
        # Start and goal positions (bottom-left and bottom-right)
        self.start_pos = (height - 1, 0)
        self.goal_pos = (height - 1, width - 1)
        
        # Actions: 0=up, 1=right, 2=down, 3=left
        self.actions = [0, 1, 2, 3]
        self.n_actions = len(self.actions)
        
        # State space: all (row, col) positions
        self.n_states = height * width
        
        self.reset()
    
    def reset(self):
        """Reset the environment to initial state."""
        self.state = self.start_pos
        self.steps = 0
        return self.state
    
    def get_state_index(self, state):
        """Convert (row, col) state to a single index."""
        row, col = state
        return row * self.width + col
    
    def step(self, action):
        """
        Take a step in the environment.
        
        Args:
            action: Action to take (0=up, 1=right, 2=down, 3=left)
        
        Returns:
            next_state, reward, done, info
        """
        row, col = self.state
        
        # Apply action
        if action == 0:  # Up
            row = max(0, row - 1)
        elif action == 1:  # Right
            col = min(self.width - 1, col + 1)
        elif action == 2:  # Down
            row = min(self.height - 1, row + 1)
        elif action == 3:  # Left
            col = max(0, col - 1)
        
        # Apply wind (pushes up)
        wind = self.wind_strength[col]
        row = max(0, row - wind)
        
        self.state = (row, col)
        self.steps += 1
        
        # Check if goal reached
        if self.state == self.goal_pos:
            reward = 0
            done = True
        # Check if cliff (bottom row except start and goal)
        elif row == self.height - 1 and col != 0 and col != self.width - 1:
            reward = -100
            done = False  # Reset to start, don't terminate episode
            self.state = self.start_pos
        else:
            reward = -1
            done = False
        
        # Check max steps
        if self.steps >= self.max_steps:
            done = True
        
        return self.state, reward, done, {}
    
    def render(self):
        """Render the current state of the environment."""
        grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
        
        # Mark cliff
        for col in range(1, self.width - 1):
            grid[self.height - 1][col] = 'C'
        
        # Mark start and goal
        grid[self.start_pos[0]][self.start_pos[1]] = 'S'
        grid[self.goal_pos[0]][self.goal_pos[1]] = 'G'
        
        # Mark agent
        row, col = self.state
        grid[row][col] = 'A'
        
        print("\n".join([" ".join(row) for row in grid]))
        print(f"Wind strength by column: {self.wind_strength}")
        print()

