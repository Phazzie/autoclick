"""Base component for UI components"""
import tkinter as tk
from tkinter import ttk
from typing import Any, Optional


class BaseComponent:
    """Base class for UI components"""
    
    def __init__(self, parent: Any) -> None:
        """
        Initialize the component
        
        Args:
            parent: Parent widget
        """
        self.parent = parent
        self.frame = ttk.Frame(parent)
    
    def pack(self, **kwargs: Any) -> None:
        """
        Pack the component
        
        Args:
            **kwargs: Pack options
        """
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs: Any) -> None:
        """
        Grid the component
        
        Args:
            **kwargs: Grid options
        """
        self.frame.grid(**kwargs)
    
    def place(self, **kwargs: Any) -> None:
        """
        Place the component
        
        Args:
            **kwargs: Place options
        """
        self.frame.place(**kwargs)
