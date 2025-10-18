from abc import ABC
import itertools
from base import LettersGameBase, TableauType, PositionType, CardType

class Card:
    """
    Represents a single card in the game
    """
    def __init__(self, features: CardType) -> None:
        self.features = features

    def __repr__(self) -> str:
        return f"Card({self.features})"

class Tableau:
    """
    Represents the tableau (grid) of cards
    """
    def __init__(self, cards: list[CardType], rows: int, cols: int) -> None:
        """
        Initializes the tableau with a grid of given rows and cols.

        Args:
            cards(list[CardType]): A list of cards to initialize the tableau
            rows (int): Number of rows in the tableau
            cols (int): Number of columns in the tableau
        """
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.fill_tableau(cards, rows, cols)

    def fill_tableau(self, cards: list[CardType], rows: int, cols: int) -> None:
        """
        Fills the tableau grid with Card objects from the list of cards.

        Args:
            cards (list[CardType]): A list of cards to populate the grid
            rows (int): Number of rows in the tableau
            cols (int): Number of columns in the tableau
        """
        idx = 0
        for r in range(rows):
            for c in range(cols):
                if idx < len(cards):
                    self.grid[r][c] = Card(cards[idx])
                    idx += 1

    def get_card(self, position: PositionType) -> Card | None:
        """
        Returns the Card object at the specified position, or None if empty.

        Args:
            position (PositionType): A tuple (row, column) representing the 
            position in the tableau

        Returns:
            Card | None: The Card at the given position, or None if the slot is 
            empty
        """
        r, c = position
        return self.grid[r][c]

    def remove_cards(self, positions: list[PositionType]) -> None:
        """
        Removes cards from the tableau at the positions by setting them to None.

        Args:
            positions (list[PositionType]): A list of (row, column) tuples 
            indicating positions to clear
        """
        for (r, c) in positions:
            self.grid[r][c] = None

    def get_non_empty(self) -> set[PositionType]:
        """
        Returns a set of all positions in the tableau that contain a Card.

        Returns:
            set[PositionType]: A set of (row, column) tuples for the positions.
        """
        nrows = len(self.grid)
        ncols = len(self.grid[0]) if nrows else 0
        return {
            (r, c)
            for r in range(nrows)
            for c in range(ncols)
            if self.grid[r][c] is not None
        }


