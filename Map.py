from Consts import map_objects, colors
import Consts
from Graph import DijkstraAlgorithm
import pygame
import ast
from Helpers import get_orientation


class Map:
    """
    This class is responsible for the functionality of the logical map.


    What is the logical map?
    ------------------------

    The design pattern that is were chosen to be implemented within the game is
    the following: we will have two classes that deals with different logical
    operations. The first is the actual map (where each player placed, what we
    have on that map and so on) and the second is the graphical operation of
    the map (such as to show and display the map on the screen). This class
    deals with the first operation - the logical functionality of the map.


    The main idea behind the implementation.
    ----------------------------------------

    The map will be represented by a rectangle matrix (list of lists in python).
    Each entry will have the following format:
        [map object, player object, update]
    This means that each entry will be list of three objects.

        (a) map object: is the 'physical' object that is on the map. In our
        real world it is an analogy to what we see on the map. For example on
        latitude of x and altitude y we find river or rocks.

        Here, we can have one of the following options 'border', 'coin' or
        'empty'. The 'empty' means that the cell or 'map tile' is currently
        empty there is nothing but an empty place. The 'border' means that the
        cell or 'map tile' has blue big object on it and player cannot move
        there, and the 'coin' means that cell has coin in it and player can
        collect it if he goes to that tile.

        (b) player object: is the player inside the cell. It can be one of the
        following: 'user_player' that is the player (yellow pac-man); 'bad_pax'
        is the bad player that chase the good pac-man (the red pac-man). It also
        can be 'empty' and that means the currently there is no player in that
        cell.

        (c) update: is flag that tell the view whether the cell should be
        updated on the screen. For example if some player had moved into the
        cell then it should be updated on the screen and show that there is
        player.

    This class handles the organization and the operation of the map. In another
    words - when we perform some action (for example moving player or collecting
    the coin) we will manipulate the matrix.

    """
    def __init__(self):
        """
        It is the default c'tor. It creates Map object but this object does
        not ready to be presented on the screen or contain any information.
        """

        # Here we create the actual matrix.
        self.map = [[[map_objects['empty'], map_objects['empty'], False]
            for i in Consts.map_cols_range]
            for j in Consts.map_rows_range]

        self.players_coordinates = [[0, 0], [19, 19], [0, 19],[19, 0]]
        """ This list holds the coordinates of all player on the board. The 
            first list (the [0, 0]) is the starting point of the users pacman. 
            All of the other are the enemy players who chase the user. """

        self.max_number_of_coins = 0
        """ This is the maximum number of coins on the map. This number is 
            is important to decide when to finish and advance the level. This 
            number is also depended on the map itself. """

        self.collected_coins = 0

        self.search_algorithm = None
        """ This variable will hold the DijkstraAlgorithm object and will allow
            us to query for shortest path. It will be used for the 'AI' of the 
            enemy players who chase the user. """

    def load_map(self, map_path):
        """
        This function responsible to load the map. The map object is saved into
        the .map file that is created by the MapEditor program. It allows us to
        extend the game and introduce new maps and new challenges.
        :param map_path: str, the path to the .map file.
        :return: None
        """
        fd = open(map_path, 'r')
        map_rows = list(fd)
        for r in Consts.map_rows_range:
            for c in Consts.map_cols_range:
                self.map[r][c] = \
                    [int(map_rows[r][c]), map_objects['empty'], True]
                if self.map[r][c][0] == map_objects['empty']:
                    self.map[r][c][0] = map_objects['coin']
                    self.max_number_of_coins += 1
        fd.close()
        self.reset_players_position()

    def get(self, row, col):
        """
        This function is getter function. It returns the map tile information
        on [row, col] coordinate. It is important to understand the to top left
        corner of the map has the [0, 0] coordinate.

        Usage note: If row and col are our of the range then it returns object
        of ['bad_object', 'empty', False] which stands for a bad object.

        :param row: int, the row coordinate of the map tile.
        :param col: int, the col coordinate of the map tile.
        :return: List, [map object, player object, update] information of tile.
        """
        if (row in Consts.map_rows_range) and (col in Consts.map_cols_range):
            return self.map[row][col]
        return [map_objects['bad_object'], map_objects['empty'], False]

    def set(self, row, col, map_obj='empty', type_of_player='empty'):
        """
        This function manipulates the map matrix and sets the map tile on
        [row, col] to have [map_obj, type_of_player, True].
        :param row: int, the row coordinate of the map tile.
        :param col: int, the col coordinate of the map tile.
        :param map_obj: string, initially is 'empty'.
        :param type_of_player: string, initially is 'empty'.
        :return: None
        """
        if (row in Consts.map_rows_range) and (col in Consts.map_cols_range):
            self.map[row][col] = \
                [map_objects[map_obj], map_objects[type_of_player], True]

    def clear_player_off_tile(self, row, col):
        """
        This function removes player out off the specified [row, col] tile. It
        is mostly used to move player from one tile to another. For example if
        we currently stand on [1, 1] and we want to move the player to [1, 2]
        and it is a legal move to be performed then prior to movement to new
        tile we should clear the [1, 1] tile.

        The 'clear' operation has some nicety - while the 'user' player collects
        the coins on the field. the 'computer' players are not. So, we should
        take it into consideration. If this function is used by the
        'computer' player movement operation then it should not collect and
        leave there.

        :param row: int, the row of tile.
        :param col: int, the col of tile.
        :return: None
        """
        map_obj = 'empty'
        if self.is_coin(row, col):
            map_obj = 'coin'
        self.set(row, col, map_obj=map_obj, type_of_player='empty')

    def put_player_inside_tile(self,
                               row, col,
                               type_of_player='user_player'):
        """
        This function places specified player in specified tile.
        :param row: int, the row coordinate of the tile.
        :param col: int, the col coordinate of the tile.
        :param type_of_player: one of {'user_player', 'computer_player'}.
        initially it is 'user_player'.
        :return: int, 1 if there was coin and it was collected by user and 0
        if there wasn't coin or if the player that is moving is not user.
        """
        if self.is_coin(row, col):
            if type_of_player == 'user_player':
                self.collected_coins += 1
                self.set(row, col,
                         type_of_player=type_of_player)
                return 1
            else:
                self.set(row, col,
                         map_obj='coin',
                         type_of_player=type_of_player)
        else:
            self.set(row, col,
                     map_obj='empty',
                     type_of_player=type_of_player)
        return 0

    def is_coin(self, row, col):
        """
        This function checks whether there is coin in the specified tile.
        :param row: int, the row coordinate of the tile.
        :param col: int, the col coordinate of the tile.
        :return: True, if and only if there is coin.
        """
        return self.map[row][col][0] == map_objects['coin']

    def is_border(self, row, col):
        """
        This function checks whether there is border object in the specified
        tile. It is especially uses when we try to limit the movement of player.
        :param row: int, the row coordinate of the tile.
        :param col: int, the col coordinate of the tile.
        :return: True, if and only if there is border.
        """
        return self.map[row][col][0] == map_objects['border']

    def move_player(self, player_number=0, direction=''):
        """
        This function responsible for players movement. Note, it takes
        player_number (that is int) and not type_of_player as we would expected.

        :param player_number: int, indicates the player to be moved. If user
        players if to be moved then this number should be 0. Otherwise, each
        number that is >0 will move one of the enemy players.
        :param direction: str, one of four directions 'left', 'right', 'up' and
        'down'. It defines towards what direction player should move.
        :return: 1 -- if user player moves and collects a coin, 0 -- otherwise.
        """

        if player_number >= len(self.players_coordinates):
            return 0

        if player_number:
            type_of_player = 'computer_player'
        else:
            type_of_player = 'user_player'

        is_legal_move = False
        row, col = self.players_coordinates[player_number]
        new_row, new_col = 0, 0

        if direction == 'left':
            if col > min(Consts.map_cols_range):
                if not self.is_border(row, col - 1):
                    new_row = row
                    new_col = col - 1
                    is_legal_move = True
        elif direction == 'right':
            if col < max(Consts.map_cols_range):
                if not self.is_border(row, col + 1):
                    new_row = row
                    new_col = col + 1
                    is_legal_move = True
        elif direction == 'up':
            if row > min(Consts.map_rows_range):
                if not self.is_border(row - 1, col):
                    new_row = row - 1
                    new_col = col
                    is_legal_move = True
        elif direction == 'down':
            if row < max(Consts.map_rows_range):
                if not self.is_border(row + 1, col):
                    new_row = row + 1
                    new_col = col
                    is_legal_move = True

        if is_legal_move:
            self.clear_player_off_tile(row, col)
            self.players_coordinates[player_number] = [new_row, new_col]
            return self.put_player_inside_tile(new_row, new_col,
                                               type_of_player=type_of_player)

        return 0

    def get_collected_coins(self):
        """
        :return: Number of collected coind on the map.
        """
        return self.collected_coins

    def map_to_graph(self):
        """
        This function responsible to take the current map and return a (V, E)
        graph reprehension of that map. This is important to be used in search
        and query algorithms.
        :return: (V, E) representation of map. Where V is the vertices (legal
        map tiles to be moved on) and E is the edges between those tile
        (relations of from where to where we can move).
        """

        vertices = []
        edges = []
        good_map_obj = [map_objects['coin'], map_objects['empty']]

        for r in Consts.map_rows_range:
            for c in Consts.map_cols_range:
                map_obj = self.get(r, c)[0]
                if map_obj in good_map_obj:
                    vertices.append(str([r, c]))
                    if c < max(Consts.map_cols_range):
                        if self.get(r, c + 1)[0] in good_map_obj:
                            edges.append([str([r, c]), str([r, c + 1]), 1])
                    if c > min(Consts.map_cols_range):
                        if self.get(r, c - 1)[0] in good_map_obj:
                            edges.append([str([r, c]), str([r, c - 1]), 1])
                    if r < max(Consts.map_rows_range):
                        if self.get(r + 1, c)[0] in good_map_obj:
                            edges.append([str([r, c]), str([r + 1, c]), 1])
                    if r > min(Consts.map_rows_range):
                        if self.get(r - 1, c)[0] in good_map_obj:
                            edges.append([str([r, c]), str([r - 1, c]), 1])
        return [vertices, edges]

    def init_search_algorithm(self, search_algorithm='Dijkstra'):
        """
        This function init the type of search algorithm we want to use to query
        the map for the paths from one point to another point.
        :param search_algorithm: str, the name of search algorithm that we want.
        :return: None
        """
        v, e = self.map_to_graph()
        if search_algorithm == 'Dijkstra':
            self.search_algorithm = DijkstraAlgorithm(v, e)

    def move_bad_players(self):
        """
        This function is responsible to 'AI' of the computer. It moves the bad
        players and make them chase user player.
        :return: bool, True if and only if one of the bad players caught user.
        """
        players_row, player_col = self.players_coordinates[0]
        for player_number in range(len(self.players_coordinates[1:])):
            row, col = self.players_coordinates[player_number + 1]
            from_vertex = str([players_row, player_col])
            to_vertex = str([row, col])
            shortest_path = \
                self.search_algorithm.find_shortest_path(from_vertex, to_vertex)
            if len(shortest_path) <= 1:
                return True
            else:
                best_move = ast.literal_eval(shortest_path[-2])
            direction = get_orientation([row, col], best_move)
            self.move_player(player_number=player_number+1, direction=direction)
        return False

    def were_all_coins_collected(self):
        """
        :return: bool, True if and only if all possible coins were collected
        by the user player.
        """
        return self.collected_coins == self.max_number_of_coins

    def reset_players_position(self):
        """
        This function resets the coordinates of all players in game.
        :return: None
        """
        for row, col in self.players_coordinates:
            self.clear_player_off_tile(row, col)
        self.map[0][0][1] = map_objects['user_player']
        self.map[19][19][1] = map_objects['computer_player']
        self.map[19][0][1] = map_objects['computer_player']
        self.map[0][19][1] = map_objects['computer_player']
        self.players_coordinates = [[0, 0], [19, 19], [0, 19], [19, 0]]

    def reset_coins(self):
        """
        This function resets all coins on the map.
        :return: None
        """
        for r in Consts.map_rows_range:
            for c in Consts.map_cols_range:
                if self.get(r, c)[0] == map_objects['empty']:
                    self.map[r][c][0] = map_objects['coin']
                    self.map[r][c][2] = True

    def reset_map(self):
        self.reset_coins()
        self.reset_players_position()
        self.collected_coins = 0


