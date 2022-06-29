import sys
import math
import time
import os

# Pygame
import pygame
pygame.init()

# TODO
# Make Undo Move
# Check if check
# 1. Fix Check and Checkmate
# 2. Drag
# 3. Make bigger drag
# 4. Make rezisable


# WN
width = 400
height = 400
wn = pygame.display.set_mode((width, height))

# GAME VARIABLES
lenSquare = height/8


indicator = False
pMove = False
ImXposB = 0
ImYposB = 0

moves = 0
lastMove = []
undo = False

piece = 0

needMove = True

check = False

# Colours
light = (118, 150, 86)
dark = 	(238, 238, 210)

#-------ROKAD

# White
kingMove1 = False

# Black
kingMove2 = False

# White
rookMove1 = False
rookMove2 = False

# Black
rookMove3 = False
rookMove4 = False

# chessBoard
#---WHITE---
# king   = 6
# queen  = 5
# bishop = 4
# horse  = 3
# rook   = 2
# pawn   = 1
#---BLACK---
# king   = 12
# queen  = 11
# bishop = 10
# horse  = 9
# rook   = 8
# pawn   = 7
chessBoard = [
	[8, 9, 10, 11, 12, 10, 9, 8],
	[7, 7, 7, 7, 7, 7, 7, 7],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[1, 1, 1, 1, 1, 1 ,1 ,1],
	[2, 3, 4, 5, 6, 4, 3, 2]]

		
# Import pieces
pieceLength = 48
pieceK1 = pieceLength / width
pieceK2 = pieceLength / height
pieceSize = (int(width * pieceK2), int(height * pieceK1))

# WHITE
wK = pygame.image.load("img/White/wk.png")
wK = pygame.transform.scale(wK, pieceSize)
wQ = pygame.image.load("img/White/wq.png")
wQ = pygame.transform.scale(wQ, pieceSize)
wN = pygame.image.load("img/White/wkn.png")
wN = pygame.transform.scale(wN, pieceSize)
wB = pygame.image.load("img/White/wb.png")
wB = pygame.transform.scale(wB, pieceSize)
wR = pygame.image.load("img/White/wr.png")
wR = pygame.transform.scale(wR, pieceSize)
wP = pygame.image.load("img/White/wp.png")
wP = pygame.transform.scale(wP, pieceSize)

# BLACK
bK = pygame.image.load("img/Black/bk.png")
bK = pygame.transform.scale(bK, pieceSize)
bQ = pygame.image.load("img/Black/bk.png")
bQ = pygame.transform.scale(bQ, pieceSize)
bN = pygame.image.load("img/Black/bkn.png")
bN = pygame.transform.scale(bN, pieceSize)
bB = pygame.image.load("img/Black/bb.png")
bB = pygame.transform.scale(bB, pieceSize)
bR = pygame.image.load("img/Black/br.png")
bR = pygame.transform.scale(bR, pieceSize)
bP = pygame.image.load("img/Black/bp.png")
bP = pygame.transform.scale(bP, pieceSize)


#pieces
whites = [1, 2, 3, 4, 5, 6]
blackes = [7,8, 9, 10, 11, 12]




# FUNKTIONS
def chessBoardDraw():
	colour = 0
	for i in range(len(chessBoard)):
		for j in range(len(chessBoard[i])):
			colour += 1 
			drawRect(light if colour % 2 == 0 else dark, j*lenSquare, i*lenSquare, lenSquare, lenSquare)
		colour += 1

def checkIfCaptureK(v):
	if len(v) > 0:
		for i in range(len(v)):
			if v[i] == 6 or v[i] == 12:
				return True
		return False


def drawRect(colour, xpos, ypos, w, h):
	pygame.draw.rect(wn, colour, pygame.Rect(xpos, ypos, w, h))

def whiteBlack(board, ImouseYB, ImouseXB):
	if board[ImouseYB][ImouseXB] == 1 or board[ImouseYB][ImouseXB] == 2 or board[ImouseYB][ImouseXB] == 3 or board[ImouseYB][ImouseXB] == 4 or board[ImouseYB][ImouseXB] == 5 or board[ImouseYB][ImouseXB] == 6:
		return "white"
	else:
		return "black"

