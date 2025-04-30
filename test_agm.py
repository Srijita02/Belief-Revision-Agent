#!/usr/bin/env python
# coding: utf-8

from belief_base import BeliefBase
from contraction import BeliefContraction
from entailment import Resolution
from expansion import BeliefExpansion  # NEW: for testing expansion
import copy

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
    bb.add_belief("(¬M ∨ Q)")
    bb.add_belief("(¬Q ∨ R)")
    bb.add_belief("(¬N ∨ S)")
    bb.add_belief("(¬R ∨ T)")
    bb.add_belief("(¬S ∨ T)")
    bb.add_belief("(¬T ∨ U)")
    bb.add_belief("(¬U ∨ V)")
    bb.add_belief("(¬P ∨ W)")
    bb.add_belief("(¬W ∨ X)")
    bb.add_belief("(¬X ∨ Y)")
    bb.add_belief("(¬Y ∨ Z)")
    bb.add_belief("(¬Z ∨ A)")
    bb.add_belief("(V ∨ A)")
    bb.add_belief("(X ∨ B)")
    bb.add_belief("(¬R ∨ M)")
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

def test_agm_postulates(bb, formula, equivalent_formula=None):
    print(f"\n=== Testing AGM Postulates for contraction of '{formula}' ===")
    original_beliefs = set(bb.list_beliefs())

    bb_clone = copy.deepcopy(bb)
    contractor = BeliefContraction(bb_clone)
    contractor.contract(formula)

    new_beliefs = set(bb_clone.list_beliefs())

    success = not Resolution.entails(bb_clone.list_beliefs(), formula)
    print(f"Success Postulate: {'PASSED' if success else 'FAILED'}")

    inclusion = new_beliefs.issubset(original_beliefs)
    print(f"Inclusion Postulate: {'PASSED' if inclusion else 'FAILED'}")

    is_consistent = Resolution.is_consistent(bb_clone.list_beliefs())
    print(f"Consistency Postulate: {'PASSED' if is_consistent else 'FAILED'}")

    if not Resolution.entails(original_beliefs, formula):
        vacuity = original_beliefs == new_beliefs
        print(f"Vacuity Postulate: {'PASSED' if vacuity else 'FAILED'}")
    else:
        print(f"Vacuity Postulate: (not applicable – formula was entailed)")

    if equivalent_formula:
        bb1 = copy.deepcopy(bb)
        bb2 = copy.deepcopy(bb)

        BeliefContraction(bb1).contract(formula)
        BeliefContraction(bb2).contract(equivalent_formula)

        extensionality = set(bb1.list_beliefs()) == set(bb2.list_beliefs())
        print(f"Extensionality Postulate: {'PASSED' if extensionality else 'FAILED'}")
    else:
        print("Extensionality Postulate: (not tested – no equivalent formula provided)")

def test_expansion(bb):
    print("\n=== TESTING EXPANSION ===")
    expander = BeliefExpansion(bb)
    new_formula = "(¬Z ∨ B)"  # A new belief to add
    before = len(bb)
    expander.expand(new_formula)
    after = len(bb)
    print(f"Belief base size: before = {before}, after = {after}")
    print("Belief base after expansion:")
    print(bb)
    if new_formula in bb.list_beliefs():
        print("Expansion Test: ✅ PASSED")
    else:
        print("Expansion Test: ❌ FAILED")

def main():
    print("\n=== BELIEF REVISION - FINAL TEST ===")

    bb = create_big_belief_base()
    print("\nInitial Belief Base:")
    print(bb)

    # Step 1: Entailment checks
    show_entailment(bb, "B")
    show_entailment(bb, "C")
    show_entailment(bb, "E")
    show_entailment(bb, "I")
    show_entailment(bb, "M")

    # Step 2: Contraction and rechecking
    contract_and_check(bb, "C")
    contract_and_check(bb, "E")

    # Step 3: AGM Postulates
    test_agm_postulates(bb, "B", equivalent_formula="¬¬B")
    test_agm_postulates(bb, "C")
    test_agm_postulates(bb, "E", equivalent_formula="¬¬E")

    # Step 4: Expansion Test
    test_expansion(bb)

    print("\n=== END OF TEST ===")

if __name__ == "__main__":
    main()
