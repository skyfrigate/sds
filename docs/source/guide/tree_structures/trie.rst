.. _guide_tree_trie:

==========
Trie Guide
==========

.. currentmodule:: sds.tree

Introduction
============

A **Trie** (pronounced "try"), also called a **prefix tree** or **digital tree**, is a specialized tree structure for storing strings where nodes represent prefixes. Each path from root to a node represents a string, and common prefixes are shared. Tries enable extremely efficient prefix-based operations, making them ideal for autocomplete, spell checking, and dictionary implementations.

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
       style C fill:#3498db,color:#fff
       style D fill:#3498db,color:#fff
       style CA fill:#2ecc71,color:#fff
       style DO fill:#2ecc71,color:#fff
       style CAT fill:#e74c3c,color:#fff
       style CAR fill:#e74c3c,color:#fff
       style CARD fill:#e74c3c,color:#fff
       style DOG fill:#e74c3c,color:#fff
       style DOOR fill:#e74c3c,color:#fff

.. note::
   
   Tries are ideal when you need fast prefix operations. Unlike hash tables
   that provide O(1) exact lookups, Tries offer O(m) prefix searches where
   m is the prefix length, making them perfect for autocomplete systems.

Mathematical Model
==================

Formal Definition
-----------------

Trie Structure
^^^^^^^^^^^^^^

A Trie :math:`T` is a rooted tree where:

1. **Each edge is labeled with a character**

   .. math::

      \forall edge \in T: label(edge) \in \Sigma

   where :math:`\Sigma` is the alphabet (e.g., lowercase letters, ASCII, Unicode)

2. **Each node represents a prefix**

   .. math::

      prefix(node) = \text{concatenation of edge labels from root to node}

3. **Words are marked at terminal nodes**

   .. math::

      \forall word \in T: \exists node : prefix(node) = word \land isEndOfWord(node) = true

4. **No two edges from same node have same label**

   .. math::

      \forall node, \forall e_1, e_2 \in children(node): label(e_1) \neq label(e_2)

Node Definition
^^^^^^^^^^^^^^^

A TrieNode contains:

.. code-block:: text

   TrieNode:
       children: Map<Character, TrieNode>
       isEndOfWord: Boolean
       
       // Optional enhancements:
       frequency: Integer (word count)
       value: Any (associated data)

The **children map** provides O(1) access to child nodes by character.

Tree Properties
---------------

Space Complexity
^^^^^^^^^^^^^^^^

**Best case** (no shared prefixes):

.. math::

   Space = \sum_{i=1}^{n} len(word_i) = O(nm)

where :math:`n` is the number of words and :math:`m` is average word length.

**Worst case** (all words share prefixes):

.. math::

   Space = len(\text{longest word}) = O(m)

**Average case** (typical dictionary):

.. math::

   Space \approx O(nm \cdot \alpha)

where :math:`\alpha` is the **sharing factor** (typically 0.3-0.7 for natural languages).

Height and Depth
^^^^^^^^^^^^^^^^

**Maximum height**:

.. math::

   h_{max} = \max_i len(word_i)

**Average depth** for random words:

.. math::

   d_{avg} \approx \log_{|\Sigma|} n

But for natural language with common prefixes, depth is much smaller.

Prefix Sharing
^^^^^^^^^^^^^^

For :math:`n` words from alphabet :math:`\Sigma`:

**Number of nodes**:

.. math::

   nodes \leq n \cdot m

**Shared prefix savings**:

.. math::

   \text{savings} = \frac{\sum len(word_i) - nodes}{sum len(word_i)}

For English words, savings typically reach 40-60%.

Algorithmic Model
=================

Abstract Data Type
------------------

.. code-block:: text

   ADT Trie:
       Data:
           - root: TrieNode
           - size: number of words
           - alphabet: character set Σ
       
       TrieNode:
           - children: Map<Char, TrieNode>
           - isEndOfWord: boolean
           - frequency: integer (optional)
       
       Operations:
           - Trie(): create empty trie
           - insert(word): add word to trie
           - search(word): check if exact word exists
           - startsWith(prefix): check if any word has prefix
           - remove(word): delete word from trie
           - autocomplete(prefix): get all words with prefix
           - countPrefix(prefix): count words with prefix
       
       Invariants:
           - Root has no character
           - Each path represents unique prefix
           - Word endpoints marked with isEndOfWord

Search Algorithm
----------------

Exact Word Search
^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: TRIE_SEARCH(trie, word)
   Input: Trie trie, string word
   Output: true if word exists, false otherwise
   
   1. node ← trie.root
   2. 
   3. // Traverse down the trie following characters
   4. for each char in word do
   5.     if char not in node.children then
   6.         return false
   7.     end if
   8.     node ← node.children[char]
   9. end for
   10. 
   11. // Check if we reached end of a word
   12. return node.isEndOfWord

**Time complexity**: O(m) where m = len(word)
**Space complexity**: O(1)

