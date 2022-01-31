import AI
from GameElements import Player, Piece
from GameTree import GameTreeNode
from State import State
from Move import Move

class CheckersGame:
    def __init__(self):
        b = Piece.BLACK.value
        w = Piece.WHITE.value
        self.__game_state = State([b for _ in range(12)] + [0 for _ in range(8)] + [w for _ in range(12)])
        self.turn = Player.Human

        # stats
        self.total_turns = 0

    def start(self):
        while ( self.winner == None ):
            print(self.__game_state)

            if (self.turn == Player.AI):
                self.__game_state = AI.get_next_move(self.__game_state)
            else:
                self.__ask_human_input()

            self.total_turns += 1
            self.__switch_turn()
        
        print("Game over.")
        if (self.winner == Player.Human):
            print("You win!\n")
        else:
            print("AI wins!\n")

        # show stats at the end of the game
        print(f"Total turns taken:                           {self.total_turns}")
        print(f"Total nodes checked:                         {GameTreeNode.NODES_GENERATED}")
        print(f"Average time elapsed in deciding next move:  {AI.get_avg_decision_time():.6f} seconds")

    def __execute_move(self, move:Move):
        self.__game_state.set_piece( move.To, self.__game_state.get_piece(move.From) )
        self.__game_state.set_piece( move.From, 0 )

        if (move.nsteps == 2): # capture
            self.__game_state.set_piece( move.getPath(), 0 )

        if (move.To in range(1, 4+1) or move.To in range(29, 32+1)):
            if ( self.__game_state.get_piece(move.To) == Piece.BLACK.value ):
                self.__game_state.set_piece( move.To, Piece.BLACK_KING.value )
            elif ( self.__game_state.get_piece(move.To) == Piece.WHITE.value ):
                self.__game_state.set_piece( move.To, Piece.WHITE_KING.value )

        self.__game_state.last_move = move
        return self.__game_state

    def __switch_turn(self):
        if self.turn == Player.Human:
            self.turn = Player.AI
        else:
            self.turn = Player.Human

    def __find_piece_indexes(self, player:Player):
        # black pieces = AI, white pieces = HUMAN
        match_piece = lambda p: (p == Piece.BLACK.value or p == Piece.BLACK_KING.value) if player == Player.AI else (p == Piece.WHITE.value or p == Piece.WHITE_KING.value)
        indexes = [i for i in range(1, State.TILES+1) if match_piece( self.__game_state.get_piece(i) )]
        return indexes

    def __get_movable_pieces(self, player:Player):
        pieces = self.__find_piece_indexes(player)
        possible_moves = []
        for piece in pieces:
            possible_moves += AI.get_possible_moves(self.__game_state, piece, player)

        if any([m.nsteps == 2 for m in possible_moves]): # only keep jump moves if available
            new_possible_moves = [m for m in possible_moves if m.nsteps == 2]
            possible_moves = new_possible_moves

        movables = sorted(list(set( [m.From for m in possible_moves] )))
        return movables

    def __ask_human_input(self):
        print(">> Select a piece to move. Movable pieces: " + ", ".join([str(m) for m in self.__get_movable_pieces(Player.Human)]))

        fromTile = 0
        while fromTile not in self.__get_movable_pieces(Player.Human):
            fromTile = int(input("    Enter tile: "))

        # get possible move destinations
        possible_dests = AI.get_possible_moves(self.__game_state, fromTile, Player.Human)
        print(f"\n>> Selected piece at {fromTile}. Piece can move to: {', '.join([str(m.To) for m in possible_dests])}")
        toTile = 0
        while toTile not in possible_dests:
            toTile = int(input("    Enter tile: "))

        user_action = Move(fromTile, toTile)
        print(f"\nMoved {user_action.nsteps} steps.\n")
        print(f"Moved {user_action}.") # DEBUG
        self.__game_state = self.__execute_move(user_action)

    @property
    def winner(self) -> Player:
        AIwins = self.__game_state.totalWhitePieces == 0 or len(AI.actions(self.__game_state, Player.Human)) == 0
        humanWins = self.__game_state.totalBlackPieces == 0 or len(AI.actions(self.__game_state, Player.AI)) == 0
        return Player.AI if AIwins else Player.Human if humanWins else None


if __name__ == "__main__":
    game = CheckersGame()
    game.start()