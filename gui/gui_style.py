"""
A module for loading and applying Tkinter themes.
"""

import os
from tkinter import ttk


class StyleManager:
    """
    A manager for loading and applying a custom theme to a Tkinter window.
    Allows you to attach `.tcl` theme to a given window.
    """

    def __init__(self, window, theme_file):
        """
        Initializes the style manager.

        Args:
            window (tkinter.Tk | tkinter.Toplevel): The window to which the theme will be applied.
            theme_file (str): The name of the theme file (e.g., 'mytheme.tcl').
        """
        self.window = window
        self.theme_file = theme_file
        self.style = None

    def load_theme_path(self):
        """
        Forms the full path to the theme file.

        Returns:
            str: The absolute path to the theme file.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, self.theme_file)

    def apply_theme(self, style_name):
        """
        Applies a theme to the window using the given style name.

        Args:
            style_name (str): The name of the theme to apply (must match the name in the .tcl file).
        """

        self.style = ttk.Style(self.window)
        self.style.theme_use(style_name)

    def activate_theme(self):
        """
        Activates a theme: loads the theme file and applies it to the window.
        """
        theme_path = self.load_theme_path()
        self.window.tk.call("source", theme_path)
        style_name = os.path.splitext(os.path.basename(self.theme_file))[0]
        self.apply_theme(style_name)
