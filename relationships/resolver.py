"""
relationships/resolver.py
Resolves named relationships for a given Person.
"""

from __future__ import annotations
from typing import Callable, List
from models.person import Person

RelationshipFn = Callable[[Person], List[Person]]


# Individual resolver functions

def _paternal_uncle(person: Person) -> list[Person]:
    """Father's brothers."""
    if person.father is None:
        return []
    return [s for s in person.father.siblings if s.is_male]


def _maternal_uncle(person: Person) -> list[Person]:
    """Mother's brothers."""
    if person.mother is None:
        return []
    return [s for s in person.mother.siblings if s.is_male]


def _paternal_aunt(person: Person) -> list[Person]:
    """Father's sisters."""
    if person.father is None:
        return []
    return [s for s in person.father.siblings if s.is_female]


def _maternal_aunt(person: Person) -> list[Person]:
    """Mother's sisters."""
    if person.mother is None:
        return []
    return [s for s in person.mother.siblings if s.is_female]


def _sister_in_law(person: Person) -> list[Person]:
    """Spouse's sisters + wives of siblings."""
    result: list[Person] = []

    # Spouse's sisters
    if person.spouse:
        result.extend(s for s in person.spouse.siblings if s.is_female)

    # Wives of siblings
    for sibling in person.siblings:
        if sibling.is_male and sibling.spouse and sibling.spouse.is_female:
            result.append(sibling.spouse)

    return result


def _brother_in_law(person: Person) -> list[Person]:
    """Spouse's brothers + husbands of siblings."""
    result: list[Person] = []

    # Spouse's brothers
    if person.spouse:
        result.extend(s for s in person.spouse.siblings if s.is_male)

    # Husbands of siblings
    for sibling in person.siblings:
        if sibling.is_female and sibling.spouse and sibling.spouse.is_male:
            result.append(sibling.spouse)

    return result


def _son(person: Person) -> list[Person]:
    return person.sons


def _daughter(person: Person) -> list[Person]:
    return person.daughters


def _siblings(person: Person) -> list[Person]:
    return person.siblings


def _children(person: Person) -> list[Person]:
    return list(person.children)


def _mother(person: Person) -> list[Person]:
    return [person.mother] if person.mother else []


def _father(person: Person) -> list[Person]:
    return [person.father] if person.father else []


def _spouse(person: Person) -> list[Person]:
    return [person.spouse] if person.spouse else []


def _grandchildren(person: Person) -> list[Person]:
    result: list[Person] = []
    for child in person.children:
        result.extend(child.children)
    return result


def _maternal_grandmother(person: Person) -> list[Person]:
    if person.mother and person.mother.mother:
        return [person.mother.mother]
    return []


def _maternal_grandfather(person: Person) -> list[Person]:
    if person.mother and person.mother.father:
        return [person.mother.father]
    return []


def _paternal_grandmother(person: Person) -> list[Person]:
    if person.father and person.father.mother:
        return [person.father.mother]
    return []


def _paternal_grandfather(person: Person) -> list[Person]:
    if person.father and person.father.father:
        return [person.father.father]
    return []


# Registry  (relationship name -> resolver function)

RELATIONSHIP_REGISTRY: dict[str, RelationshipFn] = {
    "Paternal-Uncle":       _paternal_uncle,
    "Maternal-Uncle":       _maternal_uncle,
    "Paternal-Aunt":        _paternal_aunt,
    "Maternal-Aunt":        _maternal_aunt,
    "Sister-In-Law":        _sister_in_law,
    "Brother-In-Law":       _brother_in_law,
    "Son":                  _son,
    "Daughter":             _daughter,
    "Siblings":             _siblings,
    "Children":             _children,
    "Mother":               _mother,
    "Father":               _father,
    "Spouse":               _spouse,
    "Grandchildren":        _grandchildren,
    "Maternal-Grandmother": _maternal_grandmother,
    "Maternal-Grandfather": _maternal_grandfather,
    "Paternal-Grandmother": _paternal_grandmother,
    "Paternal-Grandfather": _paternal_grandfather,
}


def resolve(relationship: str, person: Person) -> list[Person]:
   
    fn = RELATIONSHIP_REGISTRY.get(relationship)
    if fn is None:
        raise KeyError(f"Unknown relationship: '{relationship}'")
    return fn(person)
