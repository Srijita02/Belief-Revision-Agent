#!/usr/bin/env python
# coding: utf-8

from entailment import Resolution

class BeliefExpansion:
    def __init__(self, belief_base):
        """
        belief_base: a BeliefBase instance
        """
        self.belief_base = belief_base

    def expand(self, formula):
        """
        Expand the belief base by adding a new formula.
        (No consistency check done here.)
        """
        self.belief_base.add_belief(formula)
        print(f"Expanded belief base with '{formula}'.")
