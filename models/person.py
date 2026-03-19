"""models/person.py Represents a Person node in the Arthur family tree.
"""

from __future__ import annotations
from enum import Enum
from typing import Optional, List


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

    @classmethod
    def from_str(cls, value: str) -> "Gender":
        try:
            return cls(value.capitalize())
        except ValueError:
            raise ValueError(f"Invalid gender '{value}'. Must be 'Male' or 'Female'.")


class Person:

    def __init__(self, name: str, gender: Gender) -> None:
        self.name: str = name
        self.gender: Gender = gender
        self.mother: Optional[Person] = None
        self.father: Optional[Person] = None
        self.spouse: Optional[Person] = None
        self.children: List[Person] = []


    # Derived properties
    @property
    def is_male(self) -> bool:
        return self.gender == Gender.MALE

    @property
    def is_female(self) -> bool:
        return self.gender == Gender.FEMALE

    @property
    def siblings(self) -> List[Person]:
        """All children of the same mother, excluding self."""
        if self.mother is None:
            return []
        return [c for c in self.mother.children if c is not self]

    @property
    def sons(self) -> List[Person]:
        return [c for c in self.children if c.is_male]

    @property
    def daughters(self) -> List[Person]:
        return [c for c in self.children if c.is_female]


    # Addition
    def add_child(self, child: Person) -> None:
        """Attach a child to this person and set parent back-references."""
        if self.is_female:
            child.mother = self
            child.father = self.spouse
        else:
            child.father = self
            child.mother = self.spouse
        self.children.append(child)

        # Mirror the child on the spouse's children list too (same family)
        if self.spouse and child not in self.spouse.children:
            self.spouse.children.append(child)

    def set_spouse(self, partner: Person) -> None:
        self.spouse = partner
        partner.spouse = self

    # Dunder helpers
    def __repr__(self) -> str:  
        return f"Person({self.name!r}, {self.gender.value})"
