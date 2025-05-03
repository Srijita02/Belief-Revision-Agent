#!/usr/bin/env python
# coding: utf-8

# entailment.py

import itertools
import re

# ---------- CNF Converter ----------

class Formula:
    def __init__(self, op, left=None, right=None):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self):
        if self.op in {'∧', '∨', '→', '↔'}:
            return f"({self.left} {self.op} {self.right})"
        elif self.op == '¬':
            return f"¬{self.left}"
        return self.op  # atomic


class CNFConverter:
    @staticmethod
    def parse(expr):
        expr = expr.replace(' ', '')
        tokens = re.findall(r'¬|→|↔|∧|∨|\(|\)|[A-Za-z][A-Za-z0-9]*', expr)
        output = []
        ops = []

        def precedence(op):
            return {'¬': 3, '∧': 2, '∨': 2, '→': 1, '↔': 1}.get(op, 0)

        def pop_op():
            op = ops.pop()
            if op == '¬':
                right = output.pop()
                output.append(Formula(op, right))
            else:
                right = output.pop()
                left = output.pop()
                output.append(Formula(op, left, right))

        for token in tokens:
            if re.match(r'[A-Za-z][A-Za-z0-9]*', token):
                output.append(Formula(token))
            elif token == '(':
                ops.append(token)
            elif token == ')':
                while ops[-1] != '(':
                    pop_op()
                ops.pop()
            else:
                while ops and precedence(ops[-1]) >= precedence(token):
                    pop_op()
                ops.append(token)

        while ops:
            pop_op()

        return output[0]

    @staticmethod
    def eliminate_implications(f):
        if f.op == '→':
            return Formula('∨', Formula('¬', CNFConverter.eliminate_implications(f.left)),
                                 CNFConverter.eliminate_implications(f.right))
        elif f.op == '↔':
            A = CNFConverter.eliminate_implications(f.left)
            B = CNFConverter.eliminate_implications(f.right)
            return Formula('∧',
                           Formula('∨', Formula('¬', A), B),
                           Formula('∨', Formula('¬', B), A))
        elif f.op in {'∧', '∨'}:
            return Formula(f.op,
                           CNFConverter.eliminate_implications(f.left),
                           CNFConverter.eliminate_implications(f.right))
        elif f.op == '¬':
            return Formula('¬', CNFConverter.eliminate_implications(f.left))
        else:
            return f

    @staticmethod
    def move_negation_inward(f):
        if f.op == '¬':
            neg = f.left
            if neg.op == '¬':
                return CNFConverter.move_negation_inward(neg.left)
            elif neg.op == '∧':
                return Formula('∨',
                               CNFConverter.move_negation_inward(Formula('¬', neg.left)),
                               CNFConverter.move_negation_inward(Formula('¬', neg.right)))
            elif neg.op == '∨':
                return Formula('∧',
                               CNFConverter.move_negation_inward(Formula('¬', neg.left)),
                               CNFConverter.move_negation_inward(Formula('¬', neg.right)))
            else:
                return Formula('¬', CNFConverter.move_negation_inward(neg))
        elif f.op in {'∧', '∨'}:
            return Formula(f.op,
                           CNFConverter.move_negation_inward(f.left),
                           CNFConverter.move_negation_inward(f.right))
        else:
            return f

    @staticmethod
    def distribute_or_over_and(f):
        if f.op == '∨':
            A = CNFConverter.distribute_or_over_and(f.left)
            B = CNFConverter.distribute_or_over_and(f.right)
            if A.op == '∧':
                return Formula('∧',
                               CNFConverter.distribute_or_over_and(Formula('∨', A.left, B)),
                               CNFConverter.distribute_or_over_and(Formula('∨', A.right, B)))
            if B.op == '∧':
                return Formula('∧',
                               CNFConverter.distribute_or_over_and(Formula('∨', A, B.left)),
                               CNFConverter.distribute_or_over_and(Formula('∨', A, B.right)))
            return Formula('∨', A, B)
        elif f.op == '∧':
            return Formula('∧',
                           CNFConverter.distribute_or_over_and(f.left),
                           CNFConverter.distribute_or_over_and(f.right))
        else:
            return f

    @staticmethod
    def to_cnf(expr_str):
        parsed = CNFConverter.parse(expr_str)
        step1 = CNFConverter.eliminate_implications(parsed)
        step2 = CNFConverter.move_negation_inward(step1)
        step3 = CNFConverter.distribute_or_over_and(step2)
        return step3

# ---------- Resolution Engine ----------

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
        literal = literal.strip()
        return literal[1:] if literal.startswith('¬') else '¬' + literal

    @staticmethod
    def flatten_to_clauses(ast):
        def collect_clauses(node):
            if node.op == '∧':
                return collect_clauses(node.left) + collect_clauses(node.right)
            else:
                return [Resolution.collect_literals(node)]
        return collect_clauses(ast)

    @staticmethod
    def collect_literals(node):
        if node.op == '∨':
            return Resolution.collect_literals(node.left) | Resolution.collect_literals(node.right)
        elif node.op == '¬':
            return {f'¬{node.left.op}'}
        else:
            return {node.op}

    @staticmethod
    def entails(belief_base, query):
        clauses = []
        for belief in belief_base:
            cnf_ast = CNFConverter.to_cnf(belief)
            clauses.extend(Resolution.flatten_to_clauses(cnf_ast))

        negated_query_literals = Resolution.split_query_negate(query)
        clauses += [{lit} for lit in negated_query_literals]

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
        cnf_ast = CNFConverter.to_cnf(query)
        disjuncts = Resolution.collect_literals(cnf_ast)
        return [Resolution.negate(lit) for lit in disjuncts]

    @staticmethod
    def is_consistent(belief_base):
        return not Resolution.entails(belief_base, "False")