def diagonalCutout(loops, board, direc, ImouseYB, ImouseXB):

	# get our start cords(ImouseXB, ImouseYB)
	# with the direction we can add to the vector ImouseXB and 
	# y first because look at board u donot # Remember x y in direction, y x in board
	# pp Working fine
	# How can we fix nn?
	# lets get back to the basics
	# first lets check directionm
	# then we need to take the proper index
	# if i == 0


	# One more thing
	# For the check
	# We will need the last element
	v = []
	if direc != "all":
		for i in range(loops):
			v.append(board[i+ImouseYB][i+ImouseXB] if direc == "pp" else board[ImouseYB-i][ImouseXB-i] if direc == "nn" else board[ImouseYB-i][i+ImouseXB] if direc == "pn" else board[i+ImouseYB][ImouseXB-i] if direc == "np" else None)
		return v
	else:
		pass


def bishopCode(board, ImouseYB, ImouseXB, ImouseY, ImouseX, dY, dX):
	# First only going diagonal
	if dY != dX:
		return False
	
	# Second not jumping over
	# First coutout two diagonal vectors from the matrix
	direc = 0
	subY = ImouseY - ImouseYB
	subX = ImouseX - ImouseXB

	if subY > 0:
		if subX > 0:
			direc = "pp"
		else:
			direc = "np"
	else:
		if subX > 0:
			direc = "pn"
		else:
			direc = "nn"

	# now cut out proper board
	# length of the loop will be dY or dX(same thing)
	# ALL GUT
	# NOW FIX Other Direction
	v = []

	'''
	v.append(board[i+ImouseYB][i+ImouseXB] if direc == "pp" else board[ImouseYB-i][ImouseXB-i] if direc == "nn" else board[ImouseYB-i][i+ImouseXB] if direc == "pn" else board[i+ImouseYB][ImouseXB-i] if direc == "np" else None)
	'''
	v = diagonalCutout(dX+1, board, direc, ImouseYB, ImouseXB)

	# Check if not capturing king
	if checkIfCaptureK(v):
		return False

	# cut the first and last element
	if len(v) > 0:
		v.pop(0)
		if len(v) > 0:
			v.pop(len(v)-1)

	if sum(v) != 0:
		return False

def rookCode(board, ImouseYB, ImouseXB, ImouseY, ImouseX):
	# Rules
	# Not going over someone
	# Only going straight lines
	# Rockad kinda lame

	# First, only going in straight lines
	if ImouseY - ImouseYB == 0 or ImouseX - ImouseXB == 0:
		pass
	else:
		return False
	

	# Second, not going over someone
	# Y
	if ImouseY - ImouseYB != 0:	
		pathboard = []
		#----Y Check-----
		if ImouseY < ImouseYB: # Up
			# Trying to get a vector verticaly
			# Negative
			for i in range(len(board)):
				pathboard.append(board[i][ImouseX])

			# Cut the board
			pathboard = pathboard[ImouseY+1:ImouseYB+1]

			# delete last element
			if len(pathboard) > 0:
				pathboard.pop(len(pathboard)-1)

			# Check sum
			if sum(pathboard) != 0:
				return False
		
		else:
			# Trying to get a vector verticaly
			# Positive
			for i in range(len(board)):
				pathboard.append(board[i][ImouseX])
			
			# Cut the board
			pathboard = pathboard[ImouseYB+1:ImouseY]
			# Check sum
			if sum(pathboard) != 0:
				return False

	# X
	else:


		#----X Check-----
		if ImouseX < ImouseXB: # Negative
			# Cutout
			pathboard = board[ImouseY][ImouseX+1:ImouseXB]


			# Check sum
			if sum(pathboard) != 0:
				return False

		else: # Positive
			# Cutout
			pathboard = board[ImouseY][ImouseXB+1:ImouseX]


			# Check sum
			if sum(pathboard) != 0:
				return False

	# Need check king check

	
	return True
	

def checkIfCheck(board, x, y, xB, xY, piece):
	cantCheck = False
	if piece == "wr":
		# Check Vertical Right
		vR = board[y]

		# UPDATE BOARD
		vR[xB] = 0
		
		# cut
		vR = vR[x:len(vR)]

		for i in range(vR[0], len(vR)):
			print(vR[i])
	return False
		
		

