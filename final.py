'''
Alexander Sumner
FSUID: acs14k
'''

import enchant
import random
from copy import copy
from PyQt5 import QtWidgets, QtCore, QtGui
import pickle
import time
import sys

#create the dictionary to search for valid words
global d
d = enchant.Dict("en_US")

#make a list to contain all die for the board
global BaseDice
BaseDice = []
#Dice one
BaseDice.append(["A","E","A","N","E","G"])
#Dice two
BaseDice.append(["A","H","S","P","C","O"])
#Dice three
BaseDice.append(["A","S","P","F","F","K"])
#Dice four
BaseDice.append(["O","B","J","O","A","B"])
#Dice five
BaseDice.append(["I","O","T","M","U","C"])
#Dice six
BaseDice.append(["R","Y","V","D","E","L"])
#Dice seven
BaseDice.append(["L","R","E","I","X","D"])
#Dice eight
BaseDice.append(["E","I","U","N","E","S"])
#Dice nine
BaseDice.append(["W","N","G","E","E","H"])
#Dice ten
BaseDice.append(["L","N","H","N","R","Z"])
#Dice eleven
BaseDice.append(["T","S","T","I","Y","D"])
#Dice twelve
BaseDice.append(["O","W","T","O","A","T"])
#Dice thirteen
BaseDice.append(["E","R","T","T","Y","L"])
#Dice fourteen
BaseDice.append(["T","O","E","S","S","I"])
#Dice fifteen
BaseDice.append(["T","E","R","W","H","V"])
#Dice sixteen
BaseDice.append(["N","U","I","H","M","Qu"])

#list of items that can seach to the top left for another dice
topleftable = [5,6,7,9,10,11,13,14,15]
#list of items that can seach to the top right for another dice
toprightable = [4,5,6,8,9,10,12,13,14]
#list of items that can seach to the top for another dice
topable = [4,5,6,7,8,9,10,11,12,13,14,15]
#list of items that can seach to the left for another dice
leftable = [1,2,3,5,6,7,9,10,11,13,14,15]
#list of items that can seach to the right for another dice
rightable = [0,1,2,4,5,6,8,9,10,12,13,14]
#list of items that can seach to the bottom left for another dice
bottomleftable = [1,2,3,5,6,7,9,10,11]
#list of items that can seach down for another dice
bottomable = [0,1,2,3,4,5,6,7,8,9,10,11]
#list of items that can seach to the bottom right for another dice
bottomrightable = [0,1,2,4,5,6,8,9,10]

class Die(QtWidgets.QLabel):
	def __init__(self, parent, label):
		QtWidgets.QLabel.__init__(self, parent)
		self.myletter = label
		self.setText(self.myletter)
		self.setAlignment(QtCore.Qt.AlignCenter)
		self.thefont = QtGui.QFont("Times", 32, QtGui.QFont.Bold)
		self.setFont(self.thefont)
		self.setMinimumSize(120,120)


class DiceBoard(QtWidgets.QWidget):
	def __init__(self, parent, dice = None):
		QtWidgets.QWidget.__init__(self,parent)
		self.parent = parent
		self.mydice = []
		self.grid = QtWidgets.QGridLayout()
		self.setLayout(self.grid)
		
		if dice == None:
			self.mydice = self.generateDice()
		else:
			self.mydice = dice

		self.buildBoard(self.mydice)

	def generateDice(self):
		random.shuffle(BaseDice)
		dummyboard = []
		for x in range(0,16):
			dummyboard.append(random.choice(BaseDice[x]))
		return dummyboard

	def buildBoard(self, dice):
		x,y = 1,1
		for each in dice:
			if x == 5:
				x = 1
				y = y + 1
			self.grid.addWidget(Die(self,each),x,y,1,1)
			x = x + 1

	def find_points(self, word):
		if (not d.check(word)):
			return 0
		elif len(word) < 3:
			return 0
		elif len(word) == 3 or len(word) == 4:
			return 1
		elif len(word) == 5:
			return 2
		elif len(word) == 6:
			return 3
		elif len(word) == 7:
			return 5
		else:
			return 11

	def scan_board(self, word):
		#each letter we need to find
		letters = []
		#the location of each found letter
		used = []

		#populate the letters list with each individual letter form the word
		qfound = 0
		for i in word:
			if qfound and i == "U":
				qfound = 0
				continue
			if i == "Q":
				letters.append("Qu")
				qfound = 1
			else:
				letters.append(i)

		for i in range(0,16):
			if self.mydice[i] == letters[0]:
				if self.look_letter(i,letters[1:],copy(used)):
					return 1
		return 0

	#look around the place parameter for the next letter in the word
	def look_letter(self, place, findletters, usedplaces):
		#if no more letters to look for return true
		if not findletters:
			return 1

		#label the current place as used to not be able to use it again
		usedplaces.append(place)
		
		#use the top left space to continue finding the word
		if (place in topleftable) and ((place - 5) not in usedplaces) and (self.mydice[place-5] == findletters[0]):
			if self.look_letter(place-5,findletters[1:],copy(usedplaces)):
				return 1

		#use the top space to continue finding the word
		if (place in topable) and ((place - 4) not in usedplaces) and (self.mydice[place-4] == findletters[0]):
			if self.look_letter(place-4,findletters[1:],copy(usedplaces)):
				return 1

		#use the top right space to continue finding the word
		if (place in toprightable) and ((place - 3) not in usedplaces) and (self.mydice[place-3] == findletters[0]):
			if self.look_letter(place-3,findletters[1:],copy(usedplaces)):
				return 1

		#use the left space to continue finding the word
		if (place in leftable) and ((place - 1) not in usedplaces) and (self.mydice[place-1] == findletters[0]):
			if self.look_letter(place-1,findletters[1:],copy(usedplaces)):
				return 1

		#use the right space to continue finding the word
		if (place in rightable) and ((place + 1) not in usedplaces) and (self.mydice[place+1] == findletters[0]):
			if self.look_letter(place+1,findletters[1:],copy(usedplaces)):
				return 1
	    
	    #use the bottom left space to continue finding the word
		if (place in bottomleftable) and ((place + 3) not in usedplaces) and (self.mydice[place+3] == findletters[0]):
			if self.look_letter(place+3,findletters[1:],copy(usedplaces)):
				return 1

		#use the bottom space to continue finding the word
		if (place in bottomable) and ((place + 4) not in usedplaces) and (self.mydice[place+4] == findletters[0]):
			if self.look_letter(place+4,findletters[1:],copy(usedplaces)):
				return 1

		#use the top right space to continue finding the word
		if (place in bottomrightable) and ((place + 5) not in usedplaces) and (self.mydice[place+5] == findletters[0]):
			if self.look_letter(place+5,findletters[1:],copy(usedplaces)):
				return 1

		#return False because the next letter wasnt found anywhere
		return 0
	
	def check_word(self, word):
		if self.scan_board(word):
			self.parent.score = self.parent.score + self.find_points(word)


