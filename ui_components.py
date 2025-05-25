"""
UI Components for the Tkinter Graphing Calculator

This module contains functions for creating various UI elements of the calculator.
"""

import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import constants as c
import event_handlers
import view_manager


def create_main_layout(app) -> None:
    """Create the main layout structure."""
    # Main container
    app.main_container = tk.Frame(app.window, bg=c.PRIMARY_BG)
    app.main_container.pack(
        fill="both", expand=True, padx=c.PADDING_LARGE, pady=c.PADDING_LARGE
    )

    # Left panel for plot
    app.left_panel = tk.Frame(app.main_container, bg=c.PRIMARY_BG)
    app.left_panel.pack(
        side="left", fill="both", expand=True, padx=(0, c.PADDING_MEDIUM)
    )

    # Right panel for controls (reduced width for smaller window)
    app.right_panel = tk.Frame(app.main_container, bg=c.CARD_BG, width=280)
    app.right_panel.pack(side="right", fill="y", padx=(c.PADDING_MEDIUM, 0))
    app.right_panel.pack_propagate(False)


def create_header(app) -> None:
    """Create the modern header section."""
    header_frame = tk.Frame(app.left_panel, bg=c.PRIMARY_BG, height=60)
    header_frame.pack(fill="x", pady=(0, c.PADDING_LARGE))
    header_frame.pack_propagate(False)

    # Title
    title_label = tk.Label(
        header_frame,
        text="📊 Modern Graphing Calculator",
        font=c.TITLE_FONT,
        bg=c.PRIMARY_BG,
        fg=c.PRIMARY_TEXT,
    )
    title_label.pack(side="left", pady=c.PADDING_MEDIUM)

    # Subtitle
    subtitle_label = tk.Label(
        header_frame,
        text="Interactive mathematical function plotting",
        font=c.BODY_FONT,
        bg=c.PRIMARY_BG,
        fg=c.SECONDARY_TEXT,
    )
    subtitle_label.pack(side="left", padx=(c.PADDING_MEDIUM, 0), pady=c.PADDING_MEDIUM)


def create_plot_area(app) -> None:
    """Create the modern plot area."""
    # Plot container with subtle border
    app.plot_container = tk.Frame(
        app.left_panel,
        bg=c.CARD_BG,
        relief="flat",
        bd=1,
        highlightbackground=c.BORDER_COLOR,
        highlightthickness=1,
    )
    app.plot_container.pack(fill="both", expand=True)

    # Create matplotlib canvas
    app.canvas = _create_modern_canvas(app)


def _create_modern_canvas(app) -> FigureCanvasTkAgg:
    """
    Create the modern matplotlib canvas for plotting.

    Returns:
        FigureCanvasTkAgg: The matplotlib canvas widget
    """
    # Create figure with modern dark styling (smaller size for compact window)
    figure = Figure(figsize=(6, 4.5), dpi=100, facecolor=c.CARD_BG)
    ax = figure.add_subplot(111, facecolor=c.CARD_BG)

    # Style the plot with modern colors
    import plot_manager
    plot_manager._style_plot_axes(app, ax)

    # Create canvas
    canvas = FigureCanvasTkAgg(figure, app.plot_container)
    canvas.draw()
    canvas.get_tk_widget().pack(
        fill="both", expand=True, padx=c.PADDING_MEDIUM, pady=c.PADDING_MEDIUM
    )

    # Bind scroll wheel events for zooming
    event_handlers.bind_scroll_events(app, canvas)  # Call method from app instance

    return canvas


def create_modern_control_panel(app) -> None:
    """Create the modern control panel with cards and sections."""
    # Scrollable frame for controls
    canvas_frame = tk.Canvas(app.right_panel, bg=c.CARD_BG, highlightthickness=0)
    scrollbar = ttk.Scrollbar(
        app.right_panel, orient="vertical", command=canvas_frame.yview
    )
    app.controls_frame = tk.Frame(canvas_frame, bg=c.CARD_BG)

    app.controls_frame.bind(
        "<Configure>",
        lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all")),
    )

    canvas_frame.create_window((0, 0), window=app.controls_frame, anchor="nw")
    canvas_frame.configure(yscrollcommand=scrollbar.set)

    # Bind mouse wheel to canvas for scrolling
    def _on_mousewheel(event):
        canvas_frame.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bind_to_mousewheel(event):
        canvas_frame.bind_all("<MouseWheel>", _on_mousewheel)

    def _unbind_from_mousewheel(event):
        canvas_frame.unbind_all("<MouseWheel>")

    canvas_frame.bind("<Enter>", _bind_to_mousewheel)
    canvas_frame.bind("<Leave>", _unbind_from_mousewheel)

    canvas_frame.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Create control sections
    _create_function_input_card(app)
    _create_plot_settings_card(app)
    _create_navigation_card(app)
    _create_action_buttons_card(app)
    _create_info_card(app)


def _create_card(app, title: str) -> tk.Frame:
    """Create a modern card container."""
    # Card container
    card_container = tk.Frame(app.controls_frame, bg=c.CARD_BG)
    card_container.pack(fill="x", pady=(0, c.PADDING_SMALL), padx=c.PADDING_SMALL)

    # Card header (more compact)
    header = tk.Frame(card_container, bg=c.SECONDARY_BG, height=30)
    header.pack(fill="x")
    header.pack_propagate(False)

    title_label = tk.Label(
        header, text=title, font=c.HEADING_FONT, bg=c.SECONDARY_BG, fg=c.PRIMARY_TEXT
    )
    title_label.pack(side="left", padx=c.PADDING_SMALL, pady=c.PADDING_SMALL)

    # Card content
    content = tk.Frame(card_container, bg=c.CARD_BG)
    content.pack(fill="x", padx=c.PADDING_SMALL, pady=c.PADDING_SMALL)

    return content


