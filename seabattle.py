import random

class Ship:
    def __init__(self, bow, length, orientation):
        self.bow = bow  # Кортеж (x, y)
        self.length = length
        self.orientation = orientation  # 'H' - горизонтально, 'V' - вертикально
        self.hits = [False] * length

    def get_coords(self):
        coords = []
        for i in range(self.length):
            x, y = self.bow
            if self.orientation == 'H':
                coords.append((x, y + i))
            else:
                coords.append((x + i, y))
        return coords

    def is_hit(self, shot):
        if shot in self.get_coords():
            index = self.get_coords().index(shot)
            self.hits[index] = True
            return True
        return False

    def is_sunk(self):
        return all(self.hits)

class Board:
    def __init__(self, size=6):
        self.size = size
        self.grid = [['O'] * size for _ in range(size)]
        self.ships = []
        self.shots = set()

    def place_ship(self, ship):
        for x, y in ship.get_coords():
            if not (0 <= x < self.size and 0 <= y < self.size):
                raise ValueError("Корабль выходит за пределы доски")
            if self.grid[x][y] != 'O':
                raise ValueError("Клетка занята")
        for x, y in ship.get_coords():
            self.grid[x][y] = '■'
        self.ships.append(ship)

    def is_valid_position(self, ship):
        for x, y in ship.get_coords():
            if not (0 <= x < self.size and 0 <= y < self.size):
                return False
            if self.grid[x][y] != 'O':
                return False
        return True

    def add_ship(self, length):
        placed = False
        while not placed:
            bow = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            orientation = random.choice(['H', 'V'])
            ship = Ship(bow, length, orientation)
            if self.is_valid_position(ship):
                self.place_ship(ship)
                placed = True

    def receive_shot(self, shot):
        if shot in self.shots:
            raise ValueError("В эту клетку уже стреляли")
        self.shots.add(shot)
        for ship in self.ships:
            if ship.is_hit(shot):
                self.grid[shot[0]][shot[1]] = 'X'
                if ship.is_sunk():
                    print("Корабль потоплен!")
                return True
        self.grid[shot[0]][shot[1]] = 'T'
        return False

    def display(self, hide_ships=False):
        print("  | " + " | ".join(map(str, range(1, self.size + 1))) + " |")
        for i in range(self.size):
            row = [self.grid[i][j] if not hide_ships or self.grid[i][j] not in ['■'] else 'O' for j in range(self.size)]
            print(f"{i + 1} | " + " | ".join(row) + " |")

class Game:
    def __init__(self):
        self.player_board = Board()
        self.computer_board = Board()
        self.setup_boards()

    def setup_boards(self):
        for _ in range(1):
            self.player_board.add_ship(3)
            self.computer_board.add_ship(3)
        for _ in range(2):
            self.player_board.add_ship(2)
            self.computer_board.add_ship(2)
        for _ in range(4):
            self.player_board.add_ship(1)
            self.computer_board.add_ship(1)

    def player_turn(self):
        while True:
            try:
                shot = tuple(map(int, input("Введите координаты выстрела (например, 1 2): ").split()))
                shot = (shot[0] - 1, shot[1] - 1)
                if self.computer_board.receive_shot(shot):
                    print("Попадание!")
                else:
                    print("Промах!")
                break
            except ValueError as e:
                print(e)

    def computer_turn(self):
        while True:
            shot = (random.randint(0, 5), random.randint(0, 5))
            try:
                if self.player_board.receive_shot(shot):
                    print(f"Компьютер попал в {shot[0] + 1} {shot[1] + 1}!")
                else:
                    print(f"Компьютер промахнулся в {shot[0] + 1} {shot[1] + 1}.")
                break
            except ValueError:
                continue

    def play(self):
        print("Начало игры Морской бой!")
        while True:
            print("\nВаше поле:")
            self.player_board.display()
            print("\nПоле компьютера:")
            self.computer_board.display(hide_ships=True)

            self.player_turn()
            if all(ship.is_sunk() for ship in self.computer_board.ships):
                print("Вы победили!")
                break

            self.computer_turn()
            if all(ship.is_sunk() for ship in self.player_board.ships):
                print("Компьютер победил!")
                break

if __name__ == "__main__":
    game = Game()
    game.play()