**Key insight**: Time is independent of number of words in trie!

Prefix Search
^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: TRIE_STARTS_WITH(trie, prefix)
   Input: Trie trie, string prefix
   Output: true if any word starts with prefix
   
   1. node ← trie.root
   2. 
   3. for each char in prefix do
   4.     if char not in node.children then
   5.         return false
   6.     end if
   7.     node ← node.children[char]
   8. end for
   9. 
   10. return true  // Prefix exists

**Time complexity**: O(p) where p = len(prefix)

Insertion Algorithm
-------------------

.. code-block:: text

   Algorithm: TRIE_INSERT(trie, word)
   Input: Trie trie, string word
   Output: Updated trie containing word
   
   1. node ← trie.root
   2. 
   3. // Create nodes for each character
   4. for each char in word do
   5.     if char not in node.children then
   6.         node.children[char] ← TrieNode()
   7.     end if
   8.     node ← node.children[char]
   9. end for
   10. 
   11. // Mark end of word
   12. if not node.isEndOfWord then
   13.    node.isEndOfWord ← true
   14.    trie.size ← trie.size + 1
   15. end if

**Time complexity**: O(m) where m = len(word)
**Space complexity**: O(m) worst case (new word with no shared prefix)

**Visualization**:

.. code-block:: text

   Insert "cat":
   root → c → a → t (marked)
   
   Insert "car":
   root → c → a → t (marked)
              ↓
              r (marked)  // Shares "ca" prefix

Deletion Algorithm
------------------

Deletion is more complex as we must remove unnecessary nodes:

.. code-block:: text

   Algorithm: TRIE_DELETE(trie, word)
   Input: Trie trie, string word
   Output: true if deleted, false if not found
   
   1. if not TRIE_SEARCH(trie, word) then
   2.     return false
   3. end if
   4. 
   5. success ← DELETE_RECURSIVE(trie.root, word, 0)
   6. if success then
   7.     trie.size ← trie.size - 1
   8. end if
   9. return success

.. code-block:: text

   Algorithm: DELETE_RECURSIVE(node, word, index)
   Input: Current node, word, position in word
   Output: true if current node should be deleted
   
   1. // Base case: reached end of word
   2. if index = len(word) then
   3.     if not node.isEndOfWord then
   4.         return false
   5.     end if
   6.     node.isEndOfWord ← false
   7.     
   8.     // Delete node if it has no children
   9.     return len(node.children) = 0
   10. end if
   11. 
   12. // Recursive case
   13. char ← word[index]
   14. if char not in node.children then
   15.    return false
   16. end if
   17. 
   18. child ← node.children[char]
   19. shouldDeleteChild ← DELETE_RECURSIVE(child, word, index+1)
   20. 
   21. if shouldDeleteChild then
   22.    delete node.children[char]
   23.    
   24.    // Delete current node if:
   25.    // 1. Not end of another word
   26.    // 2. No other children
   27.    return not node.isEndOfWord and len(node.children) = 0
   28. end if
   29. 
   30. return false

**Time complexity**: O(m)
**Space complexity**: O(m) for recursion stack

Autocomplete Algorithm
----------------------

.. code-block:: text

   Algorithm: AUTOCOMPLETE(trie, prefix, limit)
   Input: Trie trie, string prefix, max results
   Output: List of words starting with prefix
   
   1. results ← []
   2. 
   3. // Navigate to prefix node
   4. node ← trie.root
   5. for each char in prefix do
   6.     if char not in node.children then
   7.         return []  // Prefix doesn't exist
   8.     end if
   9.     node ← node.children[char]
   10. end for
   11. 
   12. // Collect all words from this node
   13. COLLECT_WORDS(node, prefix, results, limit)
   14. return results

.. code-block:: text

   Algorithm: COLLECT_WORDS(node, current, results, limit)
   Input: Current node, current string, results list, limit
   Output: Results list populated with words
   
   1. if limit and len(results) ≥ limit then
   2.     return
   3. end if
   4. 
   5. // If current position is end of word, add it
   6. if node.isEndOfWord then
   7.     results.append(current)
   8. end if
   9. 
   10. // Recursively collect from children (alphabetically)
   11. for each (char, child) in sorted(node.children) do
   12.    COLLECT_WORDS(child, current + char, results, limit)
   13. end for

**Time complexity**: O(p + n·k) where:
- p = len(prefix)
- n = number of matching words
- k = average word length

**Space complexity**: O(n·k) for results

Complexity Analysis
-------------------

Time Complexity
^^^^^^^^^^^^^^^

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

**Key advantage**: Search time independent of number of words!

Space Complexity
^^^^^^^^^^^^^^^^

* **Best case**: O(m) - all words identical
* **Worst case**: O(nm) - no shared prefixes
* **Average case**: O(nm·α) where α ∈ [0.3, 0.7]

