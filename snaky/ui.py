import pygame

from settings import WIDTH, UI_MARGIN


class GameUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 22)

    def draw_text(self, screen, text, position, color):
        surface = self.font.render(text, True, color)
        screen.blit(surface, position)

    def draw(self, screen, score, gold, snake_length, boosting):
        self.draw_text(
            screen,
            f"Score: {score}",
            (UI_MARGIN, UI_MARGIN),
            (240, 245, 255)
        )

        self.draw_text(
            screen,
            f'Gold: {gold:.1f}',
            (UI_MARGIN, UI_MARGIN + 35),
            (255, 205, 70)
        )

        self.draw_text(
            screen,
            f'Length: {snake_length}',
            (UI_MARGIN, UI_MARGIN + 70),
            (90, 248, 195)
        )

        boost_color = (255, 100, 80) if boosting else (150, 165, 185)

        boost_label = ("Boost Active!"
                       if boosting
                       else "Hold Space to Boost!")

        boost_surface = self.small_font.render(
            boost_label,
            True,
            boost_color
        )
        screen.blit(boost_surface,
                    (WIDTH - boost_surface.get_width() - UI_MARGIN,
                     UI_MARGIN)
                    )
