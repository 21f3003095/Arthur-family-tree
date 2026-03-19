"""
seeder.py
"""

from models.person import Gender
from family_tree import FamilyTree

M = Gender.MALE
F = Gender.FEMALE


def build_arthur_family() -> FamilyTree:
    tree = FamilyTree()

    # Generation 0
    tree.add_person("King Arthur", M)
    tree.add_person("Queen Margret", F)
    tree.set_spouse("King Arthur", "Queen Margret")

    # Generation 1
    tree.seed_child("Queen Margret", "Bill", M)
    tree.add_person("Flora", F)
    tree.set_spouse("Bill", "Flora")

    tree.seed_child("Queen Margret", "Charlie", M)

    tree.seed_child("Queen Margret", "Percy", M)
    tree.add_person("Audrey", F)
    tree.set_spouse("Percy", "Audrey")

    tree.seed_child("Queen Margret", "Ronald", M)
    tree.add_person("Helen", F)
    tree.set_spouse("Ronald", "Helen")

    tree.seed_child("Queen Margret", "Ginerva", F)
    tree.add_person("Harry", M)
    tree.set_spouse("Ginerva", "Harry")

    # Generation 2: Bill & Flora children = Victoire, Dominique, Louis
    # Ted married IN as Victoire's spouse
    tree.seed_child("Flora", "Victoire", F)
    tree.seed_child("Flora", "Dominique", F)
    tree.seed_child("Flora", "Louis", M)
    tree.add_person("Ted", M)
    tree.set_spouse("Victoire", "Ted")

    # Generation 2: Percy & Audrey children
    tree.seed_child("Audrey", "Molly", F)
    tree.seed_child("Audrey", "Lucy", F)

    # Generation 2: Ronald & Helen children = Rose, Hugo
    # Malfoy married IN as Rose's spouse
    tree.seed_child("Helen", "Rose", F)
    tree.seed_child("Helen", "Hugo", M)
    tree.add_person("Malfoy", M)
    tree.set_spouse("Rose", "Malfoy")

    # Generation 2: Ginerva & Harry children = James, Albus, Lily
    # Darcy married IN as James's spouse
    # Alice married IN as Albus's spouse
    tree.seed_child("Ginerva", "James", M)
    tree.seed_child("Ginerva", "Albus", M)
    tree.seed_child("Ginerva", "Lily", F)
    tree.add_person("Darcy", F)
    tree.set_spouse("James", "Darcy")
    tree.add_person("Alice", F)
    tree.set_spouse("Albus", "Alice")

    # Generation 3
    tree.seed_child("Victoire", "Remus", M)     # Victoire + Ted
    tree.seed_child("Rose", "Draco", M)          # Rose + Malfoy
    tree.seed_child("Rose", "Aster", F)                 
    tree.seed_child("Darcy", "William", M)       # James + Darcy
    tree.seed_child("Alice", "Ron", M)           # Albus + Alice
    tree.seed_child("Alice", "Ginny", F)

    return tree