import random
import itertools
import sys
import click
from letters import LettersGame
from base import LettersGameBase

POSSIBLE_COLORS = ['red', 'green', 'blue']
POSSIBLE_FONTS = ['serif', 'sans-serif', 'monospace']
POSSIBLE_LETTERS = ['A', 'B', 'C']
POSSIBLE_NUMBERS = ['1', '2', '3']

def make_deck(colors, fonts, letters, numbers):
    """
    Create and return a list of card dicts for the Letters game.
    """
    deck = []
    for color in colors:
        for font in fonts:
            for letter in letters:
                for number in numbers:
                    card = {
                        'color': color,
                        'font': font,
                        'letter': letter,
                        'number': number
                    }
                    deck.append(card)
    return deck

def is_fit(card_list):
    """
    Determine whether card_list forms a valid fit.
    A fit requires that for each feature all cards must be either 
    all the same OR all different for that feature.
    """
    if not card_list or any(card is None for card in card_list):
        return False
    
    for key in card_list[0].keys():
        values = [card[key] for card in card_list]
        distinct_values = set(values)
        if not (len(distinct_values) == 1 or len(distinct_values) == len(card_list)):
            return False
    
    return True

class RandomBot:
    """
    A bot that picks a random set of cards for a 'fit'.
    It never triggers moonshot and never ends the game on its own.
    """
    def __init__(self, letters: LettersGameBase) -> None:
        self.letters = letters

    def suggest_move(self, player_idx=None):
        """
        Return a random set of positions for a fit if possible, else None.
        """
        positions = list(self.letters.non_empty_positions)
        fit_size = self.letters.fit_size
        if len(positions) >= fit_size:
            return random.sample(positions, fit_size)
        return None

class GreedyBot:
    """
    A bot that searches for the first 3-card 'fit' in row-major order.
    If no fit is found, checks if the board is full:
    If full, triggers moonshot.
    Otherwise, ends the game.
    """
    def __init__(self, letters: LettersGameBase) -> None:
        self.letters = letters

    def suggest_move(self, player_idx=None):
        """
        Return the first valid 'fit' found. If no fit then
        If tableau is full trigger moonshot
        Otherwise: end the game.
        """
        nrows, ncols = self.letters.nrows, self.letters.ncols
        fit_size = self.letters.fit_size

        positions = list(self.letters.non_empty_positions)
        
        if fit_size == 3:
            for r1 in range(nrows):
                for c1 in range(ncols):
                    card1 = self.letters.card_at((r1, c1))
                    if card1 is None:
                        continue
                    idx1 = r1 * ncols + c1
                    for idx2 in range(idx1 + 1, nrows * ncols):
                        r2 = idx2 // ncols
                        c2 = idx2 % ncols
                        card2 = self.letters.card_at((r2, c2))
                        if card2 is None:
                            continue
                        for r3 in range(nrows):
                            for c3 in range(ncols):
                                if (r3, c3) in [(r1, c1), (r2, c2)]:
                                    continue
                                card3 = self.letters.card_at((r3, c3))
                                if card3 is None:
                                    continue
                                if is_fit([card1, card2, card3]):
                                    return [(r1, c1), (r2, c2), (r3, c3)]
        else:
            for combo in itertools.combinations(positions, fit_size):
                cards = [self.letters.card_at(pos) for pos in combo]
                if is_fit(cards):
                    return list(combo)

        if len(self.letters.non_empty_positions) == nrows * ncols:
            try:
                if not self.letters._moonshot:
                    player = (player_idx + 1) if player_idx is not None else 1
                    self.letters.moonshot_start(player)
                return positions[:fit_size]
            except ValueError:
                if not self.letters.done:
                    try:
                        self.letters.end_game()
                    except ValueError:
                        pass
                return None
        else:
            if not self.letters.done:
                try:
                    self.letters.end_game()
                except ValueError:
                    pass
            return None

class SmartBot:
    """
    A bot that finds all fits and picks the one
    overlapping with the most other fits. If no fit is found:
    If tableau is full, trigger moonshot.
    Else end the game.
    """
    def __init__(self, letters: LettersGameBase) -> None:
        self.letters = letters

    def suggest_move(self, player_idx=None):
        """
        Find all valid fits selects the most overlapping one
        If no fits
          If full, do moonshot. Else, end game.
        """
        all_positions = list(self.letters.non_empty_positions)
        fsize = self.letters.fit_size

        if len(all_positions) < fsize:
            if not self.letters.done:
                try:
                    self.letters.end_game()
                except ValueError:
                    pass
            return None

        combos = itertools.combinations(all_positions, fsize)
        valid_fits = []
        for combo in combos:
            cards = [self.letters.card_at(pos) for pos in combo]
            if is_fit(cards):
                valid_fits.append(set(combo))

        if not valid_fits:
            if len(all_positions) == self.letters.nrows * self.letters.ncols:
                try:
                    if not self.letters._moonshot:
                        player = (player_idx + 1) if player_idx is not None else 1
                        self.letters.moonshot_start(player)
                    return all_positions[:fsize]
                except ValueError:
                    if not self.letters.done:
                        try:
                            self.letters.end_game()
                        except ValueError:
                            pass
                    return None
            else:
                if not self.letters.done:
                    try:
                        self.letters.end_game()
                    except ValueError:
                        pass
                return None

        overlaps = []
        for i, fit1 in enumerate(valid_fits):
            overlap_count = sum(
                1 for j, fit2 in enumerate(valid_fits)
                if j != i and fit1 & fit2
            )
            overlaps.append(overlap_count)

        max_overlap = max(overlaps)
        best_indices = [
            i for i, count in enumerate(overlaps) if count == max_overlap
        ]
        chosen_index = random.choice(best_indices)
        return list(valid_fits[chosen_index])

