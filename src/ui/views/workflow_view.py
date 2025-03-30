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
        self.canvas.bind("<Button-3>", self._on_canvas_right_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)
        self.canvas.bind("<MouseWheel>", self._on_canvas_scroll)  # Windows/macOS
        self.canvas.bind("<Button-4>", self._on_canvas_scroll)  # Linux scroll up
        self.canvas.bind("<Button-5>", self._on_canvas_scroll)  # Linux scroll down
        
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
        self.canvas_offset = (0, 0)
        
        # Draw grid lines
        self._draw_grid()
    
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
        
        # Create buttons for each node type
        for i, node_type in enumerate(node_types):
            button = ctk.CTkButton(
                self.node_buttons_frame,
                text=node_type["name"],
                command=lambda t=node_type["type"]: self._on_node_type_selected(t)
            )
            button.grid(row=i, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
            
            # Add tooltip
            tooltip = ctk.CTkLabel(
                self.node_buttons_frame,
                text=node_type["description"],
                font=get_small_font(),
                text_color="gray",
                wraplength=140
            )
            tooltip.grid(row=i+1, column=0, sticky="w", padx=PAD_X_INNER, pady=(0, PAD_Y_INNER))
            
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
    
    def draw_connection(self, connection: Any):
        """
        Draw a connection on the canvas.
        
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
        control1_x, control1_y = source_x, source_y + 50
        control2_x, control2_y = target_x, target_y - 50
        
        # Draw connection line
        line = self.canvas.create_line(
            source_x, source_y, control1_x, control1_y, control2_x, control2_y, target_x, target_y,
            fill="#FFFFFF", width=2, smooth=True, splinesteps=20,
            tags=(f"connection_{connection.id}",)
        )
        
        # Draw arrow
        arrow_size = 8
        arrow = self.canvas.create_polygon(
            target_x - arrow_size, target_y - arrow_size,
            target_x, target_y,
            target_x - arrow_size, target_y + arrow_size,
            fill="#FFFFFF", outline="#FFFFFF",
            tags=(f"connection_{connection.id}", "arrow")
        )
        
        # Store connection elements
        self.connection_elements[connection.id] = line
        
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
    
    def _on_canvas_drag(self, event):
        """Handle canvas drag."""
        # Pan the canvas
        pass
    
    def _on_canvas_release(self, event):
        """Handle canvas release."""
        # End pan or connection creation
        pass
    
    def _on_canvas_scroll(self, event):
        """Handle canvas scroll."""
        # Zoom the canvas
        pass
    
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
    
    def _on_node_release(self, event):
        """Handle node release."""
        # End node drag
        pass
    
    def _on_connection_click(self, event):
        """Handle connection click."""
        # Get the clicked connection
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)
        
        for tag in tags:
            if tag.startswith("connection_"):
                conn_id = tag[11:]  # Remove "connection_" prefix
                
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
    
    # === Helper Methods ===
    
    def _draw_grid(self):
        """Draw grid lines on the canvas."""
        # Grid spacing
        spacing = 20
        width = int(self.canvas.cget("width"))
        height = int(self.canvas.cget("height"))
        
        # Draw vertical lines
        for x in range(0, width + 1, spacing):
            self.canvas.create_line(x, 0, x, height, fill="#444444", tags="grid")
        
        # Draw horizontal lines
        for y in range(0, height + 1, spacing):
            self.canvas.create_line(0, y, width, y, fill="#444444", tags="grid")
