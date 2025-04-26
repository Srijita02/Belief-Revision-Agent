#!/usr/bin/env python
# coding: utf-8

# In[1]:


from entailment import Resolution

class BeliefExpansion:
    def __init__(self, belief_base):
        self.belief_base = belief_base

    def expand(self, formula):
        """
        Expand the belief base by adding a new formula.
        (No check for consistency here; could be added if needed.)
        """
        self.belief_base.add_belief(formula)
        print(f"Expanded belief base with '{formula}'.")


# In[3]:


get_ipython().system('jupyter nbconvert --to script expansion.ipynb')


# In[ ]:




