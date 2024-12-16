import random

class BlackjackGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        """Reset the game state."""
        self.user_cards = []
        self.user_score = 0

        self.dealer_cards = []
        self.dealer_score = 0

        self.game_over = False
        self.winner = None

        # Dealer starts with 2 cards (one hidden)
        self.dealer_cards = [self.draw_card(), self.draw_card(hidden=True)]

    def draw_card(self, hidden=False):
        """Simulate drawing a card (values 1-10)."""
        card = random.randint(1, 10)
        return {"value": card, "hidden": hidden}

    def calculate_score(self, cards):
        """Calculate the total score of cards."""
        return sum(card["value"] for card in cards if not card.get("hidden", False))

    def user_hit(self):
        """User draws a card."""
        card = self.draw_card()
        self.user_cards.append(card)
        self.user_score = self.calculate_score(self.user_cards)

        if self.user_score > 21:
            self.game_over = True
            self.winner = "Dealer"
            return "Bust! You exceeded 21."
        return None

    def dealer_turn(self):
        """Dealer reveals hidden cards and draws until score >= 17."""
        for card in self.dealer_cards:
            card["hidden"] = False  # Reveal hidden card

        self.dealer_score = self.calculate_score(self.dealer_cards)

        while self.dealer_score < 17:
            self.dealer_cards.append(self.draw_card())
            self.dealer_score = self.calculate_score(self.dealer_cards)

        # Determine the winner
        if self.dealer_score > 21 or self.user_score > self.dealer_score:
            self.winner = "User"
        elif self.dealer_score > self.user_score:
            self.winner = "Dealer"
        else:
            self.winner = "Tie"

        self.game_over = True

    def get_game_state(self):
        """Return the current game state."""
        return {
            "user_cards": [card["value"] for card in self.user_cards],
            "user_score": self.user_score,
            "dealer_cards": [
                card["value"] if not card["hidden"] else "Hidden" for card in self.dealer_cards
            ],
            "dealer_score": self.dealer_score if self.game_over else "Hidden",
            "game_over": self.game_over,
            "winner": self.winner,
        }
