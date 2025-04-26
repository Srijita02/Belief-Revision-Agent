#!/usr/bin/env python
# coding: utf-8

# In[5]:


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


# Example usage:
if __name__ == "__main__":
    bb = BeliefBase()

    # Adding a set of beliefs
    initial_beliefs = [
        "(A ∨ B)",
        "(¬A ∨ C)",
        "(¬B ∨ D)",
        "(E ∨ F)",
        "(¬E ∨ G)",
        "(H ∨ I)",
        "(¬H ∨ J)",
        "(K ∨ L)",
        "(¬K ∨ M)",
        "(N ∨ O)",
        "(P ∨ Q)",
        "(¬P ∨ R)",
        "(S ∨ T)",
        "(U ∨ V)",
        "(W ∨ X)",
        "(Y ∨ Z)",
        "(¬Y ∨ A)",
        "(¬X ∨ B)",
        "(¬W ∨ C)",
        "(¬U ∨ D)",
        "(¬A ∨ (B ∧ C))",
        "((D ∧ E) ∨ (F ∧ G))",
        "(H ∨ (I ∧ J))",
        "((K ∨ L) ∧ (M ∨ ¬N))",
        "(O ∧ (P ∨ Q))",
        "(¬R ∨ (S ∧ T))",
        "((U ∨ V) ∧ (¬W ∨ X))",
        "(Y ∨ (Z ∧ A))",
        "((B ∧ C) ∨ (D ∧ ¬E))",
        "(F ∨ (G ∧ H ∨ I))",
        "(J ∨ (¬K ∧ L))",
        "((M ∧ N) ∨ (O ∨ ¬P))",
        "(Q ∨ (R ∧ (S ∨ T)))",
        "((U ∨ V) ∧ (W ∨ ¬X))",
        "(Y ∧ (Z ∨ (A ∧ B)))",
        "(¬(C ∧ D) ∨ (E ∨ F))",
        "((G ∧ ¬H) ∨ (I ∧ J))",
        "(K ∨ (L ∧ (M ∨ ¬N)))",
        "((O ∨ P) ∧ (¬Q ∨ R))",
        "(S ∧ (T ∨ U))",
        "(V ∨ (W ∧ ¬X))",
        "((Y ∧ Z) ∨ (A ∧ B))",
        "(¬(C ∧ D) ∨ (E ∧ F))",
        "(G ∨ (H ∧ (I ∨ J)))"
    ]

    # Bulk add beliefs
    for belief in initial_beliefs:
        bb.add_belief(belief)

    print(bb)
    print(f"\nTotal beliefs: {len(bb)}")

    # Removing some beliefs
    beliefs_to_remove = [
        "(¬A ∨ C)", "(A ∨ B)",
        "((K ∨ L) ∧ (M ∨ ¬N))",
        "(Y ∨ (Z ∧ A))"
    ]

    for belief in beliefs_to_remove:
        bb.remove_belief(belief)

    print("\nAfter removing some beliefs:")
    print(bb)
    print(f"\nTotal beliefs: {len(bb)}")

    # List all beliefs
    beliefs_list = bb.list_beliefs()
    print("\nBeliefs as a list:", beliefs_list)

    # Clearing the entire belief base
    #bb.clear_beliefs()
    #print("\nAfter clearing all beliefs:")
    #print(bb)


# In[10]:


#!jupyter nbconvert --to script belief_base.ipynb