class BotPlayer:
    """
    General class that houses a bot instance by name.
    """
    def __init__(self, name: str, letters: LettersGameBase) -> None:
        self._name = name
        bot_cls = {'random': RandomBot,
                   'greedy': GreedyBot,
                   'smart': SmartBot}[name]
        self.bot = bot_cls(letters)

def simulate(num_games: int, 
             bot1_type: str, 
             bot2_type: str, 
             rows: int = 3, 
             cols: int = 4) -> tuple[int, int, int]:
    """
    Run simulation of 'num_games' Letters matches between
    bot1_type and bot2_type.
    
    Args:
        num_games: Number of games to simulate
        bot1_type: Strategy for player 1
        bot2_type: Strategy for player 2
        rows: Number of rows in the tableau
        cols: Number of columns in the tableau
    
    Returns:
        Tuple of (player1_wins, player2_wins, ties)
    """
    p1_wins, p2_wins, ties = 0, 0, 0
    both_random = (bot1_type == 'random' and bot2_type == 'random')

    for game_num in range(num_games):
        deck = make_deck(
            POSSIBLE_COLORS, POSSIBLE_FONTS,
            POSSIBLE_LETTERS, POSSIBLE_NUMBERS
        )
        random.shuffle(deck)

        letters = LettersGame(deck, 3, (rows, cols), 2)
        bot1 = BotPlayer(bot1_type, letters)
        bot2 = BotPlayer(bot2_type, letters)
        bots = [bot1, bot2]

        if both_random:
            fit_count = [0, 0]

            while (fit_count[0] < 15 and fit_count[1] < 15
                   and not letters.done
                   and len(letters.non_empty_positions) >= 3):
                for player_idx in [0, 1]:
                    if letters.done:
                        break
                    if fit_count[player_idx] >= 15:
                        continue
                    if len(letters.non_empty_positions) < 3:
                        break

                    move = bots[player_idx].bot.suggest_move(player_idx)
                    if move and len(move) == 3:
                        try:
                            letters.call_fit(player_idx + 1, move)
                            fit_count[player_idx] += 1
                        except ValueError:
                            try:
                                if not letters.done:
                                    letters.end_game()
                            except ValueError:
                                pass
                    else:
                        try:
                            if not letters.done:
                                letters.end_game()
                        except ValueError:
                            pass
                        break

        else:
            moonshot_turns = 0
            max_turns = float('inf')
            turn_count = 0
            
            while not letters.done and len(letters.non_empty_positions) >= 3 and turn_count < max_turns:
                for player_idx, bot_obj in enumerate(bots):
                    if letters.done:
                        break

                    if letters._moonshot:
                        moonshot_turns += 1
                        if moonshot_turns >= len(bots) * 2:
                            try:
                                letters.moonshot_end()
                                moonshot_turns = 0
                            except ValueError:
                                pass
                    else:
                        moonshot_turns = 0
                    
                    move = bot_obj.bot.suggest_move(player_idx)
                    
                    if move:
                        try:
                            letters.call_fit(player_idx + 1, move)
                        except ValueError:
                            continue
                
                turn_count += 1

            if turn_count >= max_turns and not letters.done:
                try:
                    letters.end_game()
                except ValueError:
                    pass

        if not letters.done:
            try:
                letters.end_game()
            except ValueError:
                pass

        scores = letters.scores
        max_score = max(scores.values())
        winners = [p for p, val in scores.items() if val == max_score]

        if len(winners) == 1:
            if winners[0] == 1:
                p1_wins += 1
            else:
                p2_wins += 1
        else:
            ties += 1

    return p1_wins, p2_wins, ties

def cmd(num_games: int, player1: str, player2: str, rows: int = 3, cols: int = 4) -> None:
    """
    Run 'num_games' simulations printing the results as percentages.
    
    Args:
        num_games: number of games to simulate
        player1: strategy for player 1 ('random', 'greedy', or 'smart')
        player2: strategy for player 2 ('random', 'greedy', or 'smart')
        rows: number of rows in the tableau (default: 3)
        cols: number of columns in the tableau (default: 4)
    """
    p1_wins, p2_wins, ties = simulate(num_games, player1, player2, rows, cols)
    print(f"Player 1 ({player1}) wins: {100 * p1_wins / num_games:.2f}%")
    print(f"Player 2 ({player2}) wins: {100 * p2_wins / num_games:.2f}%")
    print(f"Ties: {100 * ties / num_games:.2f}%")

@click.command()
@click.option('-n', '--num-games', type=int, default=1000)
@click.option('-r', '--rows', type=int, default=3)
@click.option('-c', '--cols', type=int, default=4)
@click.option('-1', '--player1', type=click.Choice(['random', 'greedy', 'smart']), default='random')
@click.option('-2', '--player2', type=click.Choice(['random', 'greedy', 'smart']), default='random')
def main(num_games, rows, cols, player1, player2):
    """Run Letters game simulations with bot players"""
    cmd(num_games, player1, player2, rows, cols)

if __name__ == "__main__":
    if len(sys.argv) == 4 and all(not arg.startswith('-') for arg in sys.argv[1:]):
        player1 = sys.argv[1]
        player2 = sys.argv[2]
        num_games = int(sys.argv[3])
        cmd(num_games, player1, player2)
    else:
        main()
