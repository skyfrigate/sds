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

"""Tests for Trie (Prefix Tree) implementation."""

import pytest

from sds.tree.trie import Trie


class TestTrieCreation:
    """Test Trie creation and initialization."""

    def test_create_empty_trie(self) -> None:
        """Test creating an empty trie."""
        trie = Trie()
        assert trie.is_empty()
        assert len(trie) == 0
        assert trie.size == 0

    def test_trie_bool(self) -> None:
        """Test boolean evaluation."""
        trie = Trie()
        assert not trie
        trie.insert("word")
        assert trie


class TestTrieInsertion:
    """Test trie insertion operations."""

    def test_insert_single_word(self) -> None:
        """Test inserting a single word."""
        trie = Trie()
        trie.insert("hello")
        assert len(trie) == 1
        assert trie.search("hello")

    def test_insert_multiple_words(self) -> None:
        """Test inserting multiple words."""
        trie = Trie()
        words = ["cat", "dog", "bird"]
        for word in words:
            trie.insert(word)
        assert len(trie) == 3
        for word in words:
            assert trie.search(word)

    def test_insert_words_with_common_prefix(self) -> None:
        """Test inserting words with common prefix."""
        trie = Trie()
        trie.insert("cat")
        trie.insert("car")
        trie.insert("card")
        assert len(trie) == 3
        assert trie.search("cat")
        assert trie.search("car")
        assert trie.search("card")

    def test_insert_duplicate_word(self) -> None:
        """Test inserting duplicate word doesn't increase size."""
        trie = Trie()
        trie.insert("hello")
        trie.insert("hello")
        assert len(trie) == 1

    def test_insert_empty_string_raises_error(self) -> None:
        """Test inserting empty string raises error."""
        trie = Trie()
        with pytest.raises(ValueError):
            trie.insert("")

    def test_insert_prefix_and_full_word(self) -> None:
        """Test inserting both prefix and full word."""
        trie = Trie()
        trie.insert("app")
        trie.insert("apple")
        assert len(trie) == 2
        assert trie.search("app")
        assert trie.search("apple")

    def test_insert_increments_size(self) -> None:
        """Test that insert increments size."""
        trie = Trie()
        for i in range(5):
            trie.insert(f"word{i}")
            assert len(trie) == i + 1


class TestTrieSearch:
    """Test trie search operations."""

    def test_search_empty_trie(self) -> None:
        """Test searching in empty trie."""
        trie = Trie()
        assert not trie.search("any")

    def test_search_existing_word(self) -> None:
        """Test searching for existing word."""
        trie = Trie()
        trie.insert("hello")
        assert trie.search("hello")

    def test_search_non_existing_word(self) -> None:
        """Test searching for non-existing word."""
        trie = Trie()
        trie.insert("hello")
        assert not trie.search("world")

    def test_search_prefix_of_word(self) -> None:
        """Test that prefix is not found as complete word."""
        trie = Trie()
        trie.insert("hello")
        assert not trie.search("hell")
        assert not trie.search("hel")

    def test_search_empty_string(self) -> None:
        """Test searching for empty string."""
        trie = Trie()
        trie.insert("word")
        assert not trie.search("")

    def test_contains_operator(self) -> None:
        """Test __contains__ operator."""
        trie = Trie()
        trie.insert("hello")
        assert "hello" in trie
        assert "world" not in trie


class TestTrieStartsWith:
    """Test prefix search operations."""

    def test_starts_with_empty_trie(self) -> None:
        """Test starts_with on empty trie."""
        trie = Trie()
        assert not trie.starts_with("any")

    def test_starts_with_existing_prefix(self) -> None:
        """Test starts_with for existing prefix."""
        trie = Trie()
        trie.insert("hello")
        trie.insert("help")
        assert trie.starts_with("hel")
        assert trie.starts_with("he")
        assert trie.starts_with("h")

    def test_starts_with_non_existing_prefix(self) -> None:
        """Test starts_with for non-existing prefix."""
        trie = Trie()
        trie.insert("hello")
        assert not trie.starts_with("wor")

    def test_starts_with_full_word(self) -> None:
        """Test starts_with with full word."""
        trie = Trie()
        trie.insert("hello")
        assert trie.starts_with("hello")

    def test_starts_with_empty_prefix(self) -> None:
        """Test starts_with with empty prefix returns True."""
        trie = Trie()
        trie.insert("word")
        assert trie.starts_with("")

    def test_starts_with_longer_than_words(self) -> None:
        """Test starts_with with prefix longer than all words."""
        trie = Trie()
        trie.insert("hi")
        assert not trie.starts_with("hello")


