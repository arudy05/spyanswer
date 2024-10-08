#####################################################
# SPYANSWER! - version 0.4                          #
# an answer-and-question game for the Spyder IDE    #
# by Adam Rudy                                      #
# written for the ENCMP 100 Programming Contest     #
#####################################################

import matplotlib.pyplot as plt
import matplotlib.font_manager as font
import numpy as np
import time

def buzzer(): # This function handles the "buzzer" for each answer.
    # A 5-second countdown before you can buzz in.
    for i in range(1,6):
        countdown = abs(6-i)
        print("%d ... " % countdown, end="")
        time.sleep(1)
    
    #the idea here is that the first person to buzz in will be the first to type thus yeah
    buzz = str(input("\nBuzz in and press ENTER! "))
    global pBuzz
    bnum = 0
    while True: # makes sure that the players are pressing the right keys to buzz in
        if buzz[bnum] == "a":
            pBuzz = 0 #Player 1
            break
        elif buzz[bnum] == "b":
            pBuzz = 1 # Player 2
            break
        elif buzz[bnum] == "l":
            pBuzz = 2 # Player 3
            break
        else:
            bnum = bnum+1

def graphics(): #This function handles drawing the game's graphics.
    global tablecells 
    
    #These variables are used to set the formatting for each cell.
    catSet = font.FontProperties(size="24", weight="bold")
    tileSet = font.FontProperties(size="36", weight="bold")
    gridcolours = np.full((6,6), "#010D8C")
    scorecolours = np.full((2,3), "#010D8C")
    
    #These variables take pre-existing lists and arrange them into something usable
    tablecells = [categories, answer1, answer2, answer3, answer4, answer5 ]
    scorecells = [players, scores]
    
    #base figure everything goes onto this thing
    plt.figure(figsize=(12,2),dpi=100,facecolor="#0567D2")
    
    #Draws the grid with all the answer values and everything
    grid = plt.table(tablecells,loc='top',cellLoc='center',cellColours=gridcolours)
    grid.scale(2,8)
    grid.auto_set_font_size(False)
    for i in range(0,6): #I have to individually set every single cell's text's formatting. fun
        for j in range(0,6):
            cellText = grid[(i,j)].get_text()
            if i == 0:
                cellText.set_color("white")
                cellText.set_fontproperties(catSet)
            else:
                cellText.set_color("#D69F4C")
                cellText.set_fontproperties(tileSet)
                cellText.set_text(str(cellText)[13:-3])
    
    #Draws the table with player scores
    score = plt.table(scorecells,loc='bottom',cellLoc='center',cellColours=scorecolours)
    score.scale(2,6)
    score.auto_set_font_size(False)
    for i in range(0,2): #here we go again
        for j in range(0,3):
            scoreText = score[(i,j)].get_text()
            if i == 0:
                scoreText.set_color("white")
                scoreText.set_fontproperties(catSet)
            else:
                scoreText.set_color("#D69F4C")
                scoreText.set_fontproperties(tileSet)
    
    #removes graph-specific stuff and shows the plot
    plt.gca().get_xaxis().set_visible(False)
    plt.gca().get_yaxis().set_visible(False)
    plt.box(on=None)
    plt.show()

def game(): # This function handles the basic gameplay loop, calling on graphics() and buzzer() as needed.
    # Checking that there are still spaces on the board left
    while np.sum(answer1)+np.sum(answer2)+np.sum(answer3)+np.sum(answer4)+np.sum(answer5) != 0:    
        graphics() #refreshes the board
        
        cat = int(input("Select a category (1-6, L-R): "))
        if cat < 1 or cat > 6: #there are only 6 categories. restart
            print("Not a valid category!")
        else:
            wager = int(input("For how much? "))
            indexes = wager/rnddiv # important
            if tablecells[int(indexes)][cat-1] == 0: #cant select a tile that was already selected
                print("Tile already selected!")
            elif indexes <= 5 and indexes >= 1:
                match indexes:
                    case 1|2|3|4|5:
                        buzzer()
                        if indexes == 1:
                            answer1[cat-1] = 0
                        elif indexes == 2:
                            answer2[cat-1] = 0
                        elif indexes == 3:
                            answer3[cat-1] = 0
                        elif indexes == 4:
                            answer4[cat-1] = 0
                        else:
                            answer5[cat-1] = 0                    
                        scores[pBuzz] = scores[pBuzz] + int(rnddiv*indexes) #adds value of the tile to player's score
                    case other: #you can't wager other values than the ones that are on the board
                        print("Not a valid wager!")
            else: #just in case there's some edge case i didn't think of
                print("Not a valid wager!")
        print()
    print("All questions selected! Game over!")

categories = ["These","Are","Not","Actual","Jeopardy","Categories"]
players = []
scores = [0,0,0]
pBuzz = 0

#fancy intro to the game
print("This... ", end="")
time.sleep(1)
print("is... ", end="")
time.sleep(1) # huge ascii block coming up. woah
print("\n███████╗██████╗ ██╗   ██╗ █████╗ ███╗   ██╗███████╗██╗    ██╗███████╗██████╗ ██╗\n██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║██╔════╝██║    ██║██╔════╝██╔══██╗██║\n███████╗██████╔╝ ╚████╔╝ ███████║██╔██╗ ██║███████╗██║ █╗ ██║█████╗  ██████╔╝██║\n╚════██║██╔═══╝   ╚██╔╝  ██╔══██║██║╚██╗██║╚════██║██║███╗██║██╔══╝  ██╔══██╗╚═╝\n███████║██║        ██║   ██║  ██║██║ ╚████║███████║╚███╔███╔╝███████╗██║  ██║██╗\n╚══════╝╚═╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚═╝\n")
time.sleep(1) 

for i in range(3):
    pname = str(input("Player %i: " % (i+1)))
    players += [pname]
print("Player 1 buzzes in with A, Player 2 buzzes in with B, Player 3 buzzes in with L\n")
print("What round would you like to play?")
rnd = int(input("(1 for Jeopardy!, 2 for Double Jeopardy!): "))
print()
if rnd == 1 or rnd == 2:
    rnddiv = 200*rnd
    answer1 = np.full((6,1), rnddiv*1)
    answer2 = np.full((6,1), rnddiv*2)
    answer3 = np.full((6,1), rnddiv*3)
    answer4 = np.full((6,1), rnddiv*4)
    answer5 = np.full((6,1), rnddiv*5)
    game()
else:
    print("Not a valid round type! Exiting...")