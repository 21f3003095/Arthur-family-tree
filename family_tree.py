"""
family_tree.py
The FamilyTree class is the central domain object.
It owns the registry of all Person nodes and exposes the two primary
"""

from __future__ import annotations
from typing import Optional, Dict
from models.person import Person, Gender
from relationships.resolver import resolve, RELATIONSHIP_REGISTRY


# Output constants 

CHILD_ADDED            = "CHILD_ADDED"
CHILD_ADDITION_FAILED  = "CHILD_ADDITION_FAILED"
PERSON_NOT_FOUND       = "PERSON_NOT_FOUND"
NONE_RESULT            = "NONE"


class FamilyTree:
    def __init__(self) -> None:
        self._members: Dict[str, Person] = {}

    # Public builder helpers, used when seeding the initial tree

    def add_person(self, name: str, gender: Gender) -> Person:
        if name in self._members:
            raise ValueError(f"Person '{name}' already exists in the family tree.")
        person = Person(name, gender)
        self._members[name] = person
        return person

    def set_spouse(self, name_a: str, name_b: str) -> None:
        a = self._get_or_raise(name_a)
        b = self._get_or_raise(name_b)
        a.set_spouse(b)

    def seed_child(self, mother_name: str, child_name: str, gender: Gender) -> None:
        mother = self._get_or_raise(mother_name)
        child = Person(child_name, gender)
        self._members[child_name] = child
        mother.add_child(child)

    # Primary operations
    def add_child(self, mother_name: str, child_name: str, gender_str: str) -> str:
        # Validate gender first
        try:
            gender = Gender.from_str(gender_str)
        except ValueError:
            return CHILD_ADDITION_FAILED

        mother = self._members.get(mother_name)

        if mother is None:
            return PERSON_NOT_FOUND

        if not mother.is_female:
            return CHILD_ADDITION_FAILED

        if child_name in self._members:
            return CHILD_ADDITION_FAILED

        child = Person(child_name, gender)
        self._members[child_name] = child
        mother.add_child(child)
        return CHILD_ADDED

    def get_relationship(self, name: str, relationship: str) -> str:

        person = self._members.get(name)

        if person is None:
            return PERSON_NOT_FOUND

        # Normalise relationship lookup
        canonical = self._canonical_relationship(relationship)
        if canonical is None:
            return NONE_RESULT

        try:
            results = resolve(canonical, person)
        except KeyError:
            return NONE_RESULT

        if not results:
            return NONE_RESULT

        return " ".join(p.name for p in results)

    # Internal helpers

    def _get_or_raise(self, name: str) -> Person:
        person = self._members.get(name)
        if person is None:
            raise KeyError(f"Person '{name}' not found in family tree.")
        return person

    def _canonical_relationship(self, relationship: str) -> Optional[str]:
        lower = relationship.lower()
        for key in RELATIONSHIP_REGISTRY:
            if key.lower() == lower:
                return key
        return None
