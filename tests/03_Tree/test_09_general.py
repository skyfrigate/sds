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

"""Tests for general Tree (n-ary tree) implementation."""

import pytest

from sds.core.exceptions import EmptyStructureError
from sds.tree.general import Tree
from sds.tree.node import TreeNode


class TestTreeCreation:
    """Test Tree creation and initialization."""

    def test_create_empty_tree(self) -> None:
        """Test creating an empty tree."""
        tree = Tree()
        assert tree.is_empty()
        assert len(tree) == 0
        assert tree.root is None

    def test_create_tree_with_root(self) -> None:
        """Test creating tree with root data."""
        tree = Tree("Root")
        assert not tree.is_empty()
        assert len(tree) == 1
        assert tree.root is not None
        assert tree.root.data == "Root"

    def test_tree_bool(self) -> None:
        """Test boolean evaluation."""
        tree = Tree()
        assert not tree
        tree = Tree("Root")
        assert tree

    def test_root_is_tree_node(self) -> None:
        """Test that root is a TreeNode."""
        tree = Tree("Root")
        assert isinstance(tree.root, TreeNode)


class TestTreeHeight:
    """Test Tree height calculation."""

    def test_height_empty_tree(self) -> None:
        """Test height of empty tree is -1."""
        tree = Tree()
        assert tree.height() == -1

    def test_height_single_node(self) -> None:
        """Test height of tree with only root is 0."""
        tree = Tree("Root")
        assert tree.height() == 0

    def test_height_one_level(self) -> None:
        """Test height with one level of children."""
        tree = Tree("Root")
        tree.add_child("Child1")
        tree.add_child("Child2")
        assert tree.height() == 1

    def test_height_two_levels(self) -> None:
        """Test height with two levels."""
        tree = Tree("Root")
        child = tree.add_child("Child")
        tree.add_child("Grandchild", child)
        assert tree.height() == 2

    def test_height_unbalanced_tree(self) -> None:
        """Test height with unbalanced tree."""
        tree = Tree("Root")
        tree.add_child("Child1")
        child2 = tree.add_child("Child2")
        tree.add_child("Grandchild", child2)
        # Height should be longest path
        assert tree.height() == 2


class TestTreeAddChild:
    """Test adding children to tree."""

    def test_add_child_to_root(self) -> None:
        """Test adding child to root."""
        tree = Tree("Root")
        child = tree.add_child("Child")
        assert child.data == "Child"
        assert child.parent is tree.root
        assert len(tree) == 2

    def test_add_multiple_children_to_root(self) -> None:
        """Test adding multiple children to root."""
        tree = Tree("Root")
        tree.add_child("Child1")
        tree.add_child("Child2")
        tree.add_child("Child3")
        assert len(tree) == 4
        assert len(tree.root.children) == 3

    def test_add_child_to_specific_node(self) -> None:
        """Test adding child to specific node."""
        tree = Tree("Root")
        child1 = tree.add_child("Child1")
        grandchild = tree.add_child("Grandchild", child1)
        assert grandchild.parent is child1
        assert len(tree) == 3

    def test_add_child_creates_root_if_empty(self) -> None:
        """Test that adding to empty tree creates root."""
        tree = Tree()
        tree.add_child("Root")
        assert tree.root is not None
        assert tree.root.data == "Root"
        assert len(tree) == 1

    def test_add_child_increments_size(self) -> None:
        """Test that adding child increments size."""
        tree = Tree("Root")
        initial_size = len(tree)
        tree.add_child("Child")
        assert len(tree) == initial_size + 1


class TestTreeAddChildTo:
    """Test adding child to node by data."""

    def test_add_child_to_by_data(self) -> None:
        """Test adding child using parent data."""
        tree = Tree("Root")
        tree.add_child("Child1")
        tree.add_child_to("Child1", "Grandchild")
        assert len(tree) == 3

    def test_add_child_to_non_existent_parent(self) -> None:
        """Test adding to non-existent parent raises error."""
        tree = Tree("Root")
        with pytest.raises(ValueError):
            tree.add_child_to("NonExistent", "Child")

    def test_add_child_to_maintains_hierarchy(self) -> None:
        """Test that hierarchy is maintained."""
        tree = Tree("Root")
        tree.add_child("Child")
        tree.add_child_to("Child", "Grandchild")
        parent = tree.get_parent("Grandchild")
        assert parent.data == "Child"