class WordTable(QtWidgets.QTextEdit):
	def __init__(self, parent, words = None):
		QtWidgets.QWidget.__init__(self,parent)
		self.parent = parent
		self.displayedwords = []
		if words != None:
			for each in words:
				self.addWord(each)

	def addWord(self, word):
		self.displayedwords.append(word)
		self.parent.board.check_word(word.upper())
		self.append(word)

	def displaywords(self, words):
		for each in words:
			self.append(each)

class WordEntry(QtWidgets.QLineEdit):
	def __init__(self, parent):
		QtWidgets.QLineEdit.__init__(self,parent)
		self.parent = parent
		self.returnPressed.connect(self.getword)

	def getword(self):
		self.theword = self.text()
		self.clear()
		self.parent.wordtable.addWord(self.theword)


class Timer(QtWidgets.QLCDNumber):
	def __init__(self, parent, starttime = 5):
		QtWidgets.QLCDNumber.__init__(self, parent)
		self.starttime = starttime
		self.parent = parent
		self.setup()

	def setup(self):
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.displaytimer)
		self.timer.start(1000)
		self.currenttime = self.starttime

		self.displaytimer()

	def displaytimer(self):
		self.display(self.currenttime)
		if self.currenttime:
			self.currenttime = self.currenttime - 1
		else:
			self.buttonreply = QtWidgets.QMessageBox.question(self, "final.py", "Time's Up!\nScore: "+str(self.parent.score)+"\nWould you like to play again?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
			if self.buttonreply == QtWidgets.QMessageBox.Yes:
				self.parent.NewGame()
			else:
				QtWidgets.qApp.quit()


class BoggleGame(QtWidgets.QWidget):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self, parent)
		
	def NewGame(self):
		self.score = 0
		self.board = DiceBoard(self)
		self.wordtable = WordTable(self)
		self.timer = Timer(self)
		self.wordentry = WordEntry(self)

		self.grid = QtWidgets.QGridLayout()
		self.setLayout(self.grid)

		self.grid.addWidget(self.board,1,1,10,5)
		self.grid.addWidget(self.wordtable,1,6,10,4)
		self.grid.addWidget(self.wordentry,11,1,1,8)
		self.grid.addWidget(self.timer,11,9,1,1)

	def SaveGame(self):
		print("save game")
		return

	def LoadGame(self):
		print("load game")
		return

class FirstLoadMessage(QtWidgets.QMessageBox):
	def __init__(self):
		QtWidgets.QMessageBox.__init__(self)
		self.setText("Would you like to start a new game\n or load a saved game?")
		self.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
		newbutton = self.button(QtWidgets.QMessageBox.Yes)
		newbutton.setText("Start New Game")
		loadbutton = self.button(QtWidgets.QMessageBox.No)
		loadbutton.setText("Load Game")

class BoggleMainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setup()

	def setup(self):
		self.setWindowTitle('Boggle')

		self.bogglegame = BoggleGame(self)
		self.setCentralWidget(self.bogglegame)

		initialquestion = FirstLoadMessage()
		reply = initialquestion.exec_()
		if reply == QtWidgets.QMessageBox.Yes:
			self.bogglegame.NewGame()
		else:
			self.bogglegame.LoadGame()

		new_game_action = QtWidgets.QAction('New', self)
		new_game_action.triggered.connect(self.bogglegame.NewGame)

		save_game_action = QtWidgets.QAction('Save', self)
		save_game_action.triggered.connect(self.bogglegame.SaveGame)

		load_game_action = QtWidgets.QAction('Load', self)
		load_game_action.triggered.connect(self.bogglegame.LoadGame)

		menu_bar = self.menuBar()
		menu_bar.setNativeMenuBar(False)
		game_menu = menu_bar.addMenu('Game')
		game_menu.addAction(new_game_action)
		game_menu.addAction(save_game_action)
		game_menu.addAction(load_game_action)

		self.show()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	main_window = BoggleMainWindow()
	app.exec_()
