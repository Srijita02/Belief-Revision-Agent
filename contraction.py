from entailment import Resolution
import itertools

class BeliefContraction:
    def __init__(self, belief_base, selector='max'):
        self.belief_base = list(belief_base.beliefs)
        self.selector = selector

    def partial_meet_contract(self, formula):
        remainder_sets = self._generate_remainders(formula)
        if not remainder_sets:
            print(f"[INFO] No remainder sets found for: {formula}")
            return

        if self.selector == 'max':
            selected = max(remainder_sets, key=len)
        elif self.selector == 'min':
            selected = min(remainder_sets, key=len)
        else:  # intersection of all
            selected = set.intersection(*map(set, remainder_sets))

        self.belief_base.clear()
        self.belief_base.extend(selected)
        print(f"[INFO] Contracted belief base to remove entailment of: {formula}")

    def _generate_remainders(self, formula):
        remainders = []
        for i in range(len(self.belief_base) + 1):
            for subset in itertools.combinations(self.belief_base, i):
                if not Resolution.entails(list(subset), formula):
                    remainders.append(list(subset))
        return remainders
