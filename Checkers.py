from operator import index
import AI
from GameElements import Player, Piece
from State import State
from Move import Move

class CheckersGame:
    def __init__(self):
        b = Piece.BLACK.value
        w = Piece.WHITE.value
        self.__game_state = State([b for _ in range(12)] + [0 for _ in range(8)] + [w for _ in range(12)])
        self.turn = Player.Human

    def start(self):
        while ( self.winner == None ):
            print(self.__game_state)

            if (self.turn == Player.AI):
                self.__game_state = AI.get_next_move(self.__game_state)
            else:
                self.__ask_human_input()

            self.__switch_turn()
        
        print("Game over.")
        if (self.winner == Player.Human):
            print("You win!\n")
        else:
            print("AI wins!\n")

        #AI.get_stats()

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

        return self.__game_state

    def __switch_turn(self):
        if self.turn == Player.Human:
            self.turn = Player.AI
        else:
            self.turn = Player.Human

    def __find_piece_indexes(self, player:Player):
        # black pieces = AI, white pieces = HUMAN
        match_piece = Piece.BLACK.value if player == Player.AI else Piece.WHITE.value
        indexes = [i for i in range(1, State.TILES+1) if self.__game_state.get_piece(i) == match_piece]
        return indexes

    def __ask_human_input(self):
        possible_srcs = [str(i) for i in self.__find_piece_indexes(Player.Human) if len(AI.get_possible_moves(self.__game_state, i, Player.Human)) > 0]
        print(">> Select a piece to move. Movable pieces: " + ", ".join(possible_srcs))

        fromTile = int(input("    Enter tile: "))

        # get possible move destinations
        possible_dests = [str(m.To) for m in AI.get_possible_moves(self.__game_state, fromTile, Player.Human)]
        print(f"\n>> Selected piece at  {fromTile}. Piece can move to: {', '.join(possible_dests)}")
        toTile = int(input("    Enter tile: "))

        user_action = Move(fromTile, toTile)
        print(f"\nMoved {user_action.nsteps} steps.\n")
        self.__game_state = self.__execute_move(user_action)

    @property
    def winner(self) -> Player:
        AIwins = self.__game_state.totalWhitePieces == 0 or len(AI.actions(self.__game_state, Player.Human)) == 0
        humanWins = self.__game_state.totalBlackPieces == 0 or len(AI.actions(self.__game_state, Player.AI)) == 0
        return Player.AI if AIwins else Player.Human if humanWins else None


if __name__ == "__main__":
    game = CheckersGame()
    game.start()