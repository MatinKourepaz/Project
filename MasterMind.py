import os
import sys
import threading
import random
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit

Form = uic.loadUiType(os.path.join(os.getcwd(), "Form.ui"))[0]


def number_generator():
    number_generated = random.randint(1000, 9999)
    return number_generated


class MainWindow(QMainWindow, Form):
    def __init__(self):
        self.generated_number = 0
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.start_button: QPushButton = self.start_button
        self.reset_button: QPushButton = self.reset_button
        self.exit_button: QPushButton = self.exit_button
        self.guess_label: QLabel = self.guess_label
        self.user_guess: QLineEdit = self.user_guess
        self.result_label: QLabel = self.result_label
        self.check_button: QPushButton = self.check_button
        self.warning_label: QLabel = self.warning_label
        self.guess_number: QLabel = self.guess_number

        self.start_button.clicked.connect(self.GameStart)
        self.reset_button.clicked.connect(self.GameReset)
        self.exit_button.clicked.connect(app.exit)
        self.user_guess.textEdited.connect(self.LimitsWarning)
        self.check_button.clicked.connect(self.CheckGuess)

    def GameStart(self):
        self.generated_number = number_generator()
        self.number_of_try = 0
        self.guess_number.setText("0")
        print("Game is started!")

    def GameReset(self):
        self.result_label.setText("XXXX")
        self.generated_number = number_generator()
        self.user_guess.setText("")
        self.number_of_try = 0
        self.guess_number.setText("0")

    def CheckGuess(self):
        thread1 = GameThread(self.generated_number,self.user_guess.text(),self.result_label)
        thread1.start()
        self.number_of_try += 1
        self.guess_number.setText(str(self.number_of_try))
        

    def LimitsWarning(self):
        if self.user_guess.text() == "":
            pass
        elif int(self.user_guess.text()) < 1000 or int(self.user_guess.text()) > 9999:
            self.warning_label.setText("Your Guess is out of Range! Guess between 1000 ad 9999")
        else:
            self.warning_label.setText("")   



class GameThread(threading.Thread):
    def __init__(self, generated_number, guessed_number, result_label):
        threading.Thread.__init__(self)
        self.generated_number = str(generated_number)
        self.guessed_number = guessed_number
        self.result_label = result_label

    def run(self):
        digits = [False,False,False,False]
        text = ["","","",""]
        for i in range(4):
            if self.generated_number[i] == self.guessed_number[i]:
                digits[i] = True

            if digits[i] == True:
                text[i] = self.generated_number[i]
            else:
                text[i] = "X"
        self.result_label.setText(text[0] + text[1] + text[2] + text[3])        

                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
