#!/usr/bin/env python
# coding: utf-8

# In[24]:


# entailment.py

import itertools
import copy

class CNFConverter:
    """
    Converts propositional formulas into CNF.
    Basic version assuming input is already almost in logical form with (¬, ∨, ∧) and parentheses.
    """

    @staticmethod
    def to_cnf(expression):
        # This is a simple placeholder for CNF conversion
        # Ideally, you should parse expression and apply De Morgan's laws, distribution etc.
        # For now, assume expression is already in CNF or close enough
        return CNFConverter._split_clauses(expression)

    @staticmethod
    def _split_clauses(expression):
        # Very basic splitter: assumes ∧ separates clauses
        expression = expression.replace(' ', '')  # Remove whitespace
        clauses = []
        level = 0
        current = ''
        for char in expression:
            if char == '(':
                level += 1
            elif char == ')':
                level -= 1
            if char == '∧' and level == 0:
                clauses.append(current)
                current = ''
            else:
                current += char
        if current:
            clauses.append(current)
        return [CNFConverter._split_literals(clause) for clause in clauses]

    @staticmethod
    def _split_literals(clause):
        # Split a clause into literals separated by ∨
        clause = clause.strip('()')
        literals = clause.split('∨')
        return set(literals)

class Resolution:
    @staticmethod
    def resolve(ci, cj):
        """
        Try to resolve two clauses.
        If they contain complementary literals, produce a new clause.
        """
        resolvents = []
        for di in ci:
            for dj in cj:
                if di == Resolution.negate(dj):
                    new_clause = (ci.union(cj)) - {di, dj}
                    resolvents.append(new_clause)
        return resolvents

    @staticmethod
    def negate(literal):
        """Negate a literal."""
        literal = literal.strip()
        if literal.startswith('¬'):
            return literal[1:]
        else:
            return '¬' + literal

    @staticmethod
    def entails(belief_base, query):
        """
        Check if the belief base entails the query.
        belief_base: list of formulas (strings)
        query: a single formula (string)
        """
        # Step 1: Convert beliefs to CNF
        cnf_beliefs = []
        for belief in belief_base:
            cnf_beliefs.extend(CNFConverter.to_cnf(belief))

        # Step 2: Add negated query (properly split)
        negated_query_literals = Resolution.split_query_negate(query)
        cnf_query = [{literal} for literal in negated_query_literals]

        clauses = cnf_beliefs + cnf_query

        # Step 3: Apply resolution
        new = set()
        while True:
            pairs = list(itertools.combinations(clauses, 2))
            for (ci, cj) in pairs:
                resolvents = Resolution.resolve(ci, cj)
                for resolvent in resolvents:
                    if not resolvent:
                        return True
                    new.add(frozenset(resolvent))

            if new.issubset(set(map(frozenset, clauses))):
                return False

            for clause in new:
                if set(clause) not in clauses:
                    clauses.append(set(clause))

    @staticmethod
    def split_query_negate(query):
        """
        Negates each literal individually if query is a disjunction.
        Example:
            Input: (A ∨ B)
            Output: ['¬A', '¬B']
        """
        query = query.strip()
        if query.startswith("(") and query.endswith(")"):
            query = query[1:-1]

        literals = [lit.strip() for lit in query.split('∨')]
        negated_literals = [Resolution.negate(lit) for lit in literals]
        return negated_literals

    @staticmethod
    def is_consistent(belief_base):
        """
        Check if the belief base is logically consistent.
        Consistent if it does NOT entail False.
        """
        return not Resolution.entails(belief_base, "False")



# In[26]:


get_ipython().system('jupyter nbconvert --to script entailment.ipynb')

