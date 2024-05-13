from .core import PlaceAction, Coord, BOARD_N, PlayerColor
from .helper import target_row_col, PIECE_SIZE
from math import ceil
import numpy as np


def state_h(
        board: dict[Coord, PlaceAction],
        bool_board: np.ndarray[bool],
        t: Coord
) -> int:
    
    '''
    Heuristic function for A*.
    Calculate minimum for all pieces:
        h = distance between row/col over all pieces + 
            number of empty regions in row/col.
    Return minimum over row/col as a number of pieces needed to reach the goal.
    '''

    red_squares = [sq for sq, col in board.items() if col == PlayerColor.RED]
    
    # no pieces = irrelevant heuristic
    if (len(red_squares) == 0):
        return 0

    # extract row and column as booleans
    t_row, t_col = target_row_col(bool_board, t)

    # compute closeness for row and col for all pieces
    return min(piece_h(red_squares, t_row, "r", t), piece_h(red_squares, t_col, "c", t))


def piece_h(
        red_squares: list[Coord],
        vec: list[bool],
        vectype: str,
        t: Coord
) -> int:
    
    '''
    Helper function for heuristic calculation.
    Calculates the afformentioned for a row or a column specified in vectype as
    "r" or "c".
    '''

    sq_to_piece = lambda x: ceil(x / PIECE_SIZE)
    
    min_h = np.Infinity

    # determine number of slots in pieces and largest gap in squares 
    sq_slots = piece_slots(vec)
    p_slots = sum(map(sq_to_piece, sq_slots))
    
    # want to find closest square to vec
    for sq in red_squares:
        # get minimal distance to vec
        sq_dist = abs(sq.r - t.r if vectype == "r" else sq.c - t.c)

        # adjust for board wrap-around
        sq_dist = min(sq_dist, -sq_dist % BOARD_N)
        
        # convert into a number of pieces
        p_dist = sq_to_piece(sq_dist)

        # zero-distance squares have no distance cost, so cannot reduce p_dist
        if p_dist < 1:
            min_h = min(min_h, p_dist + p_slots)
            continue

        # piece is within range to reduce number of slots in vec
        for sq_slot in sq_slots:
            # how many squares could it fill in vec?
            sq_potential = -sq_dist % PIECE_SIZE + 1

            # overflow squares could meaningfully reduce number of pieces
            # needed to fill the vector
            before_piece = sq_to_piece(sq_slot)
            after_piece = sq_to_piece(sq_slot - sq_potential)
            
            if (after_piece < before_piece): 
                p_dist -= 1
                break

        min_h = min(min_h, p_dist + p_slots)

    return min_h


def piece_slots(
        vec: list[bool]
) -> list[int]:
    
    '''
    Calculate number of empty regions in pieces for a given row/col
    Returns list of gaps sorted smallest to largest (in squares)
    '''

    gap_size = 0
    gaps = []
    
    for i in vec:
        # empty square found!
        if not i:
            gap_size += 1

        # gap has ended, add to list and reset counter
        elif gap_size > 0:
            gaps.append(gap_size)
            gap_size = 0
    
    # accounts for vec not being terminated by a True
    if gap_size > 0:
        gaps.append(gap_size)

    return sorted(gaps)