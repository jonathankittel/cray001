import random

class BlackjackGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        """Reset the game state."""
        self.deck = self.create_deck()
        random.shuffle(self.deck)

        self.user_cards = []
        self.dealer_cards = []
        self.fool_cards = []

        self.user_score = 0
        self.dealer_score = 0
        self.fool_score = 0

        self.game_over = False
        self.winner = None

        # Deal initial cards
        self.user_cards = [self.draw_card(), self.draw_card()]
        self.dealer_cards = [self.draw_card(), self.draw_card(hidden=True)]
        self.fool_cards = [self.draw_card(), self.draw_card(hidden=True)]

        # Calculate initial scores
        self.user_score = self.calculate_score(self.user_cards)
        self.dealer_score = self.calculate_score(self.dealer_cards)
        self.fool_score = self.calculate_score(self.fool_cards)

    def create_deck(self):
        """Create a standard 52-card deck."""
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        deck = [{"value": value, "suit": suit, "hidden": False} for value in values for suit in suits]
        return deck

    def draw_card(self, hidden=False):
        """Draw a card from the deck."""
        if self.deck:
            card = self.deck.pop()
            card["hidden"] = hidden
            return card
        return None

    def calculate_score(self, cards):
        """Calculate the total score, considering Ace logic."""
        score = 0
        aces = 0

        for card in cards:
            if card.get("hidden", False):
                continue  # Skip hidden cards
            value = card["value"]
            if isinstance(value, int):
                score += value
            elif value in ["J", "Q", "K"]:
                score += 10
            elif value == "A":
                aces += 1
                score += 11  # Assume Ace is 11 initially

        # Adjust for Aces if needed
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1

        return score

    def user_hit(self):
        """User draws a card."""
        card = self.draw_card()
        if card:
            self.user_cards.append(card)
            self.user_score = self.calculate_score(self.user_cards)
            if self.user_score > 21:
                self.game_over = True
                self.winner = "Dealer"
                return "Bust! You exceeded 21."
        return None

    def dealer_turn(self):
        """Dealer and Fool reveal hidden cards and play."""
        self.reveal_hidden_cards(self.dealer_cards)
        self.reveal_hidden_cards(self.fool_cards)

        self.dealer_score = self.play_until_seventeen(self.dealer_cards)
        self.fool_score = self.play_until_seventeen(self.fool_cards)

        self.determine_winner()

    def play_until_seventeen(self, cards):
        """Draw cards until the score reaches at least 17."""
        score = self.calculate_score(cards)
        while score < 17:
            cards.append(self.draw_card())
            score = self.calculate_score(cards)
        return score

    def reveal_hidden_cards(self, cards):
        """Reveal hidden cards."""
        for card in cards:
            card["hidden"] = False

    def determine_winner(self):
        """Determine the winner based on all scores."""
        if self.user_score > 21:
            self.winner = "Dealer"
        else:
            results = {
                "User": self.user_score,
                "Dealer": self.dealer_score,
                "Fool": self.fool_score,
            }
            results = {k: v for k, v in results.items() if v <= 21}

            if not results:
                self.winner = "No one (everyone busted)"
            else:
                max_score = max(results.values())
                winners = [k for k, v in results.items() if v == max_score]

                if len(winners) == 1:
                    self.winner = winners[0]
                else:
                    self.winner = f"Tie between: {', '.join(winners)}"
            
            self.game_over = True

        print(f"Final Scores: User: {self.user_score}, Dealer: {self.dealer_score}, Fool: {self.fool_score}")

    def get_game_state(self):
        """Return the current game state."""
            # Reveal all cards if the game is over
        if self.game_over:
            self.reveal_hidden_cards(self.dealer_cards)
            self.reveal_hidden_cards(self.fool_cards)

        return {
            "user_cards": [f"{card['value']} of {card['suit']}" for card in self.user_cards],
            "user_score": self.user_score,
            "dealer_cards": [
                f"{card['value']} of {card['suit']}" if not card["hidden"] else "Hidden"
                for card in self.dealer_cards
            ],
            "dealer_score": self.dealer_score if self.game_over else "Hidden",
            "fool_cards": [
                f"{card['value']} of {card['suit']}" if not card["hidden"] else "Hidden"
                for card in self.fool_cards
            ],
            "fool_score": self.fool_score if self.game_over else "Hidden",
            "game_over": self.game_over,
            "winner": self.winner,
        }
