"""
A module for creating MainWindow class.
"""

from gui.base import BaseWindow, WindowConfig
from gui.main_window.bottom_frame import BottomFrame
from gui.main_window.left_frame import LeftFrame
from gui.main_window.right_frame import RightFrame
from gui.main_window.top_frame import TopFrame


class MainWindow(BaseWindow):
    """
    A class for creating main application window.
    """

    def __init__(
        self, title, window_size, row_weight, column_weight, theme_file, app_gui
    ):
        """
        Window configuration parameters inherited from the BaseWindow base class.

        Args:
            title (str): The title text of the window.
            window_size (str): The size of the window in "WidthxHeight" format (e.g., "800x600").
            row_weight (int): Weight for row grid resizing. Default is 1.
            column_weight (int): Weight for column grid resizing. Default is 1.
            theme_file (str, optional): Path to a theme file for styling the window.
            Default is None.
        """
        config = WindowConfig(title, window_size, row_weight, column_weight, theme_file)

        super().__init__(config)
        self.app_gui = app_gui
        self.frame_bottom = None
        self.frame_left = None

    def show(self):
        """
        Configures row and column grid weight for layout management,
        and displays widgets in the window.
        """
        self.window.columnconfigure(0, weight=1)  # LeftFrame
        self.window.columnconfigure(1, weight=2)  # RightFrame
        self.window.columnconfigure(2, weight=2)  # RightFrame

        self.window.rowconfigure(0, weight=0)  # TopFrame
        self.window.rowconfigure(1, weight=1)  # RightFrame & LefFrame
        self.window.rowconfigure(2, weight=0)  # BottomFrame

        frame_top = TopFrame(self.window)
        frame_top.build()

        self.frame_left = LeftFrame(self.window)
        self.frame_left.build()

        frame_right = RightFrame(self.window)
        frame_right.build()

        self.frame_bottom = BottomFrame(
            self.window,
            app_gui=self.app_gui,
            entries=[
                frame_right.ent_trash_words,
                frame_right.ent_my_keys,
                frame_right.ent_entity_words,
            ],
            checkbox_vars=[frame_right.checkbox_vars],
            comboboxes=[frame_right.combo_menu_min, frame_right.combo_menu_max],
            text=[self.frame_left.text],
        )
        self.frame_bottom.build()
