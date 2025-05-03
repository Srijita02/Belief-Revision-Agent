#!/usr/bin/env python
# coding: utf-8

from entailment import Resolution
from itertools import chain, combinations

class BeliefContraction:
    def __init__(self, belief_base, priorities=None):
        """
        belief_base: a BeliefBase instance
        priorities: dict mapping formula -> priority (higher number = more important)
        """
        self.belief_base = belief_base
        if priorities is not None:
            self.priorities = priorities
        else:
            # Assign decreasing priority (first-added = highest)
            beliefs = list(self.belief_base.list_beliefs())
            self.priorities = {
                belief: len(beliefs) - i for i, belief in enumerate(beliefs)
            }

    def update_priorities(self, new_priorities):
        """
        Update the priorities with a new dictionary.
        """
        self.priorities.update(new_priorities)

    def auto_assign_priorities(self, reverse=False):
        """
        Automatically assign priorities to the current beliefs.
        Higher priority = more important (larger number).
        reverse=False means earlier beliefs have higher priority.
        reverse=True means later beliefs have higher priority.
        """
        beliefs = list(self.belief_base.list_beliefs())
        if reverse:
            beliefs = list(reversed(beliefs))

        self.priorities = {
            belief: len(beliefs) - i for i, belief in enumerate(beliefs)
        }

    def partial_meet_contract(self, formula, selector='all'):
        """
        Perform Partial Meet Contraction by the formula.
        - selector='all' => use all remainder sets
        - selector='max' => use only remainder sets with highest total priority

        Returns:
            contracted_set (set): The new belief set after contraction.
        """
        def powerset(s):
            "All non-empty subsets of the belief base"
            return [set(c) for c in chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)) if c]

        original_beliefs = set(self.belief_base.beliefs)
        remainders = []

        # Step 1: collect remainder sets (maximal subsets not entailing φ)
        for subset in powerset(original_beliefs):
            if not Resolution.entails(list(subset), formula):
                remainders.append(subset)

        if not remainders:
            self.belief_base.clear_beliefs()
            return set()  # No remainders found → remove all

        # Step 2: apply selector
        if selector == 'all':
            selected = remainders
        elif selector == 'max':
            max_score = max(sum(self.priorities.get(b, 0) for b in r) for r in remainders)
            selected = [r for r in remainders if sum(self.priorities.get(b, 0) for b in r) == max_score]
        else:
            raise ValueError("Selector must be 'all' or 'max'")

        # Step 3: intersect selected remainder sets
        intersection = set.intersection(*selected)
        self.belief_base.beliefs = intersection
        return intersection
