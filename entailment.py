#!/usr/bin/env python
# coding: utf-8

# entailment.py

import itertools

class CNFConverter:
    """
    Converts propositional formulas into CNF.
    Basic version assuming input uses (¬, ∨, ∧) and parentheses.
    """

    @staticmethod
    def to_cnf(expression):
        """
        Very basic CNF converter: splits at ∧ and ∨.
        Assumes expression is close to CNF already.
        """
        return CNFConverter._split_clauses(expression)

    @staticmethod
    def _split_clauses(expression):
        """Split expression into a list of clauses (sets of literals)."""
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
        """Split a clause into literals separated by ∨."""
        clause = clause.strip('()')
        literals = clause.split('∨')
        return set(literals)

class Resolution:
    @staticmethod
    def resolve(ci, cj):
        """Try to resolve two clauses and produce resolvents."""
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
        Check if belief base entails the query using resolution.
        belief_base: list of formulas (strings)
        query: single formula (string)
        """
        # Convert beliefs to CNF
        cnf_beliefs = []
        for belief in belief_base:
            cnf_beliefs.extend(CNFConverter.to_cnf(belief))

        # Add negated query
        negated_query_literals = Resolution.split_query_negate(query)
        cnf_query = [{literal} for literal in negated_query_literals]

        clauses = cnf_beliefs + cnf_query

        # Apply resolution
        new = set()
        while True:
            pairs = list(itertools.combinations(clauses, 2))
            for (ci, cj) in pairs:
                resolvents = Resolution.resolve(ci, cj)
                for resolvent in resolvents:
                    if not resolvent:
                        return True  # Empty clause derived → entailment successful
                    new.add(frozenset(resolvent))

            if new.issubset(set(map(frozenset, clauses))):
                return False  # No new resolvents → entailment failed

            for clause in new:
                if set(clause) not in clauses:
                    clauses.append(set(clause))

    @staticmethod
    def split_query_negate(query):
        """
        Negates each literal individually if query is a disjunction.
        Example: (A ∨ B) → [¬A, ¬B]
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
        Check if the belief base is consistent (does NOT entail False).
        """
        return not Resolution.entails(belief_base, "False")
