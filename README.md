# Belief Revision Agent

A propositional logic belief revision system based on the AGM model. This system maintains a set of beliefs and updates them in a rational way when new information is encountered.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/belief-revision-agent.git
   cd belief-revision-agent
   ```

2. Set up a Python environment (optional but recommended):
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. The system uses standard Python libraries and doesn't require additional dependencies.


## Project Structure

Ensure all files are in the same directory:

```
belief-revision-agent/
├── belief_base.py       # Core belief storage
├── entailment.py        # Resolution-based entailment checking
├── contraction.py       # Removes beliefs while preserving consistency
├── expansion.py         # Adds new beliefs to the belief base
├── belief_revision.py   # Main revision operations
├── test_agm.py          # Test suite and main executable
├── mastermind_agent.py  # Mastermind game implementation
└── mastermind.py        # Mastermind game rules
```

## Features

- **Belief Base Management**: Store, add, and remove propositional formulas
- **Logical Entailment**: Resolution-based checking if one belief follows from others
- **Belief Operations**: Expansion, contraction, and revision of beliefs
- **AGM Postulate Testing**: Verify that operations follow theoretical requirements
- **Mastermind Game**: Application of belief revision to solve the Mastermind game

## Running the System

1. Make sure all files are in place
2. Run the main interactive program:
   ```bash
   python test_agm.py
   ```
3. You'll see a menu with options:
   ```
   === Belief Revision Agent ===
   1. Manual input
   2. Run batch tests
   3. Mastermind
   4. Exit
   >
   ```
4. Enter your choice (1-4) and follow the prompts

## Supported Formula Syntax

- `A`, `B`, `C` - Atomic propositions
- `¬` - Negation (NOT)
- `∧` - Conjunction (AND)
- `∨` - Disjunction (OR)
- `→` - Implication (IMPLIES)
- `↔` - Equivalence (IFF)

Examples:
- `A`
- `(A ∧ B)`
- `(¬A ∨ B)`
- `(A → B)`

## Using the System

### Option 1: Manual Input
Enter your own formulas to see how the belief revision system works:
- Input a formula for revision (e.g., `A`, `(A ∧ B)`, `(¬A ∨ B)`)
- Optionally enter an equivalent formula to test extensionality
- See the resulting belief base and AGM postulate test results

### Option 2: Batch Tests
Run predefined test cases that demonstrate:
- Double negation equivalence (e.g., `C` and `(¬¬C)`)
- Logical equivalences (e.g., `(A ∨ B)` and `(¬(¬A ∧ ¬B))`)
- AGM postulate verification for each test case

### Option 3: Mastermind Game
Play the Mastermind game where the system tries to guess a secret color code:
- The default game uses colors: red, green, blue, yellow, black, white
- Default code length is 4
- The system makes guesses based on belief revision
- After each guess, the system receives feedback (correct positions, correct colors)
- It updates its beliefs and makes a new guess
- The game continues until the code is cracked or max turns are reached