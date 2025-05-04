from belief_revision import BeliefMastermindAgent

class MastermindAgent:
    def __init__(self, colors, code_length):
        self.colors = colors
        self.code_length = code_length
        self.agent = BeliefMastermindAgent(colors, code_length)

    def play_game(self, secret_code, max_turns=10):
        """play the game using belief revision agent"""
        self.agent.play_game(secret_code, max_turns)
