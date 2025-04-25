import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

dealer_one = pygame.Rect((250, 30, 120, 180))
dealer_two = pygame.Rect((390, 30, 120, 180))

player_one = pygame.Rect((250, 400, 120, 180))
player_two = pygame.Rect((390, 400, 120, 180))

hit_rect = pygame.Rect((150, 250, 190, 120))
pass_rect = pygame.Rect((450, 250, 190, 120))

font = pygame.font.Font(None, 20)
text = font.

run = True
while run:
    screen.fill((0, 0, 0,))
    pygame.draw.rect(screen, (255, 0, 0), dealer_one)
    pygame.draw.rect(screen, (255, 0, 0), dealer_two)
    pygame.draw.rect(screen, (255, 0, 0), player_one)
    pygame.draw.rect(screen, (255, 0, 0), player_two)
    pygame.draw.rect(screen, (255, 0, 0), hit_rect)
    pygame.draw.rect(screen, (255, 0, 0), pass_rect)
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        player.move_ip(-1, 0)
    elif key[pygame.K_d]:
        player.move_ip(1, 0)
    elif key[pygame.K_w]:
        player.move_ip(0, -1)
    elif key[pygame.K_s]:
        player.move_ip(0, 1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if hit_rect.collidepoint(event.pos):
                pass_rect = pygame.Rect((450, 150, 190, 120))

    pygame.display.update()
pygame.quit()