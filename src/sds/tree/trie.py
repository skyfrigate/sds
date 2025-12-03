# Copyright 2024-205, skyfrigate, biface
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Trie (Prefix Tree / Digital Tree) implementation.

This module provides a Trie data structure, also known as a prefix tree or
digital tree. A Trie is an ordered tree structure used to store strings where
common prefixes are shared, making it very efficient for prefix-based searches.

Classes
-------
TrieNode
    Node for the Trie structure with character mapping.
Trie
    Trie implementation for efficient string storage and retrieval.

Examples
--------
Basic usage:

>>> from sds.tree.trie import Trie
>>> trie = Trie()
>>> trie.insert("cat")
>>> trie.insert("car")
>>> trie.insert("card")
>>> trie.search("car")
True
>>> trie.starts_with("ca")
True

Autocompletion:

>>> trie = Trie()
>>> words = ["hello", "help", "helmet", "hero"]
>>> for word in words:
...     trie.insert(word)
>>> trie.autocomplete("hel")
['hello', 'help', 'helmet']

Notes
-----
Tries are particularly useful for:
- Autocomplete/suggestions
- Spell checking
- IP routing tables
- Dictionary implementations
- Pattern matching

Time Complexity:
- Insert: O(m) where m is the key length
- Search: O(m)
- Prefix search: O(p) where p is the prefix length
- Delete: O(m)

Space Complexity: O(ALPHABET_SIZE * N * M) where N is number of keys
and M is average key length, but shared prefixes save space.

