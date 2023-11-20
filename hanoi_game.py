from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, QTime
from time import sleep
import sys

class Disc(QLabel): #Disc class inherits from QLabel class but holds value
    def __init__(self, val,x,y,w,h,parent=None): 
        super().__init__(parent)
        self.val = val #initialize disc value
        self.setGeometry(x,y,w,h) #set xy coordinates and width and height
        self.setText(f"{self.val}") #put number on label
        self.setAlignment(Qt.AlignCenter) #Align Text in center
        self.setStyleSheet("background-color: blue") #color label blue
    
    def __str__(self): # to print dics, used for debugging
        return str(self.val)
    
    def __lt__(self,other): # to allow less than comparisons between discs
        return self.val < other.val
        

class TowersOfHanoi(QWidget): #Game pop up window
    def __init__(self,num_disc,auto):
        QWidget.__init__(self)
        self.num_disc = num_disc #number of discs in game
        self.won = False           #has the player won?
        self.auto = True if auto == "on" else False #has auto solve been selected?
        
        #Put an array of Discs onto the first tower, other towers have all Nones 
        self.tower1 = [Disc(i+1, 80-(i)*10, 55*(i+1), 60+(i+1)*20, 40, self) for i in range(self.num_disc)]
        self.tower2 = [None for i in range(self.num_disc)]
        self.tower3 = [None for i in range(self.num_disc)]
        self.towers = [self.tower1,self.tower2,self.tower3] # array holding all three towers
        self.selected = None #holds the tower number the player has selected

        self.min_moves = 2**num_disc - 1    # minimum moves for perfect game
        self.moves = 0                      # number of moves the player has made
        self.sleep_time = 1.1-(0.1*self.num_disc) # sleep time for auto solve mode, so bigger games go faster
        
        self.initUI() #initialize the rest of the UI

    
    def initUI(self):
        self.setGeometry(200, 200, 650, self.num_disc*60+200) #set window size, larger for games with more discs
        self.setWindowTitle('Towers of Hanoi Game')
        
        self.moves_label = QLabel(self) #Label at top left displays move count
        self.moves_label.setText(f"Moves: {self.moves}")
        self.moves_label.setGeometry(5,5,100,20)

        self.you_win_label = QLabel(self) #Label at top center displays minimum moves/when player has won
        self.you_win_label.setGeometry(150,5,300,20)
        self.you_win_label.setText(f"Min Moves: {self.min_moves}")
        
        self.timer = QTimer() # Set up a Qtimer to track time taken to solve
        self.elapsed_time = QTime(0, 0) # start time at 0
        self.timer.timeout.connect(self.update_time) #connect timer to update_time method
        
        self.timer_label = QLabel(self) #Label at top right displays elapsed time
        self.timer_label.setGeometry(450,5,300,20)
        self.timer_label.setText("Time: 00:00:00")

        # One select button for each tower to pick Disc on top
        button1= QPushButton(self)
        button2= QPushButton(self)
        button3= QPushButton(self)
        button1.setText("<--")
        button2.setText("^")
        button3.setText("-->")
        button1.setGeometry(30, self.num_disc*60+100, 180, 80)
        button2.setGeometry(230, self.num_disc*60+100, 180, 80)
        button3.setGeometry(430, self.num_disc*60+100, 180, 80)
        
        # Connect each button to the select_clicked method, passing tower parameter
        button1.clicked.connect(lambda: self.select_clicked(0))
        button2.clicked.connect(lambda: self.select_clicked(1))
        button3.clicked.connect(lambda: self.select_clicked(2))
        

    def paintEvent(self,event): #paints the towers onto the screen
        painter = QPainter(self)
        painter.setPen(QPen(Qt.darkGray, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.darkGray, Qt.SolidPattern))
        painter.drawRect(100, 40, 40, self.num_disc*60)
        painter.drawRect(300, 40, 40, self.num_disc*60)
        painter.drawRect(500 ,40, 40, self.num_disc*60)
        painter.drawRect(80, self.num_disc*60+40, 80, 25)
        painter.drawRect(280, self.num_disc*60+40, 80, 25)
        painter.drawRect(480, self.num_disc*60+40, 80, 25)

    def keyPressEvent(self,event): # Detects if a keyboard button has been pressed
        key = event.key()
        if key == Qt.Key_1  or key == Qt.Key_Left: #1 or left arrow picks left tower
            self.select_clicked(0)
        if key == Qt.Key_2 or key == Qt.Key_Up or key == Qt.Key_Down: #2, up arrow, or down arrow picks center tower
            self.select_clicked(1)
        if key == Qt.Key_3 or key == Qt.Key_Right: #3 or right arrow picks right tower
            self.select_clicked(2)

    def update_time(self): # Updates timer every second, Qtime can't do milliseconds
        self.elapsed_time = self.elapsed_time.addSecs(1)
        self.timer_label.setText('Time: ' + self.elapsed_time.toString('hh:mm:ss')) # update timer label

    def select_clicked(self,tower): # when select button or keyboard pressed
        if not self.won and not self.auto: #check if player has won or is auto solving
            if self.selected == None: # if there is not already a selected disc
                if not all(v is None for v in self.towers[tower]): #check if tower has at least one disc on it
                    self.selected = tower # update selected tower
                    self.towers[tower][0].setStyleSheet("background-color: red") #make top disc of selected tower red
                    self.update() #update the screen
            elif self.selected == tower: #if selected same tower twice in a row
                self.towers[self.selected][0].setStyleSheet("background-color: blue") #change top disc back to blue
                self.selected = None #deselect a tower
                self.update() #update the screen
            #check if moving to a tower with no discs or if the top disc is smaller than the selected disc
            elif self.towers[tower][0] == None or self.towers[self.selected][0] < self.towers[tower][0]:
                self.move(self.selected,tower) #make a move
                self.selected = None #deselect a tower
        
    def move(self,move_from,move_to): #makes the disc move
        QApplication.processEvents() #needed for auto solving mode
        if not self.timer.isActive(): #timer starts when first move is made
            self.timer.start(1000) #timer goes up every 1 second
        self.towers[move_from][0].setStyleSheet("background-color: blue") #make moving disc back to blue
        count_none = sum(1 for item in self.towers[move_to] if item is None) #count how many Nones on tower for spacing
        new_x = 90 - (self.towers[move_from][0].val)*10 + (200 * move_to)  
        new_y = 55 * count_none
        self.towers[move_from][0].move(new_x,new_y) #move disc on screen to new coordinates
    
        self.towers[move_to].insert(0,self.towers[move_from].pop(0)) #pop disc at element 0 off old tower and insert into element 0 of new tower
        self.towers[move_to].pop() #remove last element off new tower (a None)
        self.towers[move_from].append(None) #add a None onto back of old tower
        self.moves += 1 #increase player move counter
        self.moves_label.setText(f"Moves: {self.moves}") #update counter label
        if not any(item is None for item in self.towers[2]): # Win condition if right tower has no Nones
            self.timer.stop() #stop the timer
            self.you_win_label.setText(f"You Win! Minimum possible moves: {self.min_moves}") #update winner label
            self.won = True #player has won
        self.update() #update the screen
        

