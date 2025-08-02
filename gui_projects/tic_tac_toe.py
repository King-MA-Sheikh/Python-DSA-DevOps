import customtkinter as ctk
from tkinter import messagebox, simpledialog
import random
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TicTacToe(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🎮 Tic Tac Toe Game 🎮")
        width = 500
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)

        # Game state
        self.player_names = {"X": "Player X", "O": "Player O"}
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.vs_computer = False
        self.difficulty = "Easy"
        self.scores = {"X": 0, "O": 0, "Draw": 0}
        self.winning_line = None  # To store the winning line coordinates

        # Colors
        self.colors = {
            "X": "#FF5555",  # Red
            "O": "#55AAFF",   # Blue
            "bg": "#2B2B2B",  # Dark gray
            "button": "#3A3A3A",  # Medium gray
            "text": "#FFFFFF",  # White
            "highlight": "#4CAF50",  # Green
            "win_line": "#FFD700"  # Gold for winning line
        }

        # Header
        self.label = ctk.CTkLabel(self, text="❌ Player X's Turn ❌", 
                                font=("Arial", 20, "bold"),
                                text_color=self.colors["X"])
        self.label.pack(pady=10)

        # Button frame for top buttons
        self.top_button_frame = ctk.CTkFrame(self, fg_color=self.colors["bg"])
        self.top_button_frame.pack(pady=5)

        self.name_btn = ctk.CTkButton(self.top_button_frame, 
                                     text="✏️ Change Player Names", 
                                     command=self.change_names,
                                     fg_color=self.colors["button"],
                                     hover_color=self.colors["highlight"])
        self.name_btn.pack(side="left", padx=5)

        self.mode_btn = ctk.CTkButton(self.top_button_frame, 
                                     text="🔄 Switch to 1-Player Mode", 
                                     command=self.toggle_mode,
                                     fg_color=self.colors["button"],
                                     hover_color=self.colors["highlight"])
        self.mode_btn.pack(side="left", padx=5)

        self.difficulty_btn = ctk.CTkButton(self.top_button_frame, 
                                           text="⚡ Difficulty: Easy", 
                                           command=self.toggle_difficulty,
                                           fg_color=self.colors["button"],
                                           hover_color=self.colors["highlight"])
        self.difficulty_btn.pack(side="left", padx=5)

        # Game Board
        self.frame = ctk.CTkFrame(self, fg_color=self.colors["bg"])
        self.frame.pack(pady=10)
        
        # Canvas for drawing winning line
        self.canvas = ctk.CTkCanvas(self.frame, width=330, height=330, bg=self.colors["bg"], highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=3, columnspan=3)
        
        self.buttons = []
        for row in range(3):
            row_buttons = []
            for col in range(3):
                btn = ctk.CTkButton(self.frame, text="", width=100, height=100,
                                    font=("Arial", 32, "bold"),
                                    fg_color=self.colors["button"],
                                    hover_color=self.colors["highlight"],
                                    command=lambda r=row, c=col: self.on_click(r, c))
                btn.grid(row=row, column=col, padx=5, pady=5)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Bottom control buttons
        self.button_frame = ctk.CTkFrame(self, fg_color=self.colors["bg"])
        self.button_frame.pack(pady=10)

        self.reset_btn = ctk.CTkButton(self.button_frame, 
                                      text="🔄 Reset", 
                                      command=self.reset_game,
                                      fg_color=self.colors["button"],
                                      hover_color=self.colors["highlight"])
        self.reset_btn.pack(side="left", padx=5)

        self.cancel_btn = ctk.CTkButton(self.button_frame, 
                                        text="❌ Cancel Game", 
                                        command=self.cancel_game,
                                        fg_color=self.colors["button"],
                                        hover_color="#FF5555")  # Red for cancel
        self.cancel_btn.pack(side="left", padx=5)

        self.quit_btn = ctk.CTkButton(self.button_frame, 
                                     text="🚪 Quit", 
                                     command=self.destroy,
                                     fg_color=self.colors["button"],
                                     hover_color="#FF5555")  # Red for quit
        self.quit_btn.pack(side="left", padx=5)

        self.score_label = ctk.CTkLabel(self, 
                                       text=self.get_score_text(), 
                                       font=("Arial", 16),
                                       text_color=self.colors["text"])
        self.score_label.pack(pady=10)

    def draw_winning_line(self, win_type, index):
        """Draw a line through the winning combination"""
        padding = 10
        cell_size = 110  # Button width + padding
        
        if win_type == "row":
            y = index * cell_size + cell_size // 2
            self.canvas.create_line(padding, y, 3 * cell_size - padding, y, 
                                  fill=self.colors["win_line"], width=5)
            self.winning_line = ("row", index)
            
        elif win_type == "column":
            x = index * cell_size + cell_size // 2
            self.canvas.create_line(x, padding, x, 3 * cell_size - padding, 
                                  fill=self.colors["win_line"], width=5)
            self.winning_line = ("column", index)
            
        elif win_type == "diagonal":
            if index == 0:  # Top-left to bottom-right
                self.canvas.create_line(padding, padding, 
                                      3 * cell_size - padding, 3 * cell_size - padding, 
                                      fill=self.colors["win_line"], width=5)
                self.winning_line = ("diagonal", 0)
            else:  # Top-right to bottom-left
                self.canvas.create_line(3 * cell_size - padding, padding, 
                                      padding, 3 * cell_size - padding, 
                                      fill=self.colors["win_line"], width=5)
                self.winning_line = ("diagonal", 1)

    def check_winner(self):
        """Check for winner and return winner if found, else None"""
        # Check rows
        for i in range(3):
            if self.board[i][0] != "" and all(self.board[i][j] == self.board[i][0] for j in range(3)):
                self.draw_winning_line("row", i)
                return self.board[i][0]
        
        # Check columns
        for j in range(3):
            if self.board[0][j] != "" and all(self.board[i][j] == self.board[0][j] for i in range(3)):
                self.draw_winning_line("column", j)
                return self.board[0][j]
        
        # Check diagonals
        if self.board[0][0] != "" and all(self.board[i][i] == self.board[0][0] for i in range(3)):
            self.draw_winning_line("diagonal", 0)
            return self.board[0][0]
        
        if self.board[0][2] != "" and all(self.board[i][2 - i] == self.board[0][2] for i in range(3)):
            self.draw_winning_line("diagonal", 1)
            return self.board[0][2]
        
        return None

    def check_winner_board(self, board):
        """Check for winner on a given board state (for minimax)"""
        # Check rows
        for i in range(3):
            if board[i][0] != "" and all(board[i][j] == board[i][0] for j in range(3)):
                return board[i][0]
        
        # Check columns
        for j in range(3):
            if board[0][j] != "" and all(board[i][j] == board[0][j] for i in range(3)):
                return board[0][j]
        
        # Check diagonals
        if board[0][0] != "" and all(board[i][i] == board[0][0] for i in range(3)):
            return board[0][0]
        
        if board[0][2] != "" and all(board[i][2 - i] == board[0][2] for i in range(3)):
            return board[0][2]
        
        return None

    def toggle_mode(self):
        self.vs_computer = not self.vs_computer
        mode = "1️⃣-Player" if self.vs_computer else "2️⃣-Player"
        self.mode_btn.configure(text=f"🔄 Switch to {'2' if self.vs_computer else '1'}-Player Mode")
        player_text = f"{self.player_names['X']}'s Turn ❌" if self.current_player == "X" else f"{self.player_names['O']}'s Turn ⭕"
        self.label.configure(text=f"{mode} Mode - {player_text}")
        self.reset_game()

    def toggle_difficulty(self):
        self.difficulty = "Hard 🔥" if self.difficulty == "Easy ⚡" else "Easy ⚡"
        self.difficulty_btn.configure(text=f"⚡ Difficulty: {self.difficulty}")

    def change_names(self):
        name_x = simpledialog.askstring("Player Name", "Enter name for Player ❌:")
        name_o = simpledialog.askstring("Player Name", "Enter name for Player ⭕:")
        if name_x:
            self.player_names["X"] = name_x
        if name_o:
            self.player_names["O"] = name_o
        player_text = f"{self.player_names[self.current_player]}'s Turn ❌" if self.current_player == "X" else f"{self.player_names[self.current_player]}'s Turn ⭕"
        self.label.configure(text=player_text)

    def on_click(self, row, col):
        if self.buttons[row][col].cget("text") == "" and self.check_winner() is None:
            symbol = "❌" if self.current_player == "X" else "⭕"
            self.buttons[row][col].configure(text=symbol, 
                                           text_color=self.colors["X"] if self.current_player == "X" else self.colors["O"])
            self.board[row][col] = self.current_player

            winner = self.check_winner()
            if winner:
                win_symbol = "❌" if winner == "X" else "⭕"
                messagebox.showinfo("Game Over", f"{self.player_names[winner]} {win_symbol} wins! 🎉")
                self.label.configure(text=f"{self.player_names[winner]} Wins! {win_symbol}")
                self.scores[winner] += 1
                self.score_label.configure(text=self.get_score_text())
                return
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw! 🤝")
                self.label.configure(text="It's a Draw! 🤝")
                self.scores["Draw"] += 1
                self.score_label.configure(text=self.get_score_text())
                return

            self.current_player = "O" if self.current_player == "X" else "X"
            player_text = f"{self.player_names[self.current_player]}'s Turn ❌" if self.current_player == "X" else f"{self.player_names[self.current_player]}'s Turn ⭕"
            self.label.configure(text=player_text,
                               text_color=self.colors["X"] if self.current_player == "X" else self.colors["O"])

            if self.vs_computer and self.current_player == "O":
                self.after(300, self.computer_move)

    def computer_move(self):
        if self.difficulty.startswith("Easy"):
            empty = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ""]
            if empty:
                r, c = random.choice(empty)
                self.on_click(r, c)
        else:
            _, move = self.minimax(self.board, "O")
            if move:
                self.on_click(*move)

    def minimax(self, board, player):
        opponent = "X" if player == "O" else "O"
        winner = self.check_winner_board(board)
        if winner == "O":
            return 1, None
        elif winner == "X":
            return -1, None
        elif all(cell != "" for row in board for cell in row):
            return 0, None

        moves = []
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = player
                    score, _ = self.minimax(board, opponent)
                    board[r][c] = ""
                    moves.append((score * (-1), (r, c)))

        best_move = max(moves, key=lambda x: x[0]) if player == "O" else min(moves, key=lambda x: x[0])
        return best_move

    def is_draw(self):
        return all(self.board[r][c] != "" for r in range(3) for c in range(3)) and self.check_winner() is None

    def reset_game(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for row in self.buttons:
            for btn in row:
                btn.configure(text="")
        self.current_player = "X"
        mode = "1️⃣-Player" if self.vs_computer else "2️⃣-Player"
        player_text = f"{self.player_names['X']}'s Turn ❌"
        self.label.configure(text=f"{mode} Mode - {player_text}",
                           text_color=self.colors["X"])
        # Clear any winning line
        self.canvas.delete("all")
        self.winning_line = None

    def cancel_game(self):
        if messagebox.askyesno("Cancel Game", "Are you sure you want to cancel this game? ❌"):
            self.reset_game()

    def get_score_text(self):
        return f"❌ {self.player_names['X']}: {self.scores['X']} | ⭕ {self.player_names['O']}: {self.scores['O']} | 🤝 Draws: {self.scores['Draw']}"


if __name__ == "__main__":
    app = TicTacToe()
    app.mainloop()
