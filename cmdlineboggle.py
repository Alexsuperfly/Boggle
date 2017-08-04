'''
Alexander Sumner boggle.py
'''

import enchant
import random
from copy import copy

#create the dictionary to search for valid words
d = enchant.Dict("en_US")

#globalize the game board
Board = []

#globalize entered words list
EnteredWords = []

#make a list to contain all die for the board
Dice = []
#Dice one
Dice.append(["A","E","A","N","E","G"])
#Dice two
Dice.append(["A","H","S","P","C","O"])
#Dice three
Dice.append(["A","S","P","F","F","K"])
#Dice four
Dice.append(["O","B","J","O","A","B"])
#Dice five
Dice.append(["I","O","T","M","U","C"])
#Dice six
Dice.append(["R","Y","V","D","E","L"])
#Dice seven
Dice.append(["L","R","E","I","X","D"])
#Dice eight
Dice.append(["E","I","U","N","E","S"])
#Dice nine
Dice.append(["W","N","G","E","E","H"])
#Dice ten
Dice.append(["L","N","H","N","R","Z"])
#Dice eleven
Dice.append(["T","S","T","I","Y","D"])
#Dice twelve
Dice.append(["O","W","T","O","A","T"])
#Dice thirteen
Dice.append(["E","R","T","T","Y","L"])
#Dice fourteen
Dice.append(["T","O","E","S","S","I"])
#Dice fifteen
Dice.append(["T","E","R","W","H","V"])
#Dice sixteen
Dice.append(["N","U","I","H","M","Qu"])

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

#clear and randomize the game board
def build_board():
	for each in Board:
		Board.remove(each)

	for each in EnteredWords:
		EnteredWords.remove(each)

	random.shuffle(Dice)
	
	for x in range(0,16):
		Board.append(random.choice(Dice[x]))

#print out the game board and capture the attempted words
def print_board():
	print("["+Board[0]+"] ["+Board[1]+"] ["+Board[2]+"] ["+Board[3]+"]\n")
	print("["+Board[4]+"] ["+Board[5]+"] ["+Board[6]+"] ["+Board[7]+"]\n")
	print("["+Board[8]+"] ["+Board[9]+"] ["+Board[10]+"] ["+Board[11]+"]\n")
	print("["+Board[12]+"] ["+Board[13]+"] ["+Board[14]+"] ["+Board[15]+"]\n")

	print("Start typing your words! (press enter after each word and enter 'X' when done):")
	while True:
		enter = raw_input(">")
		enter = enter.upper()
		if enter == "X":
			break
		#make sure each word is unique
		elif enter not in EnteredWords:
			EnteredWords.append(enter)
		else:
			continue

#look around the place parameter for the next letter in the word
def look_letter(place, findletters, usedplaces):
	#if no more letters to look for return true
	if not findletters:
		return True

	#label the current place as used to not be able to use it again
	usedplaces.append(place)
	
	#use the top left space to continue finding the word
	if (place in topleftable) and ((place - 5) not in usedplaces) and (Board[place-5] == findletters[0]):
		if look_letter(place-5,findletters[1:],copy(usedplaces)):
			return True

	#use the top space to continue finding the word
	if (place in topable) and ((place - 4) not in usedplaces) and (Board[place-4] == findletters[0]):
		if look_letter(place-4,findletters[1:],copy(usedplaces)):
			return True

	#use the top right space to continue finding the word
	if (place in toprightable) and ((place - 3) not in usedplaces) and (Board[place-3] == findletters[0]):
		if look_letter(place-3,findletters[1:],copy(usedplaces)):
			return True

	#use the left space to continue finding the word
	if (place in leftable) and ((place - 1) not in usedplaces) and (Board[place-1] == findletters[0]):
		if look_letter(place-1,findletters[1:],copy(usedplaces)):
			return True

	#use the right space to continue finding the word
	if (place in rightable) and ((place + 1) not in usedplaces) and (Board[place+1] == findletters[0]):
		if look_letter(place+1,findletters[1:],copy(usedplaces)):
			return True
    
    #use the bottom left space to continue finding the word
	if (place in bottomleftable) and ((place + 3) not in usedplaces) and (Board[place+3] == findletters[0]):
		if look_letter(place+3,findletters[1:],copy(usedplaces)):
			return True

	#use the bottom space to continue finding the word
	if (place in bottomable) and ((place + 4) not in usedplaces) and (Board[place+4] == findletters[0]):
		if look_letter(place+4,findletters[1:],copy(usedplaces)):
			return True

	#use the top right space to continue finding the word
	if (place in bottomrightable) and ((place + 5) not in usedplaces) and (Board[place+5] == findletters[0]):
		if look_letter(place+5,findletters[1:],copy(usedplaces)):
			return True

	#return False because the next letter wasnt found anywhere
	return False



#look through the board for the entered word and return if its there
def scan_board(word):
	#each letter we need to find
	letters = []
	#the location of each found letter
	used = []

	#populate the letters list with each individual letter form the word
	qfound = False
	for i in word:
		if qfound and i == "U":
			qfound = False
			continue
		if i == "Q":
			letters.append("Qu")
			qfound = True
		else:
			letters.append(i)

	for i in range(0,16):
		if Board[i] == letters[0]:
			if look_letter(i,letters[1:],copy(used)):
				return True
	return False

#get the number of points the word is worth
def find_points(word):
	if len(word) == 3 or len(word) == 4:
		return 1
	elif len(word) == 5:
		return 2
	elif len(word) == 6:
		return 3
	elif len(word) == 7:
		return 5
	else:
		return 11


#check if the word is valid and print the corresponding message
def check_word(word):
	#check if word is valid length
	if len(word) < 3:
		print("The word "+word+" is too short.")
		return 0
	
	#check if word exists
	elif (not d.check(word)):
		print("The word "+word+" is ... not a word.")
		return 0
	
	#check the board of the word
	elif scan_board(word):
		result = find_points(word)
		if result == 1:
			print("The word "+word+" is worth "+str(result)+" point.")
		else:
			print("The word "+word+" is worth "+str(result)+" points.")
		#return the point total that the word gives
		return result
	
	#word isnt present on the board
	else:
		print("The word "+word+" is not present.")
		return 0

#run boggle
def run():
	Score = 0
	build_board()
	print_board()
	for each in EnteredWords:
		Score = Score + check_word(each)
	if Score > 1:
		print("Your total score is "+str(Score)+" points!\n")
	elif Score == 1:
		print("Your total score is "+str(Score)+" point!\nBetter luck next time!\n")
	else:
		print("Your total score was "+str(Score)+" points!\nDid you even try?\n")

#auto run if the module is the main module
if __name__ == "__main__":
	run()