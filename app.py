"""
Entry point for the Keyword Clustering application.

This script initializes and runs the main GUI application
using the AppGUI class defined in the gui.app_gui module.
"""

from gui.app_gui import AppGUI

if __name__ == "__main__":

    app = AppGUI()
    app.run()
