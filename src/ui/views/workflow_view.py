"""
Workflow Builder View for creating and editing workflows.
SOLID: Single responsibility - UI for workflow building.
KISS: Simple canvas-based interface with intuitive interactions.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from typing import Dict, List, Any, Optional, Tuple, TYPE_CHECKING
import json
import uuid

from ..views.base_view import BaseView
from ..utils.constants import (
    GRID_ARGS_LABEL, GRID_ARGS_WIDGET, GRID_ARGS_FULL_SPAN_WIDGET,
    PAD_X_OUTER, PAD_Y_OUTER, PAD_X_INNER, PAD_Y_INNER
)
from ..utils.ui_utils import get_header_font, get_default_font, get_small_font

if TYPE_CHECKING:
    from ..presenters.workflow_presenter import WorkflowPresenter

class WorkflowView(BaseView):
    """View for building and editing workflows."""

    # Type hint for the presenter
    presenter: 'WorkflowPresenter'

    def __init__(self, master, **kwargs):
        """Initialize the workflow view."""
        super().__init__(master, **kwargs)
        self.selected_node_id = None  # Currently selected node
        self.selected_node_type = None  # Currently selected node type for adding
        self.node_elements = {}  # Dictionary of node canvas elements
        self.connection_elements = {}  # Dictionary of connection canvas elements
        self.properties_editors = {}  # Dictionary of property editors
        self.canvas_scale = 1.0  # Canvas zoom level
        self.canvas_offset = (0, 0)  # Canvas pan offset
        self.workflow_name_var = tk.StringVar(value="Untitled Workflow")
        self.is_connecting = False  # Flag for connection creation mode
        self.connection_start = None  # Starting node/port for connection
        self.drag_data = {"x": 0, "y": 0, "item": None}  # Data for dragging
        self.is_panning = False  # Flag for canvas panning mode
        self.temp_connection = None  # Temporary connection line during creation
        self.dragged_node_type = None  # Node type being dragged from toolbox

    def _create_widgets(self):
        """Create the UI widgets."""
        # Main layout - split into toolbar, toolbox, canvas, and properties
        self.grid_columnconfigure(0, weight=0)  # Toolbox
        self.grid_columnconfigure(1, weight=1)  # Canvas
        self.grid_columnconfigure(2, weight=0)  # Properties
        self.grid_rowconfigure(0, weight=0)  # Toolbar
        self.grid_rowconfigure(1, weight=1)  # Main content

        # === Toolbar ===
        self.toolbar_frame = ctk.CTkFrame(self)
        self.toolbar_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.toolbar_frame.grid_columnconfigure(0, weight=0)
        self.toolbar_frame.grid_columnconfigure(1, weight=1)
        self.toolbar_frame.grid_columnconfigure(2, weight=0)

        # Workflow name
        self.name_label = ctk.CTkLabel(self.toolbar_frame, text="Workflow Name:", font=get_default_font())
        self.name_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.name_entry = ctk.CTkEntry(self.toolbar_frame, textvariable=self.workflow_name_var, width=200)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Toolbar buttons
        self.toolbar_buttons_frame = ctk.CTkFrame(self.toolbar_frame)
        self.toolbar_buttons_frame.grid(row=0, column=2, sticky="e", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.new_button = ctk.CTkButton(
            self.toolbar_buttons_frame, text="New", width=80, command=self._on_new_clicked
        )
        self.new_button.grid(row=0, column=0, padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.open_button = ctk.CTkButton(
            self.toolbar_buttons_frame, text="Open", width=80, command=self._on_open_clicked
        )
        self.open_button.grid(row=0, column=1, padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.save_button = ctk.CTkButton(
            self.toolbar_buttons_frame, text="Save", width=80, command=self._on_save_clicked
        )
        self.save_button.grid(row=0, column=2, padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.execute_button = ctk.CTkButton(
            self.toolbar_buttons_frame, text="Execute", width=80, command=self._on_execute_clicked
        )
        self.execute_button.grid(row=0, column=3, padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.validate_button = ctk.CTkButton(
            self.toolbar_buttons_frame, text="Validate", width=80, command=self._on_validate_clicked
        )
        self.validate_button.grid(row=0, column=4, padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # === Toolbox ===
        self.toolbox_frame = ctk.CTkFrame(self)
        self.toolbox_frame.grid(row=1, column=0, sticky="ns", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.toolbox_label = ctk.CTkLabel(
            self.toolbox_frame, text="Node Types", font=get_header_font()
        )
        self.toolbox_label.grid(row=0, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.node_buttons_frame = ctk.CTkScrollableFrame(self.toolbox_frame, width=150, height=500)
        self.node_buttons_frame.grid(row=1, column=0, sticky="ns", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.node_buttons = {}  # Will be populated in initialize_toolbox

        # === Canvas ===
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.grid(row=1, column=1, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas_frame.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            self.canvas_frame, bg="#2B2B2B", width=800, height=600,
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Canvas scrollbars
        self.canvas_x_scrollbar = ctk.CTkScrollbar(
            self.canvas_frame, orientation="horizontal", command=self.canvas.xview
        )
        self.canvas_x_scrollbar.grid(row=1, column=0, sticky="ew")

        self.canvas_y_scrollbar = ctk.CTkScrollbar(
            self.canvas_frame, orientation="vertical", command=self.canvas.yview
        )
        self.canvas_y_scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.configure(
            xscrollcommand=self.canvas_x_scrollbar.set,
            yscrollcommand=self.canvas_y_scrollbar.set,
            scrollregion=(0, 0, 1500, 1000)
        )

        # Canvas event bindings
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<Button-2>", self._on_canvas_middle_click)  # Middle button for panning
        self.canvas.bind("<Button-3>", self._on_canvas_right_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<B2-Motion>", self._on_canvas_pan)  # Middle button drag for panning
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)
        self.canvas.bind("<ButtonRelease-2>", self._on_canvas_pan_release)  # Middle button release
        self.canvas.bind("<MouseWheel>", self._on_canvas_scroll)  # Windows/macOS
        self.canvas.bind("<Button-4>", self._on_canvas_scroll)  # Linux scroll up
        self.canvas.bind("<Button-5>", self._on_canvas_scroll)  # Linux scroll down

        # Key bindings for additional controls
        self.canvas.bind("<Control-plus>", self._on_zoom_in)  # Zoom in with Ctrl+Plus
        self.canvas.bind("<Control-minus>", self._on_zoom_out)  # Zoom out with Ctrl+Minus
        self.canvas.bind("<Control-0>", self._on_zoom_reset)  # Reset zoom with Ctrl+0

        # === Properties Panel ===
        self.properties_frame = ctk.CTkFrame(self)
        self.properties_frame.grid(row=1, column=2, sticky="ns", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.properties_label = ctk.CTkLabel(
            self.properties_frame, text="Properties", font=get_header_font()
        )
        self.properties_label.grid(row=0, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.properties_scroll_frame = ctk.CTkScrollableFrame(self.properties_frame, width=250, height=500)
        self.properties_scroll_frame.grid(row=1, column=0, sticky="ns", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Properties buttons
        self.properties_buttons_frame = ctk.CTkFrame(self.properties_frame)
        self.properties_buttons_frame.grid(row=2, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.properties_save_button = ctk.CTkButton(
            self.properties_buttons_frame, text="Apply", command=self._on_properties_save
        )
        self.properties_save_button.grid(row=0, column=0, padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.node_delete_button = ctk.CTkButton(
            self.properties_buttons_frame, text="Delete Node", command=self._on_node_delete
        )
        self.node_delete_button.grid(row=0, column=1, padx=PAD_X_INNER, pady=PAD_Y_INNER)

    def _setup_layout(self):
        """Set up the layout grid."""
        # Main layout already set up in _create_widgets
        pass

    def initialize_canvas(self):
        """Initialize the canvas for workflow editing."""
        # Set up canvas properties
        self.canvas.config(width=800, height=600)
        self.canvas_scale = 1.0
        self._last_scale = 1.0
        self.canvas_offset = (0, 0)

        # Set up scroll region with padding
        self.canvas.configure(scrollregion=(-1000, -1000, 2000, 2000))

        # Draw grid lines
        self._draw_grid()

        # Add zoom controls to the canvas frame
        self.zoom_frame = ctk.CTkFrame(self.canvas_frame)
        self.zoom_frame.grid(row=2, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        self.zoom_in_button = ctk.CTkButton(
            self.zoom_frame, text="+", width=30, command=self._on_zoom_in
        )
        self.zoom_in_button.pack(side="left", padx=PAD_X_INNER)

        self.zoom_reset_button = ctk.CTkButton(
            self.zoom_frame, text="Reset", width=60, command=self._on_zoom_reset
        )
        self.zoom_reset_button.pack(side="left", padx=PAD_X_INNER)

        self.zoom_out_button = ctk.CTkButton(
            self.zoom_frame, text="-", width=30, command=self._on_zoom_out
        )
        self.zoom_out_button.pack(side="left", padx=PAD_X_INNER)

        self.zoom_label = ctk.CTkLabel(
            self.zoom_frame, text="100%", width=50
        )
        self.zoom_label.pack(side="left", padx=PAD_X_INNER)

    def initialize_toolbox(self, node_types: List[Dict[str, Any]]):
        """
        Initialize the toolbox with node types.

        Args:
            node_types: List of node types with metadata
        """
        # Clear existing buttons
        for widget in self.node_buttons_frame.winfo_children():
            widget.destroy()

        self.node_buttons = {}

        # Create draggable buttons for each node type
        for i, node_type in enumerate(node_types):
            # Create a frame to hold the button and make it draggable
            button_frame = ctk.CTkFrame(self.node_buttons_frame, fg_color="transparent")
            button_frame.grid(row=i*2, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

            # Create the button
            button = ctk.CTkButton(
                button_frame,
                text=node_type["name"],
                command=lambda t=node_type["type"]: self._on_node_type_selected(t)
            )
            button.pack(fill="x", expand=True)

            # Make the button draggable
            button.bind("<ButtonPress-1>", lambda event, t=node_type["type"]: self._on_node_button_press(event, t))
            button.bind("<B1-Motion>", self._on_node_button_drag)
            button.bind("<ButtonRelease-1>", self._on_node_button_release)

            # Add tooltip
            tooltip = ctk.CTkLabel(
                self.node_buttons_frame,
                text=node_type["description"],
                font=get_small_font(),
                text_color="gray",
                wraplength=140
            )
            tooltip.grid(row=i*2+1, column=0, sticky="w", padx=PAD_X_INNER, pady=(0, PAD_Y_INNER))

            self.node_buttons[node_type["type"]] = button

    def clear_canvas(self):
        """Clear the canvas."""
        # Delete all canvas items
        self.canvas.delete("all")

        # Reset node and connection elements
        self.node_elements = {}
        self.connection_elements = {}

        # Draw grid lines
        self._draw_grid()

    def redraw_workflow(self, workflow: Optional[Any]):
        """
        Redraw the entire workflow.

        Args:
            workflow: Workflow to draw
        """
        if not workflow:
            return

        # Clear the canvas
        self.clear_canvas()

        # Draw all nodes
        for node_id, node in workflow.nodes.items():
            self.draw_node(node)

        # Draw all connections
        for conn_id, conn in workflow.connections.items():
            self.draw_connection(conn)

    def draw_node(self, node: Any):
        """
        Draw a node on the canvas.

        Args:
            node: Node to draw
        """
        # Node dimensions
        width = 120
        height = 60
        x, y = node.position

        # Node colors based on type
        colors = {
            "Start": "#4CAF50",  # Green
            "End": "#F44336",    # Red
            "Click": "#2196F3",  # Blue
            "Type": "#9C27B0",   # Purple
            "Wait": "#FF9800",   # Orange
            "Condition": "#FFEB3B",  # Yellow
            "Loop": "#795548"    # Brown
        }

        color = colors.get(node.type, "#607D8B")  # Default to gray

        # Draw node body
        body = self.canvas.create_rectangle(
            x - width/2, y - height/2, x + width/2, y + height/2,
            fill=color, outline="#FFFFFF", width=2,
            tags=(f"node_{node.id}", "body")
        )

        # Draw node label
        label = self.canvas.create_text(
            x, y, text=node.label or node.type,
            fill="#FFFFFF", font=("Arial", 12, "bold"),
            tags=(f"node_{node.id}", "label")
        )

        # Draw input port
        input_port = self.canvas.create_oval(
            x - 5, y - height/2 - 5, x + 5, y - height/2 + 5,
            fill="#FFFFFF", outline="#000000",
            tags=(f"node_{node.id}", "input_port")
        )

        # Draw output port
        output_port = self.canvas.create_oval(
            x - 5, y + height/2 - 5, x + 5, y + height/2 + 5,
            fill="#FFFFFF", outline="#000000",
            tags=(f"node_{node.id}", "output_port")
        )

        # Store node elements
        self.node_elements[node.id] = {
            "body": body,
            "label": label,
            "input_port": input_port,
            "output_port": output_port,
            "position": (x, y),
            "width": width,
            "height": height
        }

        # Add event bindings
        self.canvas.tag_bind(f"node_{node.id}", "<Button-1>", self._on_node_click)
        self.canvas.tag_bind(f"node_{node.id}", "<B1-Motion>", self._on_node_drag)
        self.canvas.tag_bind(f"node_{node.id}", "<ButtonRelease-1>", self._on_node_release)

        # Add port event bindings for connection creation
        self.canvas.tag_bind(f"node_{node.id}&&output_port", "<Button-1>", self._on_output_port_click)
        self.canvas.tag_bind(f"node_{node.id}&&input_port", "<Button-1>", self._on_input_port_click)

    def draw_connection(self, connection: Any):
        """
        Draw a connection on the canvas with enhanced visual appearance.

        Args:
            connection: Connection to draw
        """
        # Get source and target nodes
        if connection.source_node_id not in self.node_elements or connection.target_node_id not in self.node_elements:
            return

        source_node = self.node_elements[connection.source_node_id]
        target_node = self.node_elements[connection.target_node_id]

        # Get port positions
        if connection.source_port == "output":
            source_x, source_y = source_node["position"][0], source_node["position"][1] + source_node["height"]/2
        else:
            source_x, source_y = source_node["position"]

        if connection.target_port == "input":
            target_x, target_y = target_node["position"][0], target_node["position"][1] - target_node["height"]/2
        else:
            target_x, target_y = target_node["position"]

        # Calculate control points for bezier curve
        # Make the curve more pronounced for better visual appearance
        control1_x, control1_y = source_x, source_y + 80
        control2_x, control2_y = target_x, target_y - 80

        # Draw connection line with enhanced appearance
        line = self.canvas.create_line(
            source_x, source_y, control1_x, control1_y, control2_x, control2_y, target_x, target_y,
            fill="#4FC3F7", width=3, smooth=True, splinesteps=36,  # More steps for smoother curve
            tags=(f"connection_{connection.id}", "connection")
        )

        # Draw source point (small circle at the start of the connection)
        source_point = self.canvas.create_oval(
            source_x - 4, source_y - 4, source_x + 4, source_y + 4,
            fill="#4FC3F7", outline="#FFFFFF",
            tags=(f"connection_{connection.id}", "connection")
        )

        # Draw arrow at the target end
        arrow_size = 10
        arrow = self.canvas.create_polygon(
            target_x - arrow_size, target_y - arrow_size/2,
            target_x, target_y,
            target_x - arrow_size, target_y + arrow_size/2,
            fill="#4FC3F7", outline="#FFFFFF",
            tags=(f"connection_{connection.id}", "connection", "arrow")
        )

        # Store connection elements in a dictionary for easier management
        self.connection_elements[connection.id] = {
            "line": line,
            "source_point": source_point,
            "arrow": arrow
        }

        # Add event bindings
        self.canvas.tag_bind(f"connection_{connection.id}", "<Button-1>", self._on_connection_click)

    def select_node_visual(self, node_id: Optional[str]):
        """
        Visually select a node on the canvas.

        Args:
            node_id: ID of the node to select, or None to deselect
        """
        # Reset all node highlights
        for nid, elements in self.node_elements.items():
            self.canvas.itemconfig(elements["body"], width=2)

        # Highlight the selected node
        if node_id and node_id in self.node_elements:
            self.canvas.itemconfig(self.node_elements[node_id]["body"], width=4)
            self.selected_node_id = node_id
        else:
            self.selected_node_id = None

    def display_properties_for_node(self, node_data: Optional[Any]):
        """
        Display properties for a node in the properties panel.

        Args:
            node_data: Node data to display
        """
        # Clear existing property editors
        for widget in self.properties_scroll_frame.winfo_children():
            widget.destroy()

        self.properties_editors = {}

        if not node_data:
            return

        # Display node type
        type_label = ctk.CTkLabel(
            self.properties_scroll_frame, text=f"Type: {node_data.type}",
            font=get_default_font()
        )
        type_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        # Display node ID
        id_label = ctk.CTkLabel(
            self.properties_scroll_frame, text=f"ID: {node_data.id}",
            font=get_small_font(), text_color="gray"
        )
        id_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=PAD_X_INNER, pady=(0, PAD_Y_INNER))

        # Display node label editor
        label_label = ctk.CTkLabel(
            self.properties_scroll_frame, text="Label:",
            font=get_default_font()
        )
        label_label.grid(row=2, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

        label_entry = ctk.CTkEntry(self.properties_scroll_frame)
        label_entry.grid(row=2, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        label_entry.insert(0, node_data.label or "")
        self.properties_editors["label"] = label_entry

        # Display node properties
        row = 3
        for prop_name, prop_value in node_data.properties.items():
            prop_label = ctk.CTkLabel(
                self.properties_scroll_frame, text=f"{prop_name.replace('_', ' ').title()}:",
                font=get_default_font()
            )
            prop_label.grid(row=row, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

            prop_entry = ctk.CTkEntry(self.properties_scroll_frame)
            prop_entry.grid(row=row, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
            prop_entry.insert(0, str(prop_value))
            self.properties_editors[prop_name] = prop_entry

            row += 1

        # Add property button
        add_prop_button = ctk.CTkButton(
            self.properties_scroll_frame, text="Add Property",
            command=self._on_add_property
        )
        add_prop_button.grid(row=row, column=0, columnspan=2, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)

    def get_properties_data(self) -> Optional[Dict]:
        """
        Get the data from the properties panel.

        Returns:
            Dictionary containing the property data
        """
        if not self.properties_editors:
            return None

        data = {}

        for prop_name, editor in self.properties_editors.items():
            data[prop_name] = editor.get()

        return data

    def get_workflow_name(self) -> str:
        """
        Get the workflow name.

        Returns:
            Workflow name
        """
        return self.workflow_name_var.get()

    # === Event Handlers ===

    def _on_new_clicked(self):
        """Handle new button click."""
        name = simpledialog.askstring("New Workflow", "Enter workflow name:")
        if name:
            if self.presenter:
                self.presenter.create_new_workflow(name)

    def _on_open_clicked(self):
        """Handle open button click."""
        workflow_id = filedialog.askopenfilename(
            title="Open Workflow",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if workflow_id and self.presenter:
            self.presenter.load_workflow(workflow_id)

    def _on_save_clicked(self):
        """Handle save button click."""
        if self.presenter:
            self.presenter.save_workflow()

    def _on_execute_clicked(self):
        """Handle execute button click."""
        if self.presenter:
            result = self.presenter.execute_workflow()

            if result["success"]:
                messagebox.showinfo("Execution Result", "Workflow executed successfully!")
            else:
                messagebox.showerror("Execution Error", f"Workflow execution failed: {result['message']}")

    def _on_validate_clicked(self):
        """Handle validate button click."""
        if self.presenter:
            result = self.presenter.validate_workflow()

            if result["valid"]:
                messagebox.showinfo("Validation Result", "Workflow is valid!")
            else:
                messagebox.showerror("Validation Error", f"Workflow validation failed:\n{chr(10).join(result['errors'])}")

    def _on_canvas_click(self, event):
        """Handle canvas click."""
        if self.selected_node_type:
            # Add a new node
            if self.presenter:
                self.presenter.add_node(self.selected_node_type, (event.x, event.y))
                self.selected_node_type = None  # Reset selection

                # Reset node type buttons
                for button in self.node_buttons.values():
                    button.configure(fg_color=("#3B8ED0", "#1F6AA5"))  # Default color

    def _on_canvas_right_click(self, event):
        """Handle canvas right click."""
        # Show context menu
        pass

    def _on_canvas_middle_click(self, event):
        """Handle canvas middle click for panning."""
        self.is_panning = True
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def _on_canvas_pan(self, event):
        """Handle canvas panning with middle mouse button."""
        if not self.is_panning:
            return

        # Calculate the distance moved
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]

        # Update the canvas offset
        self.canvas_offset = (
            self.canvas_offset[0] + dx,
            self.canvas_offset[1] + dy
        )

        # Move all items on the canvas
        self.canvas.move("all", dx, dy)

        # Update the scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Update the drag data
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def _on_canvas_pan_release(self, event):
        """Handle canvas pan release."""
        self.is_panning = False

    def _on_canvas_drag(self, event):
        """Handle canvas drag."""
        # If we're dragging a node from the toolbox
        if self.dragged_node_type:
            # Update the ghost node position
            if hasattr(self, "ghost_node"):
                # Move the ghost node
                x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
                self.canvas.coords(self.ghost_node, x-50, y-30, x+50, y+30)

        # If we're creating a connection
        elif self.is_connecting and self.connection_start and self.temp_connection:
            # Update the temporary connection line
            self._update_temp_connection(event.x, event.y)

    def _on_canvas_release(self, event):
        """Handle canvas release."""
        # If we're releasing a dragged node from the toolbox
        if self.dragged_node_type:
            # Get the canvas coordinates
            x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)

            # Delete the ghost node
            if hasattr(self, "ghost_node"):
                self.canvas.delete(self.ghost_node)
                delattr(self, "ghost_node")

            # Create a real node at this position
            if self.presenter:
                self.presenter.add_node(self.dragged_node_type, (x, y))

            # Reset the dragged node type
            self.dragged_node_type = None

    def _on_canvas_scroll(self, event):
        """Handle canvas scroll for zooming."""
        # Get the current mouse position
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)

        # Determine the direction of the scroll
        if event.num == 4 or event.delta > 0:  # Scroll up
            self._zoom_in(x, y)
        elif event.num == 5 or event.delta < 0:  # Scroll down
            self._zoom_out(x, y)

    def _on_zoom_in(self, x=None, y=None, event=None):
        """Zoom in on the canvas."""
        if self.canvas_scale < 2.0:  # Limit maximum zoom
            self.canvas_scale *= 1.1
            self._apply_zoom(x, y)

    def _on_zoom_out(self, x=None, y=None, event=None):
        """Zoom out on the canvas."""
        if self.canvas_scale > 0.5:  # Limit minimum zoom
            self.canvas_scale /= 1.1
            self._apply_zoom(x, y)

    def _on_zoom_reset(self, event=None):
        """Reset zoom to default level."""
        self.canvas_scale = 1.0
        self._apply_zoom()

    def _apply_zoom(self, x=None, y=None):
        """Apply the current zoom level to the canvas."""
        # If x and y are provided, zoom around that point
        # Otherwise, zoom around the center of the canvas
        if x is None or y is None:
            x = self.canvas.winfo_width() / 2
            y = self.canvas.winfo_height() / 2

        # Get the current scroll region
        old_region = self.canvas.bbox("all")
        if not old_region:
            return

        # Calculate the scaling factor relative to the previous scale
        old_scale = getattr(self, "_last_scale", 1.0)
        scale_factor = self.canvas_scale / old_scale
        self._last_scale = self.canvas_scale

        # Scale all items on the canvas around the specified point
        self.canvas.scale("all", x, y, scale_factor, scale_factor)

        # Update the scroll region
        new_region = self.canvas.bbox("all")
        if new_region:
            # Adjust the scroll region to ensure it's large enough
            padding = 100  # Add padding around the content
            self.canvas.configure(
                scrollregion=(
                    new_region[0] - padding,
                    new_region[1] - padding,
                    new_region[2] + padding,
                    new_region[3] + padding
                )
            )

        # Update the zoom label and status bar with the current zoom level
        zoom_percentage = int(self.canvas_scale * 100)
        self.zoom_label.configure(text=f"{zoom_percentage}%")

        if self.presenter:
            self.presenter.update_app_status(f"Zoom level: {zoom_percentage}%")

    def _on_node_click(self, event):
        """Handle node click."""
        # Get the clicked node
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)

        for tag in tags:
            if tag.startswith("node_"):
                node_id = tag[5:]  # Remove "node_" prefix
                if self.presenter:
                    self.presenter.select_node(node_id)
                break

    def _on_node_drag(self, event):
        """Handle node drag."""
        # Move the selected node
        if not self.selected_node_id:
            return

        # Get node elements
        elements = self.node_elements.get(self.selected_node_id)
        if not elements:
            return

        # Calculate movement
        old_x, old_y = elements["position"]
        dx = event.x - old_x
        dy = event.y - old_y

        # Move all node elements
        for key, item_id in elements.items():
            if key not in ["position", "width", "height"]:
                self.canvas.move(item_id, dx, dy)

        # Update node position
        elements["position"] = (event.x, event.y)

        # Update connections
        for conn_id, conn in self.presenter.current_workflow.connections.items():
            if conn.source_node_id == self.selected_node_id or conn.target_node_id == self.selected_node_id:
                self.draw_connection(conn)

    def _on_output_port_click(self, event):
        """Handle output port click."""
        # Get the clicked node
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)

        for tag in tags:
            if tag.startswith("node_"):
                node_id = tag[5:]  # Remove "node_" prefix

                # Start connection creation
                self.is_connecting = True
                self.connection_start = {
                    "node_id": node_id,
                    "port": "output"
                }

                # Create a temporary connection line with bezier curve
                source_node = self.node_elements[node_id]
                source_x, source_y = source_node["position"][0], source_node["position"][1] + source_node["height"]/2

                # Calculate control points for bezier curve
                control1_x, control1_y = source_x, source_y + 80
                control2_x, control2_y = event.x, event.y - 80

                self.temp_connection = self.canvas.create_line(
                    source_x, source_y, control1_x, control1_y, control2_x, control2_y, event.x, event.y,
                    fill="#4FC3F7", width=3, smooth=True, splinesteps=36, dash=(6, 4),
                    tags=("temp_connection",)
                )

                # Bind motion and release events for dragging the connection
                self.canvas.bind("<Motion>", self._on_connection_drag)
                self.canvas.bind("<ButtonRelease-1>", self._on_connection_release)

                break

    def _on_input_port_click(self, event):
        """Handle input port click."""
        # Get the clicked node
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)

        for tag in tags:
            if tag.startswith("node_"):
                node_id = tag[5:]  # Remove "node_" prefix

                # Start connection creation
                self.is_connecting = True
                self.connection_start = {
                    "node_id": node_id,
                    "port": "input"
                }

                # Create a temporary connection line with bezier curve
                target_node = self.node_elements[node_id]
                target_x, target_y = target_node["position"][0], target_node["position"][1] - target_node["height"]/2

                # Calculate control points for bezier curve
                control1_x, control1_y = event.x, event.y - 80
                control2_x, control2_y = target_x, target_y + 80

                self.temp_connection = self.canvas.create_line(
                    event.x, event.y, control1_x, control1_y, control2_x, control2_y, target_x, target_y,
                    fill="#4FC3F7", width=3, smooth=True, splinesteps=36, dash=(6, 4),
                    tags=("temp_connection",)
                )

                # Bind motion and release events for dragging the connection
                self.canvas.bind("<Motion>", self._on_connection_drag)
                self.canvas.bind("<ButtonRelease-1>", self._on_connection_release)

                break

    def _on_node_release(self, event):
        """Handle node release."""
        # End node drag
        if self.selected_node_id:
            # Update the node position in the workflow
            if self.presenter and self.presenter.current_workflow:
                node = self.presenter.current_workflow.nodes.get(self.selected_node_id)
                if node:
                    elements = self.node_elements.get(self.selected_node_id)
                    if elements:
                        node.position = elements["position"]

    def _on_node_button_press(self, event, node_type):
        """Handle node button press for dragging from toolbox."""
        # Store the node type being dragged
        self.dragged_node_type = node_type

        # Store the initial position
        self.drag_data["x"] = event.x_root
        self.drag_data["y"] = event.y_root

        # Create a ghost node on the canvas
        # First convert the coordinates to canvas coordinates
        x = self.canvas.winfo_rootx() + 100  # Center of canvas
        y = self.canvas.winfo_rooty() + 100  # Center of canvas

        # Create a ghost rectangle
        self.ghost_node = self.canvas.create_rectangle(
            x-50, y-30, x+50, y+30,
            fill="#607D8B", outline="#FFFFFF", width=2, dash=(4, 4),
            tags=("ghost_node",)
        )

    def _on_node_button_drag(self, event):
        """Handle node button drag from toolbox."""
        if not self.dragged_node_type:
            return

        # Calculate the distance moved
        dx = event.x_root - self.drag_data["x"]
        dy = event.y_root - self.drag_data["y"]

        # Update the ghost node position
        if hasattr(self, "ghost_node"):
            self.canvas.move(self.ghost_node, dx, dy)

        # Update the drag data
        self.drag_data["x"] = event.x_root
        self.drag_data["y"] = event.y_root

    def _on_node_button_release(self, event):
        """Handle node button release after dragging from toolbox."""
        if not self.dragged_node_type:
            return

        # Check if the release is over the canvas
        canvas_x = self.canvas.winfo_rootx()
        canvas_y = self.canvas.winfo_rooty()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if (canvas_x <= event.x_root <= canvas_x + canvas_width and
            canvas_y <= event.y_root <= canvas_y + canvas_height):
            # Convert to canvas coordinates
            x = event.x_root - canvas_x
            y = event.y_root - canvas_y

            # Delete the ghost node
            if hasattr(self, "ghost_node"):
                self.canvas.delete(self.ghost_node)
                delattr(self, "ghost_node")

            # Create a real node at this position
            if self.presenter:
                self.presenter.add_node(self.dragged_node_type, (x, y))
        else:
            # Delete the ghost node if not over canvas
            if hasattr(self, "ghost_node"):
                self.canvas.delete(self.ghost_node)
                delattr(self, "ghost_node")

        # Reset the dragged node type
        self.dragged_node_type = None

    def _on_connection_click(self, event):
        """Handle connection click."""
        # Get the clicked connection
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)

        for tag in tags:
            if tag.startswith("connection_"):
                conn_id = tag[11:]  # Remove "connection_" prefix

                # Highlight the connection when clicked
                for connection_id, elements in self.connection_elements.items():
                    # Reset all connections to normal appearance
                    if isinstance(elements, dict):  # New structure
                        self.canvas.itemconfig(elements["line"], width=3, fill="#4FC3F7")
                        self.canvas.itemconfig(elements["source_point"], fill="#4FC3F7")
                        self.canvas.itemconfig(elements["arrow"], fill="#4FC3F7")
                    else:  # Old structure (single line)
                        self.canvas.itemconfig(elements, width=2, fill="#FFFFFF")

                # Highlight the selected connection
                elements = self.connection_elements.get(conn_id)
                if elements:
                    if isinstance(elements, dict):  # New structure
                        self.canvas.itemconfig(elements["line"], width=4, fill="#FFEB3B")
                        self.canvas.itemconfig(elements["source_point"], fill="#FFEB3B")
                        self.canvas.itemconfig(elements["arrow"], fill="#FFEB3B")
                    else:  # Old structure (single line)
                        self.canvas.itemconfig(elements, width=3, fill="#FFEB3B")

                # Ask for confirmation
                if messagebox.askyesno("Delete Connection", "Delete this connection?"):
                    if self.presenter:
                        self.presenter.delete_connection(conn_id)
                break

    def _on_node_type_selected(self, node_type: str):
        """Handle node type selection."""
        self.selected_node_type = node_type

        # Highlight the selected button
        for type_name, button in self.node_buttons.items():
            if type_name == node_type:
                button.configure(fg_color=("#2E7D32", "#2E7D32"))  # Green
            else:
                button.configure(fg_color=("#3B8ED0", "#1F6AA5"))  # Default color

    def _on_properties_save(self):
        """Handle properties save button click."""
        if self.presenter:
            self.presenter.update_node_properties()

    def _on_node_delete(self):
        """Handle node delete button click."""
        if self.selected_node_id and messagebox.askyesno("Delete Node", "Delete this node?"):
            if self.presenter:
                self.presenter.delete_node()

    def _on_add_property(self):
        """Handle add property button click."""
        prop_name = simpledialog.askstring("Add Property", "Enter property name:")
        if prop_name:
            # Add a new property editor
            row = len(self.properties_editors) + 3  # Offset for type, ID, and label

            prop_label = ctk.CTkLabel(
                self.properties_scroll_frame, text=f"{prop_name.replace('_', ' ').title()}:",
                font=get_default_font()
            )
            prop_label.grid(row=row, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)

            prop_entry = ctk.CTkEntry(self.properties_scroll_frame)
            prop_entry.grid(row=row, column=1, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
            self.properties_editors[prop_name] = prop_entry

    def _on_connection_drag(self, event):
        """Handle connection dragging."""
        if self.is_connecting and self.temp_connection:
            # Update the temporary connection line
            self._update_temp_connection(event.x, event.y)

    def _on_connection_release(self, event):
        """Handle connection release."""
        if self.is_connecting and self.connection_start and self.temp_connection:
            # Get the item under the cursor
            items = self.canvas.find_overlapping(event.x-5, event.y-5, event.x+5, event.y+5)

            # Check if we're over a port
            target_node_id = None
            target_port = None

            for item in items:
                tags = self.canvas.gettags(item)

                # Check for input or output port
                if "input_port" in tags or "output_port" in tags:
                    for tag in tags:
                        if tag.startswith("node_"):
                            target_node_id = tag[5:]  # Remove "node_" prefix
                            target_port = "input" if "input_port" in tags else "output"
                            break
                    if target_node_id:
                        break

            # If we found a target node and it's a valid connection
            if target_node_id and self.connection_start["node_id"] != target_node_id:
                # Determine source and target based on port types
                if self.connection_start["port"] == "output" and target_port == "input":
                    # Normal flow: output -> input
                    source_id = self.connection_start["node_id"]
                    source_port = self.connection_start["port"]
                    target_id = target_node_id
                    target_port = target_port
                    valid = True
                elif self.connection_start["port"] == "input" and target_port == "output":
                    # Reverse flow: input <- output
                    source_id = target_node_id
                    source_port = target_port
                    target_id = self.connection_start["node_id"]
                    target_port = self.connection_start["port"]
                    valid = True
                else:
                    # Invalid connection: input -> input or output -> output
                    valid = False

                # Create the connection if valid
                if valid and self.presenter:
                    self.presenter.add_connection(
                        source_id,
                        source_port,
                        target_id,
                        target_port
                    )

            # Delete the temporary connection
            self.canvas.delete(self.temp_connection)
            self.temp_connection = None

            # Reset connection state
            self.is_connecting = False
            self.connection_start = None

            # Unbind motion and release events
            self.canvas.unbind("<Motion>")
            self.canvas.unbind("<ButtonRelease-1>")

    def _update_temp_connection(self, mouse_x, mouse_y):
        """Update the temporary connection line with enhanced visual appearance."""
        if not self.temp_connection or not self.connection_start:
            return

        node_id = self.connection_start["node_id"]
        port = self.connection_start["port"]

        if node_id not in self.node_elements:
            return

        node = self.node_elements[node_id]

        if port == "output":
            # Connection starts at output port
            start_x, start_y = node["position"][0], node["position"][1] + node["height"]/2
            end_x, end_y = mouse_x, mouse_y
        else:
            # Connection starts at input port
            start_x, start_y = mouse_x, mouse_y
            end_x, end_y = node["position"][0], node["position"][1] - node["height"]/2

        # Calculate control points for bezier curve with more pronounced curve
        if port == "output":
            control1_x, control1_y = start_x, start_y + 80
            control2_x, control2_y = end_x, end_y - 80
        else:
            control1_x, control1_y = start_x, start_y - 80
            control2_x, control2_y = end_x, end_y + 80

        # Update the temporary connection line
        self.canvas.coords(
            self.temp_connection,
            start_x, start_y, control1_x, control1_y, control2_x, control2_y, end_x, end_y
        )

        # Update the appearance of the temporary connection
        self.canvas.itemconfig(
            self.temp_connection,
            fill="#4FC3F7",  # Light blue color
            width=3,        # Thicker line
            dash=(6, 4)     # Dashed line pattern
        )

    # === Helper Methods ===

    def _draw_grid(self):
        """Draw grid lines on the canvas."""
        # Grid spacing
        spacing = 20
        width = int(self.canvas.cget("width")) * 2  # Extend grid beyond visible area
        height = int(self.canvas.cget("height")) * 2

        # Get the scroll region
        scroll_region = self.canvas.cget("scrollregion")
        if scroll_region:
            try:
                # Parse the scroll region string
                x1, y1, x2, y2 = map(int, scroll_region.split())
                width = max(width, x2 - x1)
                height = max(height, y2 - y1)
            except (ValueError, AttributeError):
                pass

        # Draw vertical lines
        for x in range(-width, width + 1, spacing):
            self.canvas.create_line(x, -height, x, height, fill="#444444", tags="grid")

        # Draw horizontal lines
        for y in range(-height, height + 1, spacing):
            self.canvas.create_line(-width, y, width, y, fill="#444444", tags="grid")
