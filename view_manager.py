"""
View Manager for the Tkinter Graphing Calculator

This module contains functions for managing the plot view,
including panning, zooming, resetting, and clearing the plot.
"""

import constants as c
import plot_manager


def move_view(app, dx: float = 0.0, dy: float = 0.0) -> None:
    """
    Move the view by the specified offset and replot.

    Args:
        app: The main application instance
        dx: X-axis offset
        dy: Y-axis offset
    """
    app.x_min.set(app.x_min.get() + dx)
    app.x_max.set(app.x_max.get() + dx)
    app.y_min.set(app.y_min.get() + dy)
    app.y_max.set(app.y_max.get() + dy)
    plot_manager.throttled_redraw(
        app, force=True
    )  # Force immediate redraw for button clicks


def move_up(app) -> None:
    """Move the view up by the movement step."""
    move_view(app, dy=c.MOVEMENT_STEP)


def move_down(app) -> None:
    """Move the view down by the movement step."""
    move_view(app, dy=-c.MOVEMENT_STEP)


def move_left(app) -> None:
    """Move the view left by the movement step."""
    move_view(app, dx=-c.MOVEMENT_STEP)


def move_right(app) -> None:
    """Move the view right by the movement step."""
    move_view(app, dx=c.MOVEMENT_STEP)


def zoom_in(app) -> None:
    """
    Zoom into the plot by reducing the view range.

    Only zooms if the current range is larger than the minimum zoom level.
    Args:
        app: The main application instance
    """
    if app.x_max.get() > c.ZOOM_STEP:  # Ensure x_max is used as in original logic
        current_x_min = app.x_min.get()
        current_x_max = app.x_max.get()
        current_y_min = app.y_min.get()
        current_y_max = app.y_max.get()

        new_x_min = current_x_min + c.ZOOM_STEP
        new_x_max = current_x_max - c.ZOOM_STEP
        new_y_min = current_y_min + c.ZOOM_STEP
        new_y_max = current_y_max - c.ZOOM_STEP

        # Prevent zoom if range becomes too small or inverted
        if (new_x_max - new_x_min) > 0.1 and (new_y_max - new_y_min) > 0.1:
            app.x_min.set(new_x_min)
            app.x_max.set(new_x_max)
            app.y_min.set(new_y_min)
            app.y_max.set(new_y_max)
            plot_manager.throttled_redraw(app, force=True)


def zoom_out(app) -> None:
    """Zoom out of the plot by increasing the view range.
    Args:
        app: The main application instance
    """
    app.x_min.set(app.x_min.get() - c.ZOOM_STEP)
    app.x_max.set(app.x_max.get() + c.ZOOM_STEP)
    app.y_min.set(app.y_min.get() - c.ZOOM_STEP)
    app.y_max.set(app.y_max.get() + c.ZOOM_STEP)
    plot_manager.throttled_redraw(app, force=True)


def reset_view(app) -> None:
    """Reset the view to default values.
    Args:
        app: The main application instance
    """
    app.x_min.set(c.DEFAULT_MIN_VALUE)
    app.x_max.set(c.DEFAULT_MAX_VALUE)
    app.y_min.set(c.DEFAULT_MIN_VALUE)
    app.y_max.set(c.DEFAULT_MAX_VALUE)
    if app.function.get().strip():
        plot_manager.throttled_redraw(app, force=True)


def clear_plot(app) -> None:
    """Clear the current plot.
    Args:
        app: The main application instance
    """
    app.function.set("")
    if hasattr(app, "canvas") and app.canvas:
        app.canvas.figure.clear()
        ax = app.canvas.figure.add_subplot(111, facecolor=c.CARD_BG)
        # Apply consistent styling using the centralized function
        plot_manager._style_plot_axes(app, ax)
        app.canvas.draw()
