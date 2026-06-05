.. _api_tree_trie:

====
Trie
====

.. currentmodule:: sds.tree.trie

Overview
========

This module provides a Trie (prefix tree) implementation optimized for string operations.
Tries enable efficient prefix-based searches, making them ideal for autocomplete systems,
spell checkers, and dictionary implementations.

.. mermaid::

   graph TB
       subgraph "Trie containing: cat, car, card, dog, door"
       ROOT[" "] --> C[c]
       ROOT --> D[d]
       
       C --> CA[a]
       CA --> CAT[t*]
       CA --> CAR[r*]
       CAR --> CARD[d*]
       
       D --> DO[o]
       DO --> DOG[g*]
       DO --> DOO[o]
       DOO --> DOOR[r*]
       end
       
       style ROOT fill:#95a5a6,color:#fff
       style CAT fill:#e74c3c,color:#fff
       style CAR fill:#e74c3c,color:#fff
       style CARD fill:#e74c3c,color:#fff
       style DOG fill:#e74c3c,color:#fff
       style DOOR fill:#e74c3c,color:#fff

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   Trie
   TrieNode

Detailed Documentation
======================

Trie
----

.. autoclass:: Trie
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __contains__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: size

   .. rubric:: Core Operations

   .. automethod:: insert
   .. automethod:: remove
   .. automethod:: search
   .. automethod:: starts_with

   .. rubric:: Prefix Operations

   .. automethod:: autocomplete
   .. automethod:: count_words_with_prefix
   .. automethod:: longest_common_prefix

   .. rubric:: Utility Methods

   .. automethod:: is_empty
   .. automethod:: clear

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __iter__
   .. automethod:: __contains__
   .. automethod:: __repr__
   .. automethod:: __str__

TrieNode
--------

.. autoclass:: TrieNode
   :members:
   :undoc-members:
   :show-inheritance:

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: children
   .. autoproperty:: is_end_of_word

Usage Examples
==============

Basic Operations
----------------

Creating and Populating
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.tree import Trie

   # Create empty trie
   trie = Trie()
   
   # Insert words
   trie.insert("cat")
   trie.insert("car")
   trie.insert("card")
   trie.insert("care")
   trie.insert("careful")
   
   print(f"Size: {len(trie)}")  # Output: 5

Building from Word List
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Build from dictionary
   words = ["apple", "application", "apply", "banana", "band"]
   
   trie = Trie()
   for word in words:
       trie.insert(word)
   
   # Or from file
   with open('dictionary.txt') as f:
       for line in f:
           trie.insert(line.strip().lower())

Searching
^^^^^^^^^

.. code-block:: python

   # Exact word search - O(m)
   print(trie.search("cat"))      # True
   print(trie.search("ca"))       # False (prefix, not word)
   print("car" in trie)           # True
   
   # Prefix search
   print(trie.starts_with("car"))  # True
   print(trie.starts_with("cat"))  # True
   print(trie.starts_with("dog"))  # False

Autocomplete
^^^^^^^^^^^^

.. code-block:: python

   # Get all words with prefix
   suggestions = trie.autocomplete("car")
   print(suggestions)
   # Output: ['car', 'card', 'care', 'careful']
   
   # Limit results
   top_3 = trie.autocomplete("car", limit=3)
   print(top_3)
   # Output: ['car', 'card', 'care']

Word Operations
^^^^^^^^^^^^^^^

.. code-block:: python

   # Count words with prefix
   count = trie.count_words_with_prefix("car")
   print(count)  # Output: 4
   
   # Get all words
   all_words = list(trie)
   print(sorted(all_words))
   # Output: ['car', 'card', 'care', 'careful', 'cat']
   
   # Remove word
   trie.remove("careful")
   print(trie.search("careful"))  # False
   print(trie.search("care"))     # True (still exists)

Real-World Examples
===================

Example 1: Autocomplete System
-------------------------------

Production-ready autocomplete with ranking:

