"""
This module provides functionality for saving grouped phrase data to a file
using a graphical file dialog (via tkinter). It supports exporting to .txt, .csv, and .json formats.
"""

import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import pandas as pd


class SaveData:
    """
    Save data to user-defined file via GUI file dialog.
    Supports: .txt, .csv, .json
    """

    def __init__(self, data):
        """
        Initialize the SaveData instance with data to be saved.

        Args:
            data (dict): Dictionary where keys are group names
                         and values are lists of phrases.
        """
        self.data = data

    def save(self):
        """
        Opens a file save dialog and saves the data in the selected format.
        """
        root = tk.Tk()
        root.withdraw()  # hide main window

        file_path = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("CSV files", "*.csv"),
                ("JSON files", "*.json"),
                ("All Files", "*.*"),
            ],
        )

        if not file_path:
            print("[INFO] Saving canceled by user.")
            return

        try:
            path = Path(file_path)

            if path.suffix == ".txt":
                with open(path, "w", encoding="utf-8") as f:
                    for name, items in self.data.items():
                        f.write(f"\n{name} ({len(items)} phrases):\n")
                        for item in items:
                            f.write(f"  - {item}\n")

            elif path.suffix == ".csv":
                flat_list = []
                for group, items in self.data.items():
                    for item in items:
                        flat_list.append({"Group": group, "Phrase": item})
                df = pd.DataFrame(flat_list)
                df.to_csv(path, index=False, encoding="utf-8-sig")

            elif path.suffix == ".json":
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=4)

            else:
                print(f"[ERROR] Unknown file extension: {path.suffix}")
                return

            print(f"[INFO] Data successfully saved to: {file_path}")

        except (FileNotFoundError, PermissionError, OSError) as e:
            print(f"[ERROR] File system error while saving: {e}")
        except (TypeError, ValueError) as e:
            print(f"[ERROR] Data format error while saving: {e}")