class TestTrieRemove:
    """Test trie removal operations."""

    def test_remove_from_empty_trie(self) -> None:
        """Test removing from empty trie."""
        trie = Trie()
        assert not trie.remove("word")

    def test_remove_existing_word(self) -> None:
        """Test removing existing word."""
        trie = Trie()
        trie.insert("hello")
        assert trie.remove("hello")
        assert not trie.search("hello")
        assert len(trie) == 0

    def test_remove_non_existing_word(self) -> None:
        """Test removing non-existing word."""
        trie = Trie()
        trie.insert("hello")
        assert not trie.remove("world")
        assert len(trie) == 1

    def test_remove_word_with_shared_prefix(self) -> None:
        """Test removing word doesn't affect words with shared prefix."""
        trie = Trie()
        trie.insert("cat")
        trie.insert("car")
        trie.insert("card")
        trie.remove("car")
        assert not trie.search("car")
        assert trie.search("cat")
        assert trie.search("card")

    def test_remove_prefix_word(self) -> None:
        """Test removing shorter word doesn't affect longer words."""
        trie = Trie()
        trie.insert("app")
        trie.insert("apple")
        trie.remove("app")
        assert not trie.search("app")
        assert trie.search("apple")

    def test_remove_longer_word(self) -> None:
        """Test removing longer word doesn't affect prefix."""
        trie = Trie()
        trie.insert("app")
        trie.insert("apple")
        trie.remove("apple")
        assert trie.search("app")
        assert not trie.search("apple")

    def test_remove_decrements_size(self) -> None:
        """Test that remove decrements size."""
        trie = Trie()
        trie.insert("word1")
        trie.insert("word2")
        initial_size = len(trie)
        trie.remove("word1")
        assert len(trie) == initial_size - 1


class TestTrieAutocomplete:
    """Test autocomplete functionality."""

    def test_autocomplete_empty_trie(self) -> None:
        """Test autocomplete on empty trie."""
        trie = Trie()
        assert trie.autocomplete("any") == []

    def test_autocomplete_with_matches(self) -> None:
        """Test autocomplete returns matching words."""
        trie = Trie()
        words = ["cat", "car", "card", "care", "careful"]
        for word in words:
            trie.insert(word)
        results = trie.autocomplete("car")
        assert "car" in results
        assert "card" in results
        assert "care" in results
        assert "careful" in results
        assert "cat" not in results

    def test_autocomplete_no_matches(self) -> None:
        """Test autocomplete with no matches."""
        trie = Trie()
        trie.insert("hello")
        assert trie.autocomplete("world") == []

    def test_autocomplete_with_limit(self) -> None:
        """Test autocomplete with limit."""
        trie = Trie()
        for i in range(10):
            trie.insert(f"word{i}")
        results = trie.autocomplete("word", limit=5)
        assert len(results) == 5

    def test_autocomplete_empty_prefix(self) -> None:
        """Test autocomplete with empty prefix returns all words."""
        trie = Trie()
        words = ["cat", "dog", "bird"]
        for word in words:
            trie.insert(word)
        results = trie.autocomplete("")
        assert len(results) == 3

    def test_autocomplete_sorted_results(self) -> None:
        """Test that autocomplete returns sorted results."""
        trie = Trie()
        words = ["zebra", "apple", "banana", "cherry"]
        for word in words:
            trie.insert(word)
        results = trie.autocomplete("")
        assert results == sorted(results)


class TestTrieWordsWithPrefix:
    """Test words_with_prefix method."""

    def test_words_with_prefix(self) -> None:
        """Test getting all words with prefix."""
        trie = Trie()
        words = ["test", "testing", "tester", "testimony"]
        for word in words:
            trie.insert(word)
        results = trie.words_with_prefix("test")
        assert len(results) == 4
        for word in words:
            assert word in results


class TestTrieLongestCommonPrefix:
    """Test longest common prefix functionality."""

    def test_longest_common_prefix_empty_trie(self) -> None:
        """Test LCP on empty trie."""
        trie = Trie()
        assert trie.longest_common_prefix() == ""

    def test_longest_common_prefix_single_word(self) -> None:
        """Test LCP with single word."""
        trie = Trie()
        trie.insert("hello")
        assert trie.longest_common_prefix() == "hello"

    def test_longest_common_prefix_with_common_prefix(self) -> None:
        """Test LCP when words share prefix."""
        trie = Trie()
        trie.insert("flower")
        trie.insert("flow")
        trie.insert("flight")
        assert trie.longest_common_prefix() == "fl"

    def test_longest_common_prefix_no_common(self) -> None:
        """Test LCP when no common prefix."""
        trie = Trie()
        trie.insert("dog")
        trie.insert("cat")
        trie.insert("bird")
        assert trie.longest_common_prefix() == ""

    def test_longest_common_prefix_one_is_prefix(self) -> None:
        """Test LCP when one word is prefix of others."""
        trie = Trie()
        trie.insert("test")
        trie.insert("testing")
        trie.insert("tester")
        assert trie.longest_common_prefix() == "test"


