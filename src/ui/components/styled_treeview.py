"""
Provides a reusable Treeview component with integrated scrollbars and basic styling setup.
SOLID: Encapsulates Treeview setup logic.
DRY: Avoids repeating Treeview creation/styling code in multiple views.
KISS: Provides a simpler interface for creating styled Treeviews.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple, Dict, Any, Callable

class StyledTreeview(ctk.CTkFrame):
    """A CTkFrame containing a styled ttk.Treeview with scrollbars."""
    def __init__(self, master, columns: tuple,
                 column_config: Optional[Dict[str, Dict[str, Any]]] = None,
                 show="headings", selectmode="extended", tree_column_id: str = '#0',
                 **kwargs):
        """
        Args:
            master: Parent widget.
            columns: Tuple of data column identifiers.
            column_config: Dictionary mapping column identifiers (including potentially tree_column_id like '#0')
                          to config dicts (e.g., {'width': 100, 'minwidth': 50,
                          'anchor': 'w', 'stretch': True/False, 'heading': 'Custom Heading', 'command': callback}).
            show: ttk.Treeview show option ('headings', 'tree headings', 'tree').
            selectmode: ttk.Treeview selectmode ('browse', 'extended', 'none').
            tree_column_id (str): ID used for the tree column ('#0' by default).
            **kwargs: Passed to the parent CTkFrame.
        """
        kwargs.setdefault('fg_color', 'transparent')
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Actual Treeview widget
        self.treeview = ttk.Treeview(self, columns=columns, show=show, selectmode=selectmode, style="Treeview") # Apply style

        # --- Setup Headings and Columns ---
        cfg = column_config or {}

        # Configure tree column if shown
        if 'tree' in show:
            tree_cfg = cfg.get(tree_column_id, {})
            heading_text = tree_cfg.get('heading', "Tree") # Default heading
            heading_cmd = tree_cfg.get('command')
            if heading_cmd:
                self.treeview.heading(tree_column_id, text=heading_text, command=heading_cmd)
            else:
                self.treeview.heading(tree_column_id, text=heading_text)
            self.treeview.column(tree_column_id,
                                 width=tree_cfg.get('width', 180), minwidth=tree_cfg.get('minwidth', 50),
                                 stretch=tree_cfg.get('stretch', tk.NO), anchor=tree_cfg.get('anchor', 'w'))

        # Configure data columns
        for col_id in columns:
            col_cfg = cfg.get(col_id, {})
            heading_text = col_cfg.get('heading', col_id.replace("_", " ").title())
            heading_cmd = col_cfg.get('command')
            if heading_cmd:
                self.treeview.heading(col_id, text=heading_text, command=heading_cmd)
            else:
                self.treeview.heading(col_id, text=heading_text)
            self.treeview.column(col_id,
                                 width=col_cfg.get('width', 100), minwidth=col_cfg.get('minwidth', 40),
                                 stretch=col_cfg.get('stretch', tk.YES), anchor=col_cfg.get('anchor', 'w'))

        # --- Scrollbars ---
        # Use ttk Scrollbars for better potential styling via ttk style engine
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.treeview.yview, style="Vertical.TScrollbar")
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.treeview.xview, style="Horizontal.TScrollbar")
        self.treeview.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Layout
        self.treeview.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

    # --- Delegate common Treeview methods ---
    def insert(self, *args, **kwargs): return self.treeview.insert(*args, **kwargs)
    def delete(self, *args, **kwargs): return self.treeview.delete(*args, **kwargs)
    def get_children(self, *args, **kwargs): return self.treeview.get_children(*args, **kwargs)
    def selection(self, *args, **kwargs): return self.treeview.selection(*args, **kwargs)
    def focus(self, *args, **kwargs): return self.treeview.focus(*args, **kwargs)
    def item(self, *args, **kwargs): return self.treeview.item(*args, **kwargs)
    def bind(self, *args, **kwargs): return self.treeview.bind(*args, **kwargs)
    def heading(self, *args, **kwargs): return self.treeview.heading(*args, **kwargs)
    def column(self, *args, **kwargs): return self.treeview.column(*args, **kwargs)
    def tag_configure(self, *args, **kwargs): return self.treeview.tag_configure(*args, **kwargs)
    def yview(self, *args): return self.treeview.yview(*args)
    def xview(self, *args): return self.treeview.xview(*args)
    def exists(self, item_id): return self.treeview.exists(item_id)
