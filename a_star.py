from .core import Coord, PlayerColor, PlaceAction
from .helper import f, fill_board, hash_board, goal, neighbours, add_piece, line_check
from .heuristic import state_h
from heapq import heappush as enqueue, heappop as dequeue


def a_star(
        board: dict[Coord, PlayerColor],
        target: Coord,
) -> tuple[None | list[PlaceAction], dict[Coord, PlayerColor], int, int]:
    
    '''
    Implement A* search algorithm with heuristic specified in heuristic.py.
    Input is a board and a target.
    Output is an optimal set of pieces that make up a soluiton.
    Returns none if no solution exists.
    '''
    
    s0 = [board,    # board
          [],       # actions
          0,        # g(s)
          0]        # h(s)
    
    # create queue with s0 as starting node
    queue = [(f(s0),    # f(state) = g(state) + h(state) 
              0,        # counter for tie-breaks (heapq implementation)
              s0)]      # state as specified above
    
    generated = expanded = 0
    tiebreak = 1

    # don't want to repeatedly expand identical states
    seen = set()

    while (queue):
        # pop state from queue
        s = dequeue(queue)
        curr_board, actions, g, h = s[-1]

        # we don't need to expand this state again
        bool_board = fill_board(curr_board)
        seen.add(hash_board(bool_board))
    
        # found the optimal solution! exit early
        if goal(bool_board, target):
            return actions, curr_board, generated, expanded
        
        expanded += 1

        # otherwise generate neighbours
        for piece in neighbours(curr_board):
            new_board = add_piece(curr_board, piece)
            bool_board = fill_board(new_board)
            
            # clear non-goal lines if possible
            if not goal(bool_board, target):
                line_check(new_board, bool_board, piece.coords)

            # unseen successive state located!
            if hash_board(bool_board) not in seen:
                generated += 1

                # place the piece
                new_actions = actions.copy()
                new_actions.append(piece)

                s_prime = [new_board,
                           new_actions,                                   
                           g + 1,                                           
                           state_h(new_board, bool_board, target)]

                enqueue(queue, (f(s_prime), tiebreak, s_prime))
                tiebreak += 1

    # no solution found
    return None, curr_board, generated, expanded

