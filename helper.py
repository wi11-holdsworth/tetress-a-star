from .core import Coord, PlayerColor, PlaceAction, BOARD_N, Direction
import numpy as np


PIECE_SIZE = 4


def f(
    state: list[dict[Coord, PlayerColor], list[PlaceAction], int, int]
) -> int:
    
    '''
    Represents evaluation function for A*
    Takes a state as described in A* function
    Returns g and h values added together
    '''

    # state[2] = g(s), state[3] = h(s)
    return state[2] + state[3]


def goal(
        bool_board: list[bool], 
        target: Coord
) -> bool:
    
    '''
    checks if a full line has been filled (goal state achieved or not)
    '''

    row, col = target_row_col(bool_board, target)

    # now check if either is completely full
    return np.all(row) or np.all(col)


def fill_board(
        givenBoard: dict[Coord, PlayerColor]
) -> np.ndarray:
    '''
    helper function to fill in numpy array representation of board state
    '''
        
    # initialise 2D numpy array of 0s (board is empty currently)
    currBoard = np.full((BOARD_N ,BOARD_N), False)

    # set squares that have colours in them to true
    for square in givenBoard:
        currBoard[square.r, square.c] = True
            
    return currBoard


def hash_board(
        board: np.ndarray[bool],
) -> int:
    
    '''
    Indended to minify a board so seen set does not take up so much memory
    Return integer digest for tuple form of boolean board
    '''
    
    return hash(tuple(int(i) for i in board.flat))


def add_piece(
        board: dict[Coord, PlayerColor],
        piece: PlaceAction
) -> None:
    
    '''
    Adds a piece to the input board.
    Does not modify board parameter.
    Returns updated board.
    '''
    
    board_prime = board.copy()
    
    # a piece has all red squares
    red_piece = {coord: PlayerColor.RED for coord in piece.coords}
    board_prime.update(red_piece)
    
    return board_prime


def neighbours(
        board: dict[Coord, PlayerColor]
) -> set[PlaceAction]:
    
    '''
    Return a list of successive RED coordinates that represent a valid piece
    given a current board state.
    '''
    
    # first find initial red squares the agent can launch from because
    # it only can place piece adjacent to same-colour squares
    pieces = [[coord] for coord, col in board.items() if col == PlayerColor.RED]

    # build piece by doing the following PIECE_SIZE times
    for i in range(PIECE_SIZE):
        # only launch from squares already part of the piece we are building
        for prev_piece in pieces.copy():
            # we can launch from any square that our piece encompasses
            for launch_square in prev_piece:
                # move in each valid direction
                for direction in Direction:
                    new_square = launch_square + direction

                    # only extend into (and store pieces containing)
                    # unpopulated squares
                    if new_square in board or new_square in prev_piece:
                        continue

                    # ignore initial launching point in piece path
                    # as it can cause the creation of invalid pieces.
                    # create a copy because we are iterating over incomplete
                    # piece.
                    new_path = [] if i == 0 else prev_piece.copy()
                    new_path.append(new_square)
                    pieces.append(new_path)

            # remove parent state
            pieces.remove(prev_piece)

    # return a set of PlaceActions with duplicates removed
    # sort first to ensure duplicates are being properly removed
    return set(PlaceAction(*tuple(sorted(piece))) for piece in pieces)


def target_row_col(
        board: np.ndarray[bool],
        target: Coord
) -> tuple[list[bool], list[bool]]:
    
    '''
    Generate two lists of booleans as the row and column
    the target exists in. If the square is populated, corresponding
    coordinate is True. Else False.
    '''

    return board[target.r, :], board[:, target.c]


def line_check(
        currBoard: dict[Coord, PlayerColor],
        bool_board: np.ndarray[bool],
        piece: list[Coord]
) -> None:
    
    '''
    checks if there's a full line that DOESN'T include the target coordinate.
    returns True if there is a full line. 
    '''

    # fill 2D numpy array to use to check for redundant full lines
    array_board = bool_board

    for coord in piece:
        row, col = target_row_col(array_board, coord)

        # found a full line that doesn't include the target coordinate
        if(np.all(row)):
            # get rid of the full line
            clear_line(currBoard, bool_board, coord, "HOR")

        # found a full line that doesn't include the target coordinate
        if(np.all(col)):
            # get rid of the full line
            clear_line(currBoard, bool_board, coord, "VER")
    
    
def clear_line(
        currBoard: dict[Coord, PlayerColor],
        bool_board: np.ndarray[bool],
        fullCoord: Coord,
        direction: str
) -> None:
    
    '''
    removes a full line that is in the way of achieving optimal solution
    '''

    new_board = currBoard.copy()

    # horizontal full line that's to be removed
    if(direction == "HOR"):
        for coordinate in new_board:
            # if coordinate is in the full line, delete it 
            if(fullCoord.r == coordinate.r):
                currBoard.pop(coordinate)
                bool_board[coordinate.r][coordinate.c] = False

    # vertical full line that's to be removed
    elif(direction == "VER"):
        for coordinate in new_board:
            # if coordinate is in the full line, delete it 
            if(fullCoord.c == coordinate.c):
                currBoard.pop(coordinate)
                bool_board[coordinate.r][coordinate.c] = False

