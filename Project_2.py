# Student name: Sergei Panarin
# Student number: 281652

"""
This program is meant to run a simple game: a derivative of a simple minesweeper game. The rules might seem rather
complex, so instead of rewriting them here, a special option was added to the menu where all the rules are listed
with respective subtopics. The basic version is such that the user has to look for a treasure island on a board
of 20x20 cells. In each cell there might also be an enemy ship, which then will try to gun the user down
(similarly to mines in minesweeper).
But instead of loosing immediately, the user (if successful) will continue playing. There are 3 escapes attempts
which the user can use to escape their enemies. Once the user loses a battle, they lose the entire game. If the user
finds the island - they win the game.
For convenience, the game was converged into a class.

WARNING!!! DO NOT USE HEADPHONES WHILE RUNNING THE GAME. ALSO LOWER THE SOUND ON YOUR COMPUTER.

The reason for that is that files have different sound levels and some of them are somewhat loud. The user may,
of course, not do that, just let them be warned first.

"""

from tkinter import *
import random
from winsound import *
from tkinter import messagebox
from tkinter import simpledialog


class Game:
    """ This class creates a game object that allows user to play it.

    IT describes all the game's instances.
    """

    def __init__(self):
        """
        Constructor for the Game class.

        The constructor has different static attributes that indicate certain parts of the board and the map with ships
        and treasure on it. It also creates the main tk instance, the canvas for it, starts the mainloop and sets all
        needed attributes to their initial values.
        It has no input parameters.
        :param:
        """
        self.__main_window = Tk()
        self.__main_window.title("Treasure Hunt V 1.0")
        self.__rows = 20
        self.__columns = 20
        self.__ships = 40
        self.__buttons = []
        self.__canvas = Canvas()
        self.__sea_map = []
        self.__number_of_played_games = 0
        self.__your_ship = "Frigate"
        self.__enemy_ship = ""
        self.__enemy_ships = ["Schooner", "Brig", "Frigate"]
        self.__state_of_the_game = 0
        self.__escape_attempts = 3

        self.start()
        self.__main_window.mainloop()

    def start(self):
        """Starts the menu.

        """
        self.menu()

    def menu(self):
        """The method is responsible for the main menu of the game.

        It is the very first state of the game in which you have options to start a new game, a custom game,
        read rules or quit.
        It uses a Canvas as a background image and operates with it, creating buttons, etc.
        It has no return value.
        :return:
        """
        self.__state_of_the_game = 1
        self.play_music(self.__state_of_the_game)

        self.__canvas = Canvas(self.__main_window, width=1024, height=768)
        self.__canvas.grid()

        image = PhotoImage(file="TH.png")
        self.__canvas.image = image

        self.__canvas.create_image(512, 384, image=image)

        quit_button = Button(self.__main_window, text="Quit", command=self.__main_window.quit, width=20)
        rules_button = Button(self.__main_window, text="Rules", command=self.rules, width=20)
        new_game_button = Button(self.__main_window, text="New game", command=self.new_game, width=20)
        custom_game_button = Button(self.__main_window, text="Custom difficulty", command=self.custom, width=20)

        self.__canvas.create_window(70, 550, anchor='nw', window=new_game_button)
        self.__canvas.create_window(70, 650, anchor='nw', window=rules_button)
        self.__canvas.create_window(70, 700, anchor='nw', window=quit_button)
        self.__canvas.create_window(70, 600, anchor='nw', window=custom_game_button)

    def play_music(self, state):
        """This method plays the soundtrack depending on the state of the game.

        There are separate soundtracks for the menu, game ready, battle sequence and endgame states.
        Note: the soundtrack for the battle sequence is randomized and be either one of these 2.
        It has one parameter and return different playing commands.
        :param state: State of the game, which defines what music to play.
        :return: PlaySound commands
        """
        if state == 1:
            return PlaySound('Sound0.wav', SND_FILENAME | SND_LOOP | SND_ASYNC)

        elif state == 2:
            return PlaySound('Sound1.wav', SND_FILENAME | SND_LOOP | SND_ASYNC)

        elif state == 3:
            music = random.randint(1, 2)

            if music == 1:
                return PlaySound('Sound2.wav', SND_FILENAME | SND_LOOP | SND_ASYNC)

            else:
                return PlaySound('Sound3.wav', SND_FILENAME | SND_LOOP | SND_ASYNC)

        elif state == 4:
            return PlaySound('Sound.wav', SND_FILENAME)

    def new_game(self):
        """This method starts the new game sequence which sets the board anew and all values in it.

        It puts the game in the state 2 (the game ready state), plays the soundtrack and sets the amount of escape
        attempts to the starting value of 3.
        If the number of played games is more than 1, then it resets all the values and creates the board anew.
        It has no return value.
        :return:
        """
        self.__state_of_the_game = 2
        self.play_music(self.__state_of_the_game)
        self.__number_of_played_games += 1
        self.__escape_attempts = 3

        if self.__number_of_played_games >= 2:
            self.board()
            self.info_board()
            self.restore_values()
            self.set_map()

        else:
            self.board()
            self.info_board()
            self.set_map()

    def restore_values(self):
        """This method simply restores all the values in order for the new gane to begin.

        No return value.
        :return:
        """
        for coor_x in range(0, self.__rows):

            for coor_y in range(0, self.__columns):
                self.__sea_map[coor_x][coor_y] = 0


    def board(self):
        """This method creates the board with buttons on the canvas.

        All the buttons are stored in a list and processed so they appear on the canvas in the right order.
        X and Y simply indicate the coordinates of a button. They will also be used later in the program.

        :return:
        """
        title = Label(self.__main_window, text="Sea map")
        self.__canvas.create_window(700, 100, anchor='nw', window=title)

        self.__buttons = []

        for x in range(0, self.__rows):
            self.__buttons.append([])

            for y in range(0, self.__columns):
                button = Button(self.__main_window, text=" ", width=2,
                                bg="blue", command=lambda x=x, y=y: self.push(x, y))

                self.__canvas.create_window(500+20*x, 150+20*y, anchor='nw', window=button)
                self.__buttons[x].append(button)

    def set_map(self):
        """This method sets the map and the values for each of the cells on the board.

        It firstly creates the map for the board judging by the numbers of rows and columns. It's 400.
        It then proceeds to create random ships on the map and assigns +1 values to all neighbouring cells.
        After that the random treasure island is created, and all neighbouring cells get a +2 value.
        The generated map is used when the player uses the buttons on board. A certain pair of coordinates on the map
        refers to a certain button on the board. After the button is clicked, it reveals the value that is on the cell
        with the same coordinates on the map.
        Special variables coor_x and coor_y are used in order to distinguish them from generated x and y coordinates.
        No return value.
        :return:
        """
        for coor_x in range(0, self.__rows):    # add cells for each button
            self.__sea_map.append([])

            for coor_y in range(0, self.__columns):
                self.__sea_map[coor_x].append(0)

        for cells in range(0, self.__ships):    # generate ships
            x = random.randint(0, self.__rows - 1)
            y = random.randint(0, self.__columns - 1)

            while self.__sea_map[x][y] == -1:   # prevent spawning ships on top of each other
                x = random.randint(0, self.__rows - 1)
                y = random.randint(0, self.__columns - 1)

            self.__sea_map[x][y] = -1

            if x != 0:  # A rather tidious process to get all the neighbouring cells their values.
                if y != 0 and self.__sea_map[x - 1][y - 1] != -1:
                    self.__sea_map[x - 1][y - 1] = int(self.__sea_map[x - 1][y - 1]) + 1
                # Corner cells create problems.

                if self.__sea_map[x - 1][y] != -1:
                    self.__sea_map[x - 1][y] = int(self.__sea_map[x - 1][y]) + 1

                if y != self.__columns - 1 and self.__sea_map[x - 1][y + 1] != -1:
                        self.__sea_map[x - 1][y + 1] = int(self.__sea_map[x - 1][y + 1]) + 1

            if y != 0:
                if self.__sea_map[x][y - 1] != -1:
                    self.__sea_map[x][y - 1] = int(self.__sea_map[x][y - 1]) + 1

            if y != self.__columns - 1:
                if self.__sea_map[x][y + 1] != -1:
                    self.__sea_map[x][y + 1] = int(self.__sea_map[x][y + 1]) + 1

            if x != self.__rows - 1:
                if y != 0 and self.__sea_map[x + 1][y - 1] != -1:
                        self.__sea_map[x + 1][y - 1] = int(self.__sea_map[x + 1][y - 1]) + 1

                if self.__sea_map[x + 1][y] != -1:
                    self.__sea_map[x + 1][y] = int(self.__sea_map[x + 1][y]) + 1

                if y != self.__columns - 1 and self.__sea_map[x + 1][y + 1] != -1:
                        self.__sea_map[x + 1][y + 1] = int(self.__sea_map[x + 1][y + 1]) + 1

        treasure_x = random.randint(0, self.__rows - 1)        # generate treasure island
        treasure_y = random.randint(0, self.__columns - 1)

        while self.__sea_map[treasure_x][treasure_y] == -1:    # prevent spawning treasure on top of a ship
            treasure_x = random.randint(0, self.__rows - 1)
            treasure_y = random.randint(0, self.__columns - 1)

        self.__sea_map[treasure_x][treasure_y] = 10000         # a special value so it doesn't overlap with others

        if treasure_x != 0:                                    # same as for the ships determining values process
            if treasure_y != 0 and self.__sea_map[treasure_x - 1][treasure_y - 1] != -1:
                self.__sea_map[treasure_x - 1][treasure_y - 1] = int(self.__sea_map[treasure_x - 1][treasure_y - 1]) + 2

            if self.__sea_map[treasure_x - 1][treasure_y] != -1:
                self.__sea_map[treasure_x - 1][treasure_y] = int(self.__sea_map[treasure_x - 1][treasure_y]) + 2

            if treasure_y != self.__columns - 1 and self.__sea_map[treasure_x - 1][treasure_y + 1] != -1:
                self.__sea_map[treasure_x - 1][treasure_y + 1] = int(self.__sea_map[treasure_x - 1][treasure_y + 1]) + 2

        if treasure_y != 0:
            if self.__sea_map[treasure_x][treasure_y - 1] != -1:
                self.__sea_map[treasure_x][treasure_y - 1] = int(self.__sea_map[treasure_x][treasure_y - 1]) + 2

        if treasure_y != self.__columns - 1:
            if self.__sea_map[treasure_x][treasure_y + 1] != -1:
                self.__sea_map[treasure_x][treasure_y + 1] = int(self.__sea_map[treasure_x][treasure_y + 1]) + 2

        if treasure_x != self.__rows - 1:
            if treasure_y != 0 and self.__sea_map[treasure_x + 1][treasure_y - 1] != -1:
                self.__sea_map[treasure_x + 1][treasure_y - 1] = int(self.__sea_map[treasure_x + 1][treasure_y - 1]) + 2

            if self.__sea_map[treasure_x + 1][treasure_y] != -1:
                self.__sea_map[treasure_x + 1][treasure_y] = int(self.__sea_map[treasure_x + 1][treasure_y]) + 2

            if treasure_y != self.__columns - 1 and self.__sea_map[treasure_x + 1][treasure_y + 1] != -1:
                self.__sea_map[treasure_x + 1][treasure_y + 1] = int(self.__sea_map[treasure_x + 1][treasure_y + 1]) + 2

    def info_board(self):
        """This method simply creates a small info board on the canvas which states your ship and escape attempts left.
        No return value.
        :return:
        """
        escape = Label(self.__main_window, text="Escape attempts left: "+ str(self.__escape_attempts))
        your_ship = Label(self.__main_window, text= "Your ship: "+self.__your_ship)

        self.__canvas.create_window(50, 150, anchor='nw', window=escape)
        self.__canvas.create_window(50, 200, anchor='nw', window=your_ship)

    def push(self, x, y):
        """This method defines what happens when you push a button on the board.

        If the game in the special state 4 (the endgame), then it is no longer possible to access buttons on the board.
        In case there is an enemy ship, the game will stop and the battle sequence begin.
        In case there is the treasure island, the game will end and victory is achieved.
        If there is a value, simply open the cell and sink the button.
        In case it is empty, use the clear method on it.
        The method has 2 parameters and no return value.
        :param x: x-coordinate of the investigated button.
        :param y: y-coordinate of the investigated button.
        :return:
        """

        if self.__state_of_the_game == 4:
            return

        self.__buttons[x][y]["text"] = str(self.__sea_map[x][y])

        if self.__sea_map[x][y] == -1:
            self.__buttons[x][y]["text"] = "X"
            self.__buttons[x][y].configure(background='red')
            self.__state_of_the_game = 3
            self.battle_sequence()

        elif self.__sea_map[x][y] == 10000:
            self.__buttons[x][y]["text"] = "T"
            self.__buttons[x][y].configure(background='green')
            self.treasure_island_found()

        else:
            self.__buttons[x][y].configure(disabledforeground="white")

        if self.__sea_map[x][y] == 0:
            self.__buttons[x][y]["text"] = " "
            self.clear(x, y)

        self.__buttons[x][y]['state'] = 'disabled'
        self.__buttons[x][y].config(relief=SUNKEN)

    def clear(self, x, y):
        """This method defines how to clear the board so more than one cell is investigated.

        It opens all the cells with no values in them as well as all their neighbouring cells with values in them.
        It has 2 parameters and no return value.
        :param x: x-coordinate of the investigated cell.
        :param y: y-coordinate of the investigated cell.
        :return:
        """

        if self.__buttons[x][y]["state"] == "disabled":
            return

        if self.__sea_map[x][y] != 0:
            self.__buttons[x][y]["text"] = str(self.__sea_map[x][y])

        else:
            self.__buttons[x][y]["text"] = " "

        self.__buttons[x][y].configure(disabledforeground="white")
        self.__buttons[x][y].configure(relief=SUNKEN)
        self.__buttons[x][y]["state"] = "disabled"

        if self.__sea_map[x][y] == 0:
            if x != 0 and y != 0:
                self.clear(x-1, y-1)

            if x != 0:
                self.clear(x-1, y)

            if x != 0 and y != self.__columns - 1:
                self.clear(x-1, y+1)

            if y != 0:
                self.clear(x, y-1)

            if y != self.__columns - 1:
                self.clear(x, y+1)

            if x != self.__rows - 1 and y != 0:
                self.clear(x+1, y-1)

            if x != self.__rows - 1:
                self.clear(x+1, y)

            if x != self.__rows - 1 and y != self.__columns - 1:
                self.clear(x+1, y+1)

    def treasure_island_found(self):
        """This method is used to notify the player that they have won the game.

        A game goes into the special state in which you can no longer push buttons on the board and
        a victory notification appears. Also the victory sound is played.
        No return value.
        :return:
        """
        self.__state_of_the_game = 4
        self.play_music(self.__state_of_the_game)
        messagebox.showinfo("Congratulations!", "You have found the treasure island!")

    def custom(self):
        """This method asks the player if they want to create a custom game with a custom number of enemy ships.

        It creates a simple dialog box and asks the new amount. Only positive integers are allowed, in all other
        cases an Error is raised, new message box appears and the player has to either cancel or enter again.
        No return value.
        :return:
        """

        self.__ships = simpledialog.askinteger("Custom difficulty", "Enter amount of enemy ships")

        if self.__ships is None:    # Note: this is used so the cancel option doesn't raise an Error in the console.
            self.__ships = 40
            return

        else:
            while self.__ships > self.__columns*self.__rows:
                self.__ships = simpledialog.askinteger("Custom difficulty", "Max. amount of enemy ships for this board is: "
                                            + str(self.__columns*self.__rows - 1) + "\nEnter amount of ships")
            while self.__ships < 0:
                messagebox.showinfo("Error!", "The number has to be a positive integer!")
                self.__ships = simpledialog.askinteger("Custom difficulty", "Max. amount of enemy ships for this board is: "
                                                       + str(self.__columns * self.__rows - 1) + "\nEnter amount of ships")

        self.new_game()

    def rules(self):
        """This method creates a separate tk instance that simply contains the instructions on how to play the game.

        No return value.
        :return:
        """
        rules = Tk()
        rules.title("Instructions")

        quit = Button(rules, width=10, text="Thank you!", command=rules.destroy)

        Intro = Label(rules, text="You are Captain Roger the Riddle Solver."
                                   " A curious map has come into your possesion.\n"
                                  "It points to a location in the far seas and has a treasure island on it.\n"
                                  "You are a brave pirate, and thus, you gather your crew and set sails for the mysterious island.\n"
                                  "However, you are not alone. You are followed by the Royal Navy, led by Admiral Collingwood,\n"
                                  "your old nemesis. Will you be able to find the island or end up in a prison for your crimes?")

        basic=Label(rules, text="Basics")
        basic.config(font=("Courier", 24))

        Basic = Label(rules, text="This game is a derivative form a simple minesweeper game.\n "
                                  "You have to investigate cells in order to know their and their neighbours' contents.\n"
                                  "The board consists of 400 possible locations on which you can click.\n"
                                  "After clicking, the button will become inactive no matter the contents.")

        goal = Label(rules, text="Goal")
        goal.config(font=("Courier", 24))

        Goal = Label(rules, text="In this game you have to find a treasure island located somewhere on the map.\n"
                                 "Instead of mines here you will face enemy ships and encountering one\n "
                                 "does not mean certain defeat. Instead, you will battle and if you win,\n you may "
                                 "continue your search.")

        battle = Label(rules, text="Battles")
        battle.config(font=("Courier", 24))

        Battle = Label(rules, text="Facing a foe in battle is always risky. There are three types of enemy ships:\n"
                                   "Schooners, brigs and frigates. You always have about 82% chance of success against schooners,\n"
                                   "66% success against brigs and only 50% against frigates. However, you dont have to fight always.\n"
                                   "You have 3 escape attempts, which you can use to evade your enemies and continue playing.\n"
                                   "If you win a battle or escape, you continue playing, if not, you are captured and the game is over.")

        search = Label(rules, text="How to search")
        search.config(font=("Courier", 24))

        How_to_search = Label(rules, text="Like in a simple minesweeper, if you have an enemy ship at a certain location,\n"
                                          "then all neigbouring cells (all 8) will receive +1 to their value. Say, if a cell\n"
                                          "has 3 ships near it then the value is going to be 3, etc. The treasure island, however, is trickier.\n"
                                          "Instead of a +1, it gives +2 value, which means that all cells around it will have at least value 2.\n"
                                          "The point of the game is to figure out where the island is by comparing the numbers.\n"
                                          "There is always uncertainty in this, so fighting might be inevitable.")
        custom = Label(rules, text="Custom game")
        custom.config(font=("Courier", 24))

        Customize = Label(rules, text="You may also choose the amount of ships yourself by clicking the 'Custom difficulty' button in the menu")

        Intro.grid(row=0, column=0, sticky=E)
        Basic.grid(row=1, column=1)
        Goal.grid(row=2, column=2)
        Battle.grid(row=2, column=0)
        How_to_search.grid(row=3, column=1)
        Customize.grid(row=4, column=0)
        basic.grid(row=0, column=1)
        goal.grid(row=1, column=2)
        battle.grid(row=1, column=0)
        search.grid(row=2, column=1)
        custom.grid(row=3, column=0)
        quit.grid(row=5, column=1)

    def battle_sequence(self):
        """This method executes the battle sequence.

        It makes the game go into a special state when an enemy ship has been clicked on.
        New soundtrack is launched and, by drawing a random number, the enemy ship type is defined.
        It also asks the player if they want to launch the fight sequence or try to escape.
        If the number of escape attempts is 0, fighting is inevitable.

        :return:
        """
        self.__state_of_the_game = 3
        self.play_music(self.__state_of_the_game)
        r = random.randint(1, 6)
        if r < 4:
            self.__enemy_ship = self.__enemy_ships[0]

        elif 4 <= r <= 5:
            self.__enemy_ship = self.__enemy_ships[1]

        else:
            self.__enemy_ship = self.__enemy_ships[2]

        messagebox.showinfo("A confrontation!", "You have been attacked by a royal "+self.__enemy_ship)

        action = messagebox.askyesno("What do you do?", "Do you want to fight? (if not, then you will try to escape)")

        if action == True:
            self.fight()
        else:
            if self.__escape_attempts > 0:
                self.escape()
            else:
                messagebox.showinfo("No success", "You have to fight!")
                self.fight()

    def exit_battle_sequence(self):
        """This method returns the player back to the main board after the battle sequence ends.

        It renews the soundtrack and the escape attempts info label. The new label is needed so
        the user doesn't have to use the initial label as a parameter in several functions.
        No return value.
        :return:
        """
        self.__state_of_the_game = 2
        self.play_music(self.__state_of_the_game)

        escape = Label(self.__main_window, text="Escape attempts left: " + str(self.__escape_attempts))
        self.__canvas.create_window(50, 150, anchor='nw', window=escape)

    def fight(self):
        """This method executes the fighting sequence.

        It takes a random integer from 1 to 6 and compares it to the enemy ship type.
        Based on that the outcome of the battle is shown. Victory is achieved when the player
        rolls 1-5 for Schooners, 1-4 for Brigs and 1-3 for Frigates.
        No return value
        :return:
        """
        outcome = random.randint(1, 6)

        if self.__enemy_ship == self.__enemy_ships[0]:
            if outcome == 6:
                self.defeat()

            else:
                self.victory()

        elif self.__enemy_ship == self.__enemy_ships[1]:
            if outcome >= 5:
                self.defeat()

            else:
                self.victory()

        elif self.__enemy_ship == self.__enemy_ships[2]:
            if outcome >= 4:
                self.defeat()

            else:
                self.victory()

    def victory(self):
        """This method is used to announce victory in battle to the player.

        It plays a "victory" sound, shows victory window and makes the game unplayable.
        No return value.
        :return:
        """
        PlaySound('Sound.wav', SND_FILENAME)
        messagebox.showinfo("Hurray!", "You are victorious!")
        self.exit_battle_sequence()

    def defeat(self):
        """This method is used to announce defeat in battle to the player.

        It plays a "defeat" sound, shows defeat window and makes the game unplayable.
        No return value.
        :return:
        """
        PlaySound('Sound4.wav', SND_FILENAME)
        self.__state_of_the_game = 4
        messagebox.showinfo("Game over!", "You are defeated!")

    def escape(self):
        """ This method allows player to escape combat.

        It counts the remaining escape attempts and leaves the battle sequence.
        It has no return value.
        :return:
        """
        self.__escape_attempts -= 1

        if self.__escape_attempts < 0:
            self.__escape_attempts = 0
            
        self.exit_battle_sequence()



def main():
    """The main functions that boots the game.

    No return values.
    :return:
    """
    game = Game()
    game.start()


main()
