import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Tic Tac Toe - Alpha Beta AI")

board = [" " for _ in range(9)]
buttons = []
player = "X"
ai = "O"

def check_winner(b, symbol):
    win_patterns = [(0,1,2),(3,4,5),(6,7,8),
                    (0,3,6),(1,4,7),(2,5,8),
                    (0,4,8),(2,4,6)]
    return any(b[a]==b[b1]==b[c]==symbol for a,b1,c in win_patterns)

def is_draw(b):
    return all(cell != " " for cell in b)

def minimax(b, depth, is_max, alpha, beta):
    if check_winner(b, ai):
        return 1
    elif check_winner(b, player):
        return -1
    elif is_draw(b):
        return 0

    if is_max:
        max_eval = -float("inf")
        for i in range(9):
            if b[i] == " ":
                b[i] = ai
                eval = minimax(b, depth + 1, False, alpha, beta)
                b[i] = " "
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float("inf")
        for i in range(9):
            if b[i] == " ":
                b[i] = player
                eval = minimax(b, depth + 1, True, alpha, beta)
                b[i] = " "
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def best_move():
    best_score = -float("inf")
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = ai
            score = minimax(board, 0, False, -float("inf"), float("inf"))
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    if move is not None:
        board[move] = ai
        buttons[move].config(text=ai, state="disabled")

def click(index):
    if board[index] == " ":
        board[index] = player
        buttons[index].config(text=player, state="disabled")

        if check_winner(board, player):
            messagebox.showinfo("Result", "🎉 You Win!")
            reset_board()
            return
        elif is_draw(board):
            messagebox.showinfo("Result", "🤝 It's a Draw!")
            reset_board()
            return

        best_move()

        if check_winner(board, ai):
            messagebox.showinfo("Result", "💻 AI Wins!")
            reset_board()
        elif is_draw(board):
            messagebox.showinfo("Result", "🤝 It's a Draw!")
            reset_board()

def reset_board():
    global board
    board = [" " for _ in range(9)]
    for button in buttons:
        button.config(text=" ", state="normal")


for i in range(9):
    btn = tk.Button(root, text=" ", font=("Arial", 24), width=5, height=2,
                    command=lambda i=i: click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

reset_button = tk.Button(root, text="Reset", font=("Arial", 14),
                         command=reset_board, bg="lightblue")
reset_button.grid(row=3, column=0, columnspan=3, sticky="nsew")

root.mainloop()