class TestTrieCountWordsWithPrefix:
    """Test counting words with prefix."""

    def test_count_words_with_prefix_empty_trie(self) -> None:
        """Test counting in empty trie."""
        trie = Trie()
        assert trie.count_words_with_prefix("any") == 0

    def test_count_words_with_prefix(self) -> None:
        """Test counting words with specific prefix."""
        trie = Trie()
        words = ["cat", "car", "card", "dog"]
        for word in words:
            trie.insert(word)
        assert trie.count_words_with_prefix("ca") == 3
        assert trie.count_words_with_prefix("car") == 2
        assert trie.count_words_with_prefix("d") == 1

    def test_count_words_with_non_existing_prefix(self) -> None:
        """Test counting with non-existing prefix."""
        trie = Trie()
        trie.insert("hello")
        assert trie.count_words_with_prefix("wor") == 0


class TestTrieClear:
    """Test clearing trie."""

    def test_clear_empty_trie(self) -> None:
        """Test clearing empty trie."""
        trie = Trie()
        trie.clear()
        assert trie.is_empty()

    def test_clear_non_empty_trie(self) -> None:
        """Test clearing non-empty trie."""
        trie = Trie()
        trie.insert("hello")
        trie.insert("world")
        trie.clear()
        assert trie.is_empty()
        assert len(trie) == 0
        assert not trie.search("hello")

    def test_trie_usable_after_clear(self) -> None:
        """Test that trie is usable after clear."""
        trie = Trie()
        trie.insert("hello")
        trie.clear()
        trie.insert("world")
        assert len(trie) == 1
        assert trie.search("world")


class TestTrieIteration:
    """Test trie iteration."""

    def test_iter_empty_trie(self) -> None:
        """Test iterating over empty trie."""
        trie = Trie()
        assert list(trie) == []

    def test_iter_single_word(self) -> None:
        """Test iterating over trie with single word."""
        trie = Trie()
        trie.insert("hello")
        assert list(trie) == ["hello"]

    def test_iter_multiple_words(self) -> None:
        """Test iterating over multiple words."""
        trie = Trie()
        words = ["cat", "dog", "bird"]
        for word in words:
            trie.insert(word)
        result = list(trie)
        assert len(result) == 3
        for word in words:
            assert word in result

    def test_iter_returns_sorted_words(self) -> None:
        """Test that iteration returns words in sorted order."""
        trie = Trie()
        words = ["zebra", "apple", "banana"]
        for word in words:
            trie.insert(word)
        result = list(trie)
        assert result == sorted(words)


class TestTrieStringRepresentation:
    """Test string representations."""

    def test_repr_empty_trie(self) -> None:
        """Test repr of empty trie."""
        trie = Trie()
        assert repr(trie) == "Trie(size=0)"

    def test_repr_non_empty_trie(self) -> None:
        """Test repr of non-empty trie."""
        trie = Trie()
        trie.insert("hello")
        trie.insert("world")
        assert repr(trie) == "Trie(size=2)"

    def test_str_empty_trie(self) -> None:
        """Test str of empty trie."""
        trie = Trie()
        assert str(trie) == "Trie: []"

    def test_str_small_trie(self) -> None:
        """Test str of trie with few words."""
        trie = Trie()
        trie.insert("cat")
        trie.insert("dog")
        result = str(trie)
        assert "cat" in result
        assert "dog" in result

    def test_str_large_trie(self) -> None:
        """Test str of trie with many words shows truncated."""
        trie = Trie()
        for i in range(20):
            trie.insert(f"word{i:02d}")
        result = str(trie)
        assert "..." in result
        assert "20 words" in result


