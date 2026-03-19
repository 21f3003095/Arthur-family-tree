"""
tests/test_relationships.py
Unit tests for the relationship resolver using a small isolated family tree.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.person import Person, Gender
from relationships.resolver import resolve


# Fixtures: minimal 3-generation family

@pytest.fixture
def mini_family():
    M, F = Gender.MALE, Gender.FEMALE

    grandpa   = Person("Grandpa",           M)
    grandma   = Person("Grandma",           F)
    grandpa.set_spouse(grandma)

    dad       = Person("Dad",               M)
    mom       = Person("Mom",               F)
    dad.set_spouse(mom)
    dad.mother = grandma; dad.father = grandpa
    grandma.children.append(dad); grandpa.children.append(dad)

    uncle     = Person("Uncle",             M)
    aunt_bm   = Person("AuntByMarriage",    F)
    uncle.set_spouse(aunt_bm)
    uncle.mother = grandma; uncle.father = grandpa
    grandma.children.append(uncle); grandpa.children.append(uncle)

    pat_aunt  = Person("PatAunt",           F)
    uncle_bm  = Person("UncleByMarriage",   M)
    pat_aunt.set_spouse(uncle_bm)
    pat_aunt.mother = grandma; pat_aunt.father = grandpa
    grandma.children.append(pat_aunt); grandpa.children.append(pat_aunt)

    son      = Person("Son",  M)
    daughter = Person("Daughter", F)
    mom.set_spouse(dad)
    mom.add_child(son)
    mom.add_child(daughter)

    return {
        "grandpa": grandpa, "grandma": grandma,
        "dad": dad,         "mom": mom,
        "uncle": uncle,     "aunt_bm": aunt_bm,
        "pat_aunt": pat_aunt, "uncle_bm": uncle_bm,
        "son": son,         "daughter": daughter,
    }


# Tests

class TestCoreRelationships:
    def test_son(self, mini_family):
        results = resolve("Son", mini_family["mom"])
        assert [p.name for p in results] == ["Son"]

    def test_daughter(self, mini_family):
        results = resolve("Daughter", mini_family["mom"])
        assert [p.name for p in results] == ["Daughter"]

    def test_siblings(self, mini_family):
        names = [p.name for p in resolve("Siblings", mini_family["dad"])]
        assert "Uncle" in names
        assert "PatAunt" in names
        assert "Dad" not in names

    def test_paternal_uncle(self, mini_family):
        results = resolve("Paternal-Uncle", mini_family["son"])
        assert any(p.name == "Uncle" for p in results)
        assert all(p.is_male for p in results)

    def test_paternal_aunt(self, mini_family):
        results = resolve("Paternal-Aunt", mini_family["son"])
        assert any(p.name == "PatAunt" for p in results)
        assert all(p.is_female for p in results)

    def test_maternal_uncle(self, mini_family):
        results = resolve("Maternal-Uncle", mini_family["son"])
        assert results == []

    def test_sister_in_law_spouse_sisters(self, mini_family):
        results = resolve("Sister-In-Law", mini_family["dad"])
        assert any(p.name == "AuntByMarriage" for p in results)

    def test_brother_in_law_husbands_of_siblings(self, mini_family):
        results = resolve("Brother-In-Law", mini_family["dad"])
        assert any(p.name == "UncleByMarriage" for p in results)

    def test_mother(self, mini_family):
        results = resolve("Mother", mini_family["son"])
        assert results[0].name == "Mom"

    def test_father(self, mini_family):
        results = resolve("Father", mini_family["son"])
        assert results[0].name == "Dad"

    def test_children(self, mini_family):
        names = [p.name for p in resolve("Children", mini_family["mom"])]
        assert "Son" in names
        assert "Daughter" in names

    def test_grandchildren(self, mini_family):
        results = resolve("Grandchildren", mini_family["grandma"])
        names = [p.name for p in results]
        assert "Son" in names
        assert "Daughter" in names

    def test_unknown_relationship_raises(self, mini_family):
        with pytest.raises(KeyError):
            resolve("Cousin", mini_family["son"])

    def test_no_result_returns_empty(self, mini_family):
        results = resolve("Sister-In-Law", mini_family["son"])
        assert results == []
