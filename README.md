# stockfrosh
Stockfish but worse. Quest to build a chess engine i cant beat.
inspired by: https://www.chessprogramming.org

# Idea 
- An environment where two engines play many chess games against each other. The engine winning more games is stronger. 
- By improving the evaluation function an engine uses to find the best move I can improve the engines strength. 
- By improving the search algorithms used to find the best move I can improve search time and hopefully the depth of the position tree I am able to search.

# Search
- The position tree:
```
Initial Position
       |
  +----+----+----+----+
  |    |    |    |    |
 Move1 Move2 Move3 Move4
  |    |    |    |
  P1   P2   P3   P4
  |    |    |    |
 +++  +++  +++  +++
  |    |    |    |
...   ...  ...   ...

```

- Pseudo search (The best move is the one who scored the highest evaluation.): 
```
traverse(position, depth):
if depth == 0
    return

evaluate(position)
    
legal_moves = position.generate_legal_moves()
    
for move in legal_moves:
    new_position = position.apply_move(move)
    traverse(new_position, depth - 1)
```

- MiniMax, AlphaBeta Pruning, ...

# Evaluation
- function that returns a numeric value given any position
    - add values to pieces (pawn=1, rook= 5, knight=3, queen=9, ...)
    - count material for black and white, substract, return
- for stronger engines e.g :
       - a knight in the center has higher value than one on the rim
       - a castled king has more value than one in te centre (earlygame)
- steal from here: https://github.com/official-stockfish/Stockfish
- https://chessmood.com/blog/evaluate-chess-position
- https://chessify.me/blog/chess-engine-evaluation
- https://www.chessprogramming.org/Evaluation


