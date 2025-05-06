"""
A module for base classes for creating:
- Tkinter window objects,
- Tkinter Frame objects,
- Tkinter Widget objects: ttk.Button, ttk.Entry, tk.Text, ttk.CheckButton, ttk.Combobox
"""

import tkinter as tk
from abc import ABC, abstractmethod
from dataclasses import dataclass
from tkinter import ttk
from typing import Dict

from gui.gui_style import StyleManager


@dataclass  # autogenerates __init__ and __repr__ (formal string representation) for parameters
class WindowConfig:
    """
    Configuration data for creating a window.

    Attributes:
        title (str): The title text of the window.
        window_size (str): The size of the window in "WidthxHeight" format (e.g., "800x600").
        row_weight (int): Weight for row grid resizing. Default is 1.
        column_weight (int): Weight for column grid resizing. Default is 1.
        theme_file (str, optional): Path to a theme file for styling the window. Default is None.
        master (tk.Tk, optional): The master window if this window is a child. Default is None.
    """

    title: str
    window_size: str
    row_weight: int = 1
    column_weight: int = 1
    theme_file: str = None
    master: tk.Tk = None


class BaseWindow(ABC):
    """
    Abstract base class for creating window objects.

    This class sets up a basic Tkinter window structure and handles
    optional theme application.

    Attributes:
        window (tk.Tk or tk.Toplevel): The main window or child window.
        row_weight (int): Row grid weight for layout management.
        column_weight (int): Column grid weight for layout management.
        style (StyleManager, optional): Theme manager, if theme is applied.
    """

    def __init__(self, config: WindowConfig):
        """
        Initialize the window using the provided configuration.

        Args:
            config (WindowConfig): An instance containing window setup parameters.
        """
        if config.master is None:
            self.window = tk.Tk()
        else:
            self.window = tk.Toplevel(config.master)

        self.window.title(config.title)
        self.window.geometry(config.window_size)
        self.row_weight = config.row_weight
        self.column_weight = config.column_weight

        if config.theme_file:
            self.style = StyleManager(self.window, config.theme_file)
            self.apply_theme()

    def apply_theme(self):
        """
        Apply the theme to the window using the StyleManager, if a theme is specified.
        """
        if hasattr(self, "style"):
            self.style.activate_theme()

    @abstractmethod
    def show(self):
        """
        Abstract method to display widgets in the window.
        """

    def run(self):
        """
        Start the main event loop for the window.
        """
        self.window.mainloop()


class BaseFrame(ABC):
    """
    Abstract base class for creating reusable frame objects.
    This class sets up a basic Tkinter frame widget.

    Attributes:
        parent (tk.Widget): The parent widget.
        frame (ttk.Frame): The frame container.
        widgets (dict): A dictionary to store child widgets.
    """

    def __init__(self, parent):
        """
        Initialize the frame and attach it to the parent widget.
        """
        self.parent = parent
        self.frame = ttk.Frame(self.parent)
        self.widgets = {}

    @abstractmethod
    def build(self):  # create widgets in frame
        """
        Abstract method for building widgets inside the frame.
        """

    def get_widgets(self) -> Dict:  # return dictionary with all widgets
        """
        Return the dictionary of widgets contained in this frame.

        Returns:
            dict: A dictionary where keys are widget names and values are widget instances.
        """
        return self.widgets


class BaseButton:
    """
    Base class for creating button object.

    Attributes:
        parent(tk.Widget): The parent widget.
        widget(ttk.Button): The button widget.
        results (dict): Stores user input data from widgets.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, parent, text, command, state="normal"):
        """
        Initialize the button and attach to the parent widget
        """
        self.parent = parent
        self.widget = ttk.Button(parent, text=text, command=command, state=state)
        self.results = {}

    def save_user_input(
        self, entries=None, checkbox_vars=None, comboboxes=None, text=None
    ):
        """
        Saves user's input data from widgets to result dict.

        Args:
            entries (list, optional): List of entry widgets.
            checkbox_vars (list, optional): Nested list of checkbutton widgets.
            comboboxes (list, optional): List of combobox widgets.
            text (list, optional): List of text widgets.
        """
        if entries:
            self.results["entries"] = [entry.get_value() for entry in entries]
        if checkbox_vars:
            self.results["checkbuttons"] = [
                checkbtn.get_value()
                for checkbtns in checkbox_vars
                for checkbtn in checkbtns
            ]
        if comboboxes:
            self.results["comboboxes"] = [
                combobox.get_value() for combobox in comboboxes
            ]
        if text:
            self.results["text"] = [t.get_value() for t in text]


class BaseEntry:
    """
    Base class for creating entry object.

    Attributes:
        parent(tk.Widget): The parent widget.
        widget(ttk.Entry): The entry widget.
        placeholder(str): The text shown as a hint inside the entry widget.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, parent, placeholder=""):
        """
        Initialize the entry widget, attach to the parent widget
        and set the placeholder within widget.
        """
        self.parent = parent
        self.widget = ttk.Entry(parent)
        self.placeholder = placeholder
        self._set_placeholder()
        self.widget.bind("<FocusIn>", self._clear_placeholder)
        self.widget.bind("<FocusOut>", self._set_placeholder)

    def _set_placeholder(self, event=None):
        """
        The method to set placeholder within entry widget.
        """
        _ = event  # silence unused arg warning
        if not self.widget.get():
            self.widget.delete("0", "end")
            self.widget.insert("0", self.placeholder)
            self.widget.config(foreground="gray")

    def _clear_placeholder(self, event=None):
        """
        The method to delete placeholder.
        """
        _ = event  # silence unused arg warning
        if self.widget.get() == self.placeholder:
            self.widget.delete("0", "end")
            self.widget.config(foreground="black")

    def get_value(self):
        """
        The method to get value from entry widget.

        Returns:
            str: User input if provided, otherwise an empty string.
        """
        text = self.widget.get()
        if text == self.placeholder:
            return ""
        return text


