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
ADDITIONAL FUNCTIONS
"""

def is_in_adjacent_rows(tile1, tile2):
	row = lambda x: (x-1) // 4
	return abs(row(tile1) - row(tile2)) == 1

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


def get_possible_moves(state:State, position:int, player:Player):
    side = lambda x : ((x - 1) // 4) % 2

    possible_actions = []
    piece_diagonals = [-5, -4, 3, 4] if side(position) else [-4, -3, 4, 5]

    if (state.get_piece(position) == Piece.BLACK.value): # AI pieces
        piece_diagonals = [3, 4] if side(position) else [4, 5]
    elif (state.get_piece(position) == Piece.WHITE.value): # human pieces
        piece_diagonals = [-5, -4] if side(position) else [-4, -3]

    for delta in piece_diagonals:
        if is_in_adjacent_rows(position, position+delta):
            m = Move(position, position+delta)

            if (m.isInBounds()):
                if (state.get_piece(m.To) == 0):
                    possible_actions.append(m)
                elif ( not is_players_piece(state.get_piece(m.To), player) ): # is opposing player's piece
                    m.extend()
                    if (m.isInBounds()):
                        if (state.get_piece(m.To) == 0):
                            possible_actions.append(m)

    #TODO: Sort moves for move ordering
    
    if any([a.type() == "SINGLE_JUMP_MOVE" for a in possible_actions]): # only return single jump moves if they're available
        return [a for a in possible_actions if a.type() == "SINGLE_JUMP_MOVE"]
    else:
        return possible_actions

def actions(state:State, player:Player) -> list:
    possible_actions = []

    for i in range(1, state.TILES+1):
        if ( state.get_piece(i) != 0 and is_players_piece(state.get_piece(i), player) ):
            possible_actions.extend(get_possible_moves(state, i, player))

    return possible_actions

def result(state:State, action:Move) -> State:
    resulting_state = deepcopy(state)
    
    resulting_state.set_piece( action.To, resulting_state.get_piece(action.From) )
    resulting_state.set_piece( action.From, 0 )

    if (action.nsteps == 2): # capture
        resulting_state.set_piece( action.getPath(), 0 )

    if (action.To in range(1, 4+1) or action.To in range(29, 32+1)):
        if ( resulting_state.get_piece(action.To) == Piece.BLACK.value ):
            resulting_state.set_piece( action.To, Piece.BLACK_KING.value )
        elif ( resulting_state.get_piece(action.To) == Piece.WHITE.value ):
            resulting_state.set_piece( action.To, Piece.WHITE_KING.value )

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