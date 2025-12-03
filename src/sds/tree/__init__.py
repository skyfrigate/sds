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

"""Tree data structures module.

This module provides various tree implementations including binary trees,
binary search trees, balanced trees, and heap structures.

Classes
-------
BinaryNode
    Node for binary tree structures.
TreeNode
    Node for general tree structures.
AVLNode
    Node for AVL tree with height tracking.
RedBlackNode
    Node for Red-Black tree with color attribute.
BinaryTree
    Simple binary tree implementation.
BinarySearchTree
    Binary search tree with ordering property.
AVLTree
    Self-balancing AVL tree.
RedBlackTree
    Self-balancing Red-Black tree.
MinHeap
    Min-heap implementation.
MaxHeap
    Max-heap implementation.
HeapPriorityQueue
    Optimized priority queue using min-heap.

Examples
--------
Using a B-Tree (for databases):

>>> from sds.tree import BTree
>>> btree = BTree(order=3)
>>> for i in [10, 20, 30, 40, 50]:
...     btree.insert(i)
>>> 30 in btree
True
>>> list(btree)
[10, 20, 30, 40, 50]

Using a Segment Tree (for range queries):

>>> from sds.tree import SegmentTree
>>> arr = [1, 3, 5, 7, 9, 11]
>>> tree = SegmentTree(arr, operation='sum')
>>> tree.query(1, 3)  # Sum of arr[1:4]
15
>>> tree.update(1, 10)
>>> tree.query(1, 3)
22

Using a Trie (Prefix Tree):

>>> from sds.tree import Trie
>>> trie = Trie()
>>> trie.insert("cat")
>>> trie.insert("car")
>>> trie.insert("card")
>>> trie.search("car")
True
>>> trie.autocomplete("ca")
['car', 'card', 'cat']

Using a General Tree (n-ary):

>>> from sds.tree import Tree
>>> tree = Tree("Root")
>>> tree.add_child("Child1")
TreeNode('Child1')
>>> tree.add_child("Child2")
TreeNode('Child2')
>>> tree.add_child_to("Child1", "Grandchild")
TreeNode('Grandchild')
>>> tree.height()
2

Using a Binary Tree:

>>> from sds.tree import BinaryTree
>>> tree = BinaryTree()
>>> tree.insert(10)
>>> tree.insert(5)
>>> tree.insert(15)
>>> list(tree.inorder_traversal())
[5, 10, 15]

Using a Binary Search Tree:

>>> from sds.tree import BinarySearchTree
>>> bst = BinarySearchTree()
>>> bst.insert(10)
>>> bst.insert(5)
>>> bst.insert(15)
>>> list(bst)  # Inorder gives sorted values
[5, 10, 15]
>>> bst.find_min()
5
>>> bst.find_max()
15

Using an AVL Tree:

>>> from sds.tree import AVLTree
>>> avl = AVLTree()
>>> for i in range(1, 8):
...     avl.insert(i)
>>> avl.height()  # Stays logarithmic
2

Using a Min-Heap:

>>> from sds.tree import MinHeap
>>> heap = MinHeap()
>>> heap.insert(5)
>>> heap.insert(3)
>>> heap.insert(7)
>>> heap.peek()
3
>>> heap.extract()
3

Using a Heap-based Priority Queue (optimized for performance):

>>> from sds.tree import HeapPriorityQueue
>>> pq = HeapPriorityQueue()
>>> pq.enqueue("low priority", 10)
>>> pq.enqueue("high priority", 1)
>>> pq.dequeue()
('high priority', 1)

Note: For simple use cases with small datasets, you can also use
sds.linear.queue.PriorityQueue which has O(n) enqueue but simpler code.

See Also
--------
sds.core : Core data structure components.
sds.linear : Linear data structures.
"""

from .balanced import AVLTree, RedBlackTree
from .binary import BinarySearchTree, BinaryTree
from .btree import BTree
from .general import Tree
from .heap import HeapPriorityQueue, MaxHeap, MinHeap
from .node import AVLNode, BinaryNode, BTreeNode, RedBlackNode, TreeNode, TrieNode
from .segment_tree import SegmentTree
from .trie import Trie

__all__ = [
    # Nodes
    "AVLNode",
    "BinaryNode",
    "BTreeNode",
    "RedBlackNode",
    "TreeNode",
    "TrieNode",
    # Trees
    "Tree",
    "AVLTree",
    "BinaryTree",
    "BinarySearchTree",
    "RedBlackTree",
    "Trie",
    "BTree",
    "SegmentTree",
    # Heaps
    "MinHeap",
    "MaxHeap",
    "HeapPriorityQueue",
]
