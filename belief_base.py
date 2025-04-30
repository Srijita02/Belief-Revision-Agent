#!/usr/bin/env python
# coding: utf-8

class BeliefBase:
    def __init__(self):
        """Initialize an empty belief base."""
        self.beliefs = set()

    def add_belief(self, formula):
        """Add a belief (formula) to the belief base."""
        self.beliefs.add(formula)

    def remove_belief(self, formula):
        """Remove a belief (formula) from the belief base if it exists."""
        self.beliefs.discard(formula)

    def list_beliefs(self):
        """Return a list of all beliefs in the belief base."""
        return list(self.beliefs)

    def clear_beliefs(self):
        """Clear all beliefs from the belief base."""
        self.beliefs.clear()

    def __len__(self):
        """Return the number of beliefs in the belief base."""
        return len(self.beliefs)

    def __str__(self):
        """String representation of the belief base."""
        if not self.beliefs:
            return "Belief Base is empty."
        sorted_beliefs = sorted(self.beliefs)
        return "Belief Base:\n" + "\n".join(f"- {belief}" for belief in sorted_beliefs)

if __name__ == "__main__":
    bb = BeliefBase()


    print(bb)
    print(f"\nTotal beliefs: {len(bb)}")
