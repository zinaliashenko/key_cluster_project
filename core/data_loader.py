"""
Module for loading keyword data from different sources
such as files or text input. Provides an abstract interface.
"""

from abc import ABC, abstractmethod
import pandas as pd


class LoadData(ABC):
    """
    Abstract base class for loading data.

    Provides a unified interface for loading and converting data
    from different sources (file, text).
    """

    def __init__(self):
        """
        Initialize an empty data container.
        """
        self.data = None

    @abstractmethod
    def load(self):
        """
        Abstract method to load data.
        Must be implemented by subclasses.
        """

    def to_list(self, column=0):
        """
        Convert loaded data to a list of values from the specified column.

        Args:
            column (int): Index of the column to extract data from (default is 0).

        Returns:
            list: A list of values from the selected column,
            or an empty list if data is not loaded or an error occurs.

        Raises:
            Prints error messages if something goes wrong.
        """
        if self.data is None:
            print("[WARNING] Data is not loaded yet")
            return []

        try:
            if isinstance(self.data, pd.DataFrame):
                return self.data.iloc[:, column].dropna().tolist()
            if isinstance(self.data, list):
                return self.data
            print("[ERROR] Data format is not supported for conversion to list.")
            return []
        except (IndexError, TypeError) as e:
            print(f"[ERROR] Error while converting data to list: {e}")
            return []


class LoadDataFromFile(LoadData):
    """
    Class to load data from a local CSV file.
    """

    def __init__(self, filepath):
        """
        Initialize the file loader with the provided file path.

        Args:
            filepath (str): Path to the CSV file containing the data.
        """
        super().__init__()
        self.filepath = filepath  # path to file with data

    def load(self):
        """
        Load data from a CSV file into a pandas DataFrame.

        Returns:
            pandas.DataFrame or None: The loaded data, or None if loading fails.

        Raises:
            Prints error messages for file not found or general exceptions.
        """
        try:
            self.data = pd.read_csv(self.filepath)  # read file using pandas
            print(f"[INFO] Data is successfully loaded from file: {self.filepath}")
            return self.data  # return pandas data
        except FileNotFoundError:
            print(f"[ERROR] File is not found: {self.filepath}")
            return None
        except (IndexError, TypeError) as e:
            print(f"[ERROR] Error while uploading file: {e}")
            return []


class LoadDataAsText(LoadData):
    """
    Class to load data from raw text (e.g., user input from a GUI).
    """

    def __init__(self, raw_text):
        """
        Initialize the text loader with the raw input string.

        Args:
            raw_text (str or list): Raw text input to be used as data.
        """
        super().__init__()
        self.raw_text = raw_text  # raw data from text widget

    def load(self):
        """
        Load the raw text into the internal data container.

        Returns:
            str or list: The raw input as stored data, or None if an error occurs.

        Raises:
            Prints error messages on exceptions.
        """
        try:
            self.data = self.raw_text  # зберігаємо в self.data
            return self.data
        except (IndexError, TypeError) as e:
            print(f"[ERROR] Error while processing text: {e}")
            return []
