"""
UI Constants for the Tkinter Graphing Calculator

This module contains all the constants related to the
user interface, such as colors, fonts, and layout dimensions.
"""

# Modern Color Palette
PRIMARY_BG = "#1a1a1a"           # Deep dark background
SECONDARY_BG = "#2d2d2d"         # Lighter dark for panels
ACCENT_BG = "#3d3d3d"            # Even lighter for hover states
CARD_BG = "#252525"              # Card/panel background

# Text Colors
PRIMARY_TEXT = "#ffffff"          # Pure white for primary text
SECONDARY_TEXT = "#b0b0b0"        # Light gray for secondary text
ACCENT_TEXT = "#4a9eff"           # Blue accent for highlights

# Accent Colors
ACCENT_BLUE = "#4a9eff"           # Primary accent blue
ACCENT_GREEN = "#00d4aa"          # Success/positive green
ACCENT_ORANGE = "#ff6b35"         # Warning/attention orange
ACCENT_RED = "#ff4757"            # Error/danger red
ACCENT_PURPLE = "#a55eea"         # Purple accent

# Button Colors
BUTTON_PRIMARY = "#4a9eff"        # Primary button color
BUTTON_PRIMARY_HOVER = "#357abd"  # Primary button hover
BUTTON_SECONDARY = "#3d3d3d"      # Secondary button color
BUTTON_SECONDARY_HOVER = "#4d4d4d" # Secondary button hover

# Border and Shadow Colors
BORDER_COLOR = "#404040"          # Subtle borders
SHADOW_COLOR = "#0a0a0a"          # Drop shadow color

# Modern Typography (scaled down for smaller window)
TITLE_FONT = ("Segoe UI", 18, "bold")
HEADING_FONT = ("Segoe UI", 12, "bold")
BODY_FONT = ("Segoe UI", 10)
BUTTON_FONT = ("Segoe UI", 10, "bold")
SMALL_FONT = ("Segoe UI", 8)
MONO_FONT = ("Consolas", 10)      # For function input

# Layout Constants (scaled down for smaller window)
PADDING_LARGE = 13
PADDING_MEDIUM = 8
PADDING_SMALL = 4
BORDER_RADIUS = 6
BUTTON_HEIGHT = 32
INPUT_HEIGHT = 28

# Animation Constants
HOVER_ANIMATION_MS = 150

# Default plot settings
DEFAULT_MIN_VALUE = -10.0
DEFAULT_MAX_VALUE = 10.0
MOVEMENT_STEP = 2.0
ZOOM_STEP = 2.0
SCROLL_ZOOM_FACTOR = 0.1
PLOT_RESOLUTION = 0.01

# Performance optimization constants
CACHE_RESOLUTION_FACTOR = 2.0
MIN_CACHE_RANGE = 50.0

# Modern color palette for plotting
PLOT_COLORS = [
    ('#4a9eff', 'Electric Blue'),
    ('#00d4aa', 'Mint Green'),
    ('#ff6b35', 'Coral Orange'),
    ('#a55eea', 'Purple'),
    ('#ff4757', 'Red'),
    ('#ffa502', 'Orange'),
    ('#2ed573', 'Green'),
    ('#ff3838', 'Bright Red'),
    ('#18dcff', 'Cyan'),
    ('#7bed9f', 'Light Green')
]

WINDOW_TITLE = "Modern Graphing Calculator" 