**Memory per node**:
- HashMap/Array for children: 26-256 pointers
- Boolean flag: 1 bit
- Total: typically 200-2000 bytes per node

**Space optimization techniques**:
1. **Compressed Tries (Radix Trees)**: Merge chains of single-child nodes
2. **Alphabet reduction**: Use smaller character sets
3. **Lazy deletion**: Mark nodes as deleted without removing

Practical Usage
===============

Installation and Import
-----------------------

.. code-block:: python

   # Install
   pip install sds-tools
   
   # Import
   from sds.tree import Trie

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

Real-World Applications
=======================

Application 1: Autocomplete System
-----------------------------------

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
   # Output: ['python', 'programming', 'powerful', 'popular', ...]
   
   # User selects "python" - boost its ranking
   ac.record_selection("python")

Application 2: Spell Checker
-----------------------------

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
   
   # Usage
   # spell_checker = SpellChecker('dictionary.txt')
   # 
   # # Check single word
   # corrections = spell_checker.suggest_corrections("recieve")
   # print(corrections)  # ['receive']
   # 
   # # Check text
   # text = "Teh quck brown fox jumpd"
   # errors = spell_checker.check_text(text)
   # print(errors)
   # # {'teh': ['the'], 'quck': ['quick'], 'jumpd': ['jump', 'jumped']}

Application 3: IP Router
-------------------------

Longest prefix matching for routing:

.. code-block:: python

   from sds.tree import Trie

   class IPRouter:
       """IP routing table using Trie for longest prefix match."""
       
       def __init__(self):
           self.trie = Trie()
           self.routes = {}
       
       def add_route(self, prefix, next_hop):
           """Add routing entry."""
           # Convert IP prefix to binary string
           # e.g., "192.168.1.0/24" -> "11000000101010000000000100000000"
           binary = self._ip_to_binary(prefix)
           self.trie.insert(binary)
           self.routes[binary] = next_hop
       
       def route(self, ip_address):
           """Find next hop using longest prefix match."""
           binary = self._ip_to_binary_address(ip_address)
           
           # Find longest matching prefix
           longest_match = ""
           for i in range(1, len(binary) + 1):
               prefix = binary[:i]
               if self.trie.starts_with(prefix):
                   if self.trie.search(prefix):
                       longest_match = prefix
           
           if longest_match:
               return self.routes[longest_match]
           return None  # No route
       
       def _ip_to_binary(self, ip_prefix):
           """Convert IP prefix to binary string."""
           # Simplified implementation
           ip, bits = ip_prefix.split('/')
           octets = [int(x) for x in ip.split('.')]
           binary = ''.join(f'{x:08b}' for x in octets)
           return binary[:int(bits)]
       
       def _ip_to_binary_address(self, ip):
           """Convert IP address to binary."""
           octets = [int(x) for x in ip.split('.')]
           return ''.join(f'{x:08b}' for x in octets)
   
   # Usage
   router = IPRouter()
   
   # Add routes
   router.add_route("192.168.0.0/16", "Gateway-A")
   router.add_route("192.168.1.0/24", "Gateway-B")
   router.add_route("10.0.0.0/8", "Gateway-C")
   
   # Route packets
   print(router.route("192.168.1.50"))   # Gateway-B (most specific)
   print(router.route("192.168.2.50"))   # Gateway-A
   print(router.route("10.5.1.1"))       # Gateway-C

Application 4: Search Engine Index
-----------------------------------

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
   search.index_document(
       "Java programming language basics",
       metadata={'title': 'Java Intro', 'author': 'Carol'}
   )
   
   # Search
   results = search.search("python")
   print(f"Found {len(results)} documents for 'python'")
   
   # Prefix search
   results = search.search_prefix("prog")
   print(f"Found {len(results)} documents with 'prog*'")
   
   # Suggestions
   suggestions = search.suggest("pro")
   print(f"Suggestions: {suggestions}")

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

Further Reading
===============

* :doc:`/api/tree/trie` - Complete API reference
* :doc:`general` - General tree structures
* :doc:`binary` - Binary search trees

References
==========

.. [WikiTrie] Wikipedia contributors. "Trie". Wikipedia.
   https://en.wikipedia.org/wiki/Trie
   
   Comprehensive overview of Trie structure and applications.

.. [Fredkin] Fredkin, E. "Trie Memory", 1960
   
   Original paper introducing the Trie data structure.

.. [CLRS] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition
   
   String matching algorithms including Tries.

.. [VisuAlgo] Halim, S. "Trie Visualization". VisuAlgo.
   https://visualgo.net/en/trie (if available)
   
   Interactive Trie visualization.

.. [Algorithms4] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition
   https://algs4.cs.princeton.edu/52trie/
   
   Chapter on string searching with Tries and TSTs.

.. [OpenDSATrie] OpenDSA Project. "Trie".
   https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/Trie.html
   
   Interactive Trie tutorial with exercises.
