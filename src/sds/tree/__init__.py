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
binary search trees, and other tree-based data structures.

Classes
-------
BinaryNode
    Node for binary tree structures.
TreeNode
    Node for general tree structures.
BinaryTree
    Simple binary tree implementation.
BinarySearchTree
    Binary search tree with ordering property.

Examples
--------
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

See Also
--------
sds.core : Core data structure components.
sds.linear : Linear data structures.
"""

from .balanced import AVLTree, RedBlackTree
from .binary import BinarySearchTree, BinaryTree
from .heap import HeapPriorityQueue, MaxHeap, MinHeap
from .node import AVLNode, BinaryNode, RedBlackNode, TreeNode

__all__ = [
    "AVLNode",
    "BinaryNode",
    "RedBlackTree",
    "TreeNode",
    "AVLTree",
    "BinaryTree",
    "BinarySearchTree",
    "MinHeap",
    "MaxHeap",
    "HeapPriorityQueue",
    "RedBlackNode",
]