def doMoveCheck(board, ImouseYB, ImouseXB, ImouseY, ImouseX, lastMove, moves, whiteOrBlack):
	global kingMove1, kingMove2
	global rookMove1, rookMove2, rookMove3, rookMove4
	capture = True
		
	dY = abs(ImouseY - ImouseYB)
	dX = abs(ImouseX - ImouseXB)

	# BLANK
	if board[ImouseYB][ImouseXB] == 0:
		return False
	# WHITE PAWN
	if board[ImouseYB][ImouseXB] == 1:
		# Check if capture
		if ImouseX + 1 == ImouseXB or ImouseX - 1 == ImouseXB:
			if board[ImouseY][ImouseX] != 12 and board[ImouseY][ImouseX] != 6:
				capture = True
		else:
			# Check if movement X is not 0
			if ImouseX != ImouseXB:
				capture = False
				return False
			capture = False
			


		# Check if first row
		if ImouseYB == 6:
			# Check if it isnt 2 or 1 move first move
			if ImouseY != ImouseYB - 2 and ImouseY != ImouseYB - 1:
				return False
		else:
			if ImouseY != ImouseYB - 1:
				return False


		# CHECK NOT GOING IN
		# First check if One move or two Step
		# Two step
		if capture == False:
			if ImouseY == ImouseYB - 2:
				# Collision Two steps
				if board[ImouseYB - 2][ImouseXB] != 0:
					return False
			else:
				# One Step
				if board[ImouseYB - 1][ImouseXB] != 0:
					return False

		elif capture == True:
			# Check if it doesnt move two steps
			if ImouseY == ImouseYB - 2:
				return False

			# Check if its not empty
			# Go Right
			if ImouseX - ImouseXB == 1:
				if board[ImouseYB - 1][ImouseXB + 1] == 0:
					# En passant
					# First check if YB row 3
					# Then Check if Y row 2
					# Then check pawn now is X-1
					# Then check if pawn previously was row 1
					# delete the pawn

					# row3 YB
					#if ImouseYB != 3:
					#	return False
					
					# row2 Y
					if ImouseY != 2:
						return False
					
					# black pawn
					if board[ImouseYB][ImouseXB + 1] != 7:
						return False


					# If the pawn was there the previus move
					if board[lastMove[3]][lastMove[2]] != 7:
						return False

					# delete black pawn
					return "w en passant r"

			else:
				# Go Left
				if board[ImouseYB - 1][ImouseXB - 1] == 0:


                    # row2 Y					
					if ImouseY != 2:
						return False


					# black pawn
					if board[ImouseYB][ImouseXB - 1] != 7:
						return False

					# If the pawn was there the previus move
					if board[lastMove[3]][lastMove[2]] != 7:
						return False

					# delete en passant
					return "w en passant l"
					
		# Queen
		if ImouseY == 0:
			return "w queen"
	# ROOK
	if board[ImouseYB][ImouseXB] == 2 or board[ImouseYB][ImouseXB] == 8:
		if rookCode(board, ImouseYB, ImouseXB, ImouseY, ImouseX) == False:
			return False
		else:
			# white rooks rockad
			if board[ImouseYB][ImouseXB] == 2:
				if board[ImouseYB][ImouseXB] == board[7][0]:
					rookMove1 = True
				else:
					rookMove2 = True
			else:
				# black rockad
				if board[ImouseYB][ImouseXB] == board[0][0]:
					rookMove3 = True
				else:
					rookMove4 = True


			# We also want to check if check
			
					
	# Knight
	if board[ImouseYB][ImouseXB] == 3 or board[ImouseYB][ImouseXB] == 9:
		# Here we will only check if movement is correct
		# Y + 2, X + 1 or liknande

		# use i for x + 1 or x - 1 and same for j and y. 
		# i will be 1 and 8
		if dY == 1 and dX == 2 or dY == 2 and dX == 1:
			if board[ImouseY][ImouseX] == 12 or board[ImouseY][ImouseX] == 6:
				return False
		else:
			return False
	# Bishop
	if board[ImouseYB][ImouseXB] == 4 or board[ImouseYB][ImouseXB] == 10:
		if bishopCode(board, ImouseYB, ImouseXB, ImouseY, ImouseX, dY, dX) == False:
			return False
	# QUEEN-------------------------------
	if board[ImouseYB][ImouseXB] == 5 or board[ImouseYB][ImouseXB] == 11:
		# if bishpop
		if dY == dX:
			# bishop code:
			if bishopCode(board, ImouseYB, ImouseXB, ImouseY, ImouseX, dY, dX) == False:
				return False

		# if rook
		elif ImouseY - ImouseYB == 0 or ImouseX - ImouseXB == 0:
			# rook code:
			if rookCode(board, ImouseYB, ImouseXB, ImouseY, ImouseX) == False:
				return False
		else:
			return False
	# KING
	if board[ImouseYB][ImouseXB] == 6 or board[ImouseYB][ImouseXB] == 12:
		# Diagonal and Straight movement
		if whiteBlack(board, ImouseYB, ImouseXB) == "white":
			if dY == dX:
				kingMove1 = True
			elif dY == 1 and dX == 0:
				kingMove1 = True
			elif dY == 0 and dX == 1:
				kingMove1 = True
			else:
				# Rockad Right
				if kingMove1 == False:
					if rookMove2 == False:
						if board[ImouseY][5] == 0 and board[ImouseY][6] == 0:
							if ImouseX == 6:
								return "rokad r"

				# Left
				if kingMove1 == False:
					if rookMove1 == False:
						if board[ImouseY][1] == 0 and board[ImouseY][2] == 0 and board[ImouseY][3] == 0:
							if ImouseX == 2:
								return "rokad l"
						
				return False
		else:
			if dY == dX:
				kingMove2 = True
			elif dY == 1 and dX == 0:
				kingMove2 = True
			elif dY == 0 and dX == 1:
				kingMove2 = True
			else:
			# Rockad Right
				if kingMove2 == False:
					if rookMove3 == False:
						if board[ImouseY][5] == 0 and board[ImouseY][6] == 0:
							if ImouseX == 6:
								return "rokad r"
				# Left
				if kingMove2 == False:
					if rookMove4 == False:
						if board[ImouseY][1] == 0 and board[ImouseY][2] == 0 and board[ImouseY][3] == 0:
							if ImouseX == 2:
								return "rokad l"
						
				return False
	# BLACK PAWN
	if board[ImouseYB][ImouseXB] == 7:
		# Check if capture
		if ImouseX + 1 == ImouseXB or ImouseX - 1 == ImouseXB:
			capture = True
		else:
			# Check if movement X is not 0
			if ImouseX != ImouseXB:
				capture = False
				return False
			capture = False
			


		# Check if first row
		if ImouseYB == 1:
			# Check if it isnt 2 or 1 move first move
			if ImouseY != ImouseYB + 2 and ImouseY != ImouseYB + 1:
				return False
		else:
			if ImouseY != ImouseYB + 1:
				return False


		# CHECK NOT GOING IN
		# First check if One move or two Step
		# Two step
		if capture == False:
			if ImouseY == ImouseYB + 2:
				# Collision Two steps
				if board[ImouseYB + 2][ImouseXB] != 0:
					return False
			else:
				# One Step
				if board[ImouseYB + 1][ImouseXB] != 0:
					return False

		elif capture == True:
			# Check if it doesnt move two steps
			if ImouseY == ImouseYB + 2:
				return False



			# Go Right
			if ImouseX + ImouseXB == 1:
				if board[ImouseYB + 1][ImouseXB + 1] == 0:
					# En passant
					# First check if YB row 3
					# Then Check if Y row 2
					# Then check pawn now is X-1
					# Then check if pawn previously was row 1
					# delete the pawn

					# row3 YB
					#if ImouseYB != 4:
					#	return False
					
					# row2 Y
					if ImouseY != 3:
						return False
					
					# black pawn
					if board[ImouseYB][ImouseXB + 1] != 7:
						return False

					if board[lastMove[2]][lastMove[3]] != 7:
						return False

					# delete en passant
					return "b en passant r"

			else:
				# Go Left
				if board[ImouseYB + 1][ImouseXB - 1] == 0:

					# row3 YB
					#if ImouseYB != 3:
					#	return False

					# row2 Y					
					if ImouseY != 2:
						return False
					# black pawn
					if board[ImouseYB][ImouseXB - 1] != 1:
						return False

					# If the pawn was there the previus move
					if board[lastMove[2]][lastMove[3]] != 1:
						return False

					# delete en passant
					return "b en passant l"
					
		# Queen
		if ImouseY == 7:
			return "b queen"


	print("BOARD: ", board)	
	if checkIfCheck(board, ImouseX, ImouseY, ImouseXB, ImouseYB, "wr") == True:
		print("BOARD: ", board)
		return False
	else:
		return True

	return True
	


