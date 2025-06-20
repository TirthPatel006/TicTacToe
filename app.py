from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

def check_winner(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for i,j,k in wins:
        if board[i]==board[j]==board[k] and board[i] != "":
            return board[i]
    if "" not in board:
        return "Draw"
    return None

def minimax(board, is_max, player, ai):
    winner = check_winner(board)
    if winner == ai:
        return 1
    elif winner == player:
        return -1
    elif winner == "Draw":
        return 0

    scores = []
    for i in range(9):
        if board[i] == "":
            board[i] = ai if is_max else player
            score = minimax(board, not is_max, player, ai)
            board[i] = ""
            scores.append(score)

    return max(scores) if is_max else min(scores)

def best_ai_move(board, player, ai):
    best_score = -float('inf')
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = ai
            score = minimax(board, False, player, ai)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    board = data["board"]
    player = data.get("player", "X")
    ai = data.get("ai", "O")
    mode = data.get("mode", "normal")

    if check_winner(board):
        return jsonify({"board": board, "winner": check_winner(board)})

    if mode == "god":
        move = best_ai_move(board, player, ai)
        if move is not None:
            board[move] = ai
    else:
        empty = [i for i in range(9) if board[i] == ""]
        if empty:
            board[random.choice(empty)] = ai

    winner = check_winner(board)
    return jsonify({"board": board, "winner": winner})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
