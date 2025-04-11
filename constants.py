# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700

# Grid dimensions
GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30

# Colors
BG_COLOR = (20, 20, 30)
GRID_COLOR = (40, 40, 50)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)

# Tetrimino colors
COLORS = {
    'I': (0, 240, 240),    # Cyan
    'O': (240, 240, 0),    # Yellow
    'T': (160, 0, 240),    # Purple
    'S': (0, 240, 0),      # Green
    'Z': (240, 0, 0),      # Red
    'J': (0, 0, 240),      # Blue
    'L': (240, 160, 0)     # Orange
}

# Tetrimino shapes (using relative coordinates)
SHAPES = {
    'I': [[(0, 0), (0, -1), (0, 1), (0, 2)],
          [(0, 0), (-1, 0), (1, 0), (2, 0)],
          [(0, 0), (0, -1), (0, 1), (0, 2)],
          [(0, 0), (-1, 0), (1, 0), (2, 0)]],
    
    'O': [[(0, 0), (1, 0), (0, 1), (1, 1)],
          [(0, 0), (1, 0), (0, 1), (1, 1)],
          [(0, 0), (1, 0), (0, 1), (1, 1)],
          [(0, 0), (1, 0), (0, 1), (1, 1)]],
    
    'T': [[(0, 0), (-1, 0), (1, 0), (0, -1)],
          [(0, 0), (0, -1), (0, 1), (1, 0)],
          [(0, 0), (-1, 0), (1, 0), (0, 1)],
          [(0, 0), (0, -1), (0, 1), (-1, 0)]],
    
    'S': [[(0, 0), (-1, 0), (0, -1), (1, -1)],
          [(0, 0), (0, -1), (1, 0), (1, 1)],
          [(0, 0), (-1, 0), (0, -1), (1, -1)],
          [(0, 0), (0, -1), (1, 0), (1, 1)]],
    
    'Z': [[(0, 0), (1, 0), (0, -1), (-1, -1)],
          [(0, 0), (0, 1), (1, 0), (1, -1)],
          [(0, 0), (1, 0), (0, -1), (-1, -1)],
          [(0, 0), (0, 1), (1, 0), (1, -1)]],
    
    'J': [[(0, 0), (-1, 0), (1, 0), (1, -1)],
          [(0, 0), (0, -1), (0, 1), (1, 1)],
          [(0, 0), (-1, 0), (1, 0), (-1, 1)],
          [(0, 0), (0, -1), (0, 1), (-1, -1)]],
    
    'L': [[(0, 0), (-1, 0), (1, 0), (-1, -1)],
          [(0, 0), (0, -1), (0, 1), (1, -1)],
          [(0, 0), (-1, 0), (1, 0), (1, 1)],
          [(0, 0), (0, -1), (0, 1), (-1, 1)]]
}

# Wall kick data (for J, L, S, T, Z pieces)
WALL_KICK_DATA = {
    "0->1": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    "1->0": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    "1->2": [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    "2->1": [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    "2->3": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    "3->2": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    "3->0": [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    "0->3": [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]
}

# Wall kick data for I piece
WALL_KICK_I = {
    "0->1": [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],
    "1->0": [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],
    "1->2": [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)],
    "2->1": [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
    "2->3": [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],
    "3->2": [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],
    "3->0": [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
    "0->3": [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)]
}

# Game settings
INITIAL_FALL_SPEED = 1.0  # Pieces per second
SOFT_DROP_FACTOR = 5.0    # How much faster when soft dropping
LEVEL_SPEED_FACTOR = 0.1  # How much faster per level
LINES_PER_LEVEL = 10      # Lines needed to advance a level
MAX_LEVEL = 15            # Maximum level

# Key repeat settings
KEY_REPEAT_DELAY = 170    # ms before key starts repeating
KEY_REPEAT_INTERVAL = 50  # ms between repeats

# Animation settings
LINE_CLEAR_ANIMATION_DURATION = 0.5  # seconds
PIECE_APPEAR_ANIMATION_DURATION = 0.2  # seconds

# Scoring system
SCORE_SINGLE = 100
SCORE_DOUBLE = 300
SCORE_TRIPLE = 500
SCORE_TETRIS = 800
SCORE_SOFT_DROP = 1
SCORE_HARD_DROP = 2

# File paths
HIGH_SCORE_FILE = "high_score.txt"