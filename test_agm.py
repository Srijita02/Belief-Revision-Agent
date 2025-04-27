#!/usr/bin/env python
# coding: utf-8

from belief_base import BeliefBase
from contraction import BeliefContraction
from entailment import Resolution

def create_big_belief_base():
    bb = BeliefBase()
    bb.add_belief("A")
    bb.add_belief("(¬A ∨ B)")
    bb.add_belief("(¬B ∨ C)")
    bb.add_belief("(¬B ∨ D)")
    bb.add_belief("(¬C ∨ E)")
    bb.add_belief("(¬D ∨ G)")
    bb.add_belief("(¬E ∨ I)")
    bb.add_belief("(¬G ∨ K)")
    bb.add_belief("(¬I ∨ M)")
    bb.add_belief("(¬K ∨ O)")
    bb.add_belief("(M ∨ N)")
    bb.add_belief("(O ∧ P)")
    return bb

def show_entailment(bb, formula):
    print(f"\nChecking entailment: Does Belief Base entail '{formula}'?")
    result = Resolution.entails(bb.list_beliefs(), formula)
    print(f"Result: {'YES' if result else 'NO'}")
    return result

def contract_and_check(bb, formula):
    print(f"\nTrying to contract '{formula}'...")
    priorities = {belief: 1 for belief in bb.list_beliefs()}
    contractor = BeliefContraction(bb, priorities)
    contractor.contract(formula)
    result = Resolution.entails(bb.list_beliefs(), formula)
    print(f"After contraction: Does Belief Base still entail '{formula}'? {'YES' if result else 'NO'}")
    return result

def test_agm_postulates(bb, formula):
    print(f"\n=== Testing AGM Postulates for contraction of '{formula}' ===")
    original_beliefs = set(bb.list_beliefs())

    contractor = BeliefContraction(bb)
    contractor.contract(formula)

    success = not Resolution.entails(bb.list_beliefs(), formula)
    inclusion = set(bb.list_beliefs()).issubset(original_beliefs)
    is_consistent = Resolution.is_consistent(bb.list_beliefs())

    print(f"Success Postulate: {'PASSED' if success else 'FAILED'}")
    print(f"Inclusion Postulate: {'PASSED' if inclusion else 'FAILED'}")
    print(f"Consistency Postulate: {'PASSED' if is_consistent else 'FAILED'}")

def main():
    print("\n=== BELIEF REVISION - FINAL TEST ===")

    bb = create_big_belief_base()
    print("\nInitial Belief Base:")
    print(bb)

    show_entailment(bb, "B")
    show_entailment(bb, "C")
    show_entailment(bb, "E")
    show_entailment(bb, "I")
    show_entailment(bb, "M")

    contract_and_check(bb, "C")
    contract_and_check(bb, "E")

    test_agm_postulates(bb, "B")

    print("\n=== END OF TEST ===")

if __name__ == "__main__":
    main()
