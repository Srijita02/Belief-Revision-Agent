from belief_base import BeliefBase
from contraction import BeliefContraction
from expansion import BeliefExpansion
from entailment import Resolution
import copy

class BeliefRevisionAgent:
    def __init__(self, belief_base=None):
        self.belief_base = belief_base or BeliefBase()
    
    def expand(self, formula):
        print(f"[EXPANSION] Adding formula '{formula}' to belief base")
        BeliefExpansion(self.belief_base).expand(formula)
    
    def contract(self, formula, selector='max'):
        print(f"[CONTRACTION] Removing entailment of '{formula}' using {selector} selection")
        BeliefContraction(self.belief_base, selector).partial_meet_contract(formula)
    
    def revise(self, formula, selector='max'):
        print(f"[REVISION] Starting revision with formula '{formula}'")
        
        # Normalize formula for contraction purposes
        normalized_formula = formula
        
        # Handle double negations
        while normalized_formula.startswith('¬¬'):
            normalized_formula = normalized_formula[2:]
            print(f"[NORMALIZATION] Simplified double negation to '{normalized_formula}'")
        
        # Determine what to contract
        if normalized_formula.startswith('¬') and '(' in normalized_formula and normalized_formula.endswith(')'):
            # Extract the content between parentheses in a negated formula
            open_paren_index = normalized_formula.find('(')
            negated = normalized_formula[open_paren_index+1:-1]
            print(f"[NORMALIZATION] Extracted inner formula from negation: '{negated}'")
        else:
            negated = f"¬({normalized_formula})"
            print(f"[NORMALIZATION] Created negation for contraction: '{negated}'")
        
        # Perform contraction and expansion
        self.contract(negated, selector)
        self.expand(formula)  # Keep original formula for expansion
        print(f"[REVISION] Completed revision with '{formula}'")

def test_agm_postulates(before, formula, after, equiv_formula=None):
    print(f"\n[TEST] Testing AGM revision with: '{formula}'")
    original_set = set(before.list_beliefs())
    revised_set = set(after.list_beliefs())
    
    # Test Success postulate
    success_result = Resolution.entails(list(revised_set), formula)
    print(f"[ENTAILMENT] Testing if revised base entails '{formula}': {success_result}")
    print("[TEST] Success:", "PASSED" if success_result else "FAILED")
    
    # Test Inclusion postulate
    inclusion_result = revised_set.issubset(original_set.union({formula}))
    print("[TEST] Inclusion:", "PASSED" if inclusion_result else "FAILED")
    
    # Test Vacuity postulate
    entailment_result = Resolution.entails(list(original_set), formula)
    print(f"[ENTAILMENT] Testing if original base already entails '{formula}': {entailment_result}")
    if not entailment_result:
        vacuity_result = original_set == revised_set
        print("[TEST] Vacuity:", "PASSED" if vacuity_result else "FAILED")
    else:
        print("[TEST] Vacuity: (not applicable)")
    
    # Test Consistency postulate
    consistency_result = Resolution.is_consistent(list(revised_set))
    print("[CONSISTENCY] Checking if revised belief base is consistent")
    print("[TEST] Consistency:", "PASSED" if consistency_result else "FAILED")
    
    # Test Extensionality postulate
    if equiv_formula:
        print(f"[EXTENSIONALITY] Testing if revision with '{formula}' equals revision with '{equiv_formula}'")
        base1 = copy.deepcopy(before)
        base2 = copy.deepcopy(before)
        agent1 = BeliefRevisionAgent(base1)
        agent2 = BeliefRevisionAgent(base2)
        agent1.revise(formula)
        agent2.revise(equiv_formula)
        set1 = set(agent1.belief_base.list_beliefs())
        set2 = set(agent2.belief_base.list_beliefs())
        extensionality_result = set1 == set2
        print("[TEST] Extensionality:", f"{'PASSED' if extensionality_result else 'FAILED'}")
        
        if not extensionality_result:
            print("[EXTENSIONALITY] Difference in belief sets:")
            print(f"  - Set 1 (revised with '{formula}'): {set1}")
            print(f"  - Set 2 (revised with '{equiv_formula}'): {set2}")
            only_in_set1 = set1 - set2
            only_in_set2 = set2 - set1
            if only_in_set1:
                print(f"  - Only in Set 1: {only_in_set1}")
            if only_in_set2:
                print(f"  - Only in Set 2: {only_in_set2}")
    else:
        print("[TEST] Extensionality: (not tested)")
    print("----------------------------------------------------------------------------------------------------------------------------")

def create_sample_base():
    print("[BELIEF BASE] Creating sample belief base")
    bb = BeliefBase()
    formulas = [
        # Original formulas
        "A", 
        "(¬A ∨ B)", 
        "(¬B ∨ C)", 
        "(¬C ∨ D)", 
        "(D → E)", 
        "(E ∨ F)", 
        "G",
        
        # Additional simple formulas
        "H",
        "I",
        
        # Additional implications
        "(G → H)",
        "(H → I)",
        "(I → J)",
        
        # More complex formulas
        "(A ∧ B)",
        "(C ∨ D)",
        "((A ∧ B) → (C ∨ D))",
        "(¬F → G)"
    ]
    for b in formulas:
        bb.add_belief(b)
        print(f"[BELIEF BASE] Added belief: '{b}'")
    print(f"[BELIEF BASE] Created belief base with {len(formulas)} beliefs")
    return bb

def batch_test():
    print("\n[BATCH TEST] Starting batch tests")
    tests = [
        ("C", "(¬¬C)"),
        ("E", None),
        ("F", None),
        ("D", None),
        ("(A ∨ B)", None),
        ("(¬G ∨ A)", None),
        ("(¬C ∨ G)", "(¬¬C ∨ G)"),
        # Additional test cases
        ("J", None),
        ("(¬H)", None),
        ("((C ∧ D) → E)", None)
    ]
    for i, (fml, equiv) in enumerate(tests, 1):
        print(f"\n[BATCH TEST] Test {i}: '{fml}'")
        base = create_sample_base()
        agent = BeliefRevisionAgent(copy.deepcopy(base))
        agent.revise(fml)
        test_agm_postulates(base, fml, agent.belief_base, equiv)
    print("\n[BATCH TEST] All batch tests completed")

def manual_test():
    print("\n[MANUAL TEST] Starting manual test")
    base = create_sample_base()
    agent = BeliefRevisionAgent(copy.deepcopy(base))
    
    print("\n[MANUAL TEST] Initial Belief Base:")
    for b in base.list_beliefs():
        print(f"- {b}")
    
    fml = input("\n[MANUAL TEST] Enter formula to revise with: ").strip()
    agent.revise(fml)
    
    print("\n[MANUAL TEST] Revised Belief Base:")
    for b in agent.belief_base.list_beliefs():
        print(f"- {b}")
    
    test_agm_postulates(base, fml, agent.belief_base)
    print("[MANUAL TEST] Manual test completed")

def main():
    print("=== Belief Revision Agent ===")
    while True:
        choice = input("\n1. Manual input\n2. Run batch tests\n3. Exit\n> ").strip()
        if choice == '1':
            manual_test()
        elif choice == '2':
            batch_test()
        elif choice == '3':
            print("[SYSTEM] Exiting program")
            break
        else:
            print("[SYSTEM] Invalid choice, please try again")

if __name__ == "__main__":
    print("[SYSTEM] Starting Belief Revision Agent")
    main()