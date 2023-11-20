import os

class Game():
    def __init__(self,num_disc):
        self.num_disc = num_disc # number of disks user selected 3-8
        self.moves = 0             # Count number of moves taken
        self.min_moves = 2**num_disc - 1    # minimum moves for perfect game
        self.win = [i+1 for i in range(num_disc)]   # what tower 3 needs to equal to win 
        self.tower1 = [i+1 for i in range(num_disc)] # tower 1 starts with all disks
        self.tower2 = [0 for i in range(num_disc)] # empty slot represented with 0
        self.tower3 = [0 for i in range(num_disc)] # empty slot represented with 0
        self.towers = [self.tower1,self.tower2,self.tower3] # array holding all three towers
        self.display() #initial display

    def display(self): # to print game state
        os.system('printf "\033c"') #clear terminal screen
        print('|','|','|') # show tips of towers
        for c in range(self.num_disc):
            print(self.towers[0][c] if self.towers[0][c] != 0 else '|', # print towers
                  self.towers[1][c] if self.towers[1][c] != 0 else '|', # '|' where 0s are
                  self.towers[2][c] if self.towers[2][c] != 0 else '|')
        print(f"Moves: {self.moves}") #print current move counter

    def prompt_move(self): # get user input to make a move
        move_from = input("Enter tower to move disk from (1,2,3): ") #select disc from tower 1, 2, or 3
        while(move_from != '1' and move_from != '2' and move_from != '3'):
            move_from = input("Input must be between 1, 2, or 3: ")
        move_from = int(move_from)

        move_to = input("Enter tower to move disk to (1,2,3): ") #move disc to tower 1, 2, or 3
        while(move_to != '1' and move_to != '2' and move_to != '3'):
            move_to = input("Input must be between 1, 2, or 3: ")
        move_to = int(move_to)

        if self.valid_move(move_from,move_to): #if valid move, make the move
            self.moves += 1 #increase counter
            self.display() #update display

    def valid_move(self,move_from,move_to): #makes the disc switch
        if move_from == move_to: #if selected same tower twice
            print("Doesn't count as move")
            return False
        no_zeros_from = [num for num in self.towers[move_from-1] if num != 0] #make new list with 0s ommitted
        no_zeros_to = [num for num in self.towers[move_to-1] if num != 0] #make new list with 0s ommitted
        if no_zeros_from == []: #check if selecting empty tower
            print("That tower has no disks to move")
            return False
        from_top = min(no_zeros_from) #moving disc that's the minimum in the list with no 0s
        to_top = min(no_zeros_to) if no_zeros_to != [] else self.num_disc + 1 #top of tower disc is being moved to
                                                        #if tower empty, say it's num_disc + 1 so anything could be moved there
        if from_top >= to_top: #prevent larger disc over smaller disc
            print("Can't move larger disk onto smaller disk")
            return False
        empty_slot = self.num_disc - self.towers[move_to-1][::-1].index(0) - 1 #find index of last 0
        self.towers[move_to-1][empty_slot] = from_top #transfer disc
        top_index = self.towers[move_from-1].index(from_top) 
        self.towers[move_from-1][top_index] = 0 # leave 0 behind
        return True

def main():
    print("Welcome to Towers of Hanoi!")
    num_disc = input("Enter how many discs you would like to play with (3-8): ") #get number of disks to play with
    while(num_disc != '3' and num_disc != '4' and num_disc != '5' and num_disc != '6' and num_disc != '7' and num_disc != '8'): #really could be bigger than 6
        num_disc = input("Input must be between 3 and 8: ")
    num_disc = int(num_disc)
    game = Game(num_disc) #instantiate new game from Game class
    while (game.towers[2] != game.win): #keep playing until tower 3 is full
        game.prompt_move() 
    print("You win!")
    if(game.moves == game.min_moves):
        print("Perfect Game")

if __name__ == "__main__":
    main()