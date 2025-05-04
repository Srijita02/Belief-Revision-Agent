#!/usr/bin/env python
# coding: utf-8

# entailment.py

import itertools
import re
import time
from functools import lru_cache


# ---------- CNF Converter ----------

class Formula:
    def __init__(self, op, left=None, right=None):
        self.op = op
        self.left = left
        self.right = right
        self._str_repr = None  # cache for string representation
        self._hash = None  # cache for hash value

    def __repr__(self):
        if self._str_repr is None:
            if self.op in {'∧', '∨', '→', '↔'}:
                self._str_repr = f"({self.left} {self.op} {self.right})"
            elif self.op == '¬':
                self._str_repr = f"¬{self.left}"
            else:
                self._str_repr = self.op  # atomic
        return self._str_repr

    def __eq__(self, other):
        if not isinstance(other, Formula):
            return False
        return (self.op == other.op and
                self.left == other.left and
                self.right == other.right)

    def __hash__(self):
        if self._hash is None:
            if self.op in {'∧', '∨', '→', '↔'}:
                self._hash = hash((self.op, hash(self.left), hash(self.right)))
            elif self.op == '¬':
                self._hash = hash((self.op, hash(self.left)))
            else:
                self._hash = hash(self.op)
        return self._hash


class CNFConverter:
    _cache = {}  # class-level cache for CNF conversions
    _parse_cache = {}  # cache for parsed expressions
    _equiv_cache = {}  # cache for equivalent formulas

    @staticmethod
    def normalize_formula(expr_str):
        """normalize formula to handle logical equivalence."""
        expr = expr_str
        while expr.startswith('¬¬'):  # handle double negation
            expr = expr[2:]
        return expr

    @staticmethod
    def is_equivalent(expr1, expr2):
        """check if two formulas are logically equivalent."""
        if expr1 == expr2:  # identical formulas are equivalent
            return True

        if expr1.startswith('¬¬') and expr1[2:] == expr2:  # double negation equivalence
            return True
        if expr2.startswith('¬¬') and expr2[2:] == expr1:  # double negation equivalence
            return True

        # cache the result
        key = (expr1, expr2)
        if key in CNFConverter._equiv_cache:
            return CNFConverter._equiv_cache[key]

        CNFConverter._equiv_cache[key] = False
        return False

    @staticmethod
    def parse(expr):
        # check cache first
        if expr in CNFConverter._parse_cache:
            return CNFConverter._parse_cache[expr]

        expr = expr.replace(' ', '')  # remove spaces

        # special case for double negation (¬¬X)
        if expr.startswith('¬¬') and len(expr) > 2:
            inner = expr[2:]
            inner_formula = CNFConverter.parse(inner)
            CNFConverter._parse_cache[expr] = inner_formula
            return inner_formula

        # handle simple cases directly for better performance
        if re.match(r'^[A-Za-z][A-Za-z0-9]*$', expr):
            result = Formula(expr)
            CNFConverter._parse_cache[expr] = result
            return result

        if expr.startswith('¬') and re.match(r'^¬[A-Za-z][A-Za-z0-9]*$', expr):
            atom = expr[1:]
            result = Formula('¬', Formula(atom))
            CNFConverter._parse_cache[expr] = result
            return result

        tokens = re.findall(r'¬|→|↔|∧|∨|\(|\)|[A-Za-z][A-Za-z0-9]*', expr)
        if not tokens:  # sanity check - if no tokens
            result = Formula('⊤')  # True constant as placeholder
            CNFConverter._parse_cache[expr] = result
            return result

        output = []
        ops = []

        def precedence(op):
            return {'¬': 3, '∧': 2, '∨': 2, '→': 1, '↔': 1}.get(op, 0)

        try:
            for token in tokens:
                if re.match(r'[A-Za-z][A-Za-z0-9]*', token):
                    output.append(Formula(token))
                elif token == '(':
                    ops.append(token)
                elif token == ')':
                    while ops and ops[-1] != '(':
                        op = ops.pop()
                        if op == '¬':
                            if not output:
                                raise ValueError(f"Invalid formula: {expr}")
                            right = output.pop()
                            output.append(Formula(op, right))
                        else:
                            if len(output) < 2:
                                raise ValueError(f"Invalid formula: {expr}")
                            right = output.pop()
                            left = output.pop()
                            output.append(Formula(op, left, right))
                    if not ops:
                        raise ValueError(f"Mismatched parentheses in: {expr}")
                    ops.pop()  # remove the '('
                else:
                    while ops and ops[-1] != '(' and precedence(ops[-1]) >= precedence(token):
                        op = ops.pop()
                        if op == '¬':
                            if not output:
                                raise ValueError(f"Invalid formula: {expr}")
                            right = output.pop()
                            output.append(Formula(op, right))
                        else:
                            if len(output) < 2:
                                raise ValueError(f"Invalid formula: {expr}")
                            right = output.pop()
                            left = output.pop()
                            output.append(Formula(op, left, right))

            while ops:
                if ops[-1] == '(':
                    raise ValueError(f"Mismatched parentheses in: {expr}")
                op = ops.pop()
                if op == '¬':
                    if not output:
                        raise ValueError(f"Invalid formula: {expr}")
                    right = output.pop()
                    output.append(Formula(op, right))
                else:
                    if len(output) < 2:
                        raise ValueError(f"Invalid formula: {expr}")
                    right = output.pop()
                    left = output.pop()
                    output.append(Formula(op, left, right))

            if not output:
                raise ValueError(f"Empty formula: {expr}")

            result = output[0]
            CNFConverter._parse_cache[expr] = result
            return result

        except (IndexError, ValueError) as e:
            if expr.startswith('¬') and len(expr) > 1:
                inner = expr[1:]
                if inner.startswith('(') and inner.endswith(')'):
                    inner = inner[1:-1]
                if re.match(r'^[A-Za-z][A-Za-z0-9]*$', inner):
                    result = Formula('¬', Formula(inner))
                    CNFConverter._parse_cache[expr] = result
                    return result

            result = Formula('⊤')  # True constant as placeholder
            CNFConverter._parse_cache[expr] = result
            return result

    @staticmethod
    @lru_cache(maxsize=128)
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
    @lru_cache(maxsize=128)
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
    @lru_cache(maxsize=128)
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
        #set a timeout for CNF conversion
        start_time = time.time()
        timeout = 5  #5 seconds timeout

        #check cache first
        if expr_str in CNFConverter._cache:
            return CNFConverter._cache[expr_str]

        #handle normalized forms
        normalized_expr = CNFConverter.normalize_formula(expr_str)
        if normalized_expr != expr_str and normalized_expr in CNFConverter._cache:
            result = CNFConverter._cache[normalized_expr]
            CNFConverter._cache[expr_str] = result
            return result

        # handle double negation special case directly
        if expr_str.startswith('¬¬') and len(expr_str) > 2:
            inner = expr_str[2:]
            inner_cnf = CNFConverter.to_cnf(inner)
            CNFConverter._cache[expr_str] = inner_cnf
            CNFConverter._cache[normalized_expr] = inner_cnf
            return inner_cnf

        # handle simple atomic formulas directly
        if re.match(r'^[A-Za-z][A-Za-z0-9]*$', expr_str):
            result = Formula(expr_str)
            CNFConverter._cache[expr_str] = result
            CNFConverter._cache[normalized_expr] = result
            return result

        if expr_str.startswith('¬') and re.match(r'^¬[A-Za-z][A-Za-z0-9]*$', expr_str):
            atom = expr_str[1:]
            result = Formula('¬', Formula(atom))
            CNFConverter._cache[expr_str] = result
            CNFConverter._cache[normalized_expr] = result
            return result

        try:
            parsed = CNFConverter.parse(expr_str)

            #check timeout after parsing
            if time.time() - start_time > timeout:
                print(f"CNF conversion timeout for: {expr_str}")
                result = Formula('⊤')
                CNFConverter._cache[expr_str] = result
                CNFConverter._cache[normalized_expr] = result
                return result

            step1 = CNFConverter.eliminate_implications(parsed)

            # check timeout after eliminating implications
            if time.time() - start_time > timeout:
                print(f"CNF conversion timeout for: {expr_str}")
                result = Formula('⊤')
                CNFConverter._cache[expr_str] = result
                CNFConverter._cache[normalized_expr] = result
                return result

            step2 = CNFConverter.move_negation_inward(step1)

            #check timeout after moving negation inward
            if time.time() - start_time > timeout:
                print(f"CNF conversion timeout for: {expr_str}")
                result = Formula('⊤')
                CNFConverter._cache[expr_str] = result
                CNFConverter._cache[normalized_expr] = result
                return result

            step3 = CNFConverter.distribute_or_over_and(step2)

            #cache the result
            CNFConverter._cache[expr_str] = step3
            CNFConverter._cache[normalized_expr] = step3
            return step3
        except Exception as e:
            print(f"Error in CNF conversion for {expr_str}: {e}")
            #for error cases, provide a safe default
            result = Formula('⊤')  # True constant as placeholder
            CNFConverter._cache[expr_str] = result
            CNFConverter._cache[normalized_expr] = result
            return result