class BaseText:
    """
    Base class for creating text object.

    Attributes:
        parent(tk.Widget): The parent widget.
        widget(tk.Text): The text widget.
        placeholder(str): The text shown as a hint inside the text widget.
    """

    def __init__(self, parent, placeholder=""):
        """
        Initialize the text widget, attach to the parent widget
        and set the placeholder within widget.
        """
        self.parent = parent
        self.widget = tk.Text(parent, height=5)
        self.placeholder = placeholder
        self._set_placeholder()  # check if widget is symbols empty and put placeholder there
        self.widget.bind(
            "<FocusIn>", self._clear_placeholder
        )  # if cursor in the widget
        self.widget.bind(
            "<FocusOut>", self._set_placeholder
        )  # if cursor not in the widget

    def _set_placeholder(self, event=None):
        """
        The method to set placeholder within text widget.
        """
        _ = event  # silence unused arg warning
        if not self.widget.get(
            "1.0", "end-1c"
        ).strip():  # if widget is symbols empty (ignore spaces)
            self.widget.delete("1.0", tk.END)  # delete all text in the widget
            self.widget.insert("1.0", self.placeholder)  # insert placeholder
            self.widget.config(foreground="gray")  # set font color to gray

    def _clear_placeholder(self, event=None):
        """
        The method to delete placeholder.
        """
        _ = event  # silence unused arg warning
        if (
            self.widget.get("1.0", "end-1c") == self.placeholder
        ):  # if there is placeholder in widget
            self.widget.delete("1.0", tk.END)  # delete all text in the widget
            self.widget.config(foreground="black")  # set font color to black

    def get_value(self):
        """
        The method to get value from text widget.

        Returns:
            list: List of lines from the text widget, if input is provided;
            otherwise an empty string.
        """
        text = self.widget.get("1.0", "end-1c")  # get text from the widget
        if text == self.placeholder:  # if text is placeholder
            return ""  # return empty string
        return text.strip().split(
            "\n"
        )  # otherwise return text as list divided by tab symbol

    def put_text_from_file(self, text):
        """
        The method to put value from file into entry widget.

        Args:
            text (str): The text content to insert into the widget.
        """
        self.widget.delete("1.0", tk.END)
        self.widget.insert("1.0", text)
        self.widget.config(foreground="black")


class BaseCheckButton:
    """
    Base class for creating checkbutton object.

    Attributes:
        parent(tk.Widget): The parent widget.
        var(tk.BooleanVar): Stores the state of the checkbutton.
        widget(ttk.Checkbutton): The checkbutton widget.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, parent, text, initial=True):
        """
        Initialize the checkbutton widget, attach to the parent widget
        and set the True initial value.
        """
        self.parent = parent
        self.var = tk.BooleanVar(value=initial)
        self.widget = ttk.Checkbutton(parent, text=text, variable=self.var)

    def get_value(self):
        """
        The method to get value from checkbutton widget.
        """
        return self.var.get()


class BaseComboBox:
    """
    Base class for creating combobox object.

    Attributes:
        parent(tk.Widget): The parent widget.
        widget(ttk.Checkbutton): The combobox widget.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, parent, values, default_value):
        """
        Initialize the combobox widget, attach to the parent widget
        and set the default value.
        """
        self.parent = parent
        self.widget = ttk.Combobox(parent, values=values, state="readonly")
        self.widget.current(default_value)

    def get_value(self):
        """
        The method to get value from combobox widget.

        Returns:
            str: The selected value.
        """
        return self.widget.get()