class Menu(QWidget): #Main Menu Window
    def __init__(self):
        super().__init__()
        self.game = None #holds the Tower of Hanoi game pop up window
        self.initUI()
    
    def initUI(self):
        self.setGeometry(50, 50, 500, 200)
        self.setWindowTitle('Towers of Hanoi Menu')

        label1 = QLabel(self) #Welcome Message Label
        label1.move(50, 30) 
        label1.setText("Welcome to Towers of Hanoi!")
        
        label2 = QLabel(self) # disc select label
        label2.move(50,50)
        label2.setText("Select how many discs you would like to play with:")
        
        label3 = QLabel(self) # auto solver select label
        label3.move(50, 70) 
        label3.setText("Select Auto Solve on or off:")

        self.combobox = QComboBox(self) # disc select drop down box
        self.combobox.addItems(['3', '4', '5', '6','7','8'])
        self.combobox.move(370,45)

        self.autoSolve = QComboBox(self) # auto solver select drop down box
        self.autoSolve.addItems(["off","on"])
        self.autoSolve.move(370,70)

        button = QPushButton(self) # Play Game Button
        button.setText("PLAY")
        button.setGeometry(130, 100, 200, 80)
        button.clicked.connect(self.play_clicked) #Connect Play Button to play_clicked method
    
    def play_clicked(self):
        #Make a TowersOfHanoi Pop up window based on number of discs and auto solver from drop down boxes
        self.game = TowersOfHanoi(int(self.combobox.currentText()),self.autoSolve.currentText()) 
        self.game.show() #Show pop up window
        if self.game.auto: #Start the auto solver if auto solve is on
            self.autoSolver(self.game,self.game.num_disc,0,1,2)

    def autoSolver(self,game,num,t1,t2,t3): #Towers of Hanoi recursive algorithm
        if num == 1: #base case
            sleep(self.game.sleep_time)
            self.game.move(t1,t3)
            return
        self.autoSolver(self.game,num-1,t1,t3,t2)
        sleep(self.game.sleep_time)
        self.game.move(t1,t3)
        self.autoSolver(self.game,num-1,t2,t1,t3)


def main():
    app = QApplication(sys.argv)
    window = Menu()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
