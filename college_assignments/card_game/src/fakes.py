"""
Fake implementations of LetterGameBase.

We provide a LettersGameStub implementation, and you must
implement a LettersGameFake implementation.
"""

import copy

from base import LettersGameBase, CardType, PositionType, TableauType


class LettersGameStub(LettersGameBase):
    """
    Stub implementation of LettersGameBase.

    This stub implementation behaves according to the following rules:

    - The game must be created with exactly enough cards for one tableau.
    - The constructor does not validate its parameters in any way (except
      to check the requirement in the above bullet point)
    - When a player calls a fit, if the fit includes at least one card
      in an odd-numbered row (with rows numbered from 0), the fit is
      considered valid, and the cards are removed from the tableau
      (and not replaced) Otherwise, the fit is considered invalid.
    - The game is over when the end_game() method is called.
    - When the game is over, the stub will only report at most two winners
      (even if a larger number of players was passed to the constructor):
       - If the top-left position (0, 0) and the bottom-right position
         (rows-1, cols-1) are both empty or both have a card, the game is a
         tie between Players 1 and 2.
       - If the top-left position is empty, but the bottom-right position
         has a card, Player 1 wins.
       - If the top-left position has a card, but the bottom-right position
         is empty, Player 2 wins.
    - The score for each player is equal to 100 times the player number.
    - Neither moonshot mode or lightning mode have any effect on the game.
    """

    _cards: list[CardType | None]
    _done: bool

    def __init__(
        self,
        cards: list[CardType],
        fit_size: int,
        tableau_size: tuple[int, int],
        num_players: int,
        lightning: bool = False,
    ) -> None:
        assert len(cards) == tableau_size[0] * tableau_size[1], (
            "Stub implementation requires the number of cards to be"
            "enough for exactly one tableau"
        )

        super().__init__(cards, fit_size, tableau_size, num_players, lightning)

        self._cards = []
        for c in cards:
            self._cards.append(c.copy())
        self._done = False

    @property
    def active_players(self) -> set[int]:
        """
        See LettersGameBase.active_players
        """
        return set(range(1, self._num_players + 1))

    @property
    def tableau(self) -> TableauType:
        """
        See LettersGameBase.tableau
        """
        tableau: TableauType = []
        for r in range(self.nrows):
            tableau.append(self._cards[r * self.ncols : (r + 1) * self.ncols])
        return tableau

    @property
    def non_empty_positions(self) -> set[PositionType]:
        """
        Returns a list of non-empty positions on the tableau
        """
        positions = set()
        for r in range(self.nrows):
            for c in range(self.ncols):
                i = r * self.ncols + c
                if self._cards[i] is not None:
                    positions.add((r, c))
        return positions

    @property
    def done(self) -> bool:
        """
        See LettersGameBase.done
        """
        return self._done

    @property
    def outcome(self) -> set[int]:
        """
        See LettersGameBase.outcome
        """
        if not self.done:
            return set()
        else:
            top_left = self.card_at((0, 0))
            bottom_right = self.card_at((self.nrows - 1, self.ncols - 1))

            if top_left is None and bottom_right is not None:
                return {1}
            elif top_left is not None and bottom_right is None:
                return {2}
            else:
                return {1, 2}

    @property
    def scores(self) -> dict[int, int]:
        """
        See LettersGameBase.scores
        """
        return {p: p * 100 for p in range(1, self._num_players + 1)}

    def card_at(self, pos: PositionType) -> CardType | None:
        """
        See LettersGameBase.card_at
        """
        r, c = pos
        return self._cards[r * self.ncols + c]

    def call_fit(self, player: int, positions: list[PositionType]) -> bool:
        """
        See LettersGameBase.call_fit
        """
        valid = False
        for pos in positions:
            r, c = pos
            if r % 2 == 1:
                valid = True
                break

        if not valid:
            return False

        for pos in positions:
            r, c = pos
            self._cards[r * self.ncols + c] = None

        return True

    def moonshot_start(self, player: int) -> None:
        """
        See LettersGameBase.moonshot_start
        """
        pass

    def moonshot_end(self) -> None:
        """
        See LettersGameBase.moonshot_end
        """
        pass

    def end_game(self) -> None:
        """
        See LettersGameBase.end_game
        """
        self._done = True


#
# Your LettersGameFake implementation goes here
#

