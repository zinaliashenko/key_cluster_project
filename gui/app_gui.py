"""
A module for creating window instances: MainWindow, ProcessWindow and ResultWindow.
Consists method run() to start main Tk().mainloop().
"""

from gui.main_window.gui_main_window import MainWindow
from gui.process_window.gui_process_window import ProcessWindow
from gui.result_window.gui_result_window import ResultWindow


class AppGUI:
    """
    A class for creating application windows.
    """

    def __init__(self):
        """
        Initialize creating instance of main app window.
        """
        self.main_window = MainWindow(
            title="Main",
            window_size="1200x600",
            row_weight=1,
            column_weight=3,
            theme_file="forest-dark.tcl",
            app_gui=self,
        )
        self.process_window = None
        self.result_window = None

    def run(self):
        """
        Shows main window and runs main loop.
        """
        self.main_window.show()
        self.main_window.run()
        print("App started")

    def run_process_window(self):
        """
        Creates an instance of processing window and
        shows the window.

        Returns:
            instance of ProcessWindow class.
        """
        self.process_window = ProcessWindow(
            title="Process Window",
            window_size="500x500",
            row_weight=1,
            column_weight=1,
            theme_file="forest-dark.tcl",
        )
        self.process_window.show()
        return self.process_window

    def run_result_window(self):
        """
        Creates an instance of resulting window and
        shows the window.

        Returns:
            instance of ResultWindow class.
        """
        self.result_window = ResultWindow(
            title="Result Window",
            window_size="500x500",
            row_weight=1,
            column_weight=1,
            theme_file="forest-dark.tcl",
        )
        self.result_window.show()
        return self.result_window
