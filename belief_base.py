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

    # Big and smart belief base
    initial_beliefs = [
        "A",
        "(¬A ∨ B)",         # A → B
        "(¬B ∨ C)",         # B → C
        "(¬B ∨ D)",         # B → D
        "(¬C ∨ E)",         # C → E
        "(¬C ∨ F)",         # C → F
        "(¬D ∨ G)",         # D → G
        "(¬D ∨ H)",         # D → H
        "(¬E ∨ I)",         # E → I
        "(¬F ∨ J)",         # F → J
        "(¬G ∨ K)",         # G → K
        "(¬H ∨ L)",         # H → L
        "(¬I ∨ M)",         # I → M
        "(¬J ∨ N)",         # J → N
        "(¬K ∨ O)",         # K → O
        "(¬L ∨ P)",         # L → P
        "(M ∨ N)",          # M or N
        "(O ∧ P)",          # O and P
        "(¬M ∨ Q)",         # M → Q
        "(¬N ∨ R)",         # N → R
        "(¬O ∨ S)",         # O → S
        "(¬P ∨ T)",         # P → T
        "(Q ∧ R) → U",      # (Q and R) → U
        "(S ∧ T) → V",      # (S and T) → V
        "(U ∨ V) → W",      # (U or V) → W
    ]

    for belief in initial_beliefs:
        bb.add_belief(belief)

    print(bb)
    print(f"\nTotal beliefs: {len(bb)}")
