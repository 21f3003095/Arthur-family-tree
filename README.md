# Glynac — Family Tree Coding Challeng

A clean, object-oriented Python solution modelling the King Arthur family tree for the Glynac Data Engineering coding challenge.

---

## Quick Start

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the program (command-line mode)
python3 main.py sample_input.txt
or
python3 main.py my_test.txt

# 4. Run the web UI
python3 app.py
# Then open http://localhost:5000 in your browser
```

**Python 3.8+ required.**

---

## Project Structure

```
glynac-family-tree/
│
├── main.py                   # Entry point — reads input file, prints results
├── app.py                    # Flask web server with REST API
├── family_tree.py            # FamilyTree class: add_child(), get_relationship()
├── seeder.py                 # Builds the Arthur family tree on startup
│
├── models/
│   ├── __init__.py
│   └── person.py             # Person and Gender classes
│
├── relationships/
│   ├── __init__.py
│   └── resolver.py           # One function per relationship + registry dict
│
├── tests/
│   ├── __init__.py
│   ├── test_person.py        # Unit tests: Person model
│   ├── test_relationships.py # Unit tests: each relationship resolver
│   └── test_family_tree.py   # Integration tests: full Arthur tree + commands
│
├── static/
│   └── index.html            # Web UI (HTML + CSS + JS in one file)
│
├── sample_input.txt          # Sample commands from the challenge
├── my_test.txt               # put your custom commands for the testing
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Running the Tests

```bash
pip install pytest
python3 -m pytest tests/ -v
```

---

## Usage — Command Line

Input is read from a text file. Each line is one command:

```bash
python3 main.py sample_input.txt
```

**ADD_CHILD format:**
```
ADD_CHILD <Mother's-Name> <Child's-Name> <Gender>
```

**GET_RELATIONSHIP format:**
```
GET_RELATIONSHIP <Name> <Relationship>
```

Names with spaces must be quoted:
```
GET_RELATIONSHIP "Queen Margret" Son
```

Lines starting with `#` and blank lines are ignored.

---

## Usage — Web UI

```bash
python3 app.py
```

Open `http://localhost:5000` in your browser. The UI lets you:
- Add children through the mother using a form
- Search any relationship using dropdowns
- See the full family tree diagram
- Click any person to see their details
- Reset the tree back to original

---

## Usage — Terminal Commands via curl

With `app.py` running, send commands from a second terminal:

```bash
# Add a child
curl -X POST http://localhost:5000/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "ADD_CHILD Helen Tyler Male"}'

# Get a relationship
curl -X POST http://localhost:5000/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "GET_RELATIONSHIP Remus Maternal-Aunt"}'
```

Then refresh the browser (`Cmd+R`) to see the updated tree.

---

## Output Values

| Situation | Output |
|---|---|
| Child added successfully | `CHILD_ADDED` |
| Mother not found in tree | `PERSON_NOT_FOUND` |
| Named person is male | `CHILD_ADDITION_FAILED` |
| Person not found | `PERSON_NOT_FOUND` |
| No matching relatives | `NONE` |
| Relatives found | Space-separated names in insertion order |

---

## Supported Relationships

| Relationship | Definition |
|---|---|
| `Paternal-Uncle` | Father's brothers |
| `Maternal-Uncle` | Mother's brothers |
| `Paternal-Aunt` | Father's sisters |
| `Maternal-Aunt` | Mother's sisters |
| `Sister-In-Law` | Spouse's sisters + wives of siblings |
| `Brother-In-Law` | Spouse's brothers + husbands of siblings |
| `Son` | Male children |
| `Daughter` | Female children |
| `Siblings` | All brothers and sisters |
| `Children` | All children |
| `Mother` | Mother |
| `Father` | Father |
| `Spouse` | Spouse/partner |
| `Grandchildren` | All grandchildren |
| `Maternal-Grandmother` | Mother's mother |
| `Maternal-Grandfather` | Mother's father |
| `Paternal-Grandmother` | Father's mother |
| `Paternal-Grandfather` | Father's father |

---

## Sample Input & Expected Output

**sample_input.txt:**
```
ADD_CHILD Flora Minerva Female
GET_RELATIONSHIP Remus Maternal-Aunt
GET_RELATIONSHIP Minerva Siblings
ADD_CHILD Luna Lola Female
GET_RELATIONSHIP Luna Maternal-Aunt
ADD_CHILD Ted Bella Female
GET_RELATIONSHIP Remus Siblings
GET_RELATIONSHIP Lily Sister-In-Law
```

**Expected output:**
```
CHILD_ADDED
Dominique Minerva
Victoire Dominique Louis
PERSON_NOT_FOUND
PERSON_NOT_FOUND
CHILD_ADDITION_FAILED
NONE
Alice
```

---

## Family Tree Structure

```
King Arthur + Queen Margret
│
├── Bill + Flora
│     ├── Victoire + Ted  →  Remus
│     ├── Dominique
│     └── Louis
│
├── Charlie
│
├── Percy + Audrey
│     ├── Molly
│     └── Lucy
│
├── Ronald + Helen
│     ├── Rose + Malfoy  →  Draco, Aster
│     └── Hugo
│
└── Ginerva + Harry
      ├── James + Darcy  →  William
      ├── Albus + Alice  →  Ron, Ginny
      └── Lily
```

**Spouses who married into the family:**
Flora, Audrey, Helen, Harry, Ted, Malfoy, Darcy, Alice

---

## Design Decisions

### Data Model
A `Person` stores only: name, gender, mother, father, spouse, children.
All relationships (siblings, aunts, uncles etc.) are computed on demand from these five things. This keeps the model lean and always consistent.

### Relationship Registry (Open/Closed Principle)
Each relationship is a small pure function `(Person) -> list[Person]` registered in a dictionary. To add a new relationship in the future, you write one function and add one line to the registry. No other file changes.

### Insertion Order Preserved
Python dicts (3.7+) maintain insertion order. Children are stored in a plain list. Both guarantee that `GET_RELATIONSHIP` always returns names in the order they were added, as required by the challenge.

### Children Mirrored on Both Parents
When a child is added via the mother, the child is appended to both the mother's and father's children list. This means queries like `GET_RELATIONSHIP Bill Son` work correctly even though the challenge only supports adding through mothers.

### Error Handling
All error cases return string constants (`PERSON_NOT_FOUND`, `CHILD_ADDITION_FAILED`) rather than raising exceptions. This keeps the command layer clean and testable.

---

## Assumptions

- Names are case-sensitive (`"Flora"` ≠ `"flora"`)
- Relationship names are case-insensitive (`"son"` = `"Son"` = `"SON"`)
- Adding a child with a name that already exists returns `CHILD_ADDITION_FAILED`
- Spouses who married into the family (Flora, Audrey, Helen, Harry, Ted, Malfoy, Darcy, Alice) have no parents in the tree
- No persistence is used — in-memory only, as per the out-of-scope list in the challenge

---

## Dependencies

| Dependency | Version | Purpose |
|---|---|---|
| Python | 3.8+ | Runtime |
| flask | 2.0+ | Web server |
| flask-cors | 3.0+ | Cross-origin requests |
| pytest | 7.0+ | Test runner (dev only) |

No database. No external runtime dependencies beyond Flask.
