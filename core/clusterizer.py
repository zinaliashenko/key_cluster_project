"""
A module for clustering phrases using different approaches:
- by named entities (NER),
- by user keywords,
- using BERT + KMeans.
"""

import re
import warnings
from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from itertools import chain
from typing import Dict, List, Tuple
import numpy as np
import spacy
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

stop_words = stopwords.words("english")
nlp = spacy.load("en_core_web_trf")
warnings.filterwarnings("ignore", category=FutureWarning)


class ClusterPhrase(ABC):
    """
    Abstract base class for clustering phrases using different strategies.
    Subclasses must implement the `cluster` method.
    """

    def __init__(self, phrases: List[str]):
        """
        Args:
            phrases (List[str]): A list of phrases to be clustered.
        """
        self.phrases = phrases

    @abstractmethod
    def cluster(self):
        """
        Abstract method to run clusterization.
        """


class ClusterByEntity(ClusterPhrase):
    """
    Clusters phrases by detecting named entities using spaCy and grouping by those entities.
    """

    def __init__(
        self, phrases: List[str], entities: bool = False, stop_entity: List[str] = None
    ):
        """
        Args:
            phrases (List[str]): A list of phrases to cluster.
            entities (bool): Whether to use entity-based clustering.
            stop_entity (List[str], optional): A list of entity words to ignore.
        """
        if not isinstance(phrases, list) or not all(
            isinstance(p, str) for p in phrases
        ):
            raise ValueError("Phrases must be a list of strings.")
        # if not isinstance(entities, bool):
        if not isinstance(phrases, list) or not all(
            isinstance(p, str) for p in phrases
        ):
            raise ValueError("Entities flag must be a boolean (True/False).")
        if stop_entity is not None:
            if not isinstance(stop_entity, list) or not all(
                isinstance(se, str) for se in stop_entity
            ):
                raise ValueError("Stop_entity must be a list of strings if provided.")
        else:
            stop_entity = []
        if not phrases:
            print("Warning: Empty phrases list passed to ClusterByEntity.")

        super().__init__(phrases)
        self.entities = entities
        self.stop_entity = stop_entity

    def cluster(self) -> Tuple[Dict[str, List[str]], List[str]]:
        """
        Perform entity-based clustering.

        Returns:
            Tuple[Dict[str, List[str]], List[str]]:
                - A dictionary mapping entity names to lists of phrases containing those entities.
                - A list of phrases that could not be clustered.
        """
        # if entity checkbox switched off - do not cluster
        if not [word for word in self.stop_entity if word.strip()]:
            return {}, self.phrases

        if not self.entities:
            return {}, self.phrases

        entity_cluster = defaultdict(list)

        # Create clusters using entity list
        for phrase in self.phrases:
            if not phrase:  # пропускаємо пусті строки
                continue
            doc = nlp(phrase)
            for ent in doc.ents:
                if (
                    ent.label_ in self.entities
                    and ent.text.lower() not in self.stop_entity
                ):
                    entity_cluster[ent.text].append(phrase)

        # Filter clusters: min 2 phrases, max 40
        filtered_entity_cluster = {
            key: value for key, value in entity_cluster.items() if 1 < len(value) < 40
        }
        phrases_from_entity_clusters = list(
            chain.from_iterable(filtered_entity_cluster.values())
        )

        # Detect unclustered phrases
        phrases_without_entities = [
            phrase
            for phrase in self.phrases
            if phrase not in phrases_from_entity_clusters
        ]

        # Add phrases to clusters if they contain entity in text
        for phrase in phrases_without_entities:
            for entity in filtered_entity_cluster.keys():
                if (
                    entity.lower() in phrase.lower()
                    and phrase not in filtered_entity_cluster[entity]
                ):
                    filtered_entity_cluster[entity].append(phrase)

        # Final check: phrases not included in any cluster
        phrases_from_entity_clusters = list(
            chain.from_iterable(filtered_entity_cluster.values())
        )
        phrases_without_cluster = [
            item for item in self.phrases if item not in phrases_from_entity_clusters
        ]

        return filtered_entity_cluster, phrases_without_cluster


