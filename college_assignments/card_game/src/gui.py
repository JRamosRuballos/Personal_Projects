"""
GUI for Milestone #3
"""
import sys
import random
import pygame
from letters import LettersGame

#some constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
BG_COLOR = (48, 51, 140)  # a very nice darkish blue :)
LETTER_COLORS = {"red": (181, 36, 36), "green": (51, 145, 97), 
                 "blue": (101, 152, 214)}
FONTS = ["assets/actionj.ttf", "assets/zincboom.ttf", "assets/lexo.ttf"]
BUTTON_COLOR = (180, 180, 180)
BUTTON_SELECTED_COLOR = (250, 250, 138)
BUTTON_TEXT_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (255, 255, 0)
MESSAGE_COLOR = (255, 255, 255)

def standard_deck() -> list[dict[str, str]]:
    """
    Return a standard deck of Letters cards.
    """
    letters = ["A", "B", "C"]
    numbers = ["1", "2", "3"]
    colors = ["red", "green", "blue"]
    fonts = FONTS

    all_cards = [
        {"letter": letter, "number": number, "color": color, "font": font}
        for letter in letters
        for number in numbers
        for color in colors
        for font in fonts
    ]

    return all_cards

class Button:
    def __init__(self, x, y, width, height, text, font_size=24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.is_selected = False
        
    def draw(self, surface):
        """
        To draw the buttons
        """
        if self.is_selected:
            color = BUTTON_SELECTED_COLOR
        else:
            color = BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2) #for the border
        font = pygame.font.SysFont('Arial', self.font_size)
        text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def is_over(self, pos):
        return self.rect.collidepoint(pos)