def movement(board, ImouseYB, ImouseXB, ImouseY, ImouseX, lastMove, moves, whiteOrBlack):
	if (moves % 2 != 0 and whiteOrBlack == "white") or (moves % 2 == 0 and whiteOrBlack == "black"): # WHITE and BLACK
		return doMoveCheck(board, ImouseYB, ImouseXB, ImouseY, ImouseX, lastMove, moves, whiteOrBlack)
	else:
		if needMove == True:
			return "-1"
		else:
			return doMoveCheck(board, ImouseYB, ImouseXB, ImouseY, ImouseX, lastMove, moves, whiteOrBlack)

def movePiece(ImouseX, ImouseY, ImouseXB, ImouseYB, board, lastMove):
	global moves
	moves += 1


	#  RULES:
	# Can not capture own piece
	# Must move the way its supposed to
	# Have check and checkmate
	# King cannot be put in check
	# Not going into its own square
	# Capture right way
	# Not going over a piece(not horse)

	# white or black?
	whiteOrBlack = whiteBlack(board, ImouseYB, ImouseXB)


	# Movement is correct?
	if movement(board, ImouseYB, ImouseXB, ImouseY, ImouseX, lastMove, moves, whiteOrBlack) == False:
		moves -= 1
		return board
	
	# White Special
	elif movement(board, ImouseYB, ImouseXB, ImouseY, ImouseX, lastMove, moves, whiteOrBlack) == "w en passant l":
		board[ImouseYB][ImouseXB - 1] = 0
	elif movement(board, ImouseYB, ImouseXB, ImouseY, ImouseX, lastMove, moves, whiteOrBlack) == "w en passant r":
		print("here1")
		board[ImouseYB][ImouseXB + 1] = 0
	elif movement(board, ImouseYB, ImouseXB, ImouseY, ImouseX, lastMove, moves, whiteOrBlack) == "w queen":
		board[ImouseY][ImouseX] = 5
		board[ImouseYB][ImouseXB] = 0

	elif movement(board, ImouseYB, ImouseXB, ImouseY, ImouseX, lastMove, moves, whiteOrBlack) == "rokad r":
		if whiteOrBlack == "white":
			board[ImouseY][5] = 2
		else:
			board[ImouseY][5] = 8
		board[ImouseY][7] = 0
	elif movement(board, ImouseYB, ImouseXB, ImouseY, ImouseX, lastMove, moves, whiteOrBlack) == "rokad l":
		if whiteOrBlack == "white":
			board[ImouseY][3] = 2
		else:
			board[ImouseY][3] = 8
		board[ImouseY][0] = 0

	# Black Special
	elif movement(board, ImouseYB, ImouseXB, ImouseY, ImouseX, lastMove, moves, whiteOrBlack) == "b en passant l":
		board[ImouseYB][ImouseXB - 1] = 0
	elif movement(board, ImouseYB, ImouseXB, ImouseY, ImouseX, lastMove, moves, whiteOrBlack) == "b en passant r":
		board[ImouseYB][ImouseXB + 1] = 0
	elif movement(board, ImouseYB, ImouseXB, ImouseY, ImouseX, lastMove, moves, whiteOrBlack) == "b queen":
		board[ImouseY][ImouseX] = 11
		board[ImouseYB][ImouseXB] = 0
			
	# Moves
	elif movement(board, ImouseYB, ImouseXB, ImouseY, ImouseX, lastMove, moves, whiteOrBlack) == "-1":
		moves -= 1
		return board



	# Not taking the own piece
	if whiteOrBlack == "white":
		if board[ImouseY][ImouseX] == 1 or board[ImouseY][ImouseX] == 2 or board[ImouseY][ImouseX] == 3 or board[ImouseY][ImouseX] == 4 or board[ImouseY][ImouseX] == 5 or board[ImouseY][ImouseX] == 6:
			moves -= 1
			return board
	elif whiteOrBlack == "black":
		if board[ImouseY][ImouseX] == 7 or board[ImouseY][ImouseX] == 8 or board[ImouseY][ImouseX] == 9 or board[ImouseY][ImouseX] == 10 or board[ImouseY][ImouseX] == 11 or board[ImouseY][ImouseX] == 12:
			moves -= 1
			return board




	# y before because look at board
	board[ImouseY][ImouseX]   = board[ImouseYB][ImouseXB]
	board[ImouseYB][ImouseXB] = 0
	
	return board