class MapView:
    """
    This class is responsible for the functionality of the graphical map. In
    another words, here is the functionality regarded displaying map objects on
    the screen.
    """

    def __init__(self, map_controller, display):
        """
        Default c'tor
        :param map_controller: Map object.
        :param display: pygame.Surface object to blit on the map.
        """
        self.map_controller = map_controller
        self.display = display

    def show_player(self, row, col, type_of_player='user_player'):
        """
        Display specified player on the screen.
        :param row: int, the row coordinate of the map tile.
        :param col: int, the col coordinate of the map tile.
        :param type_of_player: str, one of 'user_player' or 'computer_player'.
        It defines the type of player to be shown on screen. Initially it is
        set to 'user_player'.
        :return: None
        """
        player_color = 'yellow' if type_of_player == 'user_player' else 'red'

        # First of all, clear the [row, col] display tile.
        map_tile_display = [col * Consts.slice_height, row * Consts.slice_width,
                            Consts.slice_width, Consts.slice_height]
        pygame.draw.rect(self.display, colors['black'], map_tile_display)

        # Draw the player.
        center = \
            [col * Consts.slice_height + int(Consts.slice_width / 2),
             row * Consts.slice_width + int(Consts.slice_height / 2)]
        pygame.draw.circle(self.display, colors[player_color], center, 20)

    def show(self):
        """
        Main view function that responsible to display the map on the screen.
        :return: None
        """
        is_updated = False
        for r in Consts.map_rows_range:
            for c in Consts.map_cols_range:
                rp = r * Consts.slice_height
                cp = c * Consts.slice_width
                map_object, type_of_player, update = \
                    self.map_controller.get(r, c)
                if map_object == map_objects['bad_object']:
                    pass
                elif update:
                    is_updated = True
                    pygame.draw.rect(self.display, colors['black'],
                                     [cp, rp, Consts.slice_width,
                                      Consts.slice_height])
                    if map_object == map_objects['border']:
                        pygame.draw.rect(self.display, colors['blue'],
                                         [cp, rp, Consts.slice_width,
                                          Consts.slice_height])
                    if map_object == map_objects['coin']:
                        pygame.draw.circle(self.display, colors['white'],
                                           [cp + int(Consts.slice_width / 2),
                                            rp + int(Consts.slice_height / 2)],
                                           10)
                    if type_of_player == map_objects['computer_player']:
                        self.show_player(r, c, type_of_player='computer_player')
                    if type_of_player == map_objects['user_player']:
                        self.show_player(r, c, type_of_player='user_player')

        if is_updated:
            pygame.display.update()