def _create_function_input_card(app) -> None:
    """Create the function input card."""
    card = _create_card(app, "Function Input")

    # Function input with modern styling
    func_label = tk.Label(
        card,
        text="Enter function: y =",
        font=c.BODY_FONT,
        bg=c.CARD_BG,
        fg=c.PRIMARY_TEXT,
    )
    func_label.pack(anchor="w", pady=(0, c.PADDING_SMALL))

    app.function_entry = ttk.Entry(
        card,
        textvariable=app.function,
        font=c.MONO_FONT,
        style="Modern.TEntry",
        width=25,
    )
    app.function_entry.pack(fill="x", pady=(0, c.PADDING_MEDIUM))

    # Example functions
    examples_label = tk.Label(
        card,
        text="Examples: x**2, sin(x), exp(x), log(x), sqrt(x)",
        font=c.SMALL_FONT,
        bg=c.CARD_BG,
        fg=c.SECONDARY_TEXT,
    )
    examples_label.pack(anchor="w")

    # Color selection
    color_label = tk.Label(
        card, text="Plot Color:", font=c.BODY_FONT, bg=c.CARD_BG, fg=c.PRIMARY_TEXT
    )
    color_label.pack(anchor="w", pady=(c.PADDING_MEDIUM, c.PADDING_SMALL))

    # Create color selection with modern combobox
    color_values = [name for _, name in c.PLOT_COLORS]
    app.color_combo = ttk.Combobox(
        card,
        textvariable=app.color,
        values=color_values,
        state="readonly",
        style="Modern.TCombobox",
        width=22,
    )
    app.color_combo.pack(fill="x")
    app.color_combo.set(color_values[0])  # Set default


def _create_plot_settings_card(app) -> None:
    """Create the plot settings card."""
    card = _create_card(app, "Plot Settings")

    # Create a grid for the input fields
    settings_grid = tk.Frame(card, bg=c.CARD_BG)
    settings_grid.pack(fill="x", pady=c.PADDING_SMALL)

    # Configure grid weights
    settings_grid.columnconfigure(1, weight=1)

    # Input fields with modern styling
    fields = [
        ("X min:", app.x_min),
        ("X max:", app.x_max),
        ("Y min:", app.y_min),
        ("Y max:", app.y_max),
    ]

    for i, (label_text, variable) in enumerate(fields):
        label = tk.Label(
            settings_grid,
            text=label_text,
            font=c.BODY_FONT,
            bg=c.CARD_BG,
            fg=c.PRIMARY_TEXT,
            width=8,
        )
        label.grid(row=i, column=0, sticky="w", pady=c.PADDING_SMALL)

        entry = ttk.Entry(
            settings_grid, textvariable=variable, style="Modern.TEntry", width=12
        )
        entry.grid(
            row=i,
            column=1,
            sticky="ew",
            padx=(c.PADDING_SMALL, 0),
            pady=c.PADDING_SMALL,
        )


def _create_navigation_card(app) -> None:
    """Create the navigation controls card."""
    card = _create_card(app, "Zoom")

    # Zoom buttons only
    zoom_frame = tk.Frame(card, bg=c.CARD_BG)
    zoom_frame.pack(pady=c.PADDING_SMALL)

    ttk.Button(
        zoom_frame, text="Zoom In (+)", command=app.zoom_in, style="Modern.TButton"
    ).pack(side="left", padx=c.PADDING_SMALL)
    ttk.Button(
        zoom_frame, text="Zoom Out (-)", command=app.zoom_out, style="Modern.TButton"
    ).pack(side="left", padx=c.PADDING_SMALL)


def _create_action_buttons_card(app) -> None:
    """Create the action buttons card."""
    card = _create_card(app, "Actions")

    # Main plot button
    plot_button = ttk.Button(
        card, text="PLOT", command=app.plot, style="Primary.TButton"
    )
    plot_button.pack(fill="x", pady=c.PADDING_SMALL)

    # Quick action buttons
    actions_frame = tk.Frame(card, bg=c.CARD_BG)
    actions_frame.pack(fill="x", pady=c.PADDING_SMALL)

    reset_button = ttk.Button(
        actions_frame,
        text="Reset",
        command=lambda: view_manager.reset_view(
            app
        ),  # Assuming _reset_view is a method of app
        style="Modern.TButton",
    )
    reset_button.pack(side="left", fill="x", expand=True, padx=(0, c.PADDING_SMALL))

    clear_button = ttk.Button(
        actions_frame,
        text="Clear",
        command=lambda: view_manager.clear_plot(
            app
        ),  # Assuming _clear_plot is a method of app
        style="Modern.TButton",
    )
    clear_button.pack(side="right", fill="x", expand=True)


def _create_info_card(app) -> None:
    """Create the info card."""
    card = _create_card(app, "Tips")

    tips = [
        "• Scroll wheel: zoom in/out",
        "• Click & drag: pan the view",
        "• Try: sin(x), cos(x), x**2",
        "• Constants: pi, e",
    ]

    for tip in tips:
        tip_label = tk.Label(
            card,
            text=tip,
            font=c.SMALL_FONT,
            bg=c.CARD_BG,
            fg=c.SECONDARY_TEXT,
            justify="left",
        )
        tip_label.pack(anchor="w", pady=1)

    # Copyright
    copyright_label = tk.Label(
        card,
        text="© Oleksandr Herasymov",
        font=c.SMALL_FONT,
        bg=c.CARD_BG,
        fg=c.SECONDARY_TEXT,
    )
    copyright_label.pack(pady=(c.PADDING_SMALL, 0))