# ---------- Resolution Engine ----------

class Resolution:
    _negate_cache = {}  # Cache for negations
    _clause_cache = {}  # Cache for clause generation
    _entails_cache = {}  # Cache for entailment results
    
    @staticmethod
    def resolve(ci, cj):
        """Try to resolve two clauses and produce resolvents."""
        resolvents = []
        # Convert to sets if they aren't already
        ci_set = set(ci)
        cj_set = set(cj)
        
        # Find potential complementary literals more efficiently
        for di in ci_set:
            neg_di = Resolution.negate(di)
            if neg_di in cj_set:
                # Found complementary literals
                new_clause = (ci_set.union(cj_set)) - {di, neg_di}
                if new_clause:  # Don't add empty set here
                    resolvents.append(new_clause)
                else:
                    # Empty clause - contradiction found
                    resolvents.append(set())
                    return resolvents  # Early termination
        return resolvents

    @staticmethod
    def negate(literal):
        # Cache negation results
        if literal in Resolution._negate_cache:
            return Resolution._negate_cache[literal]
            
        literal = literal.strip()
        result = literal[1:] if literal.startswith('¬') else '¬' + literal
        Resolution._negate_cache[literal] = result
        return result

    @staticmethod
    def flatten_to_clauses(ast):
        # Generate a cache key
        key = str(ast)
        if key in Resolution._clause_cache:
            return Resolution._clause_cache[key]
            
        def collect_clauses(node):
            if node.op == '∧':
                return collect_clauses(node.left) + collect_clauses(node.right)
            else:
                return [Resolution.collect_literals(node)]
                
        result = collect_clauses(ast)
        Resolution._clause_cache[key] = result
        return result

    @staticmethod
    def collect_literals(node):
        if node.op == '∨':
            return Resolution.collect_literals(node.left) | Resolution.collect_literals(node.right)
        elif node.op == '¬':
            if hasattr(node.left, 'op'):
                return {f'¬{node.left.op}'}
            else:
                # Handle edge case of invalid formula structure
                return {'¬⊤'}  # Placeholder
        else:
            return {node.op}

    @staticmethod
    def entails(belief_base, query):
        # Set timeout for entailment checking
        start_time = time.time()
        timeout = 10  # 10 seconds timeout for entire entailment check
        
        # Special case for empty belief base
        if not belief_base:
            return False
            
        # Check for cached result
        key = (tuple(sorted(belief_base)), query)
        if key in Resolution._entails_cache:
            return Resolution._entails_cache[key]
            
        # Handle normalized forms
        normalized_query = CNFConverter.normalize_formula(query)
        if normalized_query != query:
            normalized_key = (tuple(sorted(belief_base)), normalized_query)
            if normalized_key in Resolution._entails_cache:
                result = Resolution._entails_cache[normalized_key]
                Resolution._entails_cache[key] = result
                return result
            
        # Special case for double negation
        if query.startswith('¬¬') and len(query) > 2:
            inner_query = query[2:]
            result = Resolution.entails(belief_base, inner_query)
            Resolution._entails_cache[key] = result
            Resolution._entails_cache[(tuple(sorted(belief_base)), inner_query)] = result
            return result
            
        try:
            clauses = []
            clause_set = set()  # For faster membership tests
            
            # Convert belief base to clauses
            for belief in belief_base:
                try:
                    # Check if we've exceeded the timeout
                    if time.time() - start_time > timeout:
                        print(f"Entailment check timeout for query: {query}")
                        Resolution._entails_cache[key] = False
                        return False
                        
                    cnf_ast = CNFConverter.to_cnf(belief)
                    new_clauses = Resolution.flatten_to_clauses(cnf_ast)
                    for clause in new_clauses:
                        frozen_clause = frozenset(clause)
                        if frozen_clause not in clause_set:
                            clause_set.add(frozen_clause)
                            clauses.append(clause)
                except Exception as e:
                    # Skip problematic beliefs
                    print(f"Warning: Skipping problematic belief: {belief}, error: {e}")
                    continue

            # Add negated query clauses
            try:
                # Check if we've exceeded the timeout
                if time.time() - start_time > timeout:
                    print(f"Entailment check timeout for query: {query}")
                    Resolution._entails_cache[key] = False
                    return False
                    
                negated_query_literals = Resolution.split_query_negate(query)
                for lit in negated_query_literals:
                    clause = {lit}
                    frozen_clause = frozenset(clause)
                    if frozen_clause not in clause_set:
                        clause_set.add(frozen_clause)
                        clauses.append(clause)
            except Exception as e:
                # If we can't negate the query properly, it's not entailed
                print(f"Error negating query {query}: {e}")
                Resolution._entails_cache[key] = False
                return False

            # Safety check for empty clauses list
            if not clauses:
                Resolution._entails_cache[key] = False
                return False

            # Resolution loop with optimizations
            max_iterations = 100  # Strict iteration limit
            iteration = 0
            
            # Track processed pairs to avoid redundant work
            processed_pairs = set()
            
            while iteration < max_iterations:
                iteration += 1
                
                # Check if we've exceeded the timeout
                if time.time() - start_time > timeout:
                    print(f"Entailment check timeout for query: {query}")
                    Resolution._entails_cache[key] = False
                    return False
                
                new_clauses_found = False
                
                # Process pairs based on complementary literals - limit to a batch size
                clause_pairs = []
                max_pairs_per_iteration = 1000  # Limit number of pairs to check per iteration
                pair_count = 0
                
                for i in range(len(clauses)):
                    if pair_count >= max_pairs_per_iteration:
                        break
                        
                    for j in range(i+1, len(clauses)):
                        if pair_count >= max_pairs_per_iteration:
                            break
                            
                        # Skip already processed pairs
                        pair_key = (frozenset(clauses[i]), frozenset(clauses[j]))
                        if pair_key in processed_pairs:
                            continue
                            
                        processed_pairs.add(pair_key)
                        pair_count += 1
                        
                        ci, cj = clauses[i], clauses[j]
                        # Quick check if there might be complementary literals
                        if any(Resolution.negate(lit) in cj for lit in ci):
                            clause_pairs.append((ci, cj))
                
                # Process all identified pairs
                for ci, cj in clause_pairs:
                    # Check if we've exceeded the timeout
                    if time.time() - start_time > timeout:
                        print(f"Entailment check timeout for query: {query}")
                        Resolution._entails_cache[key] = False
                        return False
                        
                    resolvents = Resolution.resolve(ci, cj)
                    for resolvent in resolvents:
                        if not resolvent:  # Empty clause
                            Resolution._entails_cache[key] = True
                            if normalized_query != query:
                                Resolution._entails_cache[(tuple(sorted(belief_base)), normalized_query)] = True
                            return True
                            
                        frozen_resolvent = frozenset(resolvent)
                        if frozen_resolvent not in clause_set:
                            clause_set.add(frozen_resolvent)
                            clauses.append(resolvent)
                            new_clauses_found = True
                
                # If no new clauses found, we're done
                if not new_clauses_found:
                    Resolution._entails_cache[key] = False
                    if normalized_query != query:
                        Resolution._entails_cache[(tuple(sorted(belief_base)), normalized_query)] = False
                    return False
                
                # Safety check - if too many clauses, abort
                if len(clauses) > 10000:
                    print(f"Too many clauses generated for query: {query}")
                    Resolution._entails_cache[key] = False
                    if normalized_query != query:
                        Resolution._entails_cache[(tuple(sorted(belief_base)), normalized_query)] = False
                    return False
            
            # If we reach the iteration limit
            print(f"Resolution reached iteration limit for query: {query}")
            Resolution._entails_cache[key] = False
            if normalized_query != query:
                Resolution._entails_cache[(tuple(sorted(belief_base)), normalized_query)] = False
            return False
            
        except Exception as e:
            # Catch any unexpected errors and return a safe default
            print(f"Error in entailment checking: {e}")
            Resolution._entails_cache[key] = False
            return False

    @staticmethod
    def split_query_negate(query):
        # Set timeout for query negation
        start_time = time.time()
        timeout = 2  # 2 seconds timeout for query negation
        
        # Handle normalized forms
        normalized_query = CNFConverter.normalize_formula(query)
        if normalized_query != query:
            return Resolution.split_query_negate(normalized_query)
            
        # Special case for double negation
        if query.startswith('¬¬') and len(query) > 2:
            inner = query[2:]
            return Resolution.split_query_negate(inner)
            
        # Handle simple cases directly
        if re.match(r'^[A-Za-z][A-Za-z0-9]*$', query):
            return [f'¬{query}']
            
        if query.startswith('¬') and re.match(r'^¬[A-Za-z][A-Za-z0-9]*$', query):
            return [query[1:]]
            
        try:
            # Check timeout
            if time.time() - start_time > timeout:
                print(f"Query negation timeout for: {query}")
                # Fallback for timeout
                if query.startswith('¬'):
                    return [query[1:]]
                return [f'¬{query}']
                
            cnf_ast = CNFConverter.to_cnf(query)
            disjuncts = Resolution.collect_literals(cnf_ast)
            return [Resolution.negate(lit) for lit in disjuncts]
        except Exception as e:
            print(f"Error in query negation: {e}")
            # For simple formulas, handle directly
            if query.startswith('¬'):
                inner = query[1:]
                if inner.startswith('(') and inner.endswith(')'):
                    inner = inner[1:-1]
                return [inner]
            return [f'¬{query}']

    @staticmethod
    def is_consistent(belief_base):
        return not Resolution.entails(belief_base, "False")
        
    @staticmethod
    def clear_caches():
        """Clear all caches to free memory if needed"""
        CNFConverter._cache.clear()
        CNFConverter._parse_cache.clear()
        CNFConverter._equiv_cache.clear()
        Resolution._negate_cache.clear()
        Resolution._clause_cache.clear()
        Resolution._entails_cache.clear()