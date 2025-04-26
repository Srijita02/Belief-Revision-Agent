#!/usr/bin/env python
# coding: utf-8

# In[6]:


from entailment import Resolution

class BeliefContraction:
    def __init__(self, belief_base, priorities=None):
        """
        belief_base: a BeliefBase instance
        priorities: dict mapping formula -> priority (higher number = more important)
        """
        self.belief_base = belief_base
        if priorities is None:
            self.priorities = {}
        else:
            self.priorities = priorities

    def contract(self, formula):
        """
        Contract the belief base by a formula.
        Removes formulas to ensure the formula is no longer entailed.
        """
        if not Resolution.entails(self.belief_base.list_beliefs(), formula):
            print(f"No need to contract. Belief base does not entail '{formula}'.")
            return
        
        # Sort beliefs by priority (lowest priority removed first)
        sorted_beliefs = sorted(
            list(self.belief_base.beliefs),
            key=lambda f: self.priorities.get(f, 0)
        )

        # Try removing beliefs one by one
        for belief in sorted_beliefs:
            self.belief_base.remove_belief(belief)
            if not Resolution.entails(self.belief_base.list_beliefs(), formula):
                print(f"Contracted successfully by removing '{belief}'.")
                return
        print("Warning: Could not fully contract.")


# In[10]:


get_ipython().system('jupyter nbconvert --to script contraction.ipynb')


# In[ ]:




