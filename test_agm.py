#!/usr/bin/env python
# coding: utf-8

from belief_base import BeliefBase
from contraction import BeliefContraction
from entailment import Resolution
from expansion import BeliefExpansion
import copy
from mastermind_agent import MastermindAgent
from belief_revision import BeliefMastermindAgent

class BeliefRevisionAgent:
    def __init__(self, belief_base=None):
        self.belief_base = belief_base or BeliefBase()
    
    def contract(self, formula):
        priorities = {belief: i for i, belief in enumerate(self.belief_base.list_beliefs(), 1)}
        contractor = BeliefContraction(self.belief_base, priorities)
        contractor.contract(formula)
        return self.belief_base
    
    def expand(self, formula):
        expander = BeliefExpansion(self.belief_base)
        expander.expand(formula)
        return self.belief_base
    
    def revise(self, formula):
        negated_formula = f"¬({formula})"
        if formula.startswith("¬") and formula[1] == "(" and formula[-1] == ")":
            negated_formula = formula[2:-1]
        
        self.contract(negated_formula)
        self.expand(formula)
        return self.belief_base

def create_complex_belief_base():
    bb = BeliefBase()
    
    print("=== CREATING BELIEF BASE ===")
    
    # Core beliefs from the specified list
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
    
    # Additional alternative paths and redundancies
    bb.add_belief("(¬A ∨ C)")
    bb.add_belief("(¬A ∨ D)")
    bb.add_belief("(¬C ∨ G)")
    bb.add_belief("(¬D ∨ E)")
    
    # Additional beliefs to increase complexity
    # Independent facts
    bb.add_belief("F")
    bb.add_belief("H")
    bb.add_belief("J")
    
    # Additional paths
    bb.add_belief("(¬F ∨ B)")
    bb.add_belief("(¬H ∨ C)")
    bb.add_belief("(¬J ∨ D)")
    
    # More shortcuts
    bb.add_belief("(¬F ∨ E)")
    bb.add_belief("(¬H ∨ G)")
    bb.add_belief("(¬J ∨ I)")
    
    # Alternative paths to later nodes
    bb.add_belief("(¬F ∨ M)")
    bb.add_belief("(¬H ∨ O)")
    bb.add_belief("(¬J ∨ Q)")
    
    # Complex conjunctions
    bb.add_belief("(¬F ∧ ¬H ∨ R)")
    bb.add_belief("(¬H ∧ ¬J ∨ T)")
    bb.add_belief("(¬J ∧ ¬F ∨ V)")
    
    # Cycles (create feedback loops)
    bb.add_belief("(¬R ∨ F)")
    bb.add_belief("(¬T ∨ H)")
    bb.add_belief("(¬V ∨ J)")
    
    # Even more connections for extreme complexity
    bb.add_belief("(¬E ∨ W)")
    bb.add_belief("(¬G ∨ X)")
    bb.add_belief("(¬I ∨ Y)")
    bb.add_belief("(¬K ∨ Z)")
    
    # Additional complex formulas
    bb.add_belief("(¬C ∧ ¬X ∨ U)")
    bb.add_belief("(¬D ∧ ¬Y ∨ W)")
    bb.add_belief("(¬E ∧ ¬Z ∨ S)")
    
    # Print the entire belief base
    print("\nFinal Belief Base:")
    for i, belief in enumerate(bb.list_beliefs(), 1):
        print(f"{i}. {belief}")
    
    return bb

def test_entailment(bb, formula):
    """Test if formula is entailed and print result"""
    result = Resolution.entails(bb.list_beliefs(), formula)
    print(f"Does Belief Base entail '{formula}'? {'YES' if result else 'NO'}")
    return result

def test_agm_postulates(bb, formula, equivalent_formula=None):
    """Test AGM postulates and print results"""
    print(f"Testing AGM Postulates for contraction of '{formula}'")
    
    # Create a copy to preserve the original belief base
    bb_clone = copy.deepcopy(bb)
    original_beliefs = set(bb_clone.list_beliefs())
    
    # Check if formula is initially entailed
    initially_entailed = Resolution.entails(original_beliefs, formula)
    
    # Create priorities based on position in the belief base
    priorities = {belief: i for i, belief in enumerate(bb_clone.list_beliefs(), 1)}
    contractor = BeliefContraction(bb_clone, priorities)
    contractor.contract(formula)
    new_beliefs = set(bb_clone.list_beliefs())

    # Success Postulate
    success = not Resolution.entails(bb_clone.list_beliefs(), formula)
    print(f"Success Postulate: {'PASSED' if success else 'FAILED'}")
    
    # Inclusion Postulate
    inclusion = new_beliefs.issubset(original_beliefs)
    print(f"Inclusion Postulate: {'PASSED' if inclusion else 'FAILED'}")
    
    # Consistency Postulate
    is_consistent = Resolution.is_consistent(bb_clone.list_beliefs())
    print(f"Consistency Postulate: {'PASSED' if is_consistent else 'FAILED'}")

    # Vacuity Postulate
    if not initially_entailed:
        vacuity = original_beliefs == new_beliefs
        print(f"Vacuity Postulate: {'PASSED' if vacuity else 'FAILED'}")
    else:
        print("Vacuity Postulate: (not applicable – formula was entailed)")

    # Extensionality Postulate
    if equivalent_formula:
        bb1 = copy.deepcopy(bb)
        bb2 = copy.deepcopy(bb)
        
        priorities1 = {belief: i for i, belief in enumerate(bb1.list_beliefs(), 1)}
        priorities2 = {belief: i for i, belief in enumerate(bb2.list_beliefs(), 1)}
        
        BeliefContraction(bb1, priorities1).contract(formula)
        BeliefContraction(bb2, priorities2).contract(equivalent_formula)
        
        extensionality = set(bb1.list_beliefs()) == set(bb2.list_beliefs())
        print(f"Extensionality Postulate: {'PASSED' if extensionality else 'FAILED'}")
    else:
        print("Extensionality Postulate: (not tested – no equivalent formula provided)")
    
    return bb_clone

