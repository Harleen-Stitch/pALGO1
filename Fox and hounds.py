class GameBoard:
    def board_size(self, n):
        """Fait en sorte que le nombre de lignes et de colonnes du plateau soit un multiple de 4 colonnes"""
        if n <= 0:
            n = 4
        elif n % 4 != 0:
            n = ((n // 4) + 1) * 4
        return n

    def __init__ (self, n):
        self.__n = self.board_size(n)
        self.__board = []
        for i in range(self.__n):
            row = []
            for j in range(self.__n):
                row.append(0)
            self.__board.append(row)

        hound = 1
        # Numérote les chiens et les place sur le plateau
        for j in range(self.__n):
            if j % 2 == 1:
                self.__board[0][j] = hound
                hound += 1
     
        fox = -1
        # Place le hound
        milieu = (self.__n // 2)
        self.__board[self.__n - 1][milieu] = fox

    def get_n(self):
        return self.__n
    
    def affichage(self):
        """Affiche le plateau et le met en forme"""
        for i in range(self.__n):
            print(f"{i+1:^3} |", end=" ")
            for j in range(self.__n):
                square = self.__board[i][j]
                if square == 0:
                    print(f"{'.':^3}", end=" | ")
                elif square == -1:
                    print(f"{'F':^3}", end=" | ")
                else:
                    print(f"{square:^3}", end=" | ")
            print()
            # Ligne de trait sous le plateau
        print((" "*5)+ "-" * (6 * self.__n+1))
        print((" "*4), end=" ")
        for i in range (1, self.__n+1):
            # Numérote les colonnes
            print(f'{i:^5}', end=" ")           
        print("\n")

    def get_square(self, row, column):
        return self.__board[row][column]

    def set_square(self, row, column, value):
        self.__board[row][column] = value

class Hound:
    def __init__ (self, row=0, column=0):
        self.__row = row
        self.__column = column
    
    def get_row(self):
        return self.__row

    def set_row(self, row):
        self.__row = row

    def get_column(self):
        return self.__column

    def set_column(self, column):
        self.__column = column

    def canMoveTo(self, board, destR, destC):
        """Retourne True si le pion peut se déplacer à la case (ligne, colonne)"""
       
        # Si le pion va sortir du plateau
        if destR < 0 or destR >= board.get_n() or destC < 0 or destC >= board.get_n():
            return False

        # Si la case est déjà prise
        if board.get_square(destR, destC) != 0:
            return False
        
        # Déplacement en diagonale
        if destR == self.get_row() + 1 and (destC == self.get_column() + 1 or destC == self.get_column() - 1):
            return True

        return False
        
    def canMove(self, board):
        """Retourne True si le pion peut se déplacer"""

        # Tester les 4 diagonales possibles
        if (
        self.canMoveTo(board, self.get_row() + 1, self.get_column() + 1) == True or 
        self.canMoveTo(board, self.get_row() + 1, self.get_column() - 1) == True or 
        self.canMoveTo(board, self.get_row() - 1, self.get_column() + 1) == True or 
        self.canMoveTo(board, self.get_row() - 1, self.get_column() - 1) == True
        ):
            return True

        return False
        
    def move(self, board):
        """Demande les coordonnées de la case de destination du pion sélectionné"""
        # Boucle jusqu'à la saisie de coordonnées valides
        while True:
            # Prend en compte les fautes de frappe
            try:
                destR = int(input("Which row? "))
                destC = int(input("Which column? "))
            except ValueError:
                print("Enter a number")
                # Permet de revenir dans la boucle en cas d'erreur
                continue
            destR -=1
            destC -=1
            # Toujours dans la boucle
            # Vérifie si le mouvement est faisable
            if not self.canMoveTo(board, destR, destC):
                print("Impossible!")
            else:
                # S'il est faisable, retourne la destination et ainsi sort de la boucle
                return destR, destC

class Fox(Hound):
    """Classe fille de Hound = hérite des attributs de Hounds"""
    def __init__(self, row, column):
        super().__init__(row, column)

    def canMoveTo(self, board, destR, destC):

        # Si le pion va sortir du plateau
        if destR < 0 or destR >= board.get_n() or destC < 0 or destC >= board.get_n():
            return False

        # Si la case est déjà prise
        if board.get_square(destR, destC) != 0:
            return False
        
        # Déplacement en diagonale
        if ( 
            ((destR == self.get_row() + 1) or (destR == self.get_row() - 1)) and
            ((destC == self.get_column() + 1 or destC == self.get_column() - 1))
        ):
            return True

        return False

    def win(self):
        # Si le pion est sur la première ligne
        row = self.get_row()
        if row == 0:
            return True
        return False    

class FoxAndHounds:
    def __init__(self, n):
        self.__board = GameBoard(n)
        self.__n = self.__board.get_n()
        self.__fox = Fox(self.__n - 1, self.__n // 2)
        self.__hounds = []
        for j in range(self.__n):
            if j % 2 == 1:
                self.__hounds.append(Hound(0, j))

        self.__fox_turn = True  # Fox commence

    def play(self):
        while True:
            # Afficher le plateau
            self.__board.affichage()

            # Si le fox a gagné
            if self.__fox.win():
                print("Fox wins")
                break

            # Si les Hounds ont gagné
            if self.__fox.canMove(self.__board) == False:
                print("Hounds win")
                break

            # Si c'est le tour du fox
            if self.__fox_turn:
                print("Fox to move: ")
                destR, destC = self.__fox.move(self.__board)
                self.__board.set_square(self.__fox.get_row(), self.__fox.get_column(), 0)
                self.__board.set_square(destR, destC, -1)
                self.__fox.set_row(destR)
                self.__fox.set_column(destC)

            # Si c'est le tour des hounds
            else:
                print("Hound to move: ")

                while True:
                    try:
                        num = int(input("Choose a hound: "))
                    except ValueError:
                        print("Enter a number")
                        continue

                    if num < 1 or num > len(self.__hounds):
                        print("Choose a valid hound!")
                        continue

                    hound = self.__hounds[num - 1]

                    if hound.canMove(self.__board) == False:
                        print(f"Hound n°{num} can't move! Choose another hound !")
                        continue
                    break

                print(f' Hound n° {num} to move: ')

                destR, destC = hound.move(self.__board)
                self.__board.set_square(hound.get_row(), hound.get_column(), 0)
                self.__board.set_square(destR, destC, num)
                hound.set_row(destR)
                hound.set_column(destC)

            # On change de joueur
            self.__fox_turn = not self.__fox_turn

##### LANCEMENT DU JEU #####
n = int(input("Select a size for the board: "))
game = FoxAndHounds(n)
game.play()