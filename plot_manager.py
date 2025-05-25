"""
Plot Manager for the Tkinter Graphing Calculator

This module handles the logic for plotting mathematical functions,
including parsing, evaluation, caching, and drawing on the canvas.
"""

import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from sympy.core.sympify import SympifyError
import warnings
from tkinter import messagebox
from typing import Callable, Tuple
import constants as c


def _style_plot_axes(app, ax) -> None:
    """Apply modern styling to plot axes."""
    ax.spines["bottom"].set_color(c.BORDER_COLOR)
    ax.spines["top"].set_color(c.BORDER_COLOR)
    ax.spines["left"].set_color(c.BORDER_COLOR)
    ax.spines["right"].set_color(c.BORDER_COLOR)
    ax.tick_params(colors=c.SECONDARY_TEXT, which="both")
    ax.xaxis.label.set_color(c.PRIMARY_TEXT)
    ax.yaxis.label.set_color(c.PRIMARY_TEXT)
    ax.grid(True, alpha=0.2, color=c.BORDER_COLOR)


def get_cached_function(app, expression: str) -> Callable:
    """
    Get a cached lambdified function for the given expression.

    Args:
        app: The main application instance
        expression: Mathematical expression string

    Returns:
        Callable: Lambdified function for evaluation

    Raises:
        ValueError: If the expression is invalid
    """
    # Check if we can use cached function
    if app.cached_function_str == expression and app.cached_lambdified_func is not None:
        return app.cached_lambdified_func

    try:
        # Parse and cache the new expression
        x_symbol = sp.Symbol("x")
        parsed_expr = parse_expr(expression, transformations="all")
        lambdified_func = sp.lambdify(x_symbol, parsed_expr, "numpy")

        # Update cache
        app.cached_function_str = expression
        app.cached_parsed_expr = parsed_expr
        app.cached_lambdified_func = lambdified_func

        # Clear data cache when function changes
        clear_data_cache(app)

        return lambdified_func

    except (SympifyError, TypeError, ValueError, AttributeError) as e:
        raise ValueError(f"Invalid mathematical expression: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {str(e)}")


def safe_function_evaluation(app, func: Callable, x_values: np.ndarray) -> np.ndarray:
    """
    Safely evaluate a function with proper domain handling.

    This method suppresses NumPy warnings for invalid operations (like sqrt of negative numbers)
    and replaces invalid results with NaN values for proper plotting.

    Args:
        app: The main application instance
        func: The lambdified function to evaluate
        x_values: Array of x values to evaluate the function at

    Returns:
        np.ndarray: Array of y values with invalid values replaced by NaN
    """
    # Suppress NumPy warnings during function evaluation
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)

        try:
            # Evaluate the function
            y_values = func(x_values)

            # Handle complex results by taking only the real part
            if np.iscomplexobj(y_values):
                # For complex results, take real part and set imaginary parts to NaN
                real_parts = np.real(y_values)
                imaginary_parts = np.imag(y_values)

                # If imaginary part is significant, mark as invalid
                significant_imaginary = np.abs(imaginary_parts) > 1e-10
                real_parts[significant_imaginary] = np.nan
                y_values = real_parts

            # Replace infinite values with NaN for better plotting
            y_values = np.where(np.isinf(y_values), np.nan, y_values)

            # Ensure we have a numpy array
            if not isinstance(y_values, np.ndarray):
                y_values = np.array(y_values, dtype=float)

            return y_values

        except Exception:
            # If evaluation fails completely, return array of NaN values
            return np.full_like(x_values, np.nan, dtype=float)


def clear_data_cache(app) -> None:
    """Clear the cached plot data."""
    app.cached_x_values = None
    app.cached_y_values = None
    app.cached_x_range = None