class TestTreeFindNode:
    """Test finding nodes in tree."""

    def test_find_root(self) -> None:
        """Test finding root node."""
        tree = Tree("Root")
        node = tree.find_node("Root")
        assert node is not None
        assert node.data == "Root"

    def test_find_child(self) -> None:
        """Test finding child node."""
        tree = Tree("Root")
        tree.add_child("Child")
        node = tree.find_node("Child")
        assert node is not None
        assert node.data == "Child"

    def test_find_non_existent(self) -> None:
        """Test finding non-existent node returns None."""
        tree = Tree("Root")
        node = tree.find_node("NotFound")
        assert node is None

    def test_find_in_empty_tree(self) -> None:
        """Test finding in empty tree returns None."""
        tree = Tree()
        node = tree.find_node("Any")
        assert node is None

    def test_find_grandchild(self) -> None:
        """Test finding grandchild node."""
        tree = Tree("Root")
        tree.add_child("Child")
        tree.add_child_to("Child", "Grandchild")
        node = tree.find_node("Grandchild")
        assert node is not None
        assert node.data == "Grandchild"


class TestTreeRemoveNode:
    """Test removing nodes from tree."""

    def test_remove_from_empty_tree(self) -> None:
        """Test removing from empty tree raises error."""
        tree = Tree()
        with pytest.raises(EmptyStructureError):
            tree.remove_node("Any")

    def test_remove_leaf(self) -> None:
        """Test removing leaf node."""
        tree = Tree("Root")
        tree.add_child("Leaf")
        removed = tree.remove_node("Leaf")
        assert removed == "Leaf"
        assert len(tree) == 1
        assert not tree.search("Leaf")

    def test_remove_node_with_children(self) -> None:
        """Test removing node removes all descendants."""
        tree = Tree("Root")
        tree.add_child("Child")
        tree.add_child_to("Child", "Grandchild")
        tree.remove_node("Child")
        assert len(tree) == 1
        assert not tree.search("Child")
        assert not tree.search("Grandchild")

    def test_remove_root(self) -> None:
        """Test removing root clears tree."""
        tree = Tree("Root")
        tree.add_child("Child")
        tree.remove_node("Root")
        assert tree.is_empty()

    def test_remove_non_existent(self) -> None:
        """Test removing non-existent node raises error."""
        tree = Tree("Root")
        with pytest.raises(ValueError):
            tree.remove_node("NotFound")

    def test_remove_decrements_size(self) -> None:
        """Test that remove decrements size correctly."""
        tree = Tree("Root")
        tree.add_child("Child1")
        tree.add_child("Child2")
        initial_size = len(tree)
        tree.remove_node("Child1")
        assert len(tree) == initial_size - 1


class TestTreeInsertRemove:
    """Test insert and remove methods."""

    def test_insert_into_empty_tree(self) -> None:
        """Test inserting into empty tree."""
        tree = Tree()
        tree.insert("Root")
        assert tree.root.data == "Root"
        assert len(tree) == 1

    def test_insert_into_non_empty_tree(self) -> None:
        """Test inserting adds to root."""
        tree = Tree("Root")
        tree.insert("Child")
        assert len(tree) == 2
        assert len(tree.root.children) == 1

    def test_remove_calls_remove_node(self) -> None:
        """Test that remove method works."""
        tree = Tree("Root")
        tree.add_child("Child")
        removed = tree.remove("Child")
        assert removed == "Child"
        assert len(tree) == 1


class TestTreeSearch:
    """Test searching in tree."""

    def test_search_empty_tree(self) -> None:
        """Test searching in empty tree."""
        tree = Tree()
        assert not tree.search("Any")

    def test_search_existing_item(self) -> None:
        """Test searching for existing item."""
        tree = Tree("Root")
        tree.add_child("Child")
        assert tree.search("Root")
        assert tree.search("Child")

    def test_search_non_existing_item(self) -> None:
        """Test searching for non-existing item."""
        tree = Tree("Root")
        assert not tree.search("NotFound")

    def test_contains_operator(self) -> None:
        """Test __contains__ operator."""
        tree = Tree("Root")
        tree.add_child("Child")
        assert "Root" in tree
        assert "Child" in tree
        assert "NotFound" not in tree


