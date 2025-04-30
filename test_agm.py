#!/usr/bin/env python
# coding: utf-8

from belief_base import BeliefBase
from contraction import BeliefContraction
from entailment import Resolution
import copy

def create_big_belief_base():
    bb = BeliefBase()
    bb.add_belief("A")  # adding belief A
    bb.add_belief("(¬A ∨ B)")  # adding belief (¬A ∨ B)
    bb.add_belief("(¬B ∨ C)")  # adding belief (¬B ∨ C)
    bb.add_belief("(¬B ∨ D)")  # adding belief (¬B ∨ D)
    bb.add_belief("(¬C ∨ E)")  # adding belief (¬C ∨ E)
    bb.add_belief("(¬D ∨ G)")  # adding belief (¬D ∨ G)
    bb.add_belief("(¬E ∨ I)")  # adding belief (¬E ∨ I)
    bb.add_belief("(¬G ∨ K)")  # adding belief (¬G ∨ K)
    bb.add_belief("(¬I ∨ M)")  # adding belief (¬I ∨ M)
    bb.add_belief("(¬K ∨ O)")  # adding belief (¬K ∨ O)
    bb.add_belief("(M ∨ N)")  # adding belief (M ∨ N)
    bb.add_belief("(O ∧ P)")  # adding belief (O ∧ P)

    # additional beliefs for complexity
    bb.add_belief("(¬M ∨ Q)")  # adding belief (¬M ∨ Q)
    bb.add_belief("(¬Q ∨ R)")  # adding belief (¬Q ∨ R)
    bb.add_belief("(¬N ∨ S)")  # adding belief (¬N ∨ S)
    bb.add_belief("(¬R ∨ T)")  # adding belief (¬R ∨ T)
    bb.add_belief("(¬S ∨ T)")  # adding belief (¬S ∨ T)
    bb.add_belief("(¬T ∨ U)")  # adding belief (¬T ∨ U)
    bb.add_belief("(¬U ∨ V)")  # adding belief (¬U ∨ V)
    bb.add_belief("(¬P ∨ W)")  # adding belief (¬P ∨ W)
    bb.add_belief("(¬W ∨ X)")  # adding belief (¬W ∨ X)
    bb.add_belief("(¬X ∨ Y)")  # adding belief (¬X ∨ Y)
    bb.add_belief("(¬Y ∨ Z)")  # adding belief (¬Y ∨ Z)

    # some circular or redundant logic
    bb.add_belief("(¬Z ∨ A)")  # circular reference
    bb.add_belief("(V ∨ A)")  # redundant re-affirmation of A
    bb.add_belief("(X ∨ B)")  # cross-path connection
    bb.add_belief("(¬R ∨ M)")  # feedback link

    return bb

def show_entailment(bb, formula):
    print(f"\nChecking entailment: Does Belief Base entail '{formula}'?")  # checking entailment of formula
    result = Resolution.entails(bb.list_beliefs(), formula)  # using resolution to check entailment
    print(f"Result: {'YES' if result else 'NO'}")  # printing result of entailment
    return result

def contract_and_check(bb, formula):
    print(f"\nTrying to contract '{formula}'...")  # trying to contract formula
    priorities = {belief: 1 for belief in bb.list_beliefs()}  # setting priorities for beliefs
    contractor = BeliefContraction(bb, priorities)  # creating a contractor for belief contraction
    contractor.contract(formula)  # contracting the formula
    result = Resolution.entails(bb.list_beliefs(), formula)  # checking if the formula is still entailed after contraction
    print(f"After contraction: Does Belief Base still entail '{formula}'? {'YES' if result else 'NO'}")  # printing result
    return result

def test_agm_postulates(bb, formula, equivalent_formula=None):
    print(f"\n=== Testing AGM Postulates for contraction of '{formula}' ===")  # testing AGM postulates
    original_beliefs = set(bb.list_beliefs())  # storing original beliefs

    # clone the belief base for isolation
    bb_clone = copy.deepcopy(bb)  # deep cloning the belief base to prevent mutation
    contractor = BeliefContraction(bb_clone)  # creating contractor for belief contraction
    contractor.contract(formula)  # contracting the formula

    new_beliefs = set(bb_clone.list_beliefs())  # storing new beliefs after contraction

    # success postulate
    success = not Resolution.entails(bb_clone.list_beliefs(), formula)  # check if formula is no longer entailed
    print(f"Success Postulate: {'PASSED' if success else 'FAILED'}")  # printing result for success postulate

    # inclusion postulate
    inclusion = new_beliefs.issubset(original_beliefs)  # checking if new beliefs are subset of original beliefs
    print(f"Inclusion Postulate: {'PASSED' if inclusion else 'FAILED'}")  # printing result for inclusion postulate

    # consistency postulate
    is_consistent = Resolution.is_consistent(bb_clone.list_beliefs())  # checking consistency of beliefs after contraction
    print(f"Consistency Postulate: {'PASSED' if is_consistent else 'FAILED'}")  # printing result for consistency postulate

    # vacuity postulate
    if not Resolution.entails(original_beliefs, formula):  # checking if formula was not entailed before contraction
        vacuity = original_beliefs == new_beliefs  # checking if beliefs are unchanged
        print(f"Vacuity Postulate: {'PASSED' if vacuity else 'FAILED'}")  # printing result for vacuity postulate
    else:
        print(f"Vacuity Postulate: (not applicable – formula was entailed)")  # printing when vacuity is not applicable

    # extensionality postulate (optional argument)
    if equivalent_formula:  # checking if an equivalent formula is provided
        bb1 = copy.deepcopy(bb)  # deep cloning the belief base again for comparison
        bb2 = copy.deepcopy(bb)  # deep cloning the belief base again for comparison

        BeliefContraction(bb1).contract(formula)  # contracting formula in first belief base
        BeliefContraction(bb2).contract(equivalent_formula)  # contracting equivalent formula in second belief base

        extensionality = set(bb1.list_beliefs()) == set(bb2.list_beliefs())  # checking if both contracted beliefs are the same
        print(f"Extensionality Postulate: {'PASSED' if extensionality else 'FAILED'}")  # printing result for extensionality postulate
    else:
        print("Extensionality Postulate: (not tested – no equivalent formula provided)")  # printing if no equivalent formula is provided

def main():
    print("\n=== BELIEF REVISION - FINAL TEST ===")  # printing header for final test

    bb = create_big_belief_base()  # creating the belief base
    print("\nInitial Belief Base:")
    print(bb)  # printing initial belief base

    # check entailment
    show_entailment(bb, "B")  # check entailment for B
    show_entailment(bb, "C")  # check entailment for C
    show_entailment(bb, "E")  # check entailment for E
    show_entailment(bb, "I")  # check entailment for I
    show_entailment(bb, "M")  # check entailment for M

    # contract and check entailment
    contract_and_check(bb, "C")  # contract and check for C
    contract_and_check(bb, "E")  # contract and check for E

    # test AGM postulates
    test_agm_postulates(bb, "B", equivalent_formula="¬¬B")  # test AGM postulates for B
    test_agm_postulates(bb, "C")  # test AGM postulates for C
    test_agm_postulates(bb, "E", equivalent_formula="¬¬E")  # test AGM postulates for E

    print("\n=== END OF TEST ===")  # printing footer for test completion

if __name__ == "__main__":
    main()  # calling the main function