class LettersGame(LettersGameBase):
    """
    A working 'Letters' game implementation that uses the REAL rules:
      - For each feature dimension, the 3 cards are either all the same or all different.
      - If correct => +fit_size points, remove/replace cards
      - If incorrect => -fit_size points, do not remove cards
    """

    def __init__(
        self,
        cards: list[CardType],
        fit_size: int,
        tableau_size: tuple[int, int],
        num_players: int,
        lightning: bool = False
    ) -> None:
        
        rows, cols = tableau_size
        if rows * cols > len(cards):
            raise ValueError("Not enough cards to fill the tableau.")

        if rows * cols < fit_size:
            raise ValueError("Tableau is too small to contain a single fit.")

        all_keys = cards[0].keys()
        for card in cards[1:]:
            if card.keys() != all_keys:
                raise ValueError("Not all cards share the same feature keys.")

        for key in all_keys:
            distinct_vals = {card[key] for card in cards}
            if len(distinct_vals) != fit_size:
                raise ValueError(
                    f"For feature '{key}', must have exactly {fit_size} distinct values across the deck."
                )

        seen_cards = set()
        for cd in cards:
            tup = tuple(sorted(cd.items()))
            if tup in seen_cards:
                raise ValueError("Duplicate card found in the deck.")
            seen_cards.add(tup)

        super().__init__(cards, fit_size, tableau_size, num_players, lightning)

        self._table_cards = cards[: rows * cols]
        self._deck = cards[rows * cols :]

        self._tableau = Tableau(self._table_cards, rows, cols)

        self._scores = {p: 0 for p in range(1, num_players + 1)}
        self._done = False
        self._outcome: set[int] = set()

        self._moonshot = False
        self._moonshot_player: int | None = None
        self._moonshot_countered = False
        self._active_players = set(range(1, self.num_players + 1))

    # ---------------------------------------------------------
    # PROPERTIES
    # ---------------------------------------------------------
    @property
    def active_players(self) -> set[int]:
        """
        All players remain active in a non-lightning game.
        For lightning mode, you could remove eliminated players here.
        """
        return self._active_players

    @property
    def tableau(self) -> Tableau:
        """
        Return a 2D list of dicts (or None) for each position.
        """
        nrows = len(self._tableau.grid)
        ncols = len(self._tableau.grid[0]) if nrows else 0
        output: Tableau = []

        for r in range(nrows):
            row_data = []
            for c in range(ncols):
                card_obj = self._tableau.grid[r][c]
                row_data.append(card_obj.features if card_obj else None)
            output.append(row_data)
        return output

    @property
    def non_empty_positions(self) -> set[PositionType]:
        return self._tableau.get_non_empty()

    @property
    def done(self) -> bool:
        return self._done

    @property
    def outcome(self) -> set[int]:
        if not self._done:
            return set()
        return self._outcome

    @property
    def scores(self) -> dict[int, int]:
        return self._scores

    # ---------------------------------------------------------
    # METHODS
    # ---------------------------------------------------------
    def card_at(self, pos: PositionType) -> CardType | None:
        """
        Return the dict of features at 'pos', or None if empty.
        """
        r, c = pos
        if not (0 <= r < self.nrows and 0 <= c < self.ncols):
            raise ValueError("Position out of bounds.")
        card_obj = self._tableau.get_card((r, c))
        return card_obj.features if card_obj else None

    def call_fit(self, player: int, positions: list[PositionType]) -> bool:
        """
        If the positions form a valid fit => +fit_size points, remove & replace the cards.
        Else => -fit_size points, do not remove cards.
        """
        self._check_can_play(player)

        if len(positions) != self.fit_size:
            raise ValueError("Number of positions != fit_size.")

        if len(set(positions)) != len(positions):
            raise ValueError("Duplicate positions specified.")

        for pos in positions:
            if self.card_at(pos) is None:
                raise ValueError("One or more positions are invalid or empty.")

        if self._moonshot:
            if self._is_valid_fit(positions):
                self._moonshot_countered = True
                for pos in positions:
                    if self._deck:
                        new_card_dict = self._deck.pop(0)
                        r, c = pos
                        self._tableau.grid[r][c] = Card(new_card_dict)
                
                self.moonshot_end()
                return True
            else:
                return False

        if self._lightning:
            if self._is_valid_fit(positions):
                self._outcome.add(player)
                self._done = True
                return True

        if self._is_valid_fit(positions):
            self._scores[player] += self.fit_size
            self._tableau.remove_cards(positions)

            for pos in positions:
                if self._deck:
                    new_card_dict = self._deck.pop(0)
                    r, c = pos
                    self._tableau.grid[r][c] = Card(new_card_dict)
                else:
                    r, c = pos
                    self._tableau.grid[r][c] = None

            return True
        else:
            self._scores[player] -= self.fit_size
            return False
        
    def moonshot_start(self, player: int) -> None:
        """
        Switch to moonshot mode if the tableau is 100% full, etc.
        """
        self._check_can_play(player)
        if self._moonshot:
            raise ValueError("Already in moonshot mode.")

        total_spots = self.nrows * self.ncols
        if len(self.non_empty_positions) < total_spots:
            raise ValueError("Cannot start moonshot with any empty positions.")

        self._moonshot = True
        self._moonshot_player = player

    def moonshot_end(self) -> None:
        """
        End the moonshot state and calculate results
        """
        if not self._moonshot:
            raise ValueError("Not in moonshot mode.")

        player = self._moonshot_player
        if player not in self.active_players:
            raise ValueError("Moonshot player invalid or not active.")
        
        if self._lightning:
            if not self._moonshot_countered:
                self._outcome.add(player)
                self._done = True
            else:
                self._active_players.remove(player)
                if len(self._active_players) == 1:
                    self._outcome = self._active_players
                    self._done = True
        else:
            if self._moonshot_countered:
                self._scores[player] -= (self.nrows * self.ncols)
                self._moonshot_countered = False
            else:
                self._scores[player] += (self.nrows * self.ncols)
                self._redeal_tableau()
                
                if not self._deck:
                    self._done = True

        self._moonshot = False
        self._moonshot_player = None

    def end_game(self) -> None:
        """
        Non-lightning game: end by consensus
        """
        if self._done:
            raise ValueError("Game is already over.")
        if self._lightning:
            raise ValueError("Cannot manually end a lightning game.")
        self._done = True

        max_score = max(self._scores.values())
        winners = [p for p, val in self._scores.items() if val == max_score]
        self._outcome = set(winners)

    # ---------------------------------------------------------
    # HELPER METHODS
    # ---------------------------------------------------------
    def _check_can_play(self, player: int) -> None:
        """
        Common checks for calling a fit or other actions.
        """
        if self._done:
            raise ValueError("Game has ended.")
        if player not in self.active_players:
            raise ValueError(f"Player {player} is not active or invalid.")

    def _is_valid_fit(self, positions: list[PositionType]) -> bool:
        """
        Real Letters logic: For each feature, all cards are either all the same or all different.
        """
        cards = [self.card_at(pos) for pos in positions]

        for feature in cards[0].keys():
            vals = [c[feature] for c in cards]
            distinct = set(vals)
            if not (len(distinct) == 1 or len(distinct) == len(cards)):
                return False
        return True

    def _any_fits_left(self) -> bool:
        """
        Returns True if there's at least one valid fit on the board.
        """
        positions = list(self.non_empty_positions)
        if len(positions) < self.fit_size:
            return False

        for combo in itertools.combinations(positions, self.fit_size):
            if self._is_valid_fit(list(combo)):
                return True
        return False
    
    def _redeal_tableau(self) -> None:
        """
        Redeals the tableu after someone calls a valid fit
        """
        for r in range(self.nrows):
            for c in range(self.ncols):
                self._tableau.grid[r][c] = None

        for r in range(self.nrows):
            for c in range(self.ncols):
                if self._deck:
                    new_card_dict = self._deck.pop(0)
                    self._tableau.grid[r][c] = Card(new_card_dict)
