#!/usr/bin/env python
# coding: utf-8

from contraction import BeliefContraction
from expansion import BeliefExpansion
from entailment import Resolution

class BeliefRevision:
    def __init__(self, belief_base, priorities=None):
        """
        belief_base: a BeliefBase instance
        priorities: dictionary of formula priorities (optional)
        """
        self.belief_base = belief_base
        self.priorities = priorities

    def revise(self, formula):
        """
        Revise the belief base by a formula.
        1. Contract the negation of the formula if necessary.
        2. Expand by the formula.
        """
        # Step 1: Contract ¬formula if it is entailed
        negated_formula = Resolution.negate(formula)
        contraction = BeliefContraction(self.belief_base, self.priorities)
        contraction.contract(negated_formula)

        # Step 2: Expand by the formula
        expansion = BeliefExpansion(self.belief_base)
        expansion.expand(formula)