class LettersGUI:
    def __init__(self, rows: int, cols: int, num_players: int) -> None:
        pygame.init()
        pygame.font.init()
        self.rows, self.cols = rows, cols
        self.num_players = num_players
        self.show_title_screen = True
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Letters Game")
        self.start_button = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 
                                   2 + 50, 200, 60, "Start Game")
        deck = standard_deck()
        random.shuffle(deck)
        self.game = LettersGame(deck, 3, (rows, cols), num_players)
        self.running = True
        self.selected_player = None
        self.selected_cards = []
        self.moon_mode = False
        self.game_over = False
        self.winner_message = ""
        self.tableau_width = WINDOW_WIDTH
        self.tableau_height = WINDOW_HEIGHT - 100  #bottom area for buttons
        self.card_width = self.tableau_width // self.cols
        self.card_height = self.tableau_height // self.rows
        self.player_buttons = []
        button_width = ((WINDOW_WIDTH - (num_players + 2) * 10) // 
                        (num_players + 1))
        for i in range(num_players):
            x = 10 + i * (button_width + 10)
            button = Button(x, WINDOW_HEIGHT - 90, button_width, 40, 
                            f"Player {i+1}")
            self.player_buttons.append(button)
        moon_x = 10 + num_players * (button_width + 10)
        self.moon_button = Button(moon_x, WINDOW_HEIGHT - 90, button_width, 
                                  40, "Moon")
    
    def draw_title_screen(self):
        """
        Displays  title screen with the game name and start button
        """
        self.window.fill(BG_COLOR)
        title_font = pygame.font.SysFont('Arial', 60, bold=True)
        title_text = title_font.render("LETTERS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 
                                                 WINDOW_HEIGHT // 3))
        self.window.blit(title_text, title_rect)
        self.start_button.draw(self.window)
        pygame.display.flip()
    
    def update_tableau(self):
        """
        Updating tableau from game
        """
        self.tableau = self.game.tableau
    
    def draw_screen(self) -> None:
        """
        Draws the game screen
        """
        self.window.fill(BG_COLOR)
        box_width, box_height = WINDOW_WIDTH // self.cols, (WINDOW_HEIGHT - 
                                                            100) // self.rows
        for i in range(self.rows):
            for j in range(self.cols):
                card = self.game.card_at((i, j))
                card_rect = pygame.Rect(j * box_width + 5, i * box_height + 5, 
                                        box_width - 10, box_height - 10)
                if (i, j) in self.selected_cards:
                    pygame.draw.rect(self.window, HIGHLIGHT_COLOR, card_rect)
                else:
                    pygame.draw.rect(self.window, (200, 200, 200), card_rect)
                if card:
                    color = LETTER_COLORS.get(card["color"], (0, 0, 0))
                    try:
                        font = pygame.font.Font(card["font"], 36)
                    except:
                        font = pygame.font.SysFont('Arial', 36)
                    letters_to_display = card["letter"] * int(card["number"])
                    text_surface = font.render(letters_to_display, True, color)
                    text_rect = text_surface.get_rect(center=card_rect.center)
                    self.window.blit(text_surface, text_rect)
        for button in self.player_buttons:
            button.draw(self.window)
            player_number = int(button.text.split()[-1])
            score = self.game.scores.get(player_number, 0)
            score_font = pygame.font.SysFont('Arial', 20)
            score_text = score_font.render(f"Score: {score}", True, 
                                           (255, 255, 255))
            score_rect = score_text.get_rect(center=(button.rect.centerx, 
                                                     button.rect.bottom + 20))
            self.window.blit(score_text, score_rect)
        self.moon_button.draw(self.window)
        pygame.display.flip()

    def draw_message_box(self, message):
        """
        Draws the message box for game announcements
        """
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.window.blit(overlay, (0, 0))
        message_box = pygame.Rect(
            WINDOW_WIDTH // 4,
            WINDOW_HEIGHT // 3,
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 3
        )
        pygame.draw.rect(self.window, (80, 80, 180), message_box)
        pygame.draw.rect(self.window, (255, 255, 255), message_box, 3)
        font = pygame.font.SysFont('Arial', 30)
        lines = message.split('\n')
        line_height = 40
        start_y = message_box.centery - (len(lines) * line_height) // 2
        for i, line in enumerate(lines):
            text = font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(message_box.centerx, 
                                              start_y + i * line_height))
            self.window.blit(text, text_rect)

    def check_for_game_over(self):
        """
        Checks for game over and calculates the winner(s) 
        """
        if self.game.done:
            self.game_over = True
            scores = self.game.scores
            max_score = max(scores.values())
            winners = [player for player, score in scores.items() if 
                       score == max_score]
            if len(winners) == 1:
                self.winner_message = f"Player {winners[0]} wins with {max_score} points!"
            else:
                self.winner_message = f"Tie game!\nPlayers {', '.join(map(str, winners))} tied with {max_score} points!"

            self.draw_message_box(self.winner_message)
            pygame.display.flip()
            pygame.time.delay(3000)
    
    def animate_card_removal(self, positions):
        """
        Animates the removal of cards
        """
        for scale in range(10, 0, -1):
            self.window.fill(BG_COLOR)
            self.draw_screen()
            for row, col in positions:
                card_rect = pygame.Rect(col * self.card_width + 5, 
                                        row * self.card_height + 5,
                                        (self.card_width - 10) * (scale / 10),
                                        (self.card_height - 10) * (scale / 10))
                pygame.draw.rect(self.window, BG_COLOR, card_rect)
            pygame.display.flip()
            pygame.time.delay(50)

    def animate_card_addition(self, positions):
        """
        Animates new cards sliding in from the top
        """
        for offset in range(-self.card_height, 0, 10):
            self.window.fill(BG_COLOR)
            self.draw_screen()
            for row, col in positions:
                card = self.game.card_at((row, col))
                if card:
                    card_rect = pygame.Rect(col * self.card_width + 5, offset + row * self.card_height + 5,
                                            self.card_width - 10, self.card_height - 10)
                    pygame.draw.rect(self.window, (200, 200, 200), card_rect)
                    color = LETTER_COLORS.get(card["color"], (0, 0, 0))
                    try:
                        font = pygame.font.Font(card["font"], 36)
                    except:
                        font = pygame.font.SysFont('Arial', 36)
                    text_surface = font.render(card["letter"], True, color)
                    text_rect = text_surface.get_rect(center=card_rect.center)
                    self.window.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.delay(50)

    def handle_card_click(self, row, col):
        """
        Handles when cards are pressed, checks for fits
        """
        if self.selected_player is None:
            return
        card_pos = (row, col)
        if card_pos not in self.selected_cards:
            self.selected_cards.append(card_pos)
        if len(self.selected_cards) == 3:
            try:
                success = self.game.call_fit(self.selected_player, 
                                             self.selected_cards)
                if success:
                    self.draw_message_box(f"Player {self.selected_player} scored points!")
                    pygame.display.flip()
                    pygame.time.delay(500)
                    self.animate_card_removal(self.selected_cards)
                    self.animate_card_addition(self.selected_cards)
                else:
                    self.draw_message_box("Invalid fit attempt.")
            except ValueError:
                self.draw_message_box("Error: Invalid fit.")
            self.selected_cards = []
            self.check_for_game_over()
            pygame.display.flip()
            pygame.time.delay(2000) 
            #maybe change later to go away after user clicks
    
    def handle_mouse_click(self, pos):
        """
        Handles when buttons r pressed
        """
        if self.show_title_screen:
            if self.start_button.is_over(pos):
                self.show_title_screen = False
            return 
        if self.game_over:
            return
        for i, button in enumerate(self.player_buttons):
            if button.is_over(pos):
                for b in self.player_buttons:
                    b.is_selected = False
                button.is_selected = True
                self.selected_player = i + 1
                self.selected_cards = []
                return
        if self.moon_button.is_over(pos):
            if self.selected_player is not None:
                if self.moon_mode:
                    self.moon_mode = False
                    self.game.moonshot_end()
                else:
                    self.moon_mode = True
                    self.game.moonshot_start(self.selected_player)
                    self.draw_message_box("Moonshot mode started!")
                    pygame.display.flip()
                    pygame.time.delay(1000)
                self.selected_cards = []
                return
        if self.selected_player is not None:
            if pos[1] < self.tableau_height:
                col = pos[0] // self.card_width
                row = pos[1] // self.card_height
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    self.handle_card_click(row, col)
    
    def run(self) -> None:
        """
        To run the game
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_mouse_click(event.pos)
            if self.show_title_screen:
                self.draw_title_screen()
            else:
                self.draw_screen()
            pygame.display.flip()
        pygame.quit()

import click

@click.command()
@click.option("-r", "--rows", default=3, show_default=True, 
              help="Number of rows in the tableau.")
@click.option("-c", "--cols", default=4, show_default=True, 
              help="Number of columns in the tableau.")
@click.option("-n", "--players", default=4, show_default=True, 
              type=click.IntRange(2, 4), 
              help="Number of players (between 2 and 4).")

def main(rows, cols, players):
    gui = LettersGUI(rows, cols, players)
    gui.run()

if __name__ == "__main__":
    main()