def apply_domain_restrictions(
    app, expression: str, x_min: float, x_max: float
) -> Tuple[float, float]:
    """
    Apply domain restrictions for functions with limited domains.

    Args:
        app: The main application instance
        expression: The mathematical expression string
        x_min: Original minimum x value
        x_max: Original maximum x value

    Returns:
        Tuple of (adjusted_x_min, adjusted_x_max) respecting function domain
    """
    # Convert expression to lowercase for easier matching
    expr_lower = expression.lower().replace(" ", "")

    # Domain restrictions for common functions
    if "log(" in expr_lower or "ln(" in expr_lower:
        # log(x) and ln(x) are only defined for x > 0
        # Use a small positive value to avoid log(0)
        x_min = max(x_min, 1e-10)

    elif "sqrt(" in expr_lower:
        # sqrt(x) is only defined for x >= 0
        x_min = max(x_min, 0.0)

    elif "asin(" in expr_lower or "acos(" in expr_lower:
        # arcsin(x) and arccos(x) are only defined for -1 <= x <= 1
        x_min = max(x_min, -1.0)
        x_max = min(x_max, 1.0)

    elif "atan(" in expr_lower:
        # arctan(x) is defined for all real x, no restrictions needed
        pass

    elif "1/x" in expr_lower or "/x" in expr_lower:
        # Functions with 1/x have discontinuity at x=0
        # We'll handle this in the evaluation, no domain restriction here
        pass

    # Handle more complex cases with multiple functions
    if ("log(" in expr_lower or "ln(" in expr_lower) and "sqrt(" in expr_lower:
        # Both log and sqrt restrictions apply
        x_min = max(x_min, 1e-10)  # More restrictive of the two

    # Ensure we still have a valid range
    if x_min >= x_max:
        # If domain restrictions make the range invalid, use a small positive range
        if "log(" in expr_lower or "ln(" in expr_lower:
            x_min = 1e-10
            x_max = max(10.0, x_max)
        elif "sqrt(" in expr_lower:
            x_min = 0.0
            x_max = max(10.0, x_max)
        elif "asin(" in expr_lower or "acos(" in expr_lower:
            x_min = -1.0
            x_max = 1.0
        else:
            x_min = 0.0
            x_max = max(1.0, x_max)

    return x_min, x_max


