import pygame


class Terminal:
    """
    This class is responsible for the functionality of the message terminal
    on the bottom of the play screen (or anywhere you put it).
    """

    def __init__(self, top_x, top_y, width, height, font_path, font_color,
                 font_size, background_color, destination):
        """
        This is the default c'tor.
        :param top_x: int, x pixel coordinate.
        :param top_y: int, y pixel coordinate.
        :param width: int, width of the terminal rectangle (in pixels).
        :param height: int, height of the terminal rectangle (in pixels).
        :param font_path: str, the path to the font that would be used.
        :param font_color: tuple (r,g,b), color of the font.
        :param font_size: int, the size of font in pixels.
        :param background_color: tuple (r,g,b), the color of the background.
        :param destination: pygame.Surface, the surface to blit on the terminal.
        """
        self.top_x = top_x
        self.top_y = top_y
        self.width = width
        self.height = height
        self.font_path = font_path
        self.font_color = font_color
        self.font_size = font_size
        self.background_color = background_color
        self.destination = destination

        self.terminal_rect = [self.top_x, self.top_y, self.width, self.height]
        self.score_content_pos = [self.top_x + 5, self.top_y + 5]
        self.lives_content_pos = [self.top_x + self.width - 80, self.top_y + 5]

        self.font = None
        self.is_updated = True
        self.score_content = 'SCORE: 0'
        self.lives_content = 'LIVES: 3'
        self.game_over_content = ''
        self.load_font()

    def load_font(self):
        """
        This function responsible to load the font that is specified in c'tor.
        :return: pygame.Font, the font object that will be used in terminal.
        """
        self.font = pygame.font.Font(self.font_path, self.font_size)

    def render_text(self, text):
        """
        This function is responsible to render the text and prepare it to be
        rendered on the screen as surface.
        :param text: str, the content that would be rendered as surface.
        :return: pygame.Surface, the surface object that should be blited.
        """
        return self.font.render(text, True, self.font_color)

    def show(self):
        """
        This function is responsible for the display operation of the screen.
        :return: None
        """

        # To be more efficient in graphical operation we will show only if
        # there is some update performed on the screen.
        if self.is_updated:
            pygame.draw.rect(self.destination,
                             self.background_color,
                             self.terminal_rect)

            if self.game_over_content:
                self.destination.blit(self.render_text(self.game_over_content),
                                      self.score_content_pos)
            else:
                self.destination.blit(self.render_text(self.score_content),
                                      self.score_content_pos)
                self.destination.blit(self.render_text(self.lives_content),
                                      self.lives_content_pos)

            pygame.display.update(self.terminal_rect)
            self.is_updated = False

    def update_score(self, score):
        """
        This function is responsible to update the content of the score.
        :param score: int, the score.
        :return: None
        """
        self.score_content = 'SCORE: ' + str(score)
        self.is_updated = True

    def update_lives(self, num_of_lives):
        """
        This function is responsible to update the number of lives in content.
        :param num_of_lives: int, the number of lives.
        :return: None
        """
        self.lives_content = 'LIVES: ' + str(num_of_lives)
        self.is_updated = True

    def create_game_over_message(self, score):
        """
        This function is responsible for the construction of 'game over'
        message.
        :param score: int, the score of the player.
        :return: None
        """
        self.game_over_content = ('Game is over! Your score is {}.' +
                                  '(Ctrl + N for new Game).').format(score)
        self.is_updated = True

    def reset_terminal(self):
        """
        This function is responsible to reset all of the content of the terminal
        and prepare it for new game.
        :return: None
        """
        self.score_content = 'SCORE: 0'
        self.lives_content = 'LIVES: 3'
        self.game_over_content = ''
        self.is_updated = True
