"""
Tkinter Graphing Calculator

A modern GUI application for plotting mathematical functions using matplotlib and tkinter.
Provides interactive controls for zooming, panning, and customizing the plot appearance.
Features a contemporary dark theme with smooth animations and modern styling.
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import sympy as sp
from typing import Optional, Callable, Tuple
import constants as c
import ui_components
import plot_manager
import view_manager


class GraphingCalculator:
    def __init__(self) -> None:
        """Initialize the graphing calculator application."""
        self.window = tk.Tk()
        self._setup_window()
        self._initialize_variables()
        self._initialize_performance_cache()
        self._create_ui_components()

    def _setup_window(self) -> None:
        """Configure the main window properties with modern styling."""
        self.window.title(c.WINDOW_TITLE)
        self.window.configure(bg=c.PRIMARY_BG)
        self.window.resizable(True, True)
        self.window.minsize(700, 550)

        # Center window on screen
        self.window.update_idletasks()
        width = 1000
        height = 750
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        # Configure modern ttk styles
        self._configure_modern_styles()

    def _configure_modern_styles(self) -> None:
        """Configure modern ttk styles for widgets."""
        style = ttk.Style()

        # Configure modern entry style
        style.theme_use("clam")
        style.configure(
            "Modern.TEntry",
            fieldbackground=c.SECONDARY_BG,
            background=c.SECONDARY_BG,
            foreground=c.PRIMARY_TEXT,
            bordercolor=c.BORDER_COLOR,
            lightcolor=c.BORDER_COLOR,
            darkcolor=c.BORDER_COLOR,
            insertcolor=c.ACCENT_BLUE,
            selectbackground=c.ACCENT_BLUE,
            selectforeground=c.PRIMARY_TEXT,
        )

        # Configure modern combobox style
        style.configure(
            "Modern.TCombobox",
            fieldbackground=c.SECONDARY_BG,
            background=c.SECONDARY_BG,
            foreground=c.PRIMARY_TEXT,
            bordercolor=c.BORDER_COLOR,
            arrowcolor=c.PRIMARY_TEXT,
            selectbackground=c.ACCENT_BLUE,
            selectforeground=c.PRIMARY_TEXT,
        )

        # Configure modern button style
        style.configure(
            "Modern.TButton",
            background=c.BUTTON_SECONDARY,
            foreground=c.PRIMARY_TEXT,
            bordercolor=c.BORDER_COLOR,
            lightcolor=c.BORDER_COLOR,
            darkcolor=c.BORDER_COLOR,
            focuscolor="none",
        )

        style.map(
            "Modern.TButton",
            background=[
                ("active", c.BUTTON_SECONDARY_HOVER),
                ("pressed", c.ACCENT_BLUE),
            ],
        )

        # Configure primary button style
        style.configure(
            "Primary.TButton",
            background=c.BUTTON_PRIMARY,
            foreground=c.PRIMARY_TEXT,
            bordercolor=c.BUTTON_PRIMARY,
            lightcolor=c.BUTTON_PRIMARY,
            darkcolor=c.BUTTON_PRIMARY,
            focuscolor="none",
        )

        style.map(
            "Primary.TButton",
            background=[("active", c.BUTTON_PRIMARY_HOVER), ("pressed", c.ACCENT_BLUE)],
        )

    def _initialize_variables(self) -> None:
        """Initialize all tkinter variables used in the application."""
        self.color = tk.StringVar()
        self.x_min = tk.DoubleVar(value=c.DEFAULT_MIN_VALUE)
        self.y_min = tk.DoubleVar(value=c.DEFAULT_MIN_VALUE)
        self.x_max = tk.DoubleVar(value=c.DEFAULT_MAX_VALUE)
        self.y_max = tk.DoubleVar(value=c.DEFAULT_MAX_VALUE)
        self.function = tk.StringVar()

    def _initialize_performance_cache(self) -> None:
        """Initialize performance optimization variables."""
        # Function caching
        self.cached_function_str: Optional[str] = None
        self.cached_parsed_expr: Optional[sp.Expr] = None
        self.cached_lambdified_func: Optional[Callable] = None

        # Data caching for smooth pan/zoom
        self.cached_x_values: Optional[np.ndarray] = None
        self.cached_y_values: Optional[np.ndarray] = None
        self.cached_x_range: Optional[Tuple[float, float]] = None

        # Idle-based redraw scheduling
        self.pending_redraw_id: Optional[str] = None

        # Plot elements for efficient updates
        self.plot_line = None
        self.axes = None

    def _create_ui_components(self) -> None:
        """Create and arrange all modern UI components."""
        ui_components.create_main_layout(self)
        ui_components.create_header(self)
        ui_components.create_plot_area(self)
        ui_components.create_modern_control_panel(self)

    def _reset_view(self) -> None:
        view_manager.reset_view(self)

    def _clear_plot(self) -> None:
        view_manager.clear_plot(self)

    def _clear_data_cache(self) -> None:
        """Clear the cached plot data."""
        plot_manager.clear_data_cache(self)

    def plot(self) -> None:
        plot_manager.plot(self)

    def move_up(self) -> None:
        view_manager.move_up(self)

    def move_down(self) -> None:
        view_manager.move_down(self)

    def move_left(self) -> None:
        view_manager.move_left(self)

    def move_right(self) -> None:
        view_manager.move_right(self)

    def zoom_in(self) -> None:
        view_manager.zoom_in(self)

    def zoom_out(self) -> None:
        view_manager.zoom_out(self)

    def run(self) -> None:
        """Start the main application loop."""
        self.window.mainloop()


def main() -> None:
    """Main entry point for the application."""
    app = GraphingCalculator()
    app.run()


if __name__ == "__main__":
    main()