.. code-block:: python

   from sds.tree import Trie
   from collections import Counter

   class AutocompleteSystem:
       """Autocomplete with frequency-based ranking."""
       
       def __init__(self):
           self.trie = Trie()
           self.frequencies = Counter()
       
       def add_word(self, word, frequency=1):
           """Add word with usage frequency."""
           word = word.lower()
           self.trie.insert(word)
           self.frequencies[word] += frequency
       
       def add_corpus(self, text):
           """Build from text corpus."""
           import re
           words = re.findall(r'\w+', text.lower())
           for word in words:
               self.add_word(word)
       
       def suggest(self, prefix, max_results=10):
           """Get suggestions ranked by frequency."""
           prefix = prefix.lower()
           
           # Get all matching words
           candidates = self.trie.autocomplete(prefix)
           
           # Rank by frequency
           ranked = sorted(
               candidates,
               key=lambda w: self.frequencies[w],
               reverse=True
           )
           
           return ranked[:max_results]
       
       def record_selection(self, word):
           """Update frequency when user selects word."""
           self.frequencies[word] += 1
   
   # Usage
   ac = AutocompleteSystem()
   
   # Build from corpus
   corpus = """
   The quick brown fox jumps over the lazy dog.
   Python programming is powerful and popular.
   People prefer Python for data science projects.
   """
   ac.add_corpus(corpus)
   
   # Get suggestions
   suggestions = ac.suggest("p")
   print(f"Suggestions for 'p': {suggestions}")

Example 2: Spell Checker
-------------------------

Spell checking with suggestions:

.. code-block:: python

   from sds.tree import Trie

   class SpellChecker:
       """Spell checker with correction suggestions."""
       
       def __init__(self, dictionary_file):
           self.trie = Trie()
           self._load_dictionary(dictionary_file)
       
       def _load_dictionary(self, filename):
           """Load dictionary into trie."""
           with open(filename) as f:
               for line in f:
                   word = line.strip().lower()
                   if word:
                       self.trie.insert(word)
       
       def is_correct(self, word):
           """Check if word is spelled correctly."""
           return self.trie.search(word.lower())
       
       def suggest_corrections(self, word, max_distance=2):
           """Suggest corrections using edit distance."""
           word = word.lower()
           
           if self.is_correct(word):
               return [word]
           
           suggestions = set()
           
           # Try single character edits
           for i in range(len(word) + 1):
               # Insertions
               for c in 'abcdefghijklmnopqrstuvwxyz':
                   candidate = word[:i] + c + word[i:]
                   if self.trie.search(candidate):
                       suggestions.add(candidate)
               
               if i < len(word):
                   # Deletions
                   candidate = word[:i] + word[i+1:]
                   if self.trie.search(candidate):
                       suggestions.add(candidate)
                   
                   # Substitutions
                   for c in 'abcdefghijklmnopqrstuvwxyz':
                       if c != word[i]:
                           candidate = word[:i] + c + word[i+1:]
                           if self.trie.search(candidate):
                               suggestions.add(candidate)
               
               # Transpositions
               if i < len(word) - 1:
                   candidate = (word[:i] + word[i+1] + 
                               word[i] + word[i+2:])
                   if self.trie.search(candidate):
                       suggestions.add(candidate)
           
           return sorted(suggestions)[:10]
       
       def check_text(self, text):
           """Check entire text and suggest corrections."""
           import re
           words = re.findall(r'\w+', text.lower())
           
           errors = {}
           for word in words:
               if not self.is_correct(word):
                   errors[word] = self.suggest_corrections(word)
           
           return errors
   
   # Usage (requires dictionary file)
   # spell_checker = SpellChecker('dictionary.txt')
   # corrections = spell_checker.suggest_corrections("recieve")
   # print(corrections)  # ['receive']

Example 3: Search Engine Index
-------------------------------

Inverted index with prefix search:

.. code-block:: python

   from sds.tree import Trie
   from collections import defaultdict

   class SearchEngine:
       """Simple search engine using Trie."""
       
       def __init__(self):
           self.word_trie = Trie()
           self.documents = {}
           self.inverted_index = defaultdict(set)
           self.doc_id = 0
       
       def index_document(self, text, metadata=None):
           """Index a document."""
           doc_id = self.doc_id
           self.doc_id += 1
           
           # Store document
           self.documents[doc_id] = {
               'text': text,
               'metadata': metadata or {}
           }
           
           # Tokenize and index
           import re
           words = set(re.findall(r'\w+', text.lower()))
           
           for word in words:
               self.word_trie.insert(word)
               self.inverted_index[word].add(doc_id)
           
           return doc_id
       
       def search(self, query):
           """Search for documents containing query."""
           query = query.lower()
           
           if not self.word_trie.search(query):
               return []
           
           # Get documents containing exact word
           doc_ids = self.inverted_index[query]
           return [self.documents[doc_id] for doc_id in doc_ids]
       
       def search_prefix(self, prefix):
           """Search for documents containing words with prefix."""
           prefix = prefix.lower()
           
           # Get all words with this prefix
           words = self.word_trie.autocomplete(prefix)
           
           # Collect all documents
           doc_ids = set()
           for word in words:
               doc_ids.update(self.inverted_index[word])
           
           return [self.documents[doc_id] for doc_id in doc_ids]
       
       def suggest(self, partial):
           """Suggest query completions."""
           return self.word_trie.autocomplete(partial.lower(), limit=10)
   
   # Usage
   search = SearchEngine()
   
   # Index documents
   search.index_document(
       "Python is a powerful programming language",
       metadata={'title': 'Python Tutorial', 'author': 'Alice'}
   )
   search.index_document(
       "Python programming for data science",
       metadata={'title': 'Data Science Guide', 'author': 'Bob'}
   )
   
   # Search
   results = search.search("python")
   print(f"Found {len(results)} documents for 'python'")
   
   # Prefix search
   results = search.search_prefix("prog")
   print(f"Found {len(results)} documents with 'prog*'")