class TestTreeClear:
    """Test clearing tree."""

    def test_clear_empty_tree(self) -> None:
        """Test clearing empty tree."""
        tree = Tree()
        tree.clear()
        assert tree.is_empty()

    def test_clear_non_empty_tree(self) -> None:
        """Test clearing non-empty tree."""
        tree = Tree("Root")
        tree.add_child("Child1")
        tree.add_child("Child2")
        tree.clear()
        assert tree.is_empty()
        assert len(tree) == 0
        assert tree.root is None

    def test_tree_usable_after_clear(self) -> None:
        """Test that tree is usable after clear."""
        tree = Tree("Root")
        tree.add_child("Child")
        tree.clear()
        tree.insert("NewRoot")
        assert len(tree) == 1


class TestTreeTraversals:
    """Test tree traversal methods."""

    def test_preorder_empty_tree(self) -> None:
        """Test preorder traversal of empty tree."""
        tree = Tree()
        assert list(tree.preorder_traversal()) == []

    def test_preorder_single_node(self) -> None:
        """Test preorder traversal of single node."""
        tree = Tree("Root")
        assert list(tree.preorder_traversal()) == ["Root"]

    def test_preorder_multiple_nodes(self) -> None:
        """Test preorder traversal with multiple nodes."""
        tree = Tree("A")
        tree.add_child("B")
        tree.add_child("C")
        b_node = tree.find_node("B")
        tree.add_child("D", b_node)
        tree.add_child("E", b_node)
        # Preorder: A, B, D, E, C
        result = list(tree.preorder_traversal())
        assert result == ["A", "B", "D", "E", "C"]

    def test_postorder_empty_tree(self) -> None:
        """Test postorder traversal of empty tree."""
        tree = Tree()
        assert list(tree.postorder_traversal()) == []

    def test_postorder_single_node(self) -> None:
        """Test postorder traversal of single node."""
        tree = Tree("Root")
        assert list(tree.postorder_traversal()) == ["Root"]

    def test_postorder_multiple_nodes(self) -> None:
        """Test postorder traversal with multiple nodes."""
        tree = Tree("A")
        tree.add_child("B")
        tree.add_child("C")
        b_node = tree.find_node("B")
        tree.add_child("D", b_node)
        tree.add_child("E", b_node)
        # Postorder: D, E, B, C, A
        result = list(tree.postorder_traversal())
        assert result == ["D", "E", "B", "C", "A"]

    def test_level_order_empty_tree(self) -> None:
        """Test level-order traversal of empty tree."""
        tree = Tree()
        assert list(tree.level_order_traversal()) == []

    def test_level_order_multiple_levels(self) -> None:
        """Test level-order traversal with multiple levels."""
        tree = Tree("A")
        tree.add_child("B")
        tree.add_child("C")
        b_node = tree.find_node("B")
        tree.add_child("D", b_node)
        tree.add_child("E", b_node)
        # Level order: A, B, C, D, E
        result = list(tree.level_order_traversal())
        assert result == ["A", "B", "C", "D", "E"]

    def test_iter_uses_preorder(self) -> None:
        """Test that __iter__ uses preorder."""
        tree = Tree("A")
        tree.add_child("B")
        tree.add_child("C")
        iter_result = list(tree)
        preorder_result = list(tree.preorder_traversal())
        assert iter_result == preorder_result