See Also
--------
sds.tree.general : General tree structure.
"""

from typing import Iterator, List, Optional

from ..core.interfaces import Collection
from .node import TrieNode

__all__ = ["Trie"]


class Trie(Collection):
    """Trie (Prefix Tree) implementation for efficient string operations.

    A Trie is a tree-like data structure where each node represents a
    character. Words are formed by paths from the root to nodes marked
    as end-of-word. This structure allows efficient prefix-based operations.

    Attributes
    ----------
    size : int
        The number of words stored in the trie (read-only property).

    Examples
    --------
    Create and populate a trie:

    >>> trie = Trie()
    >>> trie.insert("apple")
    >>> trie.insert("app")
    >>> trie.insert("application")
    >>> len(trie)
    3

    Search operations:

    >>> trie.search("app")
    True
    >>> trie.search("appl")
    False
    >>> trie.starts_with("app")
    True

    Autocomplete:

    >>> suggestions = trie.autocomplete("app")
    >>> sorted(suggestions)
    ['app', 'apple', 'application']

    Remove words:

    >>> trie.remove("app")
    >>> trie.search("app")
    False
    >>> trie.search("apple")  # Other words unaffected
    True

    Notes
    -----
    Time Complexity (m = word length, p = prefix length):
    - insert: O(m)
    - search: O(m)
    - starts_with: O(p)
    - remove: O(m)
    - autocomplete: O(p + n) where n is number of completions

    Space Complexity:
    - Worst case: O(ALPHABET_SIZE * N * M)
    - Best case: O(N * M) when words share prefixes

    The Trie is case-sensitive by default. Convert to lowercase
    if case-insensitive behavior is desired.

    See Also
    --------
    TrieNode : Node class used internally.
    """

    def __init__(self):
        """Initialize an empty trie."""
        self._root = TrieNode()
        self._size = 0

    @property
    def size(self) -> int:
        """Get the number of words in the trie.

        Returns
        -------
        int
            Number of words stored.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.size
        0
        >>> trie.insert("word")
        >>> trie.size
        1
        """
        return self._size

    def insert(self, word: str) -> None:
        """Insert a word into the trie.

        Parameters
        ----------
        word : str
            The word to insert. Must be non-empty.

        Raises
        ------
        ValueError
            If word is empty.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("hello")
        >>> trie.search("hello")
        True

        >>> trie.insert("help")
        >>> len(trie)
        2

        Notes
        -----
        Time complexity: O(m) where m is the length of the word.
        If the word already exists, this operation has no effect
        on size but ensures the word is marked.
        """
        if not word:
            raise ValueError("Cannot insert empty string")

        node = self._root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]

        # Mark end of word and increment size if new word
        if not node.is_end_of_word:
            node.is_end_of_word = True
            self._size += 1

    def search(self, word: str) -> bool:
        """Search for a complete word in the trie.

        Parameters
        ----------
        word : str
            The word to search for.

        Returns
        -------
        bool
            True if the word exists, False otherwise.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("apple")
        >>> trie.search("apple")
        True
        >>> trie.search("app")
        False
        >>> trie.search("orange")
        False

        Notes
        -----
        Time complexity: O(m) where m is the length of the word.
        """
        if not word:
            return False

        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Check if any word in the trie starts with the given prefix.

        Parameters
        ----------
        prefix : str
            The prefix to search for.

        Returns
        -------
        bool
            True if at least one word has this prefix, False otherwise.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("apple")
        >>> trie.insert("application")
        >>> trie.starts_with("app")
        True
        >>> trie.starts_with("ora")
        False

        Notes
        -----
        Time complexity: O(p) where p is the length of the prefix.
        """
        if not prefix:
            return True  # Empty prefix matches everything

        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """Find the node corresponding to a prefix.

        Parameters
        ----------
        prefix : str
            The prefix to find.

        Returns
        -------
        TrieNode or None
            The node at the end of the prefix, or None if not found.
        """
        node = self._root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def remove(self, word: str) -> bool:
        """Remove a word from the trie.

        Parameters
        ----------
        word : str
            The word to remove.

        Returns
        -------
        bool
            True if the word was removed, False if it wasn't in the trie.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("hello")
        >>> trie.insert("help")
        >>> trie.remove("hello")
        True
        >>> trie.search("hello")
        False
        >>> trie.search("help")  # Other words unaffected
        True
        >>> trie.remove("world")
        False

        Notes
        -----
        Time complexity: O(m) where m is the length of the word.
        This operation only unmarks the end-of-word flag and removes
        nodes if they become unnecessary.
        """
        if not word or not self.search(word):
            return False

        self._remove_recursive(self._root, word, 0)
        self._size -= 1
        return True

    def _remove_recursive(self, node: TrieNode, word: str, index: int) -> bool:
        """Recursively remove a word from the trie.

        Parameters
        ----------
        node : TrieNode
            Current node.
        word : str
            The word to remove.
        index : int
            Current position in the word.

        Returns
        -------
        bool
            True if the current node should be deleted.
        """
        if index == len(word):
            # Reached end of word
            node.is_end_of_word = False
            # Return True if node has no children (can be deleted)
            return len(node.children) == 0

        char = word[index]
        child = node.children.get(char)

        if child is None:
            return False

        should_delete_child = self._remove_recursive(child, word, index + 1)

        if should_delete_child:
            del node.children[char]
            # Return True if current node can also be deleted
            return len(node.children) == 0 and not node.is_end_of_word

        return False

    def autocomplete(self, prefix: str, limit: Optional[int] = None) -> List[str]:
        """Get all words that start with the given prefix.

        Parameters
        ----------
        prefix : str
            The prefix to search for.
        limit : int, optional
            Maximum number of suggestions to return. Default is None (all).

        Returns
        -------
        List[str]
            List of words that start with the prefix.

        Examples
        --------
        >>> trie = Trie()
        >>> words = ["cat", "car", "card", "care", "careful"]
        >>> for word in words:
        ...     trie.insert(word)
        >>> trie.autocomplete("car")
        ['car', 'card', 'care', 'careful']
        >>> trie.autocomplete("car", limit=2)
        ['car', 'card']

        Notes
        -----
        Time complexity: O(p + n*m) where:
        - p is the length of the prefix
        - n is the number of matching words
        - m is the average length of matching words
        """
        if not prefix:
            # Return all words if no prefix given
            return list(self)[:limit] if limit else list(self)

        node = self._find_node(prefix)
        if node is None:
            return []

        results: List[str] = []
        self._collect_words(node, prefix, results, limit)
        return results

    def _collect_words(
        self,
        node: TrieNode,
        current_word: str,
        results: List[str],
        limit: Optional[int],
    ) -> None:
        """Collect all words from a node using DFS.

        Parameters
        ----------
        node : TrieNode
            Current node.
        current_word : str
            Word formed so far.
        results : List[str]
            List to accumulate results.
        limit : int or None
            Maximum number of results to collect.
        """
        if limit is not None and len(results) >= limit:
            return

        if node.is_end_of_word:
            results.append(current_word)

        for char, child in sorted(node.children.items()):
            self._collect_words(child, current_word + char, results, limit)

    def words_with_prefix(self, prefix: str) -> List[str]:
        """Alias for autocomplete with no limit.

        Parameters
        ----------
        prefix : str
            The prefix to search for.

        Returns
        -------
        List[str]
            All words starting with the prefix.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("test")
        >>> trie.insert("testing")
        >>> trie.words_with_prefix("test")
        ['test', 'testing']
        """
        return self.autocomplete(prefix)

    def longest_common_prefix(self) -> str:
        """Find the longest common prefix of all words.

        Returns
        -------
        str
            The longest common prefix, or empty string if none.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("flower")
        >>> trie.insert("flow")
        >>> trie.insert("flight")
        >>> trie.longest_common_prefix()
        'fl'

        >>> trie = Trie()
        >>> trie.insert("dog")
        >>> trie.insert("cat")
        >>> trie.longest_common_prefix()
        ''

        Notes
        -----
        Time complexity: O(m) where m is the length of the shortest word.
        """
        if self.is_empty():
            return ""

        prefix = []
        node = self._root

        while len(node.children) == 1 and not node.is_end_of_word:
            char, child = next(iter(node.children.items()))
            prefix.append(char)
            node = child

        return "".join(prefix)

    def count_words_with_prefix(self, prefix: str) -> int:
        """Count how many words start with the given prefix.

        Parameters
        ----------
        prefix : str
            The prefix to search for.

        Returns
        -------
        int
            Number of words with this prefix.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("cat")
        >>> trie.insert("car")
        >>> trie.insert("card")
        >>> trie.count_words_with_prefix("car")
        2

        Notes
        -----
        Time complexity: O(p + n) where p is prefix length
        and n is the size of the subtree.
        """
        node = self._find_node(prefix)
        if node is None:
            return 0

        return self._count_words(node)

    def _count_words(self, node: TrieNode) -> int:
        """Count all words in subtree rooted at node.

        Parameters
        ----------
        node : TrieNode
            Root of subtree.

        Returns
        -------
        int
            Number of words in subtree.
        """
        count = 1 if node.is_end_of_word else 0
        for child in node.children.values():
            count += self._count_words(child)
        return count

    def clear(self) -> None:
        """Remove all words from the trie.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("hello")
        >>> trie.clear()
        >>> trie.is_empty()
        True

        Notes
        -----
        Time complexity: O(1)
        """
        self._root = TrieNode()
        self._size = 0

    def __len__(self) -> int:
        """Return the number of words in the trie.

        Returns
        -------
        int
            Number of words.

        Examples
        --------
        >>> trie = Trie()
        >>> len(trie)
        0
        >>> trie.insert("word")
        >>> len(trie)
        1
        """
        return self._size

    def is_empty(self) -> bool:
        """Check if the trie is empty.

        Returns
        -------
        bool
            True if empty, False otherwise.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.is_empty()
        True
        >>> trie.insert("word")
        >>> trie.is_empty()
        False
        """
        return self._size == 0

    def __contains__(self, word: str) -> bool:
        """Check if a word is in the trie.

        Parameters
        ----------
        word : str
            The word to check.

        Returns
        -------
        bool
            True if word exists in trie.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("hello")
        >>> "hello" in trie
        True
        >>> "world" in trie
        False
        """
        return self.search(word)

    def __iter__(self) -> Iterator[str]:
        """Iterate over all words in the trie.

        Yields
        ------
        str
            Words in lexicographic order.

        Examples
        --------
        >>> trie = Trie()
        >>> for word in ["cat", "car", "dog"]:
        ...     trie.insert(word)
        >>> list(trie)
        ['car', 'cat', 'dog']

        Notes
        -----
        Time complexity: O(n*m) where n is number of words
        and m is average word length.
        """
        results: List[str] = []
        self._collect_words(self._root, "", results, None)
        return iter(results)

    def __repr__(self) -> str:
        """Return string representation.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("word")
        >>> repr(trie)
        'Trie(size=1)'
        """
        return f"Trie(size={self._size})"

    def __str__(self) -> str:
        """Return string showing all words.

        Returns
        -------
        str
            String representation.

        Examples
        --------
        >>> trie = Trie()
        >>> trie.insert("cat")
        >>> trie.insert("car")
        >>> str(trie)
        "Trie: ['car', 'cat']"
        """
        if self.is_empty():
            return "Trie: []"

        words = list(self)
        if len(words) <= 10:
            return f"Trie: {words}"
        else:
            return f"Trie: [{', '.join(words[:10])}, ... ({len(words)} words)]"
