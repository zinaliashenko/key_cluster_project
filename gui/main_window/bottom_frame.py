"""
This module defines the BottomFrame class for the GUI. It provides the control buttons
to load user input and run the clustering process in a separate thread. The frame is
positioned at the bottom of the main application window.
"""

import threading
from tkinter import ttk

from controller.app_controller import Controller, ControllerConfig
from gui.base import BaseButton, BaseFrame


class BottomFrame(BaseFrame):
    """
    Bottom frame of the GUI containing buttons to load data and start clustering.
    """

    def __init__(
        self,
        parent,
        app_gui,
        entries=None,
        checkbox_vars=None,
        comboboxes=None,
        text=None,
    ):
        """
        Initialize the BottomFrame.

        Args:
            parent (tk.Frame): Parent widget.
            app_gui: Reference to the main GUI class.
            entries (list): List of entry widgets for user input.
            checkbox_vars (list): Variables linked to checkbuttons.
            comboboxes (list): Comboboxes used to set clustering parameters.
            text (BaseText): Text widget containing user-provided keywords.
        """
        super().__init__(parent)
        self.entries = entries
        self.checkbox_vars = checkbox_vars
        self.comboboxes = comboboxes
        self.text = text
        self.app_gui = app_gui
        self.btn_cluster = None

        self.frame = ttk.Frame(parent, height=50)

        self.frame.grid(
            row=2, column=0, columnspan=3, sticky="swe"
        )  # takes 3 columns starting with column 0; side biding
        self.frame.rowconfigure(0, weight=1)  # center button
        self.frame.rowconfigure(1, weight=1)  # rigth button
        self.frame.columnconfigure(0, weight=1)

    def build(self):
        """
        Build the layout of the bottom frame.

        Adds two buttons:
            - LOAD DATA: to gather and save user input
            - CLUSTERIZE: to start the clustering pipeline (initially disabled)
        """
        # Load data button
        btn_load_data = BaseButton(
            self.frame, text="LOAD DATA", command=lambda: self.save_and_enable()
        )
        btn_load_data.widget.config(width=50)
        btn_load_data.widget.grid(
            row=0, column=0, padx=(0, 0), pady=(10, 10), sticky="s"
        )

        self.widgets["btn_load_data"] = btn_load_data

        # Clusterize button
        self.btn_cluster = BaseButton(
            self.frame, text="CLUSTERIZE", command=self.clusterize_action
        )
        self.btn_cluster.widget.config(width=30, state="disabled")
        self.btn_cluster.widget.grid(
            row=1, column=0, padx=40, pady=(10, 20), sticky="e"
        )

    def save_and_enable(self):
        """
        Save user input from GUI elements and enable the Clusterize button.
        """
        self.widgets["btn_load_data"].save_user_input(
            self.entries, self.checkbox_vars, self.comboboxes, self.text
        )
        self.btn_cluster.widget.config(state="normal")

    def clusterize_action(self):
        """
        Start the clustering pipeline using a separate thread.

        Collects input data from widgets, builds a ControllerConfig,
        disables the cluster button, shows the process window, and
        launches the pipeline with asynchronous thread monitoring.
        """
        entities = [
            "EVENT",
            "FAC",
            "GPE",
            "LANGUAGE",
            "LOC",
            "MONEY",
            "ORG",
            "PERSON",
            "PRODUCT",
            "QUANTITY",
            "WORK_OF_ART",
        ]
        # Get saved data by click on button Load Data

        input_data = self.widgets["btn_load_data"].results

        if input_data:
            config = ControllerConfig(
                row_data=input_data["text"][0],
                trash_words=input_data["entries"][0].split(","),
                entities=[
                    entity
                    for entity, selected in zip(entities, input_data["checkbuttons"])
                    if selected
                ],
                stop_entity=input_data["entries"][2].split(","),
                my_keys=input_data["entries"][1].split(","),
                min_num_clusters=int(list(input_data["comboboxes"])[0]),
                max_num_clusters=int(list(input_data["comboboxes"])[1]),
            )
            controller = Controller(config)
            # Button Clusterize is disable
            self.btn_cluster.widget.config(state="disabled")

            # Build ProcessWindow
            process_window = self.app_gui.run_process_window()
            process_window.update_log_window(controller)

            # Run process in separete thread
            def run_and_check():
                """
                Run the clustering pipeline in a background thread and monitor it.
                """
                thread = threading.Thread(target=controller.run_pipeline)
                thread.start()
                check_thread_completion(thread, controller)

            def check_thread_completion(thread, controller):
                """
                Periodically check if the background thread has finished.

                If finished, updates the GUI with the results.
                """
                if thread.is_alive():
                    # wait for 200 ms
                    self.btn_cluster.widget.after(
                        200, check_thread_completion, thread, controller
                    )
                else:
                    # refresh window if thread finished
                    # Build result window
                    result_window = self.app_gui.run_result_window()
                    result_window.update_result_window(controller)

            run_and_check()

        else:
            print("Data is not loaded.")

    def get_widgets(self):
        """Return a dictionary of widgets in the frame."""
        return self.widgets