def decimate(
    app, x: np.ndarray, y: np.ndarray, width_px: int
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Return one sample per screen pixel (≈ Nyquist for a line plot).

    Args:
        app: The main application instance
        x: X-axis values
        y: Y-axis values
        width_px: Width of the plot area in pixels

    Returns:
        Tuple of decimated (x, y) arrays
    """
    if len(x) <= width_px:
        return x, y  # already light
    step = max(1, len(x) // width_px)  # keep ≈ width_px points
    return x[::step], y[::step]


def filter_and_process_data(
    app, x_values: np.ndarray, y_values: np.ndarray, 
    x_min_val: float, x_max_val: float, use_padding: bool = False
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Filter data to current view, remove NaN values, and decimate for optimal plotting.
    
    This function consolidates the common data processing logic used in both
    update_plot_optimized and update_plot functions.
    
    Args:
        app: The main application instance
        x_values: X-axis values
        y_values: Y-axis values
        x_min_val: Minimum x value for current view
        x_max_val: Maximum x value for current view
        use_padding: Whether to add padding to the view range for smoother edges
        
    Returns:
        Tuple of (filtered_x, filtered_y) arrays ready for plotting
    """
    if len(x_values) == 0:
        return np.array([]), np.array([])
    
    # Calculate view range with optional padding
    if use_padding:
        padding = (x_max_val - x_min_val) * 0.1
        data_x_min, data_x_max = x_values[0], x_values[-1]
        view_x_min = max(x_min_val - padding, data_x_min)
        view_x_max = min(x_max_val + padding, data_x_max)
    else:
        # Direct intersection of available data and current view
        data_x_min, data_x_max = x_values[0], x_values[-1]
        view_x_min = max(x_min_val, data_x_min)
        view_x_max = min(x_max_val, data_x_max)
    
    # Create mask for data within view range
    mask = (x_values >= view_x_min) & (x_values <= view_x_max)
    
    if not np.any(mask):
        return np.array([]), np.array([])
    
    # Filter data to view range
    filtered_x = x_values[mask]
    filtered_y = y_values[mask]
    
    # Remove NaN values for cleaner plotting
    valid_mask = ~np.isnan(filtered_y)
    if not np.any(valid_mask):
        return np.array([]), np.array([])
    
    filtered_x = filtered_x[valid_mask]
    filtered_y = filtered_y[valid_mask]
    
    # Get canvas width in pixels for decimation
    canvas_widget = app.canvas.get_tk_widget()
    canvas_width = canvas_widget.winfo_width()
    
    # Decimate data to match screen pixels for optimal performance
    if canvas_width > 0:
        filtered_x, filtered_y = decimate(app, filtered_x, filtered_y, canvas_width)
    
    return filtered_x, filtered_y


def get_cached_data(app, x_min: float, x_max: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Get cached plot data or compute new data with extended range for smooth zooming.

    Args:
        app: The main application instance
        x_min: Minimum x value for current view
        x_max: Maximum x value for current view

    Returns:
        Tuple of (x_values, y_values) arrays
    """
    current_range = x_max - x_min

    # Calculate extended range for caching (for smooth zoom operations)
    cache_extension = max(current_range * c.CACHE_RESOLUTION_FACTOR, c.MIN_CACHE_RANGE)
    cache_x_min = x_min - cache_extension
    cache_x_max = x_max + cache_extension

    # Check if we can use cached data
    if (
        app.cached_x_values is not None
        and app.cached_y_values is not None
        and app.cached_x_range is not None
    ):
        cached_min, cached_max = app.cached_x_range

        # Use cache if current view is within cached range
        if cached_min <= cache_x_min and cached_max >= cache_x_max:
            return app.cached_x_values, app.cached_y_values

    # Compute new data with extended range
    try:
        func = get_cached_function(app, app.function.get())

        # Use adaptive resolution based on zoom level
        resolution = min(c.PLOT_RESOLUTION, current_range / 1000)

        # Apply domain restrictions for common functions
        adjusted_x_min, adjusted_x_max = apply_domain_restrictions(
            app, app.function.get(), cache_x_min, cache_x_max
        )

        x_values = np.arange(adjusted_x_min, adjusted_x_max + resolution, resolution)
        y_values = safe_function_evaluation(app, func, x_values)

        # Cache the computed data
        app.cached_x_values = x_values
        app.cached_y_values = y_values
        app.cached_x_range = (cache_x_min, cache_x_max)

        return x_values, y_values

    except Exception as e:
        raise ValueError(f"Error computing function values: {str(e)}")


def safe_evaluate_expression(app, expression: str, x_values: np.ndarray) -> np.ndarray:
    """
    Safely evaluate a mathematical expression using sympy.

    Args:
        app: The main application instance
        expression: Mathematical expression string
        x_values: Array of x values to evaluate the expression at

    Returns:
        np.ndarray: Array of y values

    Raises:
        ValueError: If the expression is invalid or contains unsafe operations
    """
    try:
        func = get_cached_function(app, expression)
        return safe_function_evaluation(app, func, x_values)

    except Exception as e:
        raise ValueError(f"Error evaluating expression: {str(e)}")


def schedule_redraw(app) -> None:
    """
    Schedule a redraw using Tk's idle loop for optimal performance.

    This approach eliminates timer overhead by drawing whenever the event queue clears,
    providing smooth performance without wasting CPU on cancelled timeouts.
    Args:
        app: The main application instance
    """
    if not app.pending_redraw_id:
        app.pending_redraw_id = app.window.after_idle(lambda: perform_plot_update(app))


def throttled_redraw(app, force: bool = False) -> None:
    """
    Throttle redraws to maintain smooth performance during rapid pan/zoom operations.

    Args:
        app: The main application instance
        force: If True, bypass throttling and redraw immediately
    """
    if force:
        # Cancel any pending redraw and perform immediate redraw
        if app.pending_redraw_id:
            app.window.after_cancel(app.pending_redraw_id)
            app.pending_redraw_id = None
        perform_plot_update(app)
    else:
        # Use idle-based scheduling for optimal performance
        schedule_redraw(app)


def perform_plot_update(app) -> None:
    """Perform the actual plot update.
    Args:
        app: The main application instance
    """
    app.pending_redraw_id = None

    func_str = app.function.get()
    if not func_str.strip():
        return

    try:
        # Use cached data for smooth performance
        x_values, y_values = get_cached_data(app, app.x_min.get(), app.x_max.get())
        color_name = app.color.get()
        color_hex = get_color_hex(app, color_name)

        update_plot_optimized(app, x_values, y_values, color_hex)

    except Exception:
        # Fallback to full plot method on error
        plot(app)


def plot(app) -> None:
    """
    Plot the mathematical function on the canvas.

    Safely evaluates the function string using sympy and plots it using matplotlib.
    Shows error message if plotting fails.
    Args:
        app: The main application instance
    """
    color_name = app.color.get()
    func_str = app.function.get()

    if not func_str.strip():
        messagebox.showerror("Error", "Please enter a function to plot")
        return

    # Get actual color hex value from color name
    color_hex = get_color_hex(app, color_name)

    try:
        # Clear cache to ensure fresh computation for new plots
        clear_data_cache(app)

        # Use cached data computation for consistency
        x_values, y_values = get_cached_data(app, app.x_min.get(), app.x_max.get())

        update_plot(app, x_values, y_values, color_hex)

    except ValueError as e:
        messagebox.showerror(
            "Expression Error",
            f"Invalid mathematical expression:\n{str(e)}\n\n"
            "Please use standard mathematical notation.\n"
            "Examples: x**2, sin(x), exp(x), log(x)",
        )
    except Exception as e:
        messagebox.showerror(
            "Error",
            "An error occurred while plotting\n"
            "Please check the limits and the function\n"
            f"Details: {str(e)}",
        )


def get_color_hex(app, color_name: str) -> str:
    """Get hex color value from color name.
    Args:
        app: The main application instance
        color_name: The name of the color to get the hex for.
    """
    for hex_color, name in c.PLOT_COLORS:
        if name == color_name:
            return hex_color
    return c.PLOT_COLORS[0][0]  # Default to first color


def update_plot_optimized(
    app, x_values: np.ndarray, y_values: np.ndarray, color: str
) -> None:
    """
    Optimized plot update that reuses existing plot elements for better performance.

    Args:
        app: The main application instance
        x_values: X-axis values
        y_values: Y-axis values
        color: Plot line color
    """
    if app.axes is None or app.plot_line is None:
        # First time setup - create plot elements
        update_plot(app, x_values, y_values, color)
        return

    # Filter data to current view range for performance
    x_min_val, x_max_val = app.x_min.get(), app.x_max.get()
    
    # Use shared filtering logic with padding for smooth edges
    filtered_x, filtered_y = filter_and_process_data(
        app, x_values, y_values, x_min_val, x_max_val, use_padding=True
    )

    # Update existing plot line data
    app.plot_line.set_data(filtered_x, filtered_y)
    app.plot_line.set_color(color)

    # Update axis limits
    app.axes.set_xlim([x_min_val, x_max_val])
    app.axes.set_ylim([app.y_min.get(), app.y_max.get()])

    # Efficient redraw using blit for better performance
    app.canvas.draw_idle()


def update_plot(app, x_values: np.ndarray, y_values: np.ndarray, color: str) -> None:
    """
    Update the matplotlib plot with new data (full recreation).

    Args:
        app: The main application instance
        x_values: X-axis values
        y_values: Y-axis values
        color: Plot line color
    """
    app.canvas.figure.clear()
    app.axes = app.canvas.figure.add_subplot(111, facecolor=c.CARD_BG)

    # Apply modern styling (This assumes _style_plot_axes is a method of app or moved to a shared utility)
    _style_plot_axes(app, app.axes)

    # Set up axis properties
    app.axes.set_xlim([app.x_min.get(), app.x_max.get()])
    app.axes.set_ylim([app.y_min.get(), app.y_max.get()])

    # Modern axis lines
    app.axes.axhline(color=c.BORDER_COLOR, lw=1, alpha=0.8)
    app.axes.axvline(color=c.BORDER_COLOR, lw=1, alpha=0.8)

    # Filter data to current view for initial plot
    x_min_val, x_max_val = app.x_min.get(), app.x_max.get()

    # Use shared filtering logic without padding for direct intersection
    filtered_x, filtered_y = filter_and_process_data(
        app, x_values, y_values, x_min_val, x_max_val, use_padding=False
    )

    # Create plot line with filtered data
    (app.plot_line,) = app.axes.plot(
        filtered_x, filtered_y, color=color, linewidth=2.5, alpha=0.9
    )

    app.canvas.draw()
