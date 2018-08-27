import pygame
from Consts import screen_resolution, liberation_serif, colors
from Map import Map, MapView
from Terminal import Terminal


class Game:

    def __init__(self):
        self.quit_game = False
        self.end_game = False
        self.pause_game = True
        self.screen_dimensions = \
            [screen_resolution['w'], screen_resolution['h']]

        pygame.init()
        self.display = pygame.display.set_mode(self.screen_dimensions)
        pygame.display.set_caption('PyMan Game')
        self.clock = pygame.time.Clock()

        self.map = Map()
        self.map_view = MapView(self.map, self.display)

        self.score = 0
        self.level = 0
        self.lives = 3
        self.decision_cycles = 20
        self.current_cycle = 0

        self.terminal = Terminal(0, 800, 800, 100, liberation_serif,
                                 colors['white'], 20, colors['black'],
                                 self.display)

    def player_move(self, key):
        """
        This function responsible to move users player with respect to the key
        that was pressed.
        :param key: pygame.key, it is the key that was pressed on keyboard.
        :return: 1 -- if and only if user collected coin, 0 -- otherwise.
        """
        if key == pygame.K_LEFT:
            return self.map.move_player(direction='left')
        elif key == pygame.K_RIGHT:
            return self.map.move_player(direction='right')
        elif key == pygame.K_UP:
            return self.map.move_player(direction='up')
        elif key == pygame.K_DOWN:
            return self.map.move_player(direction='down')
        return 0

    def run(self):
        """
        Main function of the game.
        :return: None
        """

        self.map.load_map("./basic_map.map")
        self.map.init_search_algorithm()

        while not self.quit_game:
            self.map_view.show()
            self.terminal.show()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game = True
                if event.type == pygame.KEYDOWN:
                    if not self.end_game:
                        if event.key == pygame.K_RETURN:
                            self.pause_game = False
                        elif event.key == pygame.K_ESCAPE:
                            self.pause_game = True
                        elif not self.pause_game:
                            if self.player_move(event.key):
                                self.score += 1
                                self.terminal.update_score(self.score)
                    else:
                        if (pygame.key.get_mods() & pygame.KMOD_LCTRL) and \
                                event.key == pygame.K_n:
                            self.end_game = False
                            self.new_game()

            if not self.end_game:

                if self.map.were_all_coins_collected():
                    self.map.reset_map()
                    self.decision_cycles -= 1
                    self.pause_game = True

                if not self.pause_game:
                    if self.current_cycle < self.decision_cycles:
                        self.current_cycle += 1
                    else:
                        self.current_cycle = 0
                        if self.map.move_bad_players():
                            if self.lives == 1:
                                self.terminal.create_game_over_message(self.score)
                                self.end_game = True
                            else:
                                self.lives -= 1
                                self.map.reset_players_position()
                                self.pause_game = True
                                self.terminal.update_lives(self.lives)
            self.clock.tick(20)

        pygame.quit()

    def quit(self):
        self.quit_game = True

    def new_game(self):
        """
        Reset all of the game parameters
        :return: None
        """
        self.score = 0
        self.level = 0
        self.lives = 3
        self.pause_game = True
        self.current_cycle = 0
        self.terminal.reset_terminal()
        self.map.reset_map()


if __name__ == '__main__':
    Game().run()
    quit()