class TestTreeUtilityMethods:
    """Test utility methods for tree."""

    def test_get_children(self) -> None:
        """Test getting children of a node."""
        tree = Tree("Root")
        tree.add_child("Child1")
        tree.add_child("Child2")
        tree.add_child("Child3")
        children = tree.get_children("Root")
        assert len(children) == 3
        data = [child.data for child in children]
        assert "Child1" in data
        assert "Child2" in data
        assert "Child3" in data

    def test_get_children_of_leaf(self) -> None:
        """Test getting children of leaf returns empty list."""
        tree = Tree("Root")
        tree.add_child("Leaf")
        children = tree.get_children("Leaf")
        assert children == []

    def test_get_children_non_existent(self) -> None:
        """Test getting children of non-existent node."""
        tree = Tree("Root")
        with pytest.raises(ValueError):
            tree.get_children("NotFound")

    def test_get_parent(self) -> None:
        """Test getting parent of a node."""
        tree = Tree("Root")
        tree.add_child("Child")
        parent = tree.get_parent("Child")
        assert parent is not None
        assert parent.data == "Root"

    def test_get_parent_of_root(self) -> None:
        """Test getting parent of root returns None."""
        tree = Tree("Root")
        parent = tree.get_parent("Root")
        assert parent is None

    def test_get_parent_non_existent(self) -> None:
        """Test getting parent of non-existent returns None."""
        tree = Tree("Root")
        parent = tree.get_parent("NotFound")
        assert parent is None

    def test_degree(self) -> None:
        """Test getting degree of a node."""
        tree = Tree("Root")
        tree.add_child("Child1")
        tree.add_child("Child2")
        tree.add_child("Child3")
        assert tree.degree("Root") == 3

    def test_degree_of_leaf(self) -> None:
        """Test degree of leaf is 0."""
        tree = Tree("Root")
        tree.add_child("Leaf")
        assert tree.degree("Leaf") == 0

    def test_degree_non_existent(self) -> None:
        """Test degree of non-existent node raises error."""
        tree = Tree("Root")
        with pytest.raises(ValueError):
            tree.degree("NotFound")

    def test_is_leaf(self) -> None:
        """Test checking if node is leaf."""
        tree = Tree("Root")
        tree.add_child("Leaf")
        assert tree.is_leaf("Leaf")
        assert not tree.is_leaf("Root")

    def test_is_leaf_non_existent(self) -> None:
        """Test is_leaf on non-existent node raises error."""
        tree = Tree("Root")
        with pytest.raises(ValueError):
            tree.is_leaf("NotFound")

    def test_leaves(self) -> None:
        """Test getting all leaves."""
        tree = Tree("Root")
        tree.add_child("Child1")
        tree.add_child("Child2")
        child1 = tree.find_node("Child1")
        tree.add_child("Leaf1", child1)
        tree.add_child("Leaf2", child1)
        leaves = tree.leaves()
        assert len(leaves) == 3  # Child2, Leaf1, Leaf2
        assert "Child2" in leaves
        assert "Leaf1" in leaves
        assert "Leaf2" in leaves

    def test_leaves_empty_tree(self) -> None:
        """Test leaves on empty tree returns empty list."""
        tree = Tree()
        assert tree.leaves() == []

    def test_leaves_single_node(self) -> None:
        """Test leaves of single node tree."""
        tree = Tree("Root")
        leaves = tree.leaves()
        assert leaves == ["Root"]


class TestTreeStringRepresentation:
    """Test string representations."""

    def test_repr_empty_tree(self) -> None:
        """Test repr of empty tree."""
        tree = Tree()
        assert repr(tree) == "Tree(size=0)"

    def test_repr_non_empty_tree(self) -> None:
        """Test repr of non-empty tree."""
        tree = Tree("Root")
        tree.add_child("Child")
        assert repr(tree) == "Tree(size=2)"

    def test_str_empty_tree(self) -> None:
        """Test str of empty tree."""
        tree = Tree()
        assert str(tree) == "Tree: []"

    def test_str_single_node(self) -> None:
        """Test str of single node tree."""
        tree = Tree("Root")
        result = str(tree)
        assert "Root" in result

    def test_str_with_children(self) -> None:
        """Test str shows tree structure."""
        tree = Tree("Root")
        tree.add_child("Child1")
        tree.add_child("Child2")
        result = str(tree)
        assert "Root" in result
        assert "Child1" in result
        assert "Child2" in result


