from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

def check_winner(board):
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for i, j, k in wins:
        if board[i] == board[j] == board[k] and board[i] != '':
            return board[i]
    if '' not in board:
        return 'Draw'
    return None

def minimax(board, is_maximizing, player, ai):
    winner = check_winner(board)
    if winner == ai:
        return 1
    elif winner == player:
        return -1
    elif winner == 'Draw':
        return 0

    if is_maximizing:
        best = -float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = ai
                score = minimax(board, False, player, ai)
                board[i] = ''
                best = max(score, best)
        return best
    else:
        best = float('inf')
        for i in range(9):
            if board[i] == '':
                board[i] = player
                score = minimax(board, True, player, ai)
                board[i] = ''
                best = min(score, best)
        return best

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    board = data["board"]
    player = data["player"]
    ai = data["ai"]
    mode = data.get("mode")

    if mode == "god":
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if board[i] == '':
                board[i] = ai
                score = minimax(board, False, player, ai)
                board[i] = ''
                if score > best_score:
                    best_score = score
                    best_move = i
        if best_move is not None:
            board[best_move] = ai
    else:
        empty = [i for i in range(9) if board[i] == '']
        if empty:
            move = random.choice(empty)
            board[move] = ai

    winner = check_winner(board)
    return jsonify({"board": board, "winner": winner})