Performance Characteristics
===========================

Time Complexity
---------------

.. list-table::
   :header-rows: 1
   :widths: 35 20 40

   * - Operation
     - Complexity
     - Notes
   * - **Insert**
     - O(m)
     - m = word length
   * - **Search**
     - O(m)
     - Independent of # words!
   * - **Delete**
     - O(m)
     - May need to remove nodes
   * - **Prefix check**
     - O(p)
     - p = prefix length
   * - **Autocomplete**
     - O(p + nk)
     - n results, length k
   * - **Count prefix**
     - O(p + nodes)
     - Traverse subtree
   * - **Longest common prefix**
     - O(m)
     - m = shortest word

Space Complexity
----------------

* **Best case**: O(m) - all words identical
* **Worst case**: O(nm) - no shared prefixes
* **Average case**: O(nm·α) where α ∈ [0.3, 0.7]
* **Memory per node**: Typically 200-2000 bytes (depends on alphabet size)

Comparison: Trie vs Hash Table
===============================

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Aspect
     - Trie
     - Hash Table
   * - **Exact lookup**
     - O(m)
     - O(1) average
   * - **Prefix search**
     - O(p)
     - O(n) - must check all
   * - **Sorted iteration**
     - O(n) - natural order
     - O(n log n) - must sort
   * - **Space**
     - O(nm·α) - shared prefixes
     - O(n) - exact size
   * - **Autocomplete**
     - O(p + results)
     - Impossible efficiently
   * - **Collisions**
     - None
     - Possible

When to Use Each
----------------

**Use Trie when:**
   - Need prefix operations
   - Autocomplete required
   - Sorted iteration needed
   - Natural language processing
   - Memory available

**Use Hash Table when:**
   - Only exact matches needed
   - Memory constrained
   - No prefix operations
   - Very large keys
   - Need O(1) lookups

Best Practices
==============

Do's
----

✅ **Use Tries for prefix operations**

.. code-block:: python

   # Perfect for:
   # - Autocomplete
   # - Spell checking
   # - IP routing
   # - Dictionary lookups

✅ **Normalize input**

.. code-block:: python

   # Always normalize case and encoding
   trie = Trie()
   trie.insert(word.lower().strip())

✅ **Consider memory trade-offs**

.. code-block:: python

   # Tries use more memory than hash tables
   # But enable prefix operations impossible with hashing

Don'ts
------

❌ **Don't use for exact-match-only lookups**

.. code-block:: python

   # Bad: If you only need exact matches
   # Use hash table instead - O(1) vs O(m)
   
   # Good: Use Trie when you need prefix operations
   suggestions = trie.autocomplete(prefix)

❌ **Don't forget about radix trees**

.. code-block:: python

   # For sparse data, radix trees save space
   # They compress chains of single-child nodes

❌ **Don't store huge words**

.. code-block:: python

   # Tries work best for:
   # - Normal words (2-15 characters)
   # - Short keys
   
   # Not ideal for:
   # - Very long strings
   # - Binary data
   # - Non-string keys

Common Pitfalls
===============

1. **Not normalizing input**

.. code-block:: python

   # Always lowercase/normalize
   trie.insert(word.lower())

2. **Using for non-string data**

.. code-block:: python

   # Tries are optimized for strings
   # For other data, consider alternatives

3. **Ignoring memory usage**

.. code-block:: python

   # Each node can use significant memory
   # Monitor usage with large dictionaries

See Also
========

* :doc:`general` - General tree structures
* :doc:`binary` - Binary search trees
* :doc:`../../guide/tree_structures/trie` - Trie theory and guide

References
==========

.. [1] Fredkin, E. "Trie Memory", 1960
.. [2] Knuth, D. E. "The Art of Computer Programming, Volume 3"
.. [3] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition
.. [4] Morrison, D. R. "PATRICIA—Practical Algorithm To Retrieve Information Coded in Alphanumeric", 1968
