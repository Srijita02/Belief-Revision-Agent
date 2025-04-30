from belief_base import MastermindBeliefBase
from itertools import product

class BeliefMastermindAgent:
    def __init__(self, colors, code_length):
        """
        Initializes the agent with a belief base and random first guess.
        """
        self.colors = colors
        self.code_length = code_length
        self.belief_base = MastermindBeliefBase(colors, code_length)
        self.first_guess = self.generate_first_guess()
        print(f"Initial Guess: {self.first_guess}")

    def generate_first_guess(self):
        """
        Generates the first guess randomly.
        """
        return self.belief_base.list_beliefs()[0]  # The first possible code in the list

    def give_feedback(self, guess, secret_code):
        """
        Evaluates the feedback for a guess (number of correct positions and colors).
        """
        correct_positions = sum(1 for a, b in zip(guess, secret_code) if a == b)
        correct_colors = len(set(guess) & set(secret_code)) - correct_positions
        return correct_positions, correct_colors

    def revise_belief_base(self, guess, feedback):
        """
        Revisions the belief base based on feedback.
        """
        correct_positions, correct_colors = feedback
        possible_codes = list(self.belief_base.list_beliefs())

        for code in possible_codes:
            feedback_for_code = self.give_feedback(code, guess)
            if feedback_for_code != feedback:
                self.belief_base.remove_belief(code)

    def make_guess(self):
        """
        Makes a guess based on the revised belief base.
        Here, we will simply select the first possible combination remaining in the belief base.
        """
        return self.belief_base.list_beliefs()[0]

    def play_game(self, secret_code, max_turns=10):
        """
        Starts the game, makes guesses, and revises the belief base based on feedback.
        """
        turn = 1
        guess = self.first_guess
        while turn <= max_turns:
            print(f"Turn {turn}: Making guess {guess}")
            feedback = self.give_feedback(guess, secret_code)
            print(f"Feedback: {feedback[0]} correct positions, {feedback[1]} correct colors")
            if feedback[0] == self.code_length:
                print("Code cracked!")
                break

            self.revise_belief_base(guess, feedback)
            guess = self.make_guess()
            turn += 1
        if turn > max_turns:
            print("Failed to crack the code within the given turns.")
