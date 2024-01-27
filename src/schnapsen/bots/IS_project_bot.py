from schnapsen.game import Bot, Move, PlayerPerspective
from schnapsen.game import SchnapsenTrickScorer, GamePhase, TrumpExchange, Talon
from schnapsen.deck import Card, Suit, Rank
import random

class Human_Strategy_Bot(Bot):
    """
    This is our own bot, created with human strategies.
    In order to make the bot easier to understand and less complicated to build up,
    we are going to use different functions through the whole class
    """

    def get_move(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        This is the basic strategy for every move that the bot is going to use.
        In order to make it easier, we are going to use condition and actions functions
        """
        if leader_move:
            if self.is_trump_exchange_possible(perspective, leader_move):
                self.play_trump_exchange(perspective, leader_move)
            if self.is_marriage_possible(perspective, leader_move):
                return self.play_marriage(perspective, leader_move)
            else:
                return self.play_lowest_card(perspective, leader_move)
            
        if not leader_move:
            if self.is_higher_points_card(perspective, leader_move):
                return self.play_highest_points_card(perspective, leader_move)
            else:
                if self.played_jack_or_queen(perspective, leader_move):
                    return self.play_lowest_card(perspective, leader_move)
                else:
                    if self.is_trump_card_in_hand(perspective, leader_move):
                        return self.play_lowest_trump_suit_card(perspective, leader_move)
                    else:
                        return self.play_lowest_card(perspective, leader_move)
    

    def is_trump_exchange_possible(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:
        """
        Checks if a trump exchange is possible.
        Conditions for a trump exchange need to be met.
        Bot needs to have jack of trump suit in hand.
        Phase of the game needs to be first phase.
        Bot needs to be the leader.
        """

        # Get all the valid moves in hand
        my_valid_moves = perspective.valid_moves()

        # Loop through the valid moves
        for move in my_valid_moves:
            # Check conditions for a trump exchange
            if move.is_trump_exchange() and perspective.get_phase == GamePhase.ONE and leader_move is None:
                # Return True if trump exchange is possible
                return True 
        
        # Return False if trump exchange is not possible.
        return False

    def play_trump_exchange(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        Performs a trump exchange.
        Swaps the trump jack in hand for the trump card.
        """

        # Getting the suit of the trump card
        trump_suit = perspective.get_trump_suit()

        # Exchanging the card with rank Jack and trump suit
        return TrumpExchange(Card.get_card(Rank.JACK, trump_suit))

    def is_marriage_possible(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:
        """
        Checks if there is a marriage in hand.
        A marriage is a king and queen of the same suit.
        """

        # Getting the current valid moves
        current_moves = perspective.valid_moves()

        # Loop through the moves
        for current_move in current_moves:
            
            # If there is a marriage, return True
            if current_move.is_marriage():
                return True

        # If there is no marriage, return False
        return False

    def play_marriage(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        Plays the marriage in our hand. (If there are 2 or even 3 marriages, always prioritize the trump marriage, if there we have one)
        """

        # Get the current valid moves
        current_moves = perspective.valid_moves()

        # Loop through the moves
        for current_move in current_moves:
            # if the current move is a marriage, a regular move and the same suit as the trump card, return the current move
            if current_move.is_marriage() and current_move.as_regular_move().card.suit == Talon.trump_suit():
                return current_move

        # Loop through the moves    
        for current_move in current_moves:
            # if the current move is a marriage, return the current move
            if current_move.is_marriage():
                return current_move
    
    def play_lowest_card(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        Plays the card with the lowest points, which is not a trump card!
        """
        current_moves = perspective.valid_moves()

        # Filter out non-regular moves
        regular_moves = [move for move in current_moves if move.is_regular_move()]

        if not regular_moves:
            # If there are no regular moves, return the first move
            return current_moves[0]

        # Filter out trump cards
        non_trump_moves = [move for move in regular_moves if move.as_regular_move().card.suit != perspective.get_trump_suit()]

        if non_trump_moves:
            # Play the card with the lowest points, which is not a trump card
            non_trump_moves.sort(key=lambda move: move.as_regular_move().card.rank.value)
            return non_trump_moves[0]
        else:
            # If there are no non-trump moves, return the first move
            return regular_moves[0]

    def is_higher_points_card(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:
        """
        Checks if there there is a higher points card from the same suit in our hand, than the one that has been played by the bot
        """

        # If the bot is the leader or there is a trump exchange, return False
        if leader_move is None or leader_move.is_trump_exchange():
            return False

        # Get the card and suit played by the leader
        played_card = leader_move.as_regular_move().card
        suit = played_card.suit

        # Get all valid moves that have the same suit as the leader move
        same_suit_moves = [move.as_regular_move().card for move in perspective.valid_moves() if move.as_regular_move().card.suit == suit]

        if not same_suit_moves:
            return False  # No cards in the same suit

        # Filter out cards with lower points
        higher_points_cards = [card for card in same_suit_moves if self._card_points(card) > self._card_points(played_card)]

        return bool(higher_points_cards)
    
    def play_highest_points_card(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        plays the highest possible card from the same suit, so we can take the hand with it
        """
        # Get the suit of the card played by the leader
        played_card = leader_move.as_regular_move().card
        suit = played_card.suit

        # Create list of all cards that has the same suit as the leader's move
        same_suit_moves = [move for move in perspective.valid_moves() if move.as_regular_move().card.suit == suit]

        # Sort the list of cards in descending order based on rank/card point score
        same_suit_moves.sort(key=lambda move: self._card_points(move.as_regular_move().card), reverse=True)

        # Return the card with the highest rank
        return same_suit_moves[0]

    def played_jack_or_queen(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:
        """
        Checks if the played card from the opponent was queen or jack 
        """
        # If bot is the leader, return False
        if leader_move is None:
            return False
        
        # Get the rank of the card played by the leader
        played_card = leader_move.as_regular_move().card
        card_rank = played_card.rank

        # If the rank of the card is Queen or Jack, return True
        if card_rank == Rank.QUEEN:
            return True
        if card_rank == Rank.JACK:
            return True
        
        # Otherwise, return False
        return False

    def is_trump_card_in_hand(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:
        """
        Checks if there is a card of the trump suit in hand
        """
        # Get all the current cards in hand
        current_cards = perspective.get_hand()

        # Loop through the cards
        for current_card in current_cards:
            # If there is a card of trump suit, return True
            if current_card.suit == perspective.get_trump_suit():
                return True

        return False

    def play_lowest_trump_suit_card(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        Plays the lowest trump card from our hand
        """

        # Get current valid moves
        current_moves = perspective.valid_moves()

        # Filter out non-regular moves
        current_moves = [move for move in current_moves if move.is_regular_move()]

        # Filter out trump cards
        trump_cards_moves = [move for move in current_moves if move.as_regular_move().card.suit == perspective.get_trump_suit()]

        if trump_cards_moves:
            # Play the lowest trump card
            trump_cards_moves.sort(key=lambda move: move.as_regular_move().card.rank.value)
            return trump_cards_moves[0]
        else:
            # If there are no trump cards, return the first move
            return current_moves[0]
    
    def _card_points(self, card: Card) -> int:
            """
            Calculate points for a card.
            It is going to be used for the basic strategy, so the bot can choose the most valuable card possible.
            """
            if card.rank == Rank.ACE:
                return 11
            elif card.rank == Rank.TEN:
                return 10
            elif card.rank == Rank.KING:
                return 4
            elif card.rank == Rank.QUEEN:
                return 3
            elif card.rank == Rank.JACK:
                return 2
            else:
                return 0
            