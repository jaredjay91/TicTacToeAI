import numpy as np
import pandas as pd
import json
import sys


def save_model(modeldict, filename):
	data = json.dumps(modeldict)
	f = open(filename,"w")
	f.write(data)
	f.close()


def load_model(filename):
	with open(filename) as f:
		data = f.read()
	model = json.loads(data)
	return model


def hash_state(gameState):
	number = 0
	for index in range(len(gameState)):
		number += int(gameState[index] * (10**index))
	return str(number)


def unhash_state(number):
	gameState = [int(d) for d in str(number)]
	return gameState


def invert_gameState(gameState):
	invertedState = []
	for num in gameState:
		newnum = 1
		if num == 2:
			newnum = 3
		elif num == 3:
			newnum = 2
		invertedState.append(newnum)
	return invertedState


def gameOver(gameState):
	#print("gameState =",gameState)
	if (gameState[0]==gameState[1] and gameState[1]==gameState[2] and gameState[2]!=1) or (gameState[3]==gameState[4] and gameState[4]==gameState[5] and gameState[5]!=1)  or (gameState[6]==gameState[7] and gameState[7]==gameState[8] and gameState[8]!=1) or (gameState[0]==gameState[3] and gameState[3]==gameState[6] and gameState[6]!=1) or (gameState[1]==gameState[4] and gameState[4]==gameState[7] and gameState[7]!=1) or (gameState[2]==gameState[5] and gameState[5]==gameState[8] and gameState[8]!=1) or (gameState[6]==gameState[4] and gameState[4]==gameState[2] and gameState[2]!=1) or (gameState[0]==gameState[4] and gameState[4]==gameState[8] and gameState[8]!=1):
		return (True,1)
	elif (gameState[0]!=1 and gameState[1]!=1 and gameState[2]!=1 and gameState[3]!=1 and gameState[4]!=1 and gameState[5]!=1 and gameState[6]!=1 and gameState[7]!=1 and gameState[8]!=1):
		return (True,0)
	else:
		return (False,0)

def playTicTacToe(loadModel,trainingMode):
	if trainingMode==0:
		print("Initializing game...")
	gameState = [1,1,1,1,1,1,1,1,1]
	#gameState = np.ones((9,1))
	#gameState = np.expand_dims(gameState, axis=0)
	#print("gameState =",gameState)
	xo = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
	mark = ['?','X','O']
	squareLabel = ['bottom left','bottom middle','bottom right','left','center','right','top left','top middle','top right']
	inPlay = True
	player = np.random.randint(1,3)#The AI is player 2

	# load a saved model or build a new one
	model = {}
	if loadModel:
		model = load_model("model.json")

	if trainingMode==0:
		print("Now playing...")

	winner = 0

	usedKeys = []
	#usedKeysOpponent = []
	#modelOpponent = {}
	while inPlay:
		hashState = hash_state(gameState)
		if trainingMode==0:
			print("Player",player,"'s turn")
		choice = -1
		availableChoices = []
		for i in range(0,len(gameState)):
			if gameState[i]==1:
				availableChoices.append(i)
		validChoice = False
		while not validChoice:
			if player==2:
				#print(hashState)
				usedKeys.append(hashState)
				if hashState in model:
					choice = model[hashState]
					#print("The model says to choose",choice)
				else:
					choiceIndex = np.random.randint(0,len(availableChoices))
					choice = availableChoices[choiceIndex]
					model[hashState] = choice
				#choice = np.random.randint(0, 8)
				if trainingMode==0:
					print("availableChoices =",availableChoices)
					print("choice =",choice)
				square = choice+1
			elif player==1:
				#hashStateOpponent = hash_state(invert_gameState(gameState))
				#usedKeysOpponent.append(hashStateOpponent)
				if trainingMode>0:
					choiceIndex = np.random.randint(0,len(availableChoices))
					choice = availableChoices[choiceIndex]
					#if trainingMode==2:
						#if hashState in model:
							#choice = model[hashState]
					square = choice+1
				else:
					print("7 | 8 | 9")
					print("----------")
					print("4 | 5 | 6")
					print("----------")
					print("1 | 2 | 3")
					print()
					print(xo[7],"|",xo[8],"|",xo[9])
					print("----------")
					print(xo[4],"|",xo[5],"|",xo[6])
					print("----------")
					print(xo[1],"|",xo[2],"|",xo[3])
					try:
						square = int(input("Choose a square:"))
					except:
						print("ERROR: Invalid choice! Did you turn off NumLock?")
						validChoice = False
						continue
					choice = square-1
				#modelOpponent[hashStateOpponent] = choice
			if (choice in availableChoices):
				validChoice = True
			else:
				print(choice,"is not a valid choice")

		if trainingMode==0:
			print("Player",player," chooses",squareLabel[choice])
		xo[square] = mark[player]

		#check if the game is over
		gameState[choice] = player+1
		gameOverStatus = gameOver(gameState)
		if gameOverStatus[0]:
			inPlay = False
			winner = player

		#switch player for the next turn
		if player==1:
			player = 2
		elif player==2:
			player = 1

	if trainingMode==0:
		print(xo[7],"|",xo[8],"|",xo[9])
		print("----------")
		print(xo[4],"|",xo[5],"|",xo[6])
		print("----------")
		print(xo[1],"|",xo[2],"|",xo[3])
		print()

	# check who won the game
	if gameOverStatus[1]==1:
		if trainingMode==0:
			print("Player",winner,"wins!!!")
		elif winner==1:
			for key in usedKeys: # Forget losing strategy
				model.pop(key, None)
			#for key in usedKeysOpponent: # Learn from the opponent
				#model[key] = modelOpponent[key]
	else:
		if trainingMode==0:
			print("It's a tie!!!")
		elif trainingMode==1:
			for key in usedKeys:
				model.pop(key, None)
		winner = 0
	#print(model)
	if trainingMode>0:
		save_model(model,"model.json")
	return winner


def train_model(loadModel=True):
	epochs = 100
	batch_size = 1000
	if not loadModel:
		playTicTacToe(loadModel,1)
	loadModel = True
	for i in range(0,epochs):
		if i < epochs/4:
			trainingMode = 1
		else:
			trainingMode = 2
		results = [0,0,0]#[ties,losses,wins]
		print("Training epoch",i+1,"/",epochs)
		for j in range(0,batch_size):
			winner = playTicTacToe(loadModel,trainingMode)
			results[winner] = results[winner]+1
		winrate = results[2]/batch_size*100
		lossrate = results[1]/batch_size*100
		print("Win rate =",winrate,"%; Loss rate =",lossrate,"%")


if __name__ == '__main__':

	# trainingMode:
  # 0 = Don't train, play with user
	# 1 = Train to win against random choices
	# 2 = Train not to lose against trained AI

	trainModel = False
	if len(sys.argv) == 2:
		if sys.argv[1] == "--train":
			trainModel = True
		else:
			print("WARNING: Invalid command line argument",sys.argv[1])
	elif len(sys.argv) > 2:
		print("WARNING: The script is called with 0 or 1 arguments.")

	if trainModel:
		train_model(False)
	else:
		loadModel = True
		playTicTacToe(True,0)
