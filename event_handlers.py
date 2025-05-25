"""
Event Handlers for the Tkinter Graphing Calculator

This module contains functions for handling mouse and scroll events
for panning and zooming the plot.
"""

import constants as c
import plot_manager


def bind_scroll_events(app, canvas) -> None:
    """
    Bind scroll wheel and mouse drag events to the canvas for zooming and panning functionality.

    Args:
        app: The main application instance
        canvas: The matplotlib canvas to bind events to
    """
    canvas_widget = canvas.get_tk_widget()

    # Bind scroll wheel events for both Windows and Linux/Mac
    canvas_widget.bind(
        "<MouseWheel>", lambda event: on_scroll_wheel(app, event)
    )  # Windows
    canvas_widget.bind(
        "<Button-4>", lambda event: on_scroll_wheel(app, event)
    )  # Linux/Mac scroll up
    canvas_widget.bind(
        "<Button-5>", lambda event: on_scroll_wheel(app, event)
    )  # Linux/Mac scroll down

    # Bind mouse drag events for panning
    canvas_widget.bind(
        "<Button-1>", lambda event: on_mouse_press(app, event)
    )  # Left mouse button press
    canvas_widget.bind(
        "<B1-Motion>", lambda event: on_mouse_drag(app, event)
    )  # Mouse drag with left button
    canvas_widget.bind(
        "<ButtonRelease-1>", lambda event: on_mouse_release(app, event)
    )  # Left mouse button release

    # Ensure canvas gets focus when mouse enters for scroll events to work
    canvas_widget.bind("<Enter>", lambda e: canvas_widget.focus_set())

    # Make sure the canvas can receive focus for scroll events
    canvas_widget.focus_set()


def on_scroll_wheel(app, event) -> None:
    """
    Handle scroll wheel events for zooming.

    Args:
        app: The main application instance
        event: The scroll wheel event containing delta and position information
    """
    # Only zoom if we have a function plotted
    if not app.function.get().strip():
        return

    # Determine scroll direction and zoom factor
    # On Windows: event.delta > 0 means scroll up, event.delta < 0 means scroll down
    # On Linux/Mac: event.num == 4 means scroll up, event.num == 5 means scroll down
    # Scroll up should zoom in (make view smaller), scroll down should zoom out (make view larger)
    if event.num == 4 or event.delta > 0:  # Scroll up - zoom in
        zoom_factor = -c.SCROLL_ZOOM_FACTOR  # Negative means zoom in (reduce range)
    elif event.num == 5 or event.delta < 0:  # Scroll down - zoom out
        zoom_factor = c.SCROLL_ZOOM_FACTOR  # Positive means zoom out (increase range)
    else:
        return

    # Get current plot ranges
    x_range = app.x_max.get() - app.x_min.get()
    y_range = app.y_max.get() - app.y_min.get()

    # Calculate zoom amounts
    x_zoom = x_range * zoom_factor
    y_zoom = y_range * zoom_factor

    # Get mouse position relative to the canvas
    canvas_widget = app.canvas.get_tk_widget()
    canvas_width = canvas_widget.winfo_width()
    canvas_height = canvas_widget.winfo_height()

    # Convert mouse position to plot coordinates
    mouse_x_ratio = event.x / canvas_width if canvas_width > 0 else 0.5
    mouse_y_ratio = (
        (canvas_height - event.y) / canvas_height if canvas_height > 0 else 0.5
    )

    # Clamp ratios to [0, 1] range
    mouse_x_ratio = max(0, min(1, mouse_x_ratio))
    mouse_y_ratio = max(0, min(1, mouse_y_ratio))

    # Apply zoom centered on mouse position
    x_zoom_left = x_zoom * mouse_x_ratio
    x_zoom_right = x_zoom * (1 - mouse_x_ratio)
    y_zoom_bottom = y_zoom * mouse_y_ratio
    y_zoom_top = y_zoom * (1 - mouse_y_ratio)

    # Update plot bounds
    new_x_min = app.x_min.get() + x_zoom_left
    new_x_max = app.x_max.get() - x_zoom_right
    new_y_min = app.y_min.get() + y_zoom_bottom
    new_y_max = app.y_max.get() - y_zoom_top

    # Prevent zooming too far in (minimum range of 0.1)
    if (new_x_max - new_x_min) > 0.1 and (new_y_max - new_y_min) > 0.1:
        app.x_min.set(new_x_min)
        app.x_max.set(new_x_max)
        app.y_min.set(new_y_min)
        app.y_max.set(new_y_max)
        plot_manager.throttled_redraw(app)


def on_mouse_press(app, event) -> None:
    """
    Handle mouse button press events to start drag panning.

    Args:
        app: The main application instance
        event: The mouse press event containing position information
    """
    # Only start dragging if we have a function plotted
    if not app.function.get().strip():
        return

    app.is_dragging = True
    app.last_mouse_x = event.x
    app.last_mouse_y = event.y

    # Change cursor to indicate dragging mode
    canvas_widget = app.canvas.get_tk_widget()
    canvas_widget.config(cursor="fleur")


def on_mouse_drag(app, event) -> None:
    """
    Handle mouse drag events to pan the plot view.

    Args:
        app: The main application instance
        event: The mouse motion event containing position information
    """
    if not app.is_dragging or not app.function.get().strip():
        return

    # Calculate mouse movement in pixels
    dx_pixels = event.x - app.last_mouse_x
    dy_pixels = event.y - app.last_mouse_y

    # Get canvas dimensions
    canvas_widget = app.canvas.get_tk_widget()
    canvas_width = canvas_widget.winfo_width()
    canvas_height = canvas_widget.winfo_height()

    if canvas_width <= 0 or canvas_height <= 0:
        return

    # Convert pixel movement to plot coordinate movement
    x_range = app.x_max.get() - app.x_min.get()
    y_range = app.y_max.get() - app.y_min.get()

    # Calculate movement in plot coordinates
    # Note: negative dx_pixels because moving mouse right should move plot left
    # Note: positive dy_pixels because tkinter y increases downward, but plot y increases upward
    dx_plot = -(dx_pixels / canvas_width) * x_range
    dy_plot = (dy_pixels / canvas_height) * y_range

    # Update plot bounds
    app.x_min.set(app.x_min.get() + dx_plot)
    app.x_max.set(app.x_max.get() + dx_plot)
    app.y_min.set(app.y_min.get() + dy_plot)
    app.y_max.set(app.y_max.get() + dy_plot)

    # Update last mouse position
    app.last_mouse_x = event.x
    app.last_mouse_y = event.y

    # Use throttled redraw for smooth panning
    plot_manager.throttled_redraw(app)


def on_mouse_release(app, event) -> None:
    """
    Handle mouse button release events to end drag panning.

    Args:
        app: The main application instance
        event: The mouse release event
    """
    app.is_dragging = False

    # Reset cursor to default
    canvas_widget = app.canvas.get_tk_widget()
    canvas_widget.config(cursor="")

    # Ensure a final smooth redraw after panning ends
    plot_manager.throttled_redraw(app, force=True)
