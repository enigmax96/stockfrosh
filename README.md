# stockfrosh
- Stockfish but worse. Quest to build a chess engine i can't beat.
- inspired by: https://www.chessprogramming.org
- Usage:
```
python3 main.py <white_engine_id> <black_engine_id> <num_games>
```

## Engines

### ID 1
 - plays a random legal move
 - no search needed

### ID 2
 - evaluates position based on material count and checkmate
 - uses minimax search

### ID 3 
 - evaluates position based on material count, checkmate,  piece placement, king safety, mobility 
 - uses minimax search with alpha beta pruning

### ID 4
 - evaluates position based on material count, checkmate,  piece placement, king safety, mobility 
 - uses itterative deepening, minimax search with alpha beta pruning

