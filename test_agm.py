#!/usr/bin/env python
# coding: utf-8

from belief_base import BeliefBase
from contraction import BeliefContraction
from expansion import BeliefExpansion
from entailment import Resolution
import copy

class BeliefRevisionAgent:
    def __init__(self, belief_base=None):
        self.belief_base = belief_base or BeliefBase()

    def expand(self, formula):
        BeliefExpansion(self.belief_base).expand(formula)

    def contract(self, formula, selector='all'):
        priorities = {b: i for i, b in enumerate(self.belief_base.list_beliefs(), 1)}
        BeliefContraction(self.belief_base, priorities).partial_meet_contract(formula, selector=selector)

    def revise(self, formula, selector='all'):
        negated_formula = f"¬({formula})"
        if formula.startswith("¬") and formula[1] == "(" and formula.endswith(")"):
            negated_formula = formula[2:-1]
        self.contract(negated_formula, selector)
        self.expand(formula)

def test_agm_postulates(original_bb, formula, revised_bb, equivalent_formula=None):
    original = set(original_bb.list_beliefs())
    revised = set(revised_bb.list_beliefs())
    initially_entailed = Resolution.entails(list(original), formula)

    print(f"\n🧪 AGM Postulates for revision with: '{formula}'")

    success = Resolution.entails(list(revised), formula)
    print(f"✔️ Success: {'PASSED' if success else 'FAILED'}")

    inclusion = revised.issubset(original.union({formula}))
    print(f"📥 Inclusion: {'PASSED' if inclusion else 'FAILED'}")

    if not initially_entailed:
        vacuity = original == revised
        print(f"🫙 Vacuity: {'PASSED' if vacuity else 'FAILED'}")
    else:
        print("🫙 Vacuity: (not applicable, formula was entailed)")

    consistent = Resolution.is_consistent(list(revised))
    print(f"✅ Consistency: {'PASSED' if consistent else 'FAILED'}")

    if equivalent_formula:
        bb1 = copy.deepcopy(original_bb)
        bb2 = copy.deepcopy(original_bb)
        agent1 = BeliefRevisionAgent(bb1)
        agent2 = BeliefRevisionAgent(bb2)
        agent1.revise(formula)
        agent2.revise(equivalent_formula)
        extensional = set(agent1.belief_base.list_beliefs()) == set(agent2.belief_base.list_beliefs())
        print(f"🔁 Extensionality (with '{equivalent_formula}'): {'PASSED' if extensional else 'FAILED'}")
    else:
        print("🔁 Extensionality: (not tested – no equivalent formula provided)")

def create_sample_belief_base():
    bb = BeliefBase()
    bb.add_belief("A")
    bb.add_belief("A → B")
    bb.add_belief("(B ∧ C) → D")
    bb.add_belief("D ↔ E")
    bb.add_belief("(F ∨ G) → H")
    bb.add_belief("(H ∧ I) ↔ J")
    bb.add_belief("J → K")
    bb.add_belief("F")
    bb.add_belief("C ∨ L")
    bb.add_belief("M ∧ N")
    bb.add_belief("(¬K ∨ N) → O")
    bb.add_belief("(P ∨ Q) → R")
    bb.add_belief("(R ∧ S) ↔ (T ∨ U)")
    bb.add_belief("¬(¬E) → V")
    bb.add_belief("(V ∧ W) → X")
    return bb

def user_interaction_test():
    bb = create_sample_belief_base()
    agent = BeliefRevisionAgent(copy.deepcopy(bb))

    print("\n=== Initial Belief Base ===")
    for i, belief in enumerate(bb.list_beliefs(), 1):
        print(f"{i}. {belief}")

    formula = input("\nEnter a propositional formula to revise with: ").strip()
    agent.revise(formula)

    print("\n🔁 Revised Belief Base:")
    for belief in agent.belief_base.list_beliefs():
        print("-", belief)

    test_agm_postulates(bb, formula, agent.belief_base)

def run_batch_tests():
    test_cases = [
        ("B", "¬¬B"),
        ("E", None),
        ("F", None),
        ("K", None),
        ("(A ∨ B)", None),
        ("(¬J ∨ K)", None),
        ("(¬C ∨ H)", "(¬¬C ∨ H)")
    ]

    for formula, equiv in test_cases:
        bb = create_sample_belief_base()
        agent = BeliefRevisionAgent(copy.deepcopy(bb))
        agent.revise(formula)
        test_agm_postulates(bb, formula, agent.belief_base, equivalent_formula=equiv)

def main():
    print("=== Belief Revision Agent: AGM Testing ===")
    while True:
        choice = input("\nChoose an option:\n1. Manual user input\n2. Run batch test cases\n3. Exit\n> ").strip()
        if choice == '1':
            user_interaction_test()
        elif choice == '2':
            run_batch_tests()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
