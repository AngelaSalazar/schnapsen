from schnapsen.game import Bot, Move, PlayerPerspective
from schnapsen.game import SchnapsenTrickScorer, GamePhase, TrumpExchange, Talon
from schnapsen.deck import Card, Suit, Rank

class IS_project_bot(Bot):
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
            if self.condition1(perspective, leader_move):
                self.action1(perspective, leader_move)
            if self.condition2(perspective, leader_move):
                print('321321312')
                return self.action2(perspective, leader_move)
            else:
                return self.action3(perspective, leader_move)
            
        if not leader_move:
            if self.condition3(perspective, leader_move):
                return self.action4(perspective, leader_move)
            else:
                if self.condition4(perspective, leader_move):
                    return self.action3(perspective, leader_move)
                else:
                    if self.condition5(perspective, leader_move):
                        return self.action5(perspective, leader_move)
                    else:
                        return self.action3(perspective, leader_move)
    

    def condition1(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:
        """
        Checks if there is a trump jack in our hand, that can be swapped for more powerful trump card
        """

        my_valid_moves = perspective.valid_moves()

        for move in my_valid_moves:
            if move.is_trump_exchange() and perspective.get_phase == GamePhase.ONE and leader_move is None:
                return True
        
        return False
    
        # raise NotImplementedError("Not yet implemented")

    def action1(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        Swaps the trump card
        """

        trump_suit = perspective.get_trump_suit()

        return TrumpExchange(Card.get_card(Rank.JACK, trump_suit))
    
        # raise NotImplementedError("Not yet implemented")

    def condition2(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:
        """
        Checks if there is a marriage in our hand
        """

        current_moves = perspective.valid_moves()

        for current_move in current_moves:
            if current_move.is_marriage():
                return True

        return False

        #raise NotImplementedError("Not yet implemented")

    def action2(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        Plays the marriage in our hand. (If there are 2 or even 3 marriages, always prioritize the trump marriage, if there we have one)
        """

        current_moves = perspective.valid_moves()

        for current_move in current_moves:
            if current_move.is_marriage() and current_move[0].card.suit == Talon.trump_suit():
                return current_move
            
        for current_move in current_moves:
            if current_move.is_marriage() and current_move[0].card.suit == Talon.trump_suit():
                return current_move

        return False

        #raise NotImplementedError("Not yet implemented")
    
    def action3(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        Plays the card with the lowest points, which is not a trump card!
        """
        valid_moves = [move for move in perspective.valid_moves() if move.as_regular_move().card.suit != perspective.get_trump_suit()]
        valid_moves.sort(key=lambda move: (self._card_points(move.as_regular_move().card)))
        return valid_moves[0]
        raise NotImplementedError("Not yet implemented")

    def condition3(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:
        """
        Checks if there there is a higher points card from the same suit in our hand, than the one that has been played by the bot
        """
        if leader_move is None or leader_move.is_trump_exchange():
            return False

        played_card = leader_move.as_regular_move().card
        suit = played_card.suit

        # Get all valid moves in the same suit
        same_suit_moves = [move.as_regular_move().card for move in perspective.valid_moves() if move.as_regular_move().card.suit == suit]

        if not same_suit_moves:
            return False  # No cards in the same suit

        # Filter out cards with lower points
        higher_points_cards = [card for card in same_suit_moves if self._card_points(card) > self._card_points(played_card)]

        return bool(higher_points_cards)
        raise NotImplementedError("Not yet implemented")
    
    def action4(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        plays the highest possible card from the same suit, so we can take the hand with it
        """

        played_card = leader_move.as_regular_move().card
        suit = played_card.suit

        same_suit_moves = [move for move in perspective.valid_moves() if move.as_regular_move().card.suit == suit]
        same_suit_moves.sort(key=lambda move: self._card_points(move.as_regular_move().card), reverse=True)

        return same_suit_moves[0]

        raise NotImplementedError("Not yet implemented")

    def condition4(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:
        """
        Checks if the played card from the opponent was king, queen or jack 
        """
        played_card = leader_move.as_regular_move().card
        card_rank = played_card.rank
        if card_rank == Rank.KING:
            return True
        if card_rank == Rank.QUEEN:
            return True
        if card_rank == Rank.JACK:
            return True
        return False
        raise NotImplementedError("Not yet implemented")

    def condition5(self, perspective: PlayerPerspective, leader_move: Move | None) -> bool:
        """
        Checks if there is a trump card in our deck
        """
        current_cards = perspective.get_hand()

        for current_card in current_cards:
            if current_card.suit == Talon.trump_suit():
                return True

        return False
        #raise NotImplementedError("Not yet implemented")

    def action5(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        """
        Plays the lowest trump card from our hand
        """
        current_moves = perspective.get_moves()

        trump_cards = []

        for current_move in current_moves:
            if current_move.card.suit == Talon.trump_suit():
                trump_cards.append(current_move)

        sorted_trump_cards = sorted(trump_cards, key=lambda move, bot=self: (-SchnapsenTrickScorer.rank_to_points(bot, rank=move.card.rank), self.suit_priority.index(move.card.suit)))

        if len(sorted_trump_cards) > 0:
            return sorted_trump_cards[0]
        else:
            return None

        #raise NotImplementedError("Not yet implemented")
    
    def _card_points(self, card: Card) -> int:
            """
            Calculate points for a card.
            It is going to be used for the basic strategy,
            so the bot can choose the most valuable card possible.
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
            