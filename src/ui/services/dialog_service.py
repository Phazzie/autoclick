"""Dialog service implementation"""
import tkinter as tk
from tkinter import messagebox, filedialog
from typing import List, Optional, Tuple

from src.ui.interfaces.service_interface import DialogServiceInterface


class DialogService(DialogServiceInterface):
    """Service for dialog operations"""
    
    def show_info(self, title: str, message: str) -> None:
        """
        Show information dialog
        
        Args:
            title: Dialog title
            message: Dialog message
        """
        messagebox.showinfo(title, message)
    
    def show_error(self, title: str, message: str) -> None:
        """
        Show error dialog
        
        Args:
            title: Dialog title
            message: Dialog message
        """
        messagebox.showerror(title, message)
    
    def show_confirmation(self, title: str, message: str) -> bool:
        """
        Show confirmation dialog
        
        Args:
            title: Dialog title
            message: Dialog message
            
        Returns:
            True if confirmed, False otherwise
        """
        return messagebox.askyesno(title, message)
    
    def open_file(self, file_types: List[Tuple[str, str]]) -> Optional[str]:
        """
        Open file dialog
        
        Args:
            file_types: List of file type tuples (description, extension)
            
        Returns:
            Selected file path, or None if cancelled
        """
        path = filedialog.askopenfilename(filetypes=file_types)
        return path if path else None
    
    def save_file(self, file_types: List[Tuple[str, str]], default_extension: str) -> Optional[str]:
        """
        Save file dialog
        
        Args:
            file_types: List of file type tuples (description, extension)
            default_extension: Default file extension
            
        Returns:
            Selected file path, or None if cancelled
        """
        path = filedialog.asksaveasfilename(
            filetypes=file_types,
            defaultextension=default_extension
        )
        return path if path else None
