"""
tests/test_person.py
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.person import Person, Gender


class TestGender:
    def test_valid_male(self):
        assert Gender.from_str("Male") == Gender.MALE

    def test_valid_female(self):
        assert Gender.from_str("Female") == Gender.FEMALE

    def test_case_insensitive(self):
        assert Gender.from_str("male") == Gender.MALE
        assert Gender.from_str("FEMALE") == Gender.FEMALE

    def test_invalid_raises(self):
        with pytest.raises(ValueError):
            Gender.from_str("Unknown")


class TestPerson:
    def test_creation(self):
        p = Person("Alice", Gender.FEMALE)
        assert p.name == "Alice"
        assert p.gender == Gender.FEMALE
        assert p.is_female is True
        assert p.is_male is False
        assert p.children == []
        assert p.mother is None
        assert p.father is None
        assert p.spouse is None

    def test_set_spouse_bidirectional(self):
        alice = Person("Alice", Gender.FEMALE)
        bob   = Person("Bob", Gender.MALE)
        alice.set_spouse(bob)
        assert alice.spouse is bob
        assert bob.spouse is alice

    def test_add_child_sets_parents(self):
        mother = Person("Mother", Gender.FEMALE)
        father = Person("Father", Gender.MALE)
        mother.set_spouse(father)

        child = Person("Child", Gender.MALE)
        mother.add_child(child)

        assert child.mother is mother
        assert child.father is father
        assert child in mother.children
        assert child in father.children  # mirrored

    def test_add_child_without_spouse(self):
        mother = Person("SingleMother", Gender.FEMALE)
        child  = Person("Kid", Gender.FEMALE)
        mother.add_child(child)

        assert child.mother is mother
        assert child.father is None

    def test_siblings(self):
        mother = Person("Mom", Gender.FEMALE)
        c1 = Person("C1", Gender.MALE)
        c2 = Person("C2", Gender.FEMALE)
        c3 = Person("C3", Gender.MALE)
        mother.add_child(c1)
        mother.add_child(c2)
        mother.add_child(c3)

        assert c2 in c1.siblings
        assert c3 in c1.siblings
        assert c1 not in c1.siblings

    def test_sons_and_daughters(self):
        mother = Person("Mom", Gender.FEMALE)
        son1 = Person("Son1", Gender.MALE)
        son2 = Person("Son2", Gender.MALE)
        dau1 = Person("Dau1", Gender.FEMALE)
        for c in (son1, son2, dau1):
            mother.add_child(c)

        assert mother.sons == [son1, son2]
        assert mother.daughters == [dau1]

    def test_no_siblings_without_mother(self):
        loner = Person("Loner", Gender.MALE)
        assert loner.siblings == []