class TestTreeEdgeCases:
    """Test edge cases and special scenarios."""

    def test_tree_with_various_data_types(self) -> None:
        """Test tree with various data types."""
        tree = Tree(42)
        tree.add_child("string")
        tree.add_child(3.14)
        tree.add_child([1, 2, 3])
        assert len(tree) == 4

    def test_deep_tree(self) -> None:
        """Test creating deep tree."""
        tree = Tree("Root")
        current_data = "Root"
        for i in range(10):
            child_data = f"Level{i}"
            tree.add_child_to(current_data, child_data)
            current_data = child_data
        assert tree.height() == 10

    def test_wide_tree(self) -> None:
        """Test creating wide tree."""
        tree = Tree("Root")
        for i in range(100):
            tree.add_child(f"Child{i}")
        assert len(tree) == 101
        assert tree.degree("Root") == 100

    def test_remove_subtree(self) -> None:
        """Test removing entire subtree."""
        tree = Tree("Root")
        tree.add_child("Branch")
        for i in range(5):
            tree.add_child_to("Branch", f"Leaf{i}")
        initial_size = len(tree)
        tree.remove_node("Branch")
        # Should remove Branch + 5 leaves
        assert len(tree) == initial_size - 6

    def test_multiple_children_with_same_data(self) -> None:
        """Test handling multiple children with same data."""
        tree = Tree("Root")
        tree.add_child("Duplicate")
        tree.add_child("Duplicate")
        tree.add_child("Duplicate")
        # find_node returns first occurrence
        node = tree.find_node("Duplicate")
        assert node is not None
        assert len(tree) == 4


class TestTreeRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_file_system_hierarchy(self) -> None:
        """Test modeling file system hierarchy."""
        fs = Tree("/")
        fs.add_child("home")
        fs.add_child("usr")
        fs.add_child_to("home", "user1")
        fs.add_child_to("home", "user2")
        fs.add_child_to("user1", "documents")
        fs.add_child_to("user1", "downloads")

        assert fs.height() == 3
        assert fs.degree("home") == 2
        assert fs.is_leaf("documents")

    def test_organization_chart(self) -> None:
        """Test modeling organization chart."""
        org = Tree("CEO")
        org.add_child("CTO")
        org.add_child("CFO")
        org.add_child("COO")
        org.add_child_to("CTO", "Dev Manager")
        org.add_child_to("CTO", "QA Manager")
        org.add_child_to("Dev Manager", "Developer 1")
        org.add_child_to("Dev Manager", "Developer 2")

        assert org.height() == 3
        managers = ["CTO", "CFO", "COO"]
        for manager in managers:
            parent = org.get_parent(manager)
            assert parent.data == "CEO"

    def test_family_tree(self) -> None:
        """Test modeling family tree."""
        family = Tree("Grandparent")
        family.add_child("Parent1")
        family.add_child("Parent2")
        family.add_child_to("Parent1", "Child1")
        family.add_child_to("Parent1", "Child2")
        family.add_child_to("Parent2", "Child3")

        # Find all grandchildren
        leaves = family.leaves()
        grandchildren = [leaf for leaf in leaves if "Child" in leaf]
        assert len(grandchildren) == 3

    def test_menu_system(self) -> None:
        """Test modeling hierarchical menu."""
        menu = Tree("Main Menu")
        menu.add_child("File")
        menu.add_child("Edit")
        menu.add_child("Help")
        menu.add_child_to("File", "New")
        menu.add_child_to("File", "Open")
        menu.add_child_to("File", "Save")
        menu.add_child_to("Edit", "Copy")
        menu.add_child_to("Edit", "Paste")

        # Get all File menu options
        file_options = menu.get_children("File")
        assert len(file_options) == 3


class TestTreePerformance:
    """Test performance characteristics."""

    def test_large_tree_operations(self) -> None:
        """Test operations on large tree."""
        tree = Tree("Root")
        # Add 1000 nodes
        for i in range(1000):
            tree.add_child(f"Node{i}")
        assert len(tree) == 1001
        assert tree.search("Node500")
        assert not tree.search("Node1001")

    def test_deep_path_traversal(self) -> None:
        """Test traversing deep path."""
        tree = Tree("Root")
        current_data = "Root"
        for i in range(100):
            child_data = f"Level{i}"
            tree.add_child_to(current_data, child_data)
            current_data = child_data
        assert tree.height() == 100
        assert tree.is_leaf("Level99")
