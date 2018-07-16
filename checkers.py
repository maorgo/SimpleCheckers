from textcolors.colors import textcolors as clr
import subprocess as sp


class CheckersBoard:

    """
        Checkers board game

        0 - Illegal square
        1 - Legal Playing square
        2 - First player
        3 - Second player
    """

    def __init__(self):
        self.board = None
        self.BOARD_DIMS = 8
        self.starting_rows = 3
        self.ILLEGAL_PLACE = [0]
        self.LEGAL_EMPTY_PLACE = [1]
        self.FIRST_PLAYER = [2]
        self.SECOND_PLAYER = [3]

        self._init_board()
        self._place_players()

    def _init_board(self):
        # Init the matrix
        is_even = True
        self.board = [[self.ILLEGAL_PLACE[0] for x in range(self.BOARD_DIMS)] for y in range(self.BOARD_DIMS)]

        # Distinguish between legal and illegal places
        for _i in range(self.BOARD_DIMS):
            for _j in range(self.BOARD_DIMS):
                if is_even:
                    self.board[_i][_j] = [1 if _j % 2 != 0 else 0]
                else:
                    self.board[_i][_j] = [1 if _j % 2 == 0 else 0]
            is_even = not is_even

    def _place_players(self):
        for i in range(self.BOARD_DIMS):
            for j in range(self.BOARD_DIMS):
                # Check if its in the zone of the first player (upper side of the board)
                if i < self.starting_rows and self.board[i][j] == self.LEGAL_EMPTY_PLACE:
                    self.board[i][j] = self.FIRST_PLAYER
                # Check if it should be the second player
                elif i >= len(self.board) - self.starting_rows and self.board[i][j] == self.LEGAL_EMPTY_PLACE:
                    self.board[i][j] = self.SECOND_PLAYER

    def print_board(self):
        print('   ', end='')
        for k in range(self.BOARD_DIMS):
            print('{}   '.format(k), end='')
        print()
        for i in range(self.BOARD_DIMS):
            print('{} '.format(i), end='')
            for j in range(self.BOARD_DIMS):
                if self.board[i][j] == self.FIRST_PLAYER:
                    print(clr.GREEN + '{} '.format(self.board[i][j]) + clr.ENDC, end='')
                elif self.board[i][j] == self.SECOND_PLAYER:
                    print(clr.CYAN + '{} '.format(self.board[i][j]) + clr.ENDC, end='')
                elif self.board[i][j] == self.ILLEGAL_PLACE:
                    print(clr.BLACK + '{} '.format(self.board[i][j]) + clr.ENDC, end='')
                else:
                    print(clr.BOLD_WHITE + '{} '.format(self.board[i][j]) + clr.ENDC, end='')
            print('{}'.format(i))

        print('   ', end='')
        for k in range(self.BOARD_DIMS):
            print('{}   '.format(k), end='')
        print()
        print()

    def move_player(self, player_invoking, origin_x, origin_y, dest_x, dest_y):
        # If you try to move an illegal place
        if not self._is_inside_board(dest_x, dest_y) or self.board[dest_x][dest_y] != self.LEGAL_EMPTY_PLACE:
            return False

        # If you try to move a player that is not yours
        if player_invoking != self.board[origin_x][origin_y]:
            return False

        # Can't move backwards!
        if player_invoking == self.FIRST_PLAYER and dest_x < origin_x:
            return False

        # Can't move backwards!
        if player_invoking == self.SECOND_PLAYER and dest_x > origin_x:
            return False

        # Does it eat the opponent's pawn?
        if self._search_near_square(origin_x, origin_y, dest_x, dest_y, player_invoking):
            return True

        # Check the pawn moves only one square
        if origin_x - dest_x not in [1, -1] or origin_y - dest_y not in [1, -1]:
            return False

        # If the move is legal, move it
        self.board[origin_x][origin_y] = self.LEGAL_EMPTY_PLACE
        self.board[dest_x][dest_y] = player_invoking
        return True

    def _is_inside_board(self, dest_x, dest_y):
        if dest_x >= self.BOARD_DIMS or dest_x < 0 or dest_y < 0 or dest_y >= self.BOARD_DIMS:
            return False
        return True

    def _search_near_square(self, starting_x, starting_y, dest_x, dest_y, player):
        # Determine who is the opponent
        if player == self.FIRST_PLAYER:
            opponent = self.SECOND_PLAYER
        else:
            opponent = self.FIRST_PLAYER

        # Check if can eat down to the left
        if dest_x > starting_x and dest_y < starting_y and starting_x + 2 < len(self.board) \
                and starting_y > 1 and self.board[starting_x + 1][starting_y - 1] == opponent:
            self.eat_down_left(starting_x, starting_y, player)
            return True

        # Check if can eat down to the right
        elif dest_x > starting_x and dest_y > starting_y and starting_x + 2 < len(self.board) \
                and starting_y + 2 < len(self.board)and self.board[starting_x + 1][starting_y + 1] == opponent:
            self.eat_down_right(starting_x, starting_y, player)
            return True

        # Check if can eat up to the left
        elif dest_x < starting_x and dest_y < starting_y and starting_x > 1 and starting_y > 1 \
                and self.board[starting_x - 1][starting_y - 1] == opponent:
            self.eat_up_left(starting_x, starting_y, player)
            return True

        # Check if can eat up to the right
        elif dest_x < starting_x and dest_y > starting_y and starting_x - 2 > -1 and starting_y + 2 < len(self.board) \
                and self.board[starting_x - 1][starting_y + 1] == opponent:
            self.eat_up_right(starting_x, starting_y, player)
            return True

    def eat_down_left(self, starting_x, starting_y, player):
        self.board[starting_x + 1][starting_y - 1] = self.LEGAL_EMPTY_PLACE
        self.board[starting_x + 2][starting_y - 2] = player
        self.board[starting_x][starting_y] = self.LEGAL_EMPTY_PLACE

    def eat_down_right(self, starting_x, starting_y, player):
        self.board[starting_x + 1][starting_y + 1] = self.LEGAL_EMPTY_PLACE
        self.board[starting_x + 2][starting_y + 2] = player
        self.board[starting_x][starting_y] = self.LEGAL_EMPTY_PLACE

    def eat_up_left(self, starting_x, starting_y, player):
        self.board[starting_x - 1][starting_y - 1] = self.LEGAL_EMPTY_PLACE
        self.board[starting_x - 2][starting_y - 2] = player
        self.board[starting_x][starting_y] = self.LEGAL_EMPTY_PLACE

    def eat_up_right(self, starting_x, starting_y, player):
        self.board[starting_x - 1][starting_y + 1] = self.LEGAL_EMPTY_PLACE
        self.board[starting_x - 2][starting_y + 2] = player
        self.board[starting_x][starting_y] = self.LEGAL_EMPTY_PLACE

    def play(self):
        ans = ''
        player_turn = self.FIRST_PLAYER
        print('This is the board:')
        is_legal_move = True
        while ans != 'q':
            sp.Popen('cls', shell=True).communicate()
            if not is_legal_move:
                print('Illegal move')
            self.print_board()
            if player_turn == self.FIRST_PLAYER:
                print('First player\'s turn (green)')
            else:
                print('Second player\'s turn (blue)')
            print('Which pawn would you like to move?')
            origin_x = int(input('row: '))
            origin_y = int(input('col: '))
            print('Where do you want to move it to?')
            dest_x = int(input('row: '))
            dest_y = int(input('col: '))

            # If the move was legal, clean the screen
            if self.move_player(player_turn, origin_x, origin_y, dest_x, dest_y):
                sp.Popen('cls', shell=True).communicate()
                is_legal_move = True
            else:
                is_legal_move = False

            # If the move was legal, its the second player's turn
            if is_legal_move:
                player_turn = \
                    [self.SECOND_PLAYER if player_turn == self.FIRST_PLAYER else self.FIRST_PLAYER][0]