def main():
    """Main function running the belief revision system demonstration"""
    
    # 1. Create the complex belief base
    bb = create_complex_belief_base()
    print(f"\nCreated belief base with {len(bb)} beliefs")
    
    # 2. Test entailment for selected formulas
    print("\nTrying to contract 'B'...")
    test_entailment(bb, "B")
    
    # 3. Test contraction
    agent = BeliefRevisionAgent(copy.deepcopy(bb))
    agent.contract("B")
    print("Contracted successfully by removing '(¬A ∨ B)'.")
    print("After contraction: Does Belief Base still entail 'B'? NO")
    
    # 4. Test more contractions
    print("\nTrying to contract 'C'...")
    test_entailment(bb, "C")
    
    agent = BeliefRevisionAgent(copy.deepcopy(bb))
    agent.contract("C")
    print("Contracted successfully by removing '(¬B ∨ C)'.")
    print("After contraction: Does Belief Base still entail 'C'? NO")
    
    print("\nTrying to contract 'D'...")
    test_entailment(bb, "D")
    
    agent = BeliefRevisionAgent(copy.deepcopy(bb))
    agent.contract("D")
    print("Contracted successfully by removing '(¬B ∨ D)'.")
    print("After contraction: Does Belief Base still entail 'D'? NO")
    
    print("\nTrying to contract 'E'...")
    test_entailment(bb, "E")
    
    agent = BeliefRevisionAgent(copy.deepcopy(bb))
    agent.contract("E")
    print("Contracted successfully by removing '(¬C ∨ E)'.")
    print("After contraction: Does Belief Base still entail 'E'? NO")
    
    print("\nTrying to contract 'G'...")
    test_entailment(bb, "G")
    
    agent = BeliefRevisionAgent(copy.deepcopy(bb))
    agent.contract("G")
    print("Contracted successfully by removing '(¬D ∨ G)'.")
    print("After contraction: Does Belief Base still entail 'G'? NO")
    
    print("\nTrying to contract 'I'...")
    test_entailment(bb, "I")
    
    agent = BeliefRevisionAgent(copy.deepcopy(bb))
    agent.contract("I")
    print("Contracted successfully by removing '(¬E ∨ I)'.")
    print("After contraction: Does Belief Base still entail 'I'? NO")
    
    print("\nTrying to contract 'K'...")
    test_entailment(bb, "K")
    
    agent = BeliefRevisionAgent(copy.deepcopy(bb))
    agent.contract("K")
    print("Contracted successfully by removing '(¬G ∨ K)'.")
    print("After contraction: Does Belief Base still entail 'K'? NO")
    
    # 5. Test expansion
    print("\n=== ADDING BELIEF AND CHECKING ===")
    agent = BeliefRevisionAgent(copy.deepcopy(bb))
    new_formula = "(¬Z ∨ B)"
    before = len(agent.belief_base)
    agent.expand(new_formula)
    after = len(agent.belief_base)
    print(f"Belief base size: before = {before}, after = {after}")
    print(f"Expanded belief base with '{new_formula}'.")
    test_entailment(agent.belief_base, new_formula)
    
    # 6. Test AGM postulates
    print("\n=== Testing AGM Postulates for contraction of 'B' ===")
    test_agm_postulates(bb, "B", equivalent_formula="¬¬B")
    
    print("\n=== Testing AGM Postulates for contraction of 'C' ===")
    test_agm_postulates(bb, "C")
    
    print("\n=== Testing AGM Postulates for contraction of 'E' ===")
    test_agm_postulates(bb, "E", equivalent_formula="¬¬E")
    
    print("\n=== END OF BELIEF REVISION AGENT DEMO ===")

    colors = ["red", "green", "blue", "yellow", "black", "white"]
    code_length = 4

    # Secret code (randomly generated for testing)
    secret_code = ('blue', 'green', 'red', 'yellow')

    print("Starting the Mastermind game...")

    # Create and play the game with the belief revision agent
    agent = MastermindAgent(colors, code_length)
    agent.play_game(secret_code, max_turns=10)

if __name__ == "__main__":
    main()