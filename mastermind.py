import random
import itertools

class Mastermind:
    def __init__(self, colors, code_length):
        self.colors = colors  # List of possible colors
        self.code_length = code_length  # Length of the secret code
        self.secret_code = self.generate_code()  # Generate a secret code

    def generate_code(self):
        """Randomly generate the secret code from the available colors."""
        return random.choices(self.colors, k=self.code_length)

    def get_feedback(self, guess):
        """Compare guess with the secret code and return feedback."""
        black_pegs = sum([1 for i in range(self.code_length) if guess[i] == self.secret_code[i]])
        white_pegs = sum([min(guess.count(color), self.secret_code.count(color)) for color in set(guess)]) - black_pegs
        return black_pegs, white_pegs
