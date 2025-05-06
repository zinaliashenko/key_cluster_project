"""
This module defines the RightFrame class which builds the right-side frame
of the GUI. It includes input fields for trash words, keywords, and entity words,
a set of checkbuttons to select named entities, and comboboxes to specify
minimum and maximum number of clusters.
"""

from tkinter import ttk

from gui.base import BaseCheckButton, BaseComboBox, BaseEntry, BaseFrame


class RightFrame(BaseFrame):
    """
    Right-side frame that contains user input fields for trash words, entity words,
    keywords for clustering, selectable entity types, and cluster range options.
    """

    def __init__(self, parent):
        """
        Initialize the RightFrame.

        Args:
            parent: The parent widget to which this frame is attached.
        """
        super().__init__(parent)
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=1, column=1, columnspan=2, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)

        # Placeholder attributes
        self.ent_trash_words = None
        self.ent_my_keys = None
        self.ent_entity_words = None
        self.checkbox_vars = []
        self.combo_menu_min = None
        self.combo_menu_max = None

    def build(self):
        """Create and place all GUI elements inside the right frame."""
        # Main Label for all Entry fields
        lbl_entry_names = ttk.Label(
            self.frame,
            text="Enter the words you want to include/exclude from the list.",
            font=("Arial", 12, "bold"),
        )
        lbl_entry_names.grid(row=0, column=0)

        # 1. ENTRY - Trash_words____________________________________________________
        self.ent_trash_words = BaseEntry(
            self.frame, placeholder="Enter your trash words here..."
        )
        self.ent_trash_words.widget.grid(
            row=1, column=0, sticky="ew", padx=(20, 20), pady=(10, 10)
        )

        # 2. ENTRY - My_keys____________________________________________________
        self.ent_my_keys = BaseEntry(
            self.frame, placeholder="Enter your keywords to create cluster here..."
        )
        self.ent_my_keys.widget.grid(
            row=2, column=0, sticky="ew", padx=(20, 20), pady=(10, 10)
        )

        # 3. ENTRY - Entity_words____________________________________________________
        self.ent_entity_words = BaseEntry(
            self.frame, placeholder="Enter your entity words to delete here..."
        )
        self.ent_entity_words.widget.grid(
            row=3, column=0, sticky="ew", padx=(20, 20), pady=(10, 10)
        )

        # 4. CHECKBUTTON - Entity____________________________________________________
        # Label for checkbuttons
        lbl_checkbox_names = ttk.Label(
            self.frame, text="Choose the entities:", font=("Arial", 12, "bold")
        )
        lbl_checkbox_names.grid(row=4, column=0, sticky="w", padx=20, pady=(20, 5))

        # Frame for checkbuttons
        frame_checkbuttons = ttk.Frame(self.frame)
        frame_checkbuttons.grid(row=5, column=0, columnspan=2, sticky="w")
        frame_checkbuttons.columnconfigure(0, weight=1)
        frame_checkbuttons.columnconfigure(1, weight=1)
        frame_checkbuttons.columnconfigure(2, weight=1)
        # frame_checkbuttons.rowconfigure(0, weight=1)

        # Checkbutton labels
        checkbox_labels = {
            "EVENT": "Named events: wars, sports...",
            "FAC": "Buildings, airports...",
            "GPE": "Countries, cities...",
            "LANGUAGE": "Named language.",
            "LOC": "Non-GPE locations, mountain ranges...",
            "MONEY": "Monetary values.",
            "ORG": "Companies, agencies...",
            "PERSON": "People, including fictional.",
            "PRODUCT": "Objects, vehicles, foods...",
            "QUANTITY": "Measurements: weights, distance...",
        }

        self.checkbox_vars = []
        # Checkbuttons
        for i, name in enumerate(checkbox_labels.values()):
            checkbtn = BaseCheckButton(frame_checkbuttons, text=f"{name}")
            row = i % 5  # from 0 to 5
            col = i // 5  # 0 or 1
            checkbtn.widget.grid(row=row, column=col, sticky="w", pady=5, padx=20)
            self.checkbox_vars.append(checkbtn)

        # 5. COMBOBOX - min_clusters____________________________________________________

        # Label for Combobox min_clusters
        lbl_min_clusters = ttk.Label(
            frame_checkbuttons, text="min_clusters:", font=("Arial", 12, "bold")
        )
        lbl_min_clusters.grid(row=0, column=2, sticky="we", padx=50, pady=5)
        # List values for Combobox
        cluster_values_min = list(range(5, 15))
        # Combobox min_clusters
        self.combo_menu_min = BaseComboBox(
            frame_checkbuttons,
            values=cluster_values_min,
            default_value=cluster_values_min.index(5),
        )
        self.combo_menu_min.widget.grid(row=1, column=2, sticky="we", padx=50, pady=5)

        # 6. COMBOBOX - max_clusters____________________________________________________

        # Label for Combobox max_clusters
        lbl_max_clusters = ttk.Label(
            frame_checkbuttons, text="max_clusters:", font=("Arial", 12, "bold")
        )
        lbl_max_clusters.grid(row=2, column=2, sticky="we", padx=50, pady=5)
        # List values for Combobox
        cluster_values_max = list(range(16, 31))
        # Combobox max_clusters
        self.combo_menu_max = BaseComboBox(
            frame_checkbuttons,
            values=cluster_values_max,
            default_value=cluster_values_max.index(16),
        )
        self.combo_menu_max.widget.grid(row=3, column=2, sticky="we", padx=50, pady=5)

    def get_widgets(self):
        """Return a dictionary of widgets in the frame."""
        return self.widgets
