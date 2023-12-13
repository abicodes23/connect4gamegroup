import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring

class Connect4Game:
    def __init__(self, master):
        self.master = master
        self.master.title("SoftwareDev1, Rion, Asim, Abi, Wayne, Bernice")
        self.master.geometry("500x450")
        self.board = [[0] * 7 for _ in range(6)]  # Initialize a 6x7 grid
        self.current_player = 1
        self.light_mode = True

        # Ask players for their names
        self.player1_name = askstring("Player 1", "Enter Player 1's name:")
        self.player2_name = askstring("Player 2", "Enter Player 2's name:")

        # Create buttons for each column
        self.buttons = []
        for col in range(7):
            button = tk.Button(master, text=str(col + 1), command=lambda c=col: self.drop_piece(c))
            button.grid(row=0, column=col)
            self.buttons.append(button)

        # Create the game board
        self.canvas = tk.Canvas(master, width=400, height=350, bg='white' if self.light_mode else 'black')
        self.canvas.grid(row=1, column=0, columnspan=7, padx=10, pady=10)

        # Create light mode toggle button
        self.light_mode_button = tk.Button(master, text="Toggle Light Mode", command=self.toggle_light_mode)
        self.light_mode_button.grid(row=2, column=0, columnspan=7, pady=5)

    def toggle_light_mode(self):
        self.light_mode = not self.light_mode
        self.canvas.configure(bg='white' if self.light_mode else 'black')
        self.draw_board()

    def drop_piece(self, column):
        row = self.get_next_open_row(column)
        if row is not None:
            self.board[row][column] = self.current_player
            self.draw_board()
            if self.check_winner(row, column):
                winner_name = self.player1_name if self.current_player == 1 else self.player2_name
                messagebox.showinfo("Connect 4", f"{winner_name} wins!")
                self.reset_game()
            elif self.is_board_full():
                messagebox.showinfo("Connect 4", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = 3 - self.current_player  # Switch player

    def get_next_open_row(self, column):
        for row in range(5, -1, -1):
            if self.board[row][column] == 0:
                return row
        return None

    def draw_board(self):
        self.canvas.delete("all")  # Clear the canvas

        # Draw the grid
        for row in range(6):
            for col in range(7):
                x1, y1 = col * 50, row * 50
                x2, y2 = x1 + 50, y1 + 50
                self.canvas.create_rectangle(x1, y1, x2, y2, outline='black')

                if self.board[row][col] == 1:
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill='red')
                elif self.board[row][col] == 2:
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill='yellow')

    def check_winner(self, row, col):
        # Check horizontally
        if self.check_line(row, col, 0, 1):
            return True
        # Check vertically
        if self.check_line(row, col, 1, 0):
            return True
        # Check diagonally (positive slope)
        if self.check_line(row, col, 1, 1):
            return True
        # Check diagonally (negative slope)
        if self.check_line(row, col, -1, 1):
            return True
        return False

    def check_line(self, row, col, row_delta, col_delta):
        player = self.board[row][col]
        count = 1
        for i in range(1, 4):
            r = row + i * row_delta
            c = col + i * col_delta
            if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == player:
                count += 1
            else:
                break
        for i in range(1, 4):
            r = row - i * row_delta
            c = col - i * col_delta
            if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == player:
                count += 1
            else:
                break
        return count >= 4

    def is_board_full(self):
        return all(cell != 0 for row in self.board for cell in row)

    def reset_game(self):
        self.board = [[0] * 7 for _ in range(6)]
        self.current_player = 1
        self.draw_board()

if __name__ == "__main__":
    root = tk.Tk()
    connect4_game = Connect4Game(root)
    root.mainloop()
