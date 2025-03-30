"""
Provides utility functions for the UI, including dialogs,
font getters, ttk styling helpers, and Treeview creation.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import os
from typing import Optional, List, Tuple, Dict, Any # Added typing

# Import constants

from .constants import (
    FONT_FAMILY_PRIMARY, FONT_FAMILY_MONO, FONT_SIZE_BASE, FONT_SIZE_SMALL,
    FONT_SIZE_LARGE, FONT_WEIGHT_BOLD, COLOR_SECONDARY, COLOR_ERROR,
    COLOR_WARNING, COLOR_PRIMARY, COLOR_DISABLED, PAD_X_INNER as INNER_PAD_X, PAD_Y_INNER as INNER_PAD_Y
)

# --- Font Helpers ---

def get_font(size=FONT_SIZE_BASE, weight=None, family=FONT_FAMILY_PRIMARY): return (family, size, weight) if weight else (family, size)
def get_default_font(): return get_font()
def get_small_font(): return get_font(size=FONT_SIZE_SMALL)
def get_large_font(): return get_font(size=FONT_SIZE_LARGE)
def get_header_font(): return get_font(weight=FONT_WEIGHT_BOLD)
def get_mono_font(): return get_font(family=FONT_FAMILY_MONO)

# --- Dialog Wrappers (Added type hints) ---

def show_message(parent: tk.Misc, title: str, message: str): messagebox.showinfo(title, message, parent=parent)
def show_error(parent: tk.Misc, title: str, message: str): messagebox.showerror(title, message, parent=parent)
def show_warning(parent: tk.Misc, title: str, message: str): messagebox.showwarning(title, message, parent=parent)
def ask_yes_no(parent: tk.Misc, title: str, message: str) -> bool: return messagebox.askyesno(title, message, parent=parent)
def get_input(parent: tk.Misc, title: str, prompt: str, initialvalue: str = "") -> Optional[str]: return simpledialog.askstring(title, prompt, initialvalue=initialvalue, parent=parent)
def select_file(parent: tk.Misc, title: str = "Select File", filetypes: Optional[List[Tuple[str, str]]] = None) -> Optional[str]:
    result = filedialog.askopenfilename(title=title, filetypes=filetypes or [("All files", "*.*")], parent=parent)
    return result if result else None
def select_directory(parent: tk.Misc, title: str = "Select Directory") -> Optional[str]:
    result = filedialog.askdirectory(title=title, parent=parent)
    return result if result else None

# --- Path Helper ---

def get_app_path(filename: str) -> str:
    """Gets absolute path relative to assumed project root (parent of src)."""
    try: # Find the 'src' directory and go one level up
        src_dir = os.path.dirname(os.path.abspath(__file__)) # utils dir
        project_root = os.path.dirname(os.path.dirname(src_dir)) # Up two levels # If running as a bundled executable (pyinstaller), resource_path might be needed # base_path = getattr(sys, '_MEIPASS', project_root) # Basic check
        return os.path.join(project_root, filename)
    except Exception: # Fallback if path calculation fails, assume current working directory
        print("Warning: Could not determine project root reliably. Using current working directory for path.")
        return os.path.abspath(filename)

# --- TTK Styling Helper ---

def configure_ttk_style(appearance_mode: Optional[str] = None):
    """Configure ttk styles to roughly match CustomTkinter theme."""
    style = ttk.Style()
    mode = appearance_mode or ctk.get_appearance_mode()
    theme_dict = ctk.ThemeManager.theme

    # Define fallback colors
    fallback_dark = {"bg": "#2B2B2B", "fg": "#DCE4EE", "sel": "#2A5E8A", "hdr": "#323232", "tree_bg": "#2B2B2B"}
    fallback_light = {"bg": "#EBEBEB", "fg": "#1F1F1F", "sel": "#3B8ED0", "hdr": "#DADADA", "tree_bg": "#F5F5F5"}

    try: # Try to get colors from theme
        if mode == "Dark":
            bg = theme_dict["CTkFrame"]["fg_color"][1]
            fg = theme_dict["CTkLabel"]["text_color"][1]
            sel = theme_dict["CTkButton"]["fg_color"][1]
            hdr = theme_dict["CTkFrame"].get("top_fg_color", bg)[1]
            tree_bg = bg
        else: # Light mode
            bg = theme_dict["CTkFrame"]["fg_color"][0]
            fg = theme_dict["CTkLabel"]["text_color"][0]
            sel = theme_dict["CTkButton"]["fg_color"][0]
            hdr = theme_dict["CTkFrame"].get("top_fg_color", bg)[0]
            tree_bg = theme_dict.get("CTk",{}).get("fg_color",tree_bg)[0] # Try root background
    except (IndexError, KeyError, AttributeError): # Fallback on any error
        print("Warning: Using fallback ttk style colors due to theme read error.")
        colors = fallback_dark if mode == "Dark" else fallback_light
        bg, fg, sel, hdr, tree_bg = colors["bg"], colors["fg"], colors["sel"], colors["hdr"], colors["tree_bg"]

    style.theme_use('default')
    # Configure Treeview
    style.configure("Treeview", background=tree_bg, foreground=fg, fieldbackground=tree_bg, borderwidth=0, relief="flat", rowheight=25)
    style.map("Treeview", foreground=[('!selected', fg)], background=[('!selected', tree_bg)])
    style.map("Treeview", foreground=[('selected', fg)], background=[('selected', sel)]) # Ensure selected text readable

    # Configure Heading
    style.configure("Treeview.Heading", background=hdr, foreground=fg, font=get_header_font(), padding=(INNER_PAD_X, INNER_PAD_Y), relief="flat")
    style.map("Treeview.Heading", relief=[('active', 'groove'), ('!active', 'flat')])

    # Layout (remove default border)
    style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

    # --- Configure Tags (ensure all needed tags exist) ---
    # Status tags
    style.configure("status_Active.Treeview", foreground=fg)
    style.configure("status_Inactive.Treeview", foreground=COLOR_WARNING)
    style.configure("status_Unused.Treeview", foreground=COLOR_DISABLED) # Use disabled color
    style.configure("status_Success.Treeview", foreground=COLOR_SECONDARY)
    style.configure("status_Failure.Treeview", foreground=COLOR_ERROR)
    # Severity tags
    style.configure("sev_Info.Treeview", foreground=COLOR_PRIMARY)
    style.configure("sev_Warning.Treeview", foreground=COLOR_WARNING)
    style.configure("sev_Error.Treeview", foreground=COLOR_ERROR)
    style.configure("sev_Critical.Treeview", foreground=COLOR_ERROR)
    style.configure("sev_Fatal.Treeview", foreground=COLOR_ERROR)

    # Required for Vertical Scrollbar styling (use TScrollbar)
    style.configure("Vertical.TScrollbar", background=hdr, troughcolor=tree_bg, bordercolor=hdr, arrowcolor=fg)
    style.map("Vertical.TScrollbar", background=[('active', sel)])
    # Required for Horizontal Scrollbar styling (use TScrollbar)
    style.configure("Horizontal.TScrollbar", background=hdr, troughcolor=tree_bg, bordercolor=hdr, arrowcolor=fg)
    style.map("Horizontal.TScrollbar", background=[('active', sel)])