class LettersGameFake(LettersGameBase):


    def __init__(self, 
                 cards: list[CardType], 
                 fit_size: int, 
                 tableau_size: tuple[int,int], 
                 num_players: int, 
                 lightning: bool =False) -> None:
        #Checks tableau is correct
        if tableau_size[0] * tableau_size[1] > len(cards):
            raise ValueError
        
        if tableau_size[0] * tableau_size[1] < fit_size:
            raise ValueError
        
        for i in range(len(cards)-1):
            if cards[i].keys() != cards[i+1].keys():
                raise ValueError('keys are not same')

        for key in cards[0].keys():
            uniques = set()
            for i in range(len(cards)):
                uniques.add(cards[i][key])
            if len(uniques) != fit_size:
                raise ValueError('Fit size is wack')
        
        seen_card = set()
        for card in cards:
            card_tuple = tuple(sorted(card.items()))
            if card_tuple in seen_card:
                raise ValueError('Cards are same')
            
            seen_card.add(card_tuple)
        
        super().__init__(cards, fit_size, tableau_size, num_players, lightning)
        self.deck = cards[tableau_size[0] * tableau_size[1]:]
        self._cards = cards[:tableau_size[0] * tableau_size[1]]
        
        self._scores = {p: 0 for p in range(1, self.num_players + 1)}
        self._done = False

    @property
    def nrows(self) -> int:
        """
        See LettersGameBase.call_fit
        """
        return self._tableau_size[0]

    @property
    def ncols(self) -> int:
        """
        See LettersGameBase.call_fit
        """
        return self._tableau_size[1]

    @property
    def fit_size(self) -> int:
        """
        See LettersGameBase.call_fit
        """
        return self._fit_size

    @property
    def num_players(self) -> int:
        """
        See LettersGameBase.call_fit
        """
        return self._num_players

    @property
    def lightning(self) -> bool:
        """
        See LettersGameBase.call_fit
        """
        return self._lightning

    @property
    def moonshot(self) -> bool:
        """
        See LettersGameBase.call_fit
        """
        return self._moonshot

    @property
    def active_players(self) -> set[int]:
        """
        See LettersGameBase.call_fit
        """
        return set(range(1, self._num_players + 1))

    @property
    def tableau(self) -> TableauType:
        """
        See LettersGameBase.call_fit
        """
        
        tableau: TableauType = []
        for r in range(self.nrows):
            tableau.append(self._cards[r * self.ncols : (r + 1) * self.ncols])
        return tableau

    @property
    def non_empty_positions(self) -> set[PositionType]:
        """
        See LettersGameBase.call_fit
        """
    
        positions = set()
        for r in range(self.nrows):
            for c in range(self.ncols):
                i = r * self.ncols + c
                if self._cards[i] is not None:
                    positions.add((r, c))
        return positions

    @property
    def done(self) -> bool:
        """
        See LettersGameBase.call_fit
        """
        return self._done

    @property
    def outcome(self) -> set[int]:
        """
        See LettersGameBase.call_fit
        """
        scores = self.scores
        if not self.done:
            return set()
        else:
            winners_set = set()
            max_score = max(scores.values())
            winners = [player for player in scores if scores[player] == max_score]
            for player in winners:
                winners_set.add(player)
            return winners_set
                

    @property
    def scores(self) -> dict[int, int]:
        """
        See LettersGameBase.call_fit
        """
        
        return self._scores

    #
    # METHODS
    #

    def card_at(self, pos: PositionType) -> CardType | None:
        """
        See LettersGameBase.call_fit
        """
        i, j = pos

        if not(0 <= i < self.nrows and 0 <= j < self.ncols):
            raise ValueError
        
        tableau = self.tableau
        
        return tableau[i][j]

    def call_fit(self, player: int, positions: list[PositionType]) -> bool:
        """
        See LettersGameBase.call_fit
        """

        if self.done:
            raise ValueError

        if len(set(positions)) != len(positions):
            raise ValueError
        
        if player not in self.active_players:
            raise ValueError
            
        if len(positions) != self.fit_size:
            raise ValueError
        
        if self.lightning:
            if player not in self.active_players:
                raise ValueError

        card_lst = [self.card_at(pos) for pos in positions]

        if any(card is None for card in card_lst):
            raise ValueError
  
        if self.moonshot:
            self.scores[player] += 100
            self.end_game()
            return True
        
        for key in card_lst[0].keys():
            if all(c[key] == card_lst[0][key] for c in card_lst):
                self.scores[player] += self.fit_size

                for pos in positions:
                    i, j = pos
                    self._cards[i * self.ncols + j] = None

                for pos in positions:
                    if len(self.deck) == 0:
                        continue 

                    i, j = pos
                    new_card = self.deck.pop(0)
                    self._cards[i * self.ncols + j] = new_card
                
                return True

        self.scores[player] -= self.fit_size  
        return False

    def moonshot_start(self, player: int) -> None:
        """
        See LettersGameBase.call_fit
        """
        
        if self.moonshot:
            raise ValueError("Error Here Bro")
        
        for i, row in enumerate(self.tableau):
            for j, val in enumerate(row):
                if self.tableau[i][j] == None:
                    raise ValueError("Called Moonshot here")
                
        if self.lightning:
            if player not in self.active_players:
                raise ValueError
                
        if player not in self.active_players:
            raise ValueError
        
        self._moonshot = True


    def moonshot_end(self) -> None:
        """
        See LettersGameBase.call_fit
        """
        
        if self.moonshot is False:
            raise ValueError
        
        self._moonshot = False


    def end_game(self) -> None:
        """
        See LettersGameBase.call_fit
        """
        
        if self.done:
            raise ValueError
        
        if self.lightning:
            raise ValueError
        
        self._done = True
