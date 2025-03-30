"""
Action Execution View for monitoring and controlling workflow execution.
SOLID: Single responsibility - UI for action execution.
KISS: Simple interface with intuitive controls.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Dict, List, Any, Optional, Tuple, TYPE_CHECKING
import json
import csv
from datetime import datetime

from ..views.base_view import BaseView
from ..utils.constants import (
    GRID_ARGS_LABEL, GRID_ARGS_WIDGET, GRID_ARGS_FULL_SPAN_WIDGET,
    PAD_X_OUTER, PAD_Y_OUTER, PAD_X_INNER, PAD_Y_INNER
)
from ..utils.ui_utils import get_header_font, get_default_font, get_small_font

if TYPE_CHECKING:
    from ..presenters.action_execution_presenter import ActionExecutionPresenter

class ActionExecutionView(BaseView):
    """View for monitoring and controlling workflow execution."""
    
    # Type hint for the presenter
    presenter: 'ActionExecutionPresenter'
    
    def __init__(self, master, **kwargs):
        """Initialize the action execution view."""
        super().__init__(master, **kwargs)
        self.selected_workflow_id = None
        self.execution_results = []
    
    def _create_widgets(self):
        """Create the UI widgets."""
        # Main layout - split into workflow selection, execution controls, and results
        self.grid_columnconfigure(0, weight=0)  # Workflow selection
        self.grid_columnconfigure(1, weight=1)  # Execution area
        self.grid_rowconfigure(0, weight=1)  # Main content
        
        # === Workflow Selection ===
        self.workflow_frame = ctk.CTkFrame(self)
        self.workflow_frame.grid(row=0, column=0, sticky="ns", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.workflow_label = ctk.CTkLabel(
            self.workflow_frame, text="Available Workflows", font=get_header_font()
        )
        self.workflow_label.grid(row=0, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.workflow_list_frame = ctk.CTkScrollableFrame(self.workflow_frame, width=200, height=400)
        self.workflow_list_frame.grid(row=1, column=0, sticky="ns", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.workflow_buttons = {}  # Will be populated in update_workflow_list
        
        self.refresh_button = ctk.CTkButton(
            self.workflow_frame, text="Refresh", command=self._on_refresh_clicked
        )
        self.refresh_button.grid(row=2, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # === Execution Area ===
        self.execution_frame = ctk.CTkFrame(self)
        self.execution_frame.grid(row=0, column=1, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.execution_frame.grid_columnconfigure(0, weight=1)
        self.execution_frame.grid_rowconfigure(0, weight=0)  # Details
        self.execution_frame.grid_rowconfigure(1, weight=0)  # Controls
        self.execution_frame.grid_rowconfigure(2, weight=0)  # Progress
        self.execution_frame.grid_rowconfigure(3, weight=1)  # Results
        
        # Workflow details
        self.details_frame = ctk.CTkFrame(self.execution_frame)
        self.details_frame.grid(row=0, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.details_frame.grid_columnconfigure(1, weight=1)
        
        self.details_label = ctk.CTkLabel(
            self.details_frame, text="Workflow Details", font=get_header_font()
        )
        self.details_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.name_label = ctk.CTkLabel(
            self.details_frame, text="Name:", font=get_default_font()
        )
        self.name_label.grid(row=1, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.name_value = ctk.CTkLabel(
            self.details_frame, text="", font=get_default_font()
        )
        self.name_value.grid(row=1, column=1, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.id_label = ctk.CTkLabel(
            self.details_frame, text="ID:", font=get_default_font()
        )
        self.id_label.grid(row=2, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.id_value = ctk.CTkLabel(
            self.details_frame, text="", font=get_default_font()
        )
        self.id_value.grid(row=2, column=1, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.nodes_label = ctk.CTkLabel(
            self.details_frame, text="Nodes:", font=get_default_font()
        )
        self.nodes_label.grid(row=3, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.nodes_value = ctk.CTkLabel(
            self.details_frame, text="", font=get_default_font()
        )
        self.nodes_value.grid(row=3, column=1, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Execution controls
        self.controls_frame = ctk.CTkFrame(self.execution_frame)
        self.controls_frame.grid(row=1, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.execute_button = ctk.CTkButton(
            self.controls_frame, text="Execute", command=self._on_execute_clicked, state="disabled"
        )
        self.execute_button.grid(row=0, column=0, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.pause_resume_button = ctk.CTkButton(
            self.controls_frame, text="Pause", command=self._on_pause_resume_clicked, state="disabled"
        )
        self.pause_resume_button.grid(row=0, column=1, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.stop_button = ctk.CTkButton(
            self.controls_frame, text="Stop", command=self._on_stop_clicked, state="disabled"
        )
        self.stop_button.grid(row=0, column=2, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.save_button = ctk.CTkButton(
            self.controls_frame, text="Save Results", command=self._on_save_clicked, state="disabled"
        )
        self.save_button.grid(row=0, column=3, padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        # Progress bar
        self.progress_frame = ctk.CTkFrame(self.execution_frame)
        self.progress_frame.grid(row=2, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame, text="Progress: 0/0", font=get_default_font()
        )
        self.progress_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.grid(row=1, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.progress_bar.set(0)
        
        # Results
        self.results_frame = ctk.CTkFrame(self.execution_frame)
        self.results_frame.grid(row=3, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(1, weight=1)
        
        self.results_label = ctk.CTkLabel(
            self.results_frame, text="Execution Results", font=get_header_font()
        )
        self.results_label.grid(row=0, column=0, sticky="w", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        
        self.results_text = ctk.CTkTextbox(self.results_frame, height=200)
        self.results_text.grid(row=1, column=0, sticky="nsew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
        self.results_text.configure(state="disabled")
    
    def _setup_layout(self):
        """Set up the layout grid."""
        # Main layout already set up in _create_widgets
        pass
    
    def update_workflow_list(self, workflows: List[Any]):
        """
        Update the workflow list.
        
        Args:
            workflows: List of workflows
        """
        # Clear existing buttons
        for widget in self.workflow_list_frame.winfo_children():
            widget.destroy()
        
        self.workflow_buttons = {}
        
        # Create buttons for each workflow
        for i, workflow in enumerate(workflows):
            button = ctk.CTkButton(
                self.workflow_list_frame,
                text=workflow.name,
                command=lambda wid=workflow.id: self._on_workflow_selected(wid)
            )
            button.grid(row=i, column=0, sticky="ew", padx=PAD_X_INNER, pady=PAD_Y_INNER)
            
            self.workflow_buttons[workflow.id] = button
    
    def display_workflow_details(self, workflow: Any):
        """
        Display workflow details.
        
        Args:
            workflow: Workflow to display
        """
        # Update details
        self.name_value.configure(text=workflow.name)
        self.id_value.configure(text=workflow.id)
        self.nodes_value.configure(text=str(len(workflow.nodes)))
        
        # Store selected workflow ID
        self.selected_workflow_id = workflow.id
    
    def set_execution_controls_state(self, enabled: bool):
        """
        Set the state of execution controls.
        
        Args:
            enabled: Whether the controls should be enabled
        """
        state = "normal" if enabled else "disabled"
        self.execute_button.configure(state=state)
        self.save_button.configure(state=state)
    
    def set_pause_resume_button_state(self, enabled: bool, text: str = "Pause"):
        """
        Set the state of the pause/resume button.
        
        Args:
            enabled: Whether the button should be enabled
            text: Text to display on the button
        """
        state = "normal" if enabled else "disabled"
        self.pause_resume_button.configure(state=state, text=text)
    
    def set_stop_button_state(self, enabled: bool):
        """
        Set the state of the stop button.
        
        Args:
            enabled: Whether the button should be enabled
        """
        state = "normal" if enabled else "disabled"
        self.stop_button.configure(state=state)
    
    def update_progress(self, current: int, total: int):
        """
        Update the progress bar.
        
        Args:
            current: Current step
            total: Total steps
        """
        # Update progress label
        self.progress_label.configure(text=f"Progress: {current}/{total}")
        
        # Update progress bar
        progress = current / total if total > 0 else 0
        self.progress_bar.set(progress)
    
    def reset_execution_display(self):
        """Reset the execution display."""
        # Clear results
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.configure(state="disabled")
        
        # Reset progress
        self.update_progress(0, 0)
        
        # Clear execution results
        self.execution_results = []
    
    def add_execution_result(self, result: Dict[str, Any]):
        """
        Add an execution result.
        
        Args:
            result: Execution result
        """
        # Format the result
        timestamp = datetime.fromtimestamp(result["timestamp"]).strftime("%H:%M:%S")
        status = "✓" if result["success"] else "✗"
        text = f"[{timestamp}] {status} {result['node_label']}: {result['message']}\n"
        
        # Add to results text
        self.results_text.configure(state="normal")
        self.results_text.insert("end", text)
        self.results_text.see("end")
        self.results_text.configure(state="disabled")
        
        # Store the result
        self.execution_results.append(result)
    
    def display_execution_results(self, results: Dict[str, Any]):
        """
        Display execution results.
        
        Args:
            results: Execution results
        """
        # Format the results
        text = f"\n--- Execution Summary ---\n"
        text += f"Workflow: {self.name_value.cget('text')}\n"
        text += f"Status: {'Success' if results['success'] else 'Failed'}\n"
        text += f"Message: {results['message']}\n"
        
        # Add to results text
        self.results_text.configure(state="normal")
        self.results_text.insert("end", text)
        self.results_text.see("end")
        self.results_text.configure(state="disabled")
        
        # Enable save button
        self.save_button.configure(state="normal")
    
    def highlight_current_node(self, node_id: str):
        """
        Highlight the current node in the workflow.
        
        Args:
            node_id: ID of the node to highlight
        """
        # This would be implemented if we had a workflow visualization
        pass
    
    def save_results_to_file(self, results: List[Dict[str, Any]], file_path: str):
        """
        Save execution results to a file.
        
        Args:
            results: Execution results
            file_path: Path to save the results
        """
        # Determine file format
        if file_path.endswith(".json"):
            # Save as JSON
            with open(file_path, "w") as f:
                json.dump(results, f, indent=2)
        elif file_path.endswith(".csv"):
            # Save as CSV
            with open(file_path, "w", newline="") as f:
                if not results:
                    return
                
                # Get field names from the first result
                fieldnames = list(results[0].keys())
                
                # Create CSV writer
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                # Write header
                writer.writeheader()
                
                # Write rows
                for result in results:
                    writer.writerow(result)
        else:
            # Save as text
            with open(file_path, "w") as f:
                for result in results:
                    timestamp = datetime.fromtimestamp(result["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
                    status = "Success" if result["success"] else "Failed"
                    f.write(f"[{timestamp}] {status} {result['node_label']}: {result['message']}\n")
    
    # === Event Handlers ===
    
    def _on_workflow_selected(self, workflow_id: str):
        """
        Handle workflow selection.
        
        Args:
            workflow_id: ID of the selected workflow
        """
        # Highlight the selected workflow
        for wid, button in self.workflow_buttons.items():
            if wid == workflow_id:
                button.configure(fg_color=("#2E7D32", "#2E7D32"))  # Green
            else:
                button.configure(fg_color=("#3B8ED0", "#1F6AA5"))  # Default color
        
        # Call the presenter
        if self.presenter:
            self.presenter.select_workflow(workflow_id)
    
    def _on_refresh_clicked(self):
        """Handle refresh button click."""
        if self.presenter:
            self.presenter.load_workflows()
    
    def _on_execute_clicked(self):
        """Handle execute button click."""
        if self.presenter:
            self.presenter.execute_workflow()
    
    def _on_pause_resume_clicked(self):
        """Handle pause/resume button click."""
        if self.presenter:
            self.presenter.pause_resume_execution()
    
    def _on_stop_clicked(self):
        """Handle stop button click."""
        if self.presenter:
            self.presenter.stop_execution()
    
    def _on_save_clicked(self):
        """Handle save button click."""
        if not self.execution_results:
            messagebox.showinfo("No Results", "No execution results to save.")
            return
        
        # Get file path
        file_path = filedialog.asksaveasfilename(
            title="Save Execution Results",
            filetypes=[
                ("JSON Files", "*.json"),
                ("CSV Files", "*.csv"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ],
            defaultextension=".json"
        )
        
        if file_path and self.presenter:
            self.presenter.save_execution_results(file_path)
