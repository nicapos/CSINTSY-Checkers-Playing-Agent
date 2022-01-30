from GameElements import Player, Piece
from State import State
from Move import Move, MoveType
from GameTree import GameTreeNode

from copy import deepcopy
from time import time
from random import randint, choice

NEGATIVE_INFINITY = float('-inf')
POSITIVE_INFINITY = float('inf')
SEARCH_DEPTH = 7

move_decision_times = []

def is_players_piece(piece:int, player:Player):
    return False if piece == None else piece > 0 if player == Player.AI else piece < 0

def executed_by(move:Move, state:State): # returns the player executing the move passed in the parameters
    # black pieces = AI, white pieces = HUMAN
    return Player.AI if (state.get_piece(move.From) == Piece.BLACK.value or state.get_piece(move.From) == Piece.BLACK_KING.value) else Player.Human

"""
ADDITIONAL FUNCTIONS
"""

def is_in_adjacent_rows(tile1, tile2):
	row = lambda x: (x-1) // 4
	return abs(row(tile1) - row(tile2)) == 1

def rows_away(tile1, tile2):
	row = lambda x: (x-1) // 4
	return abs(row(tile1) - row(tile2))

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

    edge_pieces = [4, 5, 12, 13, 20, 21, 28, 29]

    if position in edge_pieces:
        piece_diagonals = [-4, 4] # default values for King pieces

        if (state.get_piece(position) == Piece.BLACK.value): # AI normal pieces
            piece_diagonals = [4]
        elif (state.get_piece(position) == Piece.WHITE.value): # human normal pieces
            piece_diagonals = [-4]
    else:
        piece_diagonals = []

        if (state.get_piece(position) == Piece.BLACK.value): # AI normal pieces
            piece_diagonals = [3, 4] if side(position) else [4, 5]
        elif (state.get_piece(position) == Piece.WHITE.value): # human normal pieces
            piece_diagonals = [-5, -4] if side(position) else [-4, -3]
        else:
            piece_diagonals = [-5, -4, 3, 4] if side(position) else [-4, -3, 4, 5] # default values for King pieces

    possible_actions = []
    for delta in piece_diagonals:
        m = Move(position, position+delta)

        if (m.isInBounds() and rows_away(m.From, m.To) == 1):
            if ( not is_players_piece(state.get_piece(m.To), player) ):
                if (state.get_piece(m.To) == 0):
                    possible_actions.append(m)

                else:
                    move_extended = m.extend()
                    if (m.isInBounds() and move_extended):
                        if (state.get_piece(m.To) == 0 and rows_away(m.From, m.To) == 2):
                            possible_actions.append(m)

    if any([a.nsteps == 2 for a in possible_actions]): # only return single jump moves if they're available
        return [a for a in possible_actions if a.nsteps == 2]
    else:
        return possible_actions

def find_piece_indexes(state:State, player:Player):
    # black pieces = AI, white pieces = HUMAN
    match_piece = lambda p: (p == Piece.BLACK.value or p == Piece.BLACK_KING.value) if player == Player.AI else (p == Piece.WHITE.value or p == Piece.WHITE_KING.value)
    indexes = [i for i in range(1, State.TILES+1) if match_piece( state.get_piece(i) )]
    return indexes


def actions(state:State, player:Player) -> list:
    pieces = find_piece_indexes(state, player)
    possible_moves = []
    for piece in pieces:
        possible_moves += get_possible_moves(state, piece, player)

    if any([m.nsteps == 2 for m in possible_moves]): # only keep jump moves if available
        new_possible_moves = [m for m in possible_moves if m.nsteps == 2]
        possible_moves = new_possible_moves

    return possible_moves


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

    resulting_state.last_move = action
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


def quadrant(pos):
	if pos <= 16:
		return 2 if (pos-1)%4 <= 1 else 1
	else:
		return 3 if (pos-1)%4 <= 1 else 4

def mergeSort(arr, custom_condition):
    if len(arr) > 1:
        mid = len(arr)//2
  
        H1 = arr[:mid]
        H2 = arr[mid:]
  
        mergeSort(H1, custom_condition)
        mergeSort(H2, custom_condition)
  
        i = j = k = 0
  
        while i < len(H1) and j < len(H2):
            if custom_condition(H1[i], H2[j]):
                arr[k] = H1[i]
                i += 1
            else:
                arr[k] = H2[j]
                j += 1
            k += 1
  
        # Checking if any element was left
        while i < len(H1):
            arr[k] = H1[i]
            i += 1
            k += 1
  
        while j < len(H2):
            arr[k] = H2[j]
            j += 1
            k += 1

def heuristic_center(h1, h2):
    col = lambda x: ((x - 1) % 4) + 1
    side = lambda x : ((x - 1) // 4) % 2

    # lower eval = closer to center
    eval1 = [3, 2, 4, 1].index( col(h1.last_move.To) ) if side(h1.last_move.To) else [2, 3, 1, 4].index( col(h1.last_move.To) )
    eval2 = [3, 2, 4, 1].index( col(h2.last_move.To) ) if side(h2.last_move.To) else [2, 3, 1, 4].index( col(h2.last_move.To) )

    return eval1 > eval2

def order_moves(candidates):
    """
    Try to keep your pieces on the back row or king row for as long as possible, to keep the other player from gaining a king.
    """
    heuristic_back = lambda h1, h2: h1.last_move.From > h2.last_move.From
    mergeSort(candidates, custom_condition=heuristic_back) 

    """
    Control the center
    """
    mergeSort(candidates, custom_condition=heuristic_center) 


def get_next_move(currentState:State) -> State:
    APPLY_MOVE_ORDERING = True      # CUSTOM

    print("AI thinking of next move...")
    start_time = time()

    game_tree_head = GameTreeNode(state=currentState)
    best_heuristic = minimax(game_tree_head, SEARCH_DEPTH, NEGATIVE_INFINITY, POSITIVE_INFINITY, True)

    best_next_candidates = []
    for child_node in game_tree_head.children:
        if (child_node.heuristic == best_heuristic):
            best_next_candidates.append(child_node.state)

    candidates_actions = [c.last_move for c in best_next_candidates]
    if any([c.nsteps == 2 for c in candidates_actions]):
        new_candidates = [c for c in best_next_candidates if c.last_move.nsteps == 2]
        best_next_candidates = new_candidates

    # there can be more than 1 candidates. apply move ordering or choose random
    count_candidates = len(best_next_candidates)
    if (count_candidates > 1):
        if APPLY_MOVE_ORDERING:
            order_moves(best_next_candidates)
            best_candidate = best_next_candidates[0]
        else:
            best_candidate = choice(best_next_candidates)
    elif (count_candidates == 1):
        best_candidate = best_next_candidates[0]
    else:
        print("ERROR")

    end_time = time()
    time_elapsed = end_time - start_time
    move_decision_times.append(time_elapsed)

    print(f"Moved {best_candidate.last_move}.")
    print(f"{time_elapsed:.6f}s elapsed.\n")
    
    return best_candidate

def get_avg_decision_time():
    return sum(move_decision_times) / len(move_decision_times)