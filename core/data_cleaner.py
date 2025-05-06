"""
Module providing classes for cleaning phrases from datasets.

- `RemoveDuplicates` removes duplicate phrases based on lemmatized content.
- `RemoveTrashPhrase` removes phrases containing user-defined trash words.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

stop_words = stopwords.words("english")
lemmatizer = WordNetLemmatizer()


class RemovePhrase(ABC):
    """
    Abstract base class for removing phrases based on specific conditions.
    """

    def __init__(self, phrases: List[str]):
        """
        Initialize the base class with a list of phrases.

        Args:
            phrases (List[str]): List of phrases to clean.
        """
        self.phrases = phrases

    @abstractmethod
    def delete(self) -> Tuple[List[str], List[str]]:
        """
        Delete phrases based on specific conditions.

        Returns:
            Tuple[List[str], List[str]]: A tuple with:
              - List of cleaned (retained) phrases.
              - List of removed (filtered out) phrases.
        """


class RemoveDuplicates(RemovePhrase):
    """
    Removes duplicate phrases ignoring case, word order, stopwords, and lemmatization.
    """

    def _lemmatize_phrase(self, phrase: str) -> str:
        """
        Normalize a phrase by lowercasing, removing stopwords, and lemmatizing.

        Args:
            phrase (str): Phrase to normalize.

        Returns:
            str: Normalized phrase string.
        """
        words = word_tokenize(phrase.lower())
        lemmatized_words = [
            lemmatizer.lemmatize(word)
            for word in words
            if word.isalnum() and word not in stop_words
        ]
        return " ".join(lemmatized_words)

    def delete(self) -> Tuple[List[str], List[str]]:
        """
        Remove duplicate phrases based on lemmatized and normalized form.

        Returns:
            Tuple[List[str], List[str]]: A tuple with:
              - List of unique phrases.
              - List of removed duplicate phrases.
        """
        unique_phrases = []
        seen = set()
        deleted_phrases = []
        print(f"[DEBUG] First 5 phrases for check: {self.phrases[:5]}")
        for phrase in self.phrases:
            sorted_phrase = " ".join(sorted(phrase.lower().split()))
            lemmatized = self._lemmatize_phrase(sorted_phrase)

            if not any(lemmatized == seen_phrase for seen_phrase in seen):
                unique_phrases.append(phrase)
                seen.add(lemmatized)
            else:
                deleted_phrases.append(phrase)

        return unique_phrases, deleted_phrases


class RemoveTrashPhrase(RemovePhrase):
    """
    Removes phrases that contain user-specified 'trash words'.
    """

    def __init__(self, phrases: List[str], trash_words: List[str]):
        """
        Initialize with phrases and trash words.

        Args:
            phrases (List[str]): List of phrases to check.
            trash_words (List[str]): List of words to be treated as trash.
        """
        super().__init__(phrases)
        self.trash_words = trash_words

    def delete(self) -> Tuple[List[str], List[str]]:
        """
        Remove phrases that contain any trash words.

        Returns:
            Tuple[List[str], List[str]]: A tuple with:
              - List of phrases without trash words.
              - List of removed phrases containing trash words.
        """
        if not [word for word in self.trash_words if word.strip()]:
            return self.phrases, []

        phrases_without_trash_words = []
        deleted_phrases = []
        for phrase in self.phrases:
            if not any(word in phrase for word in self.trash_words):
                phrases_without_trash_words.append(phrase)
            else:
                deleted_phrases.append(phrase)

        return phrases_without_trash_words, deleted_phrases
