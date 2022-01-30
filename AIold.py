from GameElements import Player, Piece
from State import State
from Move import Move, MoveType
from GameTree import GameTreeNode

from copy import deepcopy
from time import time
from random import randint

NEGATIVE_INFINITY = float('-inf')
POSITIVE_INFINITY = float('inf')
SEARCH_DEPTH = 7

move_decision_times = []

def is_players_piece(piece:int, player:Player):
    return False if piece == None else piece > 0 if player == Player.AI else piece < 0


"""
HEURISTIC FUNCTIONS
"""

def eval_position_strength(state:State, r:int, c:int):
    pass

def eval_material_strength(state:State, player:Player):
    pass

"""
END OF HEURISTIC FUNCTIONS
"""


def get_possible_moves(state:State, r:int, c:int, player:Player):
    possible_actions = []
    piece_diagonals = []

    if (state.get_piece(r,c) == Piece.BLACK.value): # AI pieces
        piece_diagonals = [(1,1), (1,-1)]
    elif (state.get_piece(r,c) == Piece.WHITE.value): # human pieces
        piece_diagonals = [(-1,1), (-1,-1)]
    else:
        piece_diagonals = [(1,1), (1,-1), (-1,1), (-1,-1)]

    for add_r, add_c in piece_diagonals:
        m = Move(r, c, r+add_r, c+add_c)

        if (m.isInBounds()):
            if (state.get_piece(m.toRow,m.toCol) == 0):
                possible_actions.append(m)
            elif ( not is_players_piece(state.get_piece(m.toRow,m.toCol), player) ): # is opposing player's piece
                m.set_path( (m.toRow, m.toCol) )
                m.update_to((r+(2*add_r),c+(2*add_c)))
                if (state.get_piece(m.toRow,m.toCol) == 0 and m.isInBounds()):
                    possible_actions.append(m)

    #TODO: Sort moves for move ordering

    if any([a.type() == MoveType.SINGLE_JUMP_MOVE for a in possible_actions]):
        return [a for a in possible_actions if a.type() == MoveType.SINGLE_JUMP_MOVE]
    else:
        return possible_actions

def actions(state:State, player:Player) -> list:
    possible_actions = []

    for r in range(state.SIZE):
        for c in range(state.SIZE):
            if ( state.get_piece(r,c) != 0 and is_players_piece(state.get_piece(r,c), player) ):
                possible_actions.extend(get_possible_moves(state, r, c, player))

    return possible_actions

def result(state:State, action:Move) -> State:
    resulting_state = deepcopy(state)
    
    resulting_state.set_piece( action.toRow, action.toCol, resulting_state.get_piece(action.fromRow, action.fromCol) )
    resulting_state.set_piece( action.fromRow, action.fromCol, 0 )

    if (action.nsteps == 2): # capture
        resulting_state.set_piece( action.getPath()[0], action.getPath()[1], 0 )

    if (action.toRow == 0 or action.toRow == State.SIZE-1):
        if ( resulting_state.get_piece(action.toRow, action.toCol) == Piece.BLACK.value ):
            resulting_state.set_piece( action.toRow, action.toCol, Piece.BLACK_KING.value )
        elif ( resulting_state.get_piece(action.toRow, action.toCol) == Piece.WHITE.value ):
            resulting_state.set_piece( action.toRow, action.toCol, Piece.WHITE_KING.value )

    return resulting_state

def terminal_test(s:State) -> bool:
    bHaveRemainingPieces = s.totalBlackPieces > 0           and s.totalWhitePieces > 0
    bHaveRemainingMoves =  len(actions(s, Player.AI)) > 0   and len(actions(s, Player.Human)) > 0
    return not bHaveRemainingPieces or not bHaveRemainingMoves

def utility(s:State, p:Player) -> float:
    # temporary
    if p == Player.AI:
        return s.normalBlackPieces - s.normalWhitePieces + (s.blackKingPieces * 0.5 - s.whiteKingPieces * 0.5)
    else:
        return s.normalWhitePieces - s.normalBlackPieces + (s.whiteKingPieces * 0.5 - s.blackKingPieces * 0.5)

def minimax(node:GameTreeNode, depth:int, alpha:float, beta:float, isMaximizingPlayer:bool) -> tuple: #-> tuple(float, Move):
    if depth == 0 or terminal_test(node.state):
        if isMaximizingPlayer:  # AI is the maximizing player
            return utility(node.state, Player.AI)
        else:
            return utility(node.state, Player.Human)

    if isMaximizingPlayer:
        max_v = NEGATIVE_INFINITY

        for a in actions(node.state, Player.AI): # AI is the maximizing player
            result_node = GameTreeNode(state=result(node.state,a))
            node.add_child(result_node)
            v = minimax(result_node, depth-1, alpha, beta, False)
            result_node.set_heuristic(v)

            max_v = max(max_v, v)
            alpha = max(alpha, v)
            if beta <= alpha:
                break

        return max_v

    else:
        min_v = POSITIVE_INFINITY

        for a in actions(node.state, Player.Human): # Human is the minimizing player
            result_node = GameTreeNode(state=result(node.state,a))
            node.add_child(result_node)
            v = minimax(result_node, depth-1, alpha, beta, True)
            result_node.set_heuristic(v)

            min_v = min(min_v, v)
            beta = min(beta, v)
            if beta <= alpha:
                break

        return min_v


def get_next_move(currentState:State) -> State:
    print("AI thinking of next move...")
    start_time = time()

    game_tree_head = GameTreeNode(state=currentState)
    best_heuristic = minimax(game_tree_head, SEARCH_DEPTH, NEGATIVE_INFINITY, POSITIVE_INFINITY, True)

    best_next_candidates = []
    for child_node in game_tree_head.children:
        if (child_node.heuristic == best_heuristic):
            best_next_candidates.append(child_node.state)

    end_time = time()
    time_elapsed = end_time - start_time
    move_decision_times.append(time_elapsed)
    print(f"{time_elapsed:.6f}s elapsed.\n")
    
    # there can be more than 1 candidates. choose random
    r = randint(0, len(best_next_candidates)-1)
    return best_next_candidates[r]

def get_stats():
    print("Average time elapsed in deciding next move:")
    print(f"{sum(move_decision_times) / len(move_decision_times):.6f} seconds")