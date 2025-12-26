import tkinter as tk
from tkinter import messagebox, font
import random

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Судоку")
        self.root.geometry("550x650")
        self.root.configure(bg='#f0f0f0')

        # Шрифты
        self.big_font = font.Font(family='Arial', size=20, weight='bold')
        self.small_font = font.Font(family='Arial', size=12)

        # Игровые данные
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = [[0 for _ in range(9)] for _ in range(9)]
        self.cells = [[None for _ in range(9)] for _ in range(9)]

        self.setup_ui()
        self.generate_new_game()

    def setup_ui(self):
        #Интерфейса
        # Заголовок
        title = tk.Label(self.root, text="СУДОКУ",
                         font=('Arial', 28, 'bold'),
                         bg='#f0f0f0', fg='#2c3e50')
        title.pack(pady=10)

        # Фрейм для игрового поля
        board_frame = tk.Frame(self.root, bg='black', padx=2, pady=2)
        board_frame.pack(pady=10)

        # Ячейки
        for row in range(9):
            for col in range(9):
                # Цвет фона для блоков 3x3
                bg_color = '#ffffff'
                if (row // 3 + col // 3) % 2 == 0:
                    bg_color = '#f8f9fa'

                # Entry (поле ввода)
                cell = tk.Entry(board_frame, width=2, font=self.big_font,
                                justify='center', bg=bg_color,
                                relief='solid', borderwidth=1)

                # Ввод
                cell.config(validate="key",
                            validatecommand=(self.root.register(self.validate_input), '%P'))

                cell.grid(row=row, column=col, padx=(1, 1), pady=(1, 1))
                self.cells[row][col] = cell

                # Жирные границы для блоков 3x3
                if col % 3 == 0:
                    cell.grid(padx=(3, 1))
                if row % 3 == 0:
                    cell.grid(pady=(3, 1))

        # Фрейм для кнопок
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)

        # Кнопки
        buttons = [
            ("Новая игра", self.generate_new_game, '#3498db'),
            ("Проверить", self.check_solution, '#2ecc71'),
            ("Решить", self.solve_game, '#e74c3c'),
            ("Очистить", self.clear_board, '#f39c12')
        ]

        for text, command, color in buttons:
            btn = tk.Button(button_frame, text=text, font=self.small_font,
                            command=command, bg=color, fg='white',
                            padx=15, pady=8, relief='raised', borderwidth=2)
            btn.pack(side='left', padx=5)

        # Статус
        self.status = tk.Label(self.root, text="Заполните все ячейки цифрами 1-9",
                               font=self.small_font, bg='#f0f0f0', fg='#34495e')
        self.status.pack(pady=10)

        # Подсказка
        hint = tk.Label(self.root,
                        text="Правила: каждая строка, столбец и блок 3x3 должны содержать цифры 1-9 без повторений",
                        font=('Arial', 10), bg='#f0f0f0', fg='#7f8c8d')
        hint.pack(pady=5)

    def validate_input(self, text):
        # Валидация ввода - только цифры 1-9
        if text == "":
            return True
        if len(text) > 1:
            return False
        return text.isdigit() and text != '0'

    def generate_new_game(self):
        # Новая игра
        # Полная доска
        self.generate_full_board()
        self.solution = [row[:] for row in self.board]

        # Удалить часть цифр
        to_remove = 40
        removed = 0

        while removed < to_remove:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.board[row][col] != 0:
                backup = self.board[row][col]
                self.board[row][col] = 0

                # Копировать доску для проверки уникальности решения
                temp_board = [r[:] for r in self.board]
                if self.count_solutions(temp_board) == 1:
                    removed += 1
                else:
                    self.board[row][col] = backup

        # Обновить интерфейс
        self.update_board()
        self.status.config(text="Новая игра! Удачи!", fg='#2c3e50')

    def generate_full_board(self):
        # Решенная доска
        self.board = [[0 for _ in range(9)] for _ in range(9)]

        # Заполнить диагональные блоки
        for i in range(0, 9, 3):
            numbers = list(range(1, 10))
            random.shuffle(numbers)
            for r in range(3):
                for c in range(3):
                    self.board[i + r][i + c] = numbers.pop()

        # Решить остальное
        self.solve(self.board)

    def solve(self, board):
        # Решение судоку
        empty = self.find_empty(board)
        if not empty:
            return True

        row, col = empty

        for num in range(1, 10):
            if self.is_valid(board, num, (row, col)):
                board[row][col] = num
                if self.solve(board):
                    return True
                board[row][col] = 0

        return False

    def find_empty(self, board):
        # Поиск пустой ячейки
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, board, num, pos):
        # Проверка числа
        row, col = pos

        # Проверка строки
        for j in range(9):
            if board[row][j] == num and j != col:
                return False

        # Проверка столбца
        for i in range(9):
            if board[i][col] == num and i != row:
                return False

        # Проверка блока 3x3
        box_x = col // 3
        box_y = row // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def count_solutions(self, board, count=0):
        # Кол-во решений
        empty = self.find_empty(board)
        if not empty:
            return count + 1

        row, col = empty
        total = 0

        for num in range(1, 10):
            if self.is_valid(board, num, (row, col)):
                board[row][col] = num
                total = self.count_solutions(board, count)
                if total > 1:
                    return total
                board[row][col] = 0

        return total

    def update_board(self):
        # Обновление интерфейса доски
        for row in range(9):
            for col in range(9):
                cell = self.cells[row][col]
                value = self.board[row][col]

                cell.delete(0, 'end')
                if value != 0:
                    cell.insert(0, str(value))
                    cell.config(fg='blue', state='readonly')
                else:
                    cell.config(fg='black', state='normal')

    def get_current_board(self):
        # Получение текущего состояния из интерфейса
        current = [[0 for _ in range(9)] for _ in range(9)]

        for row in range(9):
            for col in range(9):
                text = self.cells[row][col].get()
                if text.isdigit():
                    current[row][col] = int(text)

        return current

    def check_solution(self):
        # Проверка решения
        current = self.get_current_board()

        # Проверка заполненности
        for row in range(9):
            for col in range(9):
                if current[row][col] == 0:
                    self.status.config(text="Не все ячейки заполнены!", fg='#e74c3c')
                    return

        # Проверка правильности
        for row in range(9):
            for col in range(9):
                if current[row][col] != self.solution[row][col]:
                    self.status.config(text="Есть ошибки! Попробуйте еще раз.", fg='#e74c3c')
                    # Подсветка ошибки
                    self.cells[row][col].config(bg='#ffcccc')
                    return
                else:
                    self.cells[row][col].config(bg='#ffffff')

        # Всё правильно
        self.status.config(text="Поздравляем! Вы решили судоку правильно!", fg='#27ae60')
        for row in range(9):
            for col in range(9):
                self.cells[row][col].config(bg='#ccffcc')

    def solve_game(self):
        # Автоматическое решение
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    self.cells[row][col].delete(0, 'end')
                    self.cells[row][col].insert(0, str(self.solution[row][col]))
                    self.cells[row][col].config(fg='green', bg='#ccffcc', state='readonly')

        self.status.config(text="Игра решена!", fg='#27ae60')

    def clear_board(self):
        # Очистка только пользовательских ячеек
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:  # Только пустые изначально
                    self.cells[row][col].delete(0, 'end')
                    self.cells[row][col].config(bg='#ffffff', fg='black', state='normal')

        self.status.config(text="Доска очищена. Начните заново!", fg='#f39c12')

def main():
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()