"""
tests/test_family_tree.py
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from seeder import build_arthur_family
from family_tree import (
    FamilyTree,
    CHILD_ADDED,
    CHILD_ADDITION_FAILED,
    PERSON_NOT_FOUND,
    NONE_RESULT,
)
from main import process_command


# Fixtures

@pytest.fixture
def tree():
    return build_arthur_family()

# ADD_CHILD tests

class TestAddChild:
    def test_add_child_success(self, tree):
        result = tree.add_child("Flora", "Minerva", "Female")
        assert result == CHILD_ADDED

    def test_added_child_appears_in_siblings(self, tree):
        tree.add_child("Flora", "Minerva", "Female")
        result = tree.get_relationship("Minerva", "Siblings")
        for name in ["Victoire", "Ted", "Dominique", "Louis"]:
            assert name in result

    def test_add_child_mother_not_found(self, tree):
        result = tree.add_child("Luna", "Lola", "Female")
        assert result == PERSON_NOT_FOUND

    def test_add_child_to_male_fails(self, tree):
        result = tree.add_child("Ted", "Bella", "Female")
        assert result == CHILD_ADDITION_FAILED

    def test_add_child_invalid_gender(self, tree):
        result = tree.add_child("Flora", "Unknown", "Alien")
        assert result == CHILD_ADDITION_FAILED

    def test_add_child_duplicate_name_fails(self, tree):
        tree.add_child("Flora", "Minerva", "Female")
        result = tree.add_child("Flora", "Minerva", "Male")
        assert result == CHILD_ADDITION_FAILED


# GET_RELATIONSHIP tests 

class TestGetRelationshipSamples:

    def test_remus_maternal_aunt(self, tree):
        result = tree.get_relationship("Remus", "Maternal-Aunt")
        assert result == "Dominique"

    def test_minerva_siblings(self, tree):
        tree.add_child("Flora", "Minerva", "Female")
        result = tree.get_relationship("Minerva", "Siblings")
        assert result == "Victoire Ted Dominique Louis"

    def test_lily_sister_in_law(self, tree):
        result = tree.get_relationship("Lily", "Sister-In-Law")
        assert result == "Alice"

    def test_person_not_found(self, tree):
        result = tree.get_relationship("Luna", "Maternal-Aunt")
        assert result == PERSON_NOT_FOUND

    def test_unknown_relationship(self, tree):
        result = tree.get_relationship("Remus", "Cousin")
        assert result == NONE_RESULT


# GET_RELATIONSHIP tests — various relationships

class TestGetRelationshipExtended:
    def test_paternal_uncle_of_ted(self, tree):
        result = tree.get_relationship("Ted", "Paternal-Uncle")
        for name in ["Charlie", "Percy", "Ronald"]:
            assert name in result

    def test_paternal_aunt_of_ted(self, tree):
        result = tree.get_relationship("Ted", "Paternal-Aunt")
        assert "Ginerva" in result

    def test_maternal_uncle_of_draco(self, tree):
        result = tree.get_relationship("Draco", "Maternal-Uncle")
        for name in ["Hugo"]:
            assert name in result

    def test_son_of_queen_margret(self, tree):
        result = tree.get_relationship("Queen Margret", "Son")
        for name in ["Bill", "Charlie", "Percy", "Ronald"]:
            assert name in result

    def test_daughter_of_queen_margret(self, tree):
        result = tree.get_relationship("Queen Margret", "Daughter")
        assert "Ginerva" in result

    def test_siblings_of_ginerva(self, tree):
        result = tree.get_relationship("Ginerva", "Siblings")
        for name in ["Bill", "Charlie", "Percy", "Ronald"]:
            assert name in result

    def test_grandchildren_of_king_arthur(self, tree):
        result = tree.get_relationship("King Arthur", "Grandchildren")
        for name in ["Victoire", "Ted", "Molly", "Lucy", "Malfoy", "Rose", "Darcy", "James"]:
            assert name in result

    def test_children_insertion_order(self, tree):
        result = tree.get_relationship("Queen Margret", "Children")
        names = result.split()
        assert names == ["Bill", "Charlie", "Percy", "Ronald", "Ginerva"]

    def test_none_when_no_results(self, tree):
        result = tree.get_relationship("Charlie", "Daughter")
        assert result == NONE_RESULT

    def test_case_insensitive_relationship(self, tree):
        r1 = tree.get_relationship("Queen Margret", "son")
        r2 = tree.get_relationship("Queen Margret", "Son")
        assert r1 == r2


# Command-level tests

class TestProcessCommand:
    def test_add_child_command(self, tree):
        result = process_command(tree, "ADD_CHILD Flora Minerva Female")
        assert result == CHILD_ADDED

    def test_get_relationship_command(self, tree):
        result = process_command(tree, "GET_RELATIONSHIP Remus Maternal-Aunt")
        assert result == "Dominique"

    def test_blank_line_returns_none(self, tree):
        assert process_command(tree, "   ") is None

    def test_comment_line_returns_none(self, tree):
        assert process_command(tree, "# this is a comment") is None

    def test_quoted_tokens(self, tree):
        result = process_command(tree, 'ADD_CHILD "Flora" "Minerva" "Female"')
        assert result == CHILD_ADDED

    def test_wrong_arg_count_add_child(self, tree):
        result = process_command(tree, "ADD_CHILD Flora")
        assert result == CHILD_ADDITION_FAILED

    def test_unknown_command(self, tree):
        result = process_command(tree, "DELETE_PERSON Remus")
        assert result is not None
        assert "UNKNOWN_COMMAND" in result
