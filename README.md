# Belief Revision Agent

This project builds a smart belief revision system.  
It can expand, contract, and revise beliefs.  
It also checks entailment between beliefs.

---

## Project Structure

| File | Purpose |
|:---|:---|
| `belief_base.py` | Stores and manages all beliefs. |
| `entailment.py` | Checks if a belief can be logically derived (entailment). |
| `contraction.py` | Removes beliefs carefully while keeping the belief base consistent. |
| `expansion.py` | Adds new beliefs to the belief base. |
| `test_agm.py` | Tests the behavior: entailment, contraction, and AGM postulates. |

---

## How to Run

1. Open a terminal.
2. Go to the project folder:

    ```bash
    cd Belief-Revision-Agent
    ```

3. Run the smart testing file:

    ```bash
    python test_agm.py
    ```

4. You will see:
   - Beliefs printed.
   - Entailment results (YES/NO).
   - Contraction happening.
   - AGM postulates (Success, Inclusion, Consistency) being checked.

---

## Belief Base

The belief base is big.  
Beliefs are connected.  
Example:

- A → B
- B → (C and D)
- C → (E and F)
- D → (G and H)
- E → I
- and so on...

---

## What This Agent Can Do

- Add new beliefs (expansion).
- Remove beliefs (contraction).
- Revise beliefs (using expansion and contraction together).
- Check logical entailment (using Resolution).
- Test main AGM postulates:
  - Success
  - Inclusion
  - Consistency

---

## Notes

- `expansion.py` is part of the project but not directly used in `test_agm.py`.
- Contraction and entailment are the main focus.