class TestTrieEdgeCases:
    """Test edge cases and special scenarios."""

    def test_case_sensitivity(self) -> None:
        """Test that trie is case-sensitive."""
        trie = Trie()
        trie.insert("Hello")
        trie.insert("hello")
        assert len(trie) == 2
        assert trie.search("Hello")
        assert trie.search("hello")

    def test_single_character_words(self) -> None:
        """Test with single character words."""
        trie = Trie()
        trie.insert("a")
        trie.insert("i")
        assert len(trie) == 2
        assert trie.search("a")
        assert trie.search("i")

    def test_very_long_word(self) -> None:
        """Test with very long word."""
        trie = Trie()
        long_word = "a" * 1000
        trie.insert(long_word)
        assert trie.search(long_word)

    def test_special_characters(self) -> None:
        """Test with special characters."""
        trie = Trie()
        trie.insert("hello-world")
        trie.insert("test@example")
        trie.insert("number_123")
        assert trie.search("hello-world")
        assert trie.search("test@example")
        assert trie.search("number_123")

    def test_unicode_characters(self) -> None:
        """Test with unicode characters."""
        trie = Trie()
        trie.insert("café")
        trie.insert("naïve")
        trie.insert("résumé")
        assert trie.search("café")
        assert trie.search("naïve")

    def test_numbers_as_strings(self) -> None:
        """Test with number strings."""
        trie = Trie()
        trie.insert("123")
        trie.insert("1234")
        trie.insert("12")
        assert trie.search("123")
        assert trie.autocomplete("12") == ["12", "123", "1234"]


class TestTrieRealWorldScenarios:
    """Test real-world usage scenarios."""

    def test_dictionary_implementation(self) -> None:
        """Test using trie as dictionary."""
        dictionary = Trie()
        words = ["apple", "application", "apply", "appreciate"]
        for word in words:
            dictionary.insert(word)

        # Check if word exists
        assert "apple" in dictionary
        assert "apples" not in dictionary

        # Get suggestions
        suggestions = dictionary.autocomplete("app")
        assert len(suggestions) == 4

    def test_autocomplete_system(self) -> None:
        """Test autocomplete for search suggestions."""
        autocomplete = Trie()
        searches = [
            "python tutorial",
            "python programming",
            "python basics",
            "java tutorial",
        ]
        for search in searches:
            autocomplete.insert(search)

        # Get python-related suggestions
        python_suggestions = autocomplete.autocomplete("python")
        assert len(python_suggestions) == 3
        assert all("python" in s for s in python_suggestions)

    def test_spell_checker(self) -> None:
        """Test basic spell checking."""
        spell_checker = Trie()
        correct_words = ["hello", "world", "python", "programming"]
        for word in correct_words:
            spell_checker.insert(word)

        # Check spellings
        assert "hello" in spell_checker
        assert "helo" not in spell_checker
        assert "wrld" not in spell_checker

    def test_prefix_matching(self) -> None:
        """Test prefix matching for search."""
        trie = Trie()
        urls = [
            "https://example.com",
            "https://example.org",
            "https://test.com",
            "https://httpbin.org/",
        ]
        for url in urls:
            trie.insert(url)

        # Find all https URLs
        https_urls = trie.autocomplete("https://")
        assert len(https_urls) == 4

        # Find example.com URLs
        example_urls = trie.autocomplete("https://example")
        assert len(example_urls) == 2


class TestTriePerformance:
    """Test performance characteristics."""

    def test_large_dictionary(self) -> None:
        """Test with large number of words."""
        trie = Trie()
        # Insert 1000 words
        for i in range(1000):
            trie.insert(f"word{i:04d}")
        assert len(trie) == 1000
        assert trie.search("word0500")
        assert not trie.search("word1001")

    def test_prefix_search_performance(self) -> None:
        """Test prefix search with many words."""
        trie = Trie()
        # Insert words with common prefix
        for i in range(100):
            trie.insert(f"prefix{i:03d}")
        results = trie.autocomplete("prefix")
        assert len(results) == 100

    def test_deep_trie(self) -> None:
        """Test with very long words (deep trie)."""
        trie = Trie()
        # Create progressively longer words
        for i in range(1, 51):
            trie.insert("a" * i)
        assert len(trie) == 50
        assert trie.search("a" * 25)


class TestTrieComparisonWithOtherStructures:
    """Compare trie with other structures."""

    def test_trie_vs_list_prefix_search(self) -> None:
        """Demonstrate trie advantage for prefix search."""
        # Using trie
        trie = Trie()
        words = [f"word{i}" for i in range(100)]
        for word in words:
            trie.insert(word)

        # Trie prefix search is O(p) where p is prefix length
        results_trie = trie.autocomplete("word1")
        assert len(results_trie) > 0

        # List would need O(n*m) to check all words
        # Trie is much more efficient for prefix operations

    def test_space_efficiency_with_common_prefixes(self) -> None:
        """Test that trie saves space with common prefixes."""
        trie = Trie()
        words = ["test", "testing", "tester", "testament"]
        for word in words:
            trie.insert(word)

        # All words share "test" prefix
        # Trie stores this prefix only once internally
        assert len(trie) == 4
        assert trie.starts_with("test")
