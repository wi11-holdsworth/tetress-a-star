# tetress-a-star
An implementation of the A-star admissible heuristic search algorithm to find the optimal path between a source square and a target row/column with squares to fill

## Heuristic

1. vec = [target row, target column]
2. distance in pieces to vec + number of piece-slots in vec
3. minimise over vec: take smaller