def drawIndicator(xposB, yposB, xpos, ypos):
	pass

def transferPosToboard(pos, length):
	boardPos = math.floor(pos/length)
	return boardPos


def undoMove(board, ImouseX, ImouseY, mouseX, mouseY):
	board[ImouseY][ImouseX] = 0
	board[ImouseYB][ImouseXB] = board[ImouseY][ImouseX]

	return board


	
# Call Funktions

# MAIN




diffX = -1
diffY = 3
run = True
while run:
	# EVENTS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			ImXposB = transferPosToboard(pygame.mouse.get_pos()[0], lenSquare)
			ImYposB = transferPosToboard(pygame.mouse.get_pos()[1], lenSquare)
			if event.button == 1:
				pMove = True
			elif event.button == 3:
				indicator = True


		# MOVE PIECES
		if event.type == pygame.MOUSEBUTTONUP:
			# Move
			mouseX = pygame.mouse.get_pos()[0]
			mouseY = pygame.mouse.get_pos()[1]


			if pMove == True:
				chessBoard = movePiece(transferPosToboard(mouseX, lenSquare), transferPosToboard(mouseY, lenSquare), ImXposB, ImYposB, chessBoard, lastMove)
				lastMove = [ImXposB, ImYposB, transferPosToboard(mouseX, lenSquare), transferPosToboard(mouseY, lenSquare)]

			# Indicator
			if indicator == True:
				drawIndicator(ImXposB, ImYposB, mouseX, mouseY)

			indicator = False
			pMove = False



		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				print(chessBoard)
			if event.key == pygame.K_RETURN:
				needMove = False
			if event.key == pygame.K_z:
				undo = True
				# So give it a mouseX so it knows what piece
				chessBoard = undoMove(chessBoard, ImXposB, ImYposB, mouseX, mouseY)
				undo = False



	#DRAW
	#FILL
	chessBoardDraw()

	# Draw Pieces
	for i in range(len(chessBoard)):
		for j in range(len(chessBoard[0])):
			#WHITE
			if chessBoard[i][j] == 1:
				piece = 1
				wn.blit(wP, (j*lenSquare+diffX, i*lenSquare+diffY))
			if chessBoard[i][j] == 2:
				piece = 2
				wn.blit(wR, (j*lenSquare+diffX, i*lenSquare+diffY))
			if chessBoard[i][j] == 3:
				piece = 3
				wn.blit(wN, (j*lenSquare+diffX, i*lenSquare+diffY))
			if chessBoard[i][j] == 4:
				piece = 4
				wn.blit(wB, (j*lenSquare+diffX, i*lenSquare+diffY))
			if chessBoard[i][j] == 5:
				piece = 5
				wn.blit(wQ, (j*lenSquare+diffX, i*lenSquare+diffY))
			if chessBoard[i][j] == 6:
				piece = 6
				wn.blit(wK, (j*lenSquare+diffX, i*lenSquare+diffY))
				
			#BLACK
			if chessBoard[i][j] == 7:
				piece = 7
				wn.blit(bP, (j*lenSquare+diffX, i*lenSquare+diffY))
			if chessBoard[i][j] == 8:
				piece = 8
				wn.blit(bR, (j*lenSquare+diffX, i*lenSquare+diffY))
			if chessBoard[i][j] == 9:
				piece = 9
				wn.blit(bN, (j*lenSquare+diffX, i*lenSquare+diffY))
			if chessBoard[i][j] == 10:
				piece = 10
				wn.blit(bB, (j*lenSquare+diffX, i*lenSquare+diffY))
			if chessBoard[i][j] == 11:
				piece = 11
				wn.blit(bQ, (j*lenSquare+diffX, i*lenSquare+diffY))
			if chessBoard[i][j] == 12:
				piece = 12
				wn.blit(bK, (j*lenSquare+diffX, i*lenSquare+diffY))

				
	# UPDATE AND FLIP
	pygame.display.flip()
	pygame.display.update()
	
	
pygame.quit()