class ClusterByUserKeys(ClusterPhrase):
    """
    Clusters phrases using custom keywords provided by the user.
    """

    def __init__(
        self,
        phrases: List[str],
        clusters: Dict[str, List[str]] = None,
        my_keys: List[str] = None,
    ):
        """
        Args:
            phrases (List[str]): A list of phrases to cluster.
            clusters (Dict[str, List[str]], optional): Predefined clusters (optional).
            my_keys (List[str], optional): List of keywords for clustering.
        """
        if not isinstance(phrases, list) or not all(
            isinstance(p, str) for p in phrases
        ):
            raise ValueError("Phrases must be a list of strings.")

        if clusters is not None:
            if not isinstance(clusters, dict) or not all(
                isinstance(k, str) and isinstance(v, list) for k, v in clusters.items()
            ):
                raise ValueError(
                    "Clusters must be a dictionary with string keys and list-of-strings values."
                )
        else:
            clusters = {}

        if my_keys is not None:
            if not isinstance(my_keys, list) or not all(
                isinstance(k, str) for k in my_keys
            ):
                raise ValueError("My_keys must be a list of strings if provided.")
        else:
            my_keys = []

        if not phrases:
            print("Warning: Empty phrases list passed to ClusterByUserKeys.")

        super().__init__(phrases)
        self.clusters = clusters
        self.my_keys = my_keys

    def cluster(self) -> Tuple[Dict[str, List[str]], List[str]]:
        """
        Perform clustering based on user-defined keywords.

        Returns:
            Tuple[Dict[str, List[str]], List[str]]:
                - A dictionary mapping each keyword to phrases that contain it.
                - A list of phrases not matched to any keyword.
        """
        if not [word for word in self.my_keys if word.strip()]:
            return self.clusters, self.phrases

        for phrase in self.phrases:
            for key in self.my_keys:
                if key.lower() in phrase.lower():
                    self.clusters.setdefault(key, []).append(phrase)

        phrases_clusters = list(chain.from_iterable(self.clusters.values()))
        phrases_without_cluster = [
            item for item in self.phrases if item not in phrases_clusters
        ]

        return self.clusters, phrases_without_cluster


class ClusterUsingKMeans(ClusterPhrase):
    """
    Clusters phrases using BERT embeddings and the KMeans algorithm.
    Automatically selects an optimal number of clusters using the elbow method.
    """

    def __init__(
        self,
        phrases: List[str],
        clusters: Dict[str, List[str]] = None,
        min_clusters: int = 5,
        max_clusters: int = 25,
    ):
        """
        Args:
            phrases (List[str]): A list of phrases to cluster.
            clusters (Dict[str, List[str]], optional): Predefined clusters.
            min_clusters (int): Minimum number of clusters to try.
            max_clusters (int): Maximum number of clusters to try.
        """
        if not isinstance(phrases, list) or not all(
            isinstance(p, str) for p in phrases
        ):
            raise ValueError("Phrases must be a list of strings.")

        if clusters is not None:
            if not isinstance(clusters, dict) or not all(
                isinstance(k, str) and isinstance(v, list) for k, v in clusters.items()
            ):
                raise ValueError(
                    "Clusters must be a dictionary with string keys and list-of-strings values."
                )
        else:
            clusters = {}

        if not isinstance(min_clusters, int) or not isinstance(max_clusters, int):
            raise ValueError("min_clusters and max_clusters must be integers.")

        if min_clusters < 1 or max_clusters < 1:
            raise ValueError("min_clusters and max_clusters must be positive integers.")

        if min_clusters > max_clusters:
            raise ValueError("min_clusters cannot be greater than max_clusters.")

        if not phrases:
            print("Warning: Empty phrases list passed to ClusterUsingKMeans.")

        super().__init__(phrases)
        self.clusters = clusters
        self.min_clusters = min_clusters
        self.max_clusters = max_clusters

    def cluster(self) -> Dict[str, List[str]]:
        """
        Cluster phrases using Sentence-BERT embeddings and KMeans.

        Returns:
            Dict[str, List[str]]: Dictionary of clusters with descriptive names
            as keys and lists of phrases as values.
        """
        if not self.phrases:
            print("No phrases to cluster.")
            return self.clusters
        # Download Bert model
        model = SentenceTransformer("all-MiniLM-L6-v2")
        # Transform phrases into embedding vectors using model
        embeddings = model.encode(self.phrases)
        # Find optimal k using elbow method
        inertias = []
        for k in range(self.min_clusters, self.max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=None)
            kmeans.fit(embeddings)
            inertias.append(kmeans.inertia_)
        # Use gradient to determine the optimal number of clusters
        gradient = np.gradient(inertias)
        optimal_k = np.argmax(gradient) + self.min_clusters

        kmeans = KMeans(n_clusters=optimal_k, random_state=None)
        labels = kmeans.fit_predict(embeddings)

        clustered_phrases = defaultdict(list)
        # clustered_phrases = {}
        for label, phrase in zip(labels, self.phrases):
            clustered_phrases[label].append(phrase)

        # Create meaningful cluster names based on the most common words
        cluster_names = {}
        for label, phrases_in_cluster in clustered_phrases.items():
            if label == -1:
                continue

            all_words = [
                word
                for phrase in phrases_in_cluster
                for word in re.findall(r"\b\w+\b", phrase.lower())
                if word not in stop_words
            ]
            top_words = [word for word, _ in Counter(all_words).most_common(3)]
            cluster_names[label] = " / ".join(top_words)

        for label, phrases_in_cluster in clustered_phrases.items():
            name = (
                "No cluster chosen"
                if label == -1
                else cluster_names.get(label, f"Cluster {label}")
            )
            self.clusters[name] = phrases_in_cluster

        return self.clusters
