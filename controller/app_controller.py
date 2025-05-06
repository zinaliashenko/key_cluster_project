"""
This module contains the application controller for handling various operations.
"""

from dataclasses import dataclass
from pathlib import Path
from queue import Queue
from typing import List

from core.clusterizer import (ClusterByEntity, ClusterByUserKeys,
                              ClusterUsingKMeans)
from core.data_cleaner import RemoveDuplicates, RemoveTrashPhrase
from core.data_loader import LoadDataAsText, LoadDataFromFile


@dataclass
class ControllerConfig:
    """
    Configuration data for creating a controller.

    Attributes:
        row_data (List): Input phrases to be clusterize.
        trash_words (List): A list of words for phrases to be deleted.
        entities (List): A list of entity for phrases to be clusterised by if exists.
        stop_entity (List): A list of words for phrases to not be clusterised by.
        my_keys (List): A list of words for phrases to be clusterised by.
        min_num_clusters (int): A minimum number of clusters created during KMeans clustering.
        max_num_clusters (int): A maximum number of clusters created during KMeans clustering.
    """

    row_data: List
    trash_words: List
    entities: List
    stop_entity: List
    my_keys: List
    min_num_clusters: int
    max_num_clusters: int


class Controller:
    """This class is responsible for managing the entire data processing pipeline."""

    def __init__(self, config: ControllerConfig):
        """ """
        if isinstance(config.row_data, str):
            self.loader = LoadDataFromFile(config.row_data)
        elif isinstance(config.row_data, List):
            self.loader = LoadDataAsText(config.row_data)
        else:
            raise ValueError("Uncorrect data.")
        self.trash_words = config.trash_words
        self.entities = config.entities
        self.stop_entity = config.stop_entity
        self.my_keys = config.my_keys
        self.min_num_clusters = config.min_num_clusters
        self.max_num_clusters = config.max_num_clusters
        self.log_queue = Queue()
        self.clusters = None

    def log(self, message):
        """Put the message into logging queue."""
        self.log_queue.put(message)

    def print_result(self):
        """Returns clusters as List."""
        return self.clusters

    def run_pipeline(self):
        """
        Executes the entire data processing pipeline,
        including loading, cleaning, clustering, and saving.
        """
        data = self.__load_data()
        data = self.__remove_duplicates(data)
        data = self.__remove_trash(data)
        clusters, data = self.__cluster_by_entity(data)
        clusters, data = self.__cluster_by_user_keys(clusters, data)
        self.__cluster_using_kmeans(data, clusters)
        #self.__save_data()

    def __load_data(self):
        """Load data and log the process."""
        self.loader.load()
        data = self.loader.to_list()
        self.log(f"Loaded {len(data)} phrases.")
        return data

    def __remove_duplicates(self, data):
        """Remove duplicate phrases and log the process."""
        self.log("Cleaning data from phrases with duplicates...")
        duplicate_cleaner = RemoveDuplicates(data)
        unique_phrases, deleted_phrases = duplicate_cleaner.delete()
        self.log(f"Was deleted: {len(deleted_phrases)} phrases.")
        self.log(f"After deleting duplicates left {len(unique_phrases)} phrases.")
        return unique_phrases

    def __remove_trash(self, data):
        """Remove phrases with trash words and log the process."""
        self.log("Deleting phrases with trash words...")
        trash_cleaner = RemoveTrashPhrase(data, self.trash_words or [])
        phrases_without_trash, deleted_phrases = trash_cleaner.delete()
        self.log(f"Was deleted: {len(deleted_phrases)} phrases.")
        self.log(
            f"After deleting trash words left {len(phrases_without_trash)} phrases."
        )
        return phrases_without_trash

    def __cluster_by_entity(self, data):
        """Cluster phrases by named entities and log the process."""
        self.log("Clusterizing by named entities...")
        entity_clusterizer = ClusterByEntity(
            data, self.entities or [], self.stop_entity or []
        )
        filtered_entity_cluster, phrases_without_cluster = entity_clusterizer.cluster()
        self.log(f"Was created: {len(filtered_entity_cluster)} clusters.")
        self.log(
            f"After clustering by named entities left {len(phrases_without_cluster)} phrases."
        )
        return filtered_entity_cluster, phrases_without_cluster

    def __cluster_by_user_keys(self, clusters, data):
        """Cluster phrases by user keys and log the process."""
        self.log("Adding user's keys to clusters...")
        key_clusterizer = ClusterByUserKeys(data, clusters, self.my_keys or [])
        clusters, phrases_without_cluster = key_clusterizer.cluster()
        self.log(f"Was created: {len(clusters)} clusters.")
        self.log(
            f"After clustering by named entities left {len(phrases_without_cluster)} phrases."
        )
        return clusters, phrases_without_cluster

    def __cluster_using_kmeans(self, data, clusters):
        """Cluster remaining phrases using KMeans if any."""
        self.log("Clusterizing using kmeans...")
        if data:
            kmeans_clusterizer = ClusterUsingKMeans(
                data, clusters, self.min_num_clusters, self.max_num_clusters
            )
            self.clusters = kmeans_clusterizer.cluster()
            self.log(
                f"After clustering using kmeans got: {len(self.clusters)} clusters."
            )
        else:
            self.log("No phrases left for KMeans clustering.")

    def __save_data(self):
        """Save the resulting clusters and log the process."""
        if self.clusters:
            self.log("Saving data....")
            target_dir = Path("results")
            file_path = target_dir / "res1"
            if not target_dir.is_dir():
                target_dir.mkdir(parents=True, exist_ok=True)
            with open(file_path, "a", encoding="utf-8") as f:
                for name, items in self.clusters.items():
                    f.write(f"\n {name} ({len(items)} phrases):\n")
                    for item in items:
                        f.write(f"  - {item}\n")
            self.log("Data is saved.")
        else:
            self.log("No clusters to save.")
