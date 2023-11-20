from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, QTime
from time import sleep
import sys

class Disc(QLabel): #Disc class inherits from QLabel class but holds value
    def __init__(self, val,x,y,w,h,parent=None):
        super().__init__(parent)
        self.val = val 
        self.setGeometry(x,y,w,h) 
        self.setText(f"{self.val}")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: blue")
    
    def __str__(self): # to print dics, used for debugging
        return str(self.val)
    
    def __lt__(self,other): # to allow less than comparisons between discs
        return self.val < other.val
        

class TowersOfHanoi(QWidget):
    def __init__(self,num_disc,auto):
        QWidget.__init__(self)
        self.num_disc = num_disc
        self.won = False
        self.auto = True if auto == "on" else False
        
        self.tower1 = [Disc(i+1, 80-(i)*10, 55*(i+1), 60+(i+1)*20, 40, self) for i in range(self.num_disc)]
        self.tower2 = [None for i in range(self.num_disc)]
        self.tower3 = [None for i in range(self.num_disc)]
        self.towers = [self.tower1,self.tower2,self.tower3] # array holding all three towers
        self.selected = None

        self.min_moves = 2**num_disc - 1    # minimum moves for perfect game
        self.moves = 0
        self.sleep_time = 1.1-(0.1*self.num_disc)
        
        self.timer = QTimer()
        self.elapsed_time = QTime(0, 0)
        self.timer.timeout.connect(self.update_time)
        

        self.initUI()

    
    def initUI(self):
        self.setGeometry(200, 200, 650, self.num_disc*60+200)
        self.setWindowTitle('Towers of Hanoi Game')
        
        self.moves_label = QLabel(self)
        self.you_win_label = QLabel(self)
        self.timer_label = QLabel(self)
        self.moves_label.setText(f"Moves: {self.moves}")
        self.moves_label.setGeometry(5,5,100,20)
        self.you_win_label.setGeometry(150,5,300,20)
        self.you_win_label.setText(f"Min Moves: {self.min_moves}")
        self.timer_label.setGeometry(450,5,300,20)
        self.timer_label.setText("Elapsed Time: 00:00:00")

        button1= QPushButton(self)
        button2= QPushButton(self)
        button3= QPushButton(self)
        button1.setText("Select")
        button2.setText("Select")
        button3.setText("Select")
        button1.setGeometry(30, self.num_disc*60+100, 180, 80)
        button2.setGeometry(230, self.num_disc*60+100, 180, 80)
        button3.setGeometry(430, self.num_disc*60+100, 180, 80)
        
        button1.clicked.connect(lambda: self.select_clicked(0))
        button2.clicked.connect(lambda: self.select_clicked(1))
        button3.clicked.connect(lambda: self.select_clicked(2))
        

    def paintEvent(self,event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.darkGray, 5, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.darkGray, Qt.SolidPattern))
        painter.drawRect(100, 40, 40, self.num_disc*60)
        painter.drawRect(300, 40, 40, self.num_disc*60)
        painter.drawRect(500 ,40, 40, self.num_disc*60)
        painter.drawRect(80, self.num_disc*60+40, 80, 25)
        painter.drawRect(280, self.num_disc*60+40, 80, 25)
        painter.drawRect(480, self.num_disc*60+40, 80, 25)

    def keyPressEvent(self,event):
        key = event.key()
        if key == Qt.Key_1  or key == Qt.Key_Left:
            self.select_clicked(0)
        if key == Qt.Key_2 or key == Qt.Key_Up or key == Qt.Key_Down:
            self.select_clicked(1)
        if key == Qt.Key_3 or key == Qt.Key_Right:
            self.select_clicked(2)

    def update_time(self):
        self.elapsed_time = self.elapsed_time.addSecs(1)
        self.timer_label.setText('Elapsed Time: ' + self.elapsed_time.toString('hh:mm:ss'))

    def select_clicked(self,tower):
        if not self.won and not self.auto:
            if self.selected == None:
                if not all(v is None for v in self.towers[tower]):
                    self.selected = tower
                    self.towers[tower][0].setStyleSheet("background-color: red")
                    self.update()
            elif self.selected == tower: #if selected same tower twice
                self.towers[self.selected][0].setStyleSheet("background-color: blue")
                self.selected = None
                self.update()
            elif self.towers[tower][0] == None or self.towers[self.selected][0] < self.towers[tower][0]:
                self.move(self.selected,tower)
                self.selected = None
        
    def move(self,move_from,move_to): #makes the disc switch
        QApplication.processEvents()
        if not self.timer.isActive():
            self.timer.start(1000) 
        self.towers[move_from][0].setStyleSheet("background-color: blue")
        count_none = sum(1 for item in self.towers[move_to] if item is None)
        new_x = 90-(self.towers[move_from][0].val)*10 + (200 * move_to)
        new_y = 55 * count_none
        self.towers[move_from][0].move(new_x,new_y)
    
        self.towers[move_to].insert(0,self.towers[move_from].pop(0))
        self.towers[move_to].pop()
        self.towers[move_from].append(None)
        self.moves += 1
        self.moves_label.setText(f"Moves: {self.moves}")
        if not any(item is None for item in self.towers[2]):
            self.you_win_label.setText(f"You Win! Minimum possible moves: {self.min_moves}")
            self.won = True
            self.timer.stop()
        self.update()
        

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.game = None
        self.initUI()
    
    def initUI(self):
        self.setGeometry(50, 50, 500, 200)
        self.setWindowTitle('Towers of Hanoi Menu')

        label1 = QLabel(self)
        label2 = QLabel(self)
        label3 = QLabel(self)

        label1.move(50, 30) 
        label1.setText("Welcome to Towers of Hanoi!")
        label2.move(50,50)
        label2.setText("Select how many discs you would like to play with:")
        label1.move(50, 70) 
        label1.setText("Select Auto Solve on or off:")

        self.combobox = QComboBox(self)
        self.combobox.addItems(['3', '4', '5', '6','7','8'])
        self.combobox.move(370,45)

        self.autoSolve = QComboBox(self)
        self.autoSolve.addItems(["off","on"])
        self.autoSolve.move(370,70)

        button = QPushButton(self)
        button.setText("PLAY")
        button.setGeometry(130, 100, 200, 80)
        button.clicked.connect(self.play_clicked)
    
    def play_clicked(self):
        self.game = TowersOfHanoi(int(self.combobox.currentText()),self.autoSolve.currentText())
        self.game.show()
        #x = input("test")
        if self.game.auto:
            self.autoSolver(self.game,self.game.num_disc,0,1,2)

    def autoSolver(self,game,num,t1,t2,t3):
        if num == 1:
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
