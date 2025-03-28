"""Theme service implementation"""
from src.ui.interfaces.service_interface import ThemeServiceInterface


class ThemeService(ThemeServiceInterface):
    """Service for theme management"""
    
    def __init__(self, initial_theme: str = "system") -> None:
        """
        Initialize the theme service
        
        Args:
            initial_theme: Initial theme name
        """
        self._theme = initial_theme
    
    def set_theme(self, theme: str) -> None:
        """
        Set the application theme
        
        Args:
            theme: Theme name
        """
        self._theme = theme
        
        # In a real implementation with CustomTkinter, we would do:
        # import customtkinter as ctk
        # ctk.set_appearance_mode(theme)
    
    def get_theme(self) -> str:
        """
        Get the current theme
        
        Returns:
            Current theme name
        """
        return self._theme
