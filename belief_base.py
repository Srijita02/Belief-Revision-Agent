import itertools

class BeliefBase:
    def __init__(self):
        """initialize an empty belief base."""
        self.beliefs = set()

    def add_belief(self, formula):
        """add a belief to the belief base."""
        self.beliefs.add(formula)

    def remove_belief(self, formula):
        """remove a belief (formula) from belief base if it exists."""
        self.beliefs.discard(formula)

    def list_beliefs(self):
        """return a list of all beliefs in the belief base."""
        return list(self.beliefs)

    def clear_beliefs(self):
        """clear all beliefs from belief base."""
        self.beliefs.clear()

    def __len__(self):
        """return the number of beliefs in belief base."""
        return len(self.beliefs)

    def __str__(self):
        """string representation of the belief base."""
        if not self.beliefs:
            return "Belief Base is empty."
        sorted_beliefs = sorted(self.beliefs)
        return "Belief Base:\n" + "\n".join(f"- {belief}" for belief in sorted_beliefs)


# New Belief Base for the Mastermind game
class MastermindBeliefBase:
    def __init__(self, colors, code_length):
        """
        initialize the belief base with all possible code combinations.
        """
        self.colors = colors
        self.code_length = code_length
        self.possible_codes = list(itertools.product(colors, repeat=code_length))  # All possible combinations
        self.beliefs = set(self.possible_codes)  # Initial belief base contains all possible codes

    def remove_belief(self, formula):
        """remove a belief from the belief base."""
        self.beliefs.discard(formula)

    def add_belief(self, formula):
        """add a belief to belief base."""
        self.beliefs.add(formula)

    def list_beliefs(self):
        """return list of all beliefs in belief base."""
        return list(self.beliefs)

    def __str__(self):
        """string representation of belief base."""
        return f"Belief Base contains {len(self.beliefs)} possible codes"

