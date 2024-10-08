################################################################################
# SPYANSWER! - version 0.5                                                     #
# an answer-and-question game (like Jeopardy!) for the Spyder IDE              #
# by Adam Rudy (arudy@ualberta.ca)                                             #
# written for the ENCMP 100 Programming Contest at the University of Alberta   #
################################################################################

import matplotlib.pyplot as plt
import matplotlib.font_manager as font
import numpy as np
import time

def buzzer(): # This function handles the "buzzer" for each answer.
    #A 5-second countdown before you can buzz in.
    for i in range(1,6):
        countdown = abs(6-i)
        print("%d ... " % countdown, end="")
        time.sleep(1)
    
    #the idea here is that the first person to buzz in will be the first to type thus yeah
    buzz = str(input("\nBuzz in and press ENTER! "))
    global pBuzz
    bnum = 0
    while True: # makes sure that the players are pressing the right keys to buzz in
        try:
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
        except IndexError:
            pBuzz = 3 #special condition for if no one answered at all
            break

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
    graphics() # initial rendering of the board
    # Checking that there are still spaces on the board left
    while np.sum(answer1)+np.sum(answer2)+np.sum(answer3)+np.sum(answer4)+np.sum(answer5) != 0:        
        error = False
        cat = input("Select a category (1-6, L-R): ")
        try: # Error handling - making sure that cat can be an integer
            int(cat) # I realize that decimals just end up ignored -- that's fine honestly
        except ValueError:
            error = True
        if error:
            print("Not a valid category!")
        elif int(cat) < 1 or int(cat) > 6: #there are only 6 categories. restart
            print("Not a valid category!")
        else:
            cat = int(cat)
            wager = input("For how much? ")
            try: # more error handling :)
                indexes = int(wager)/rnddiv # important
            except ValueError:
                error = True
            if error:
                print("Not a valid wager!")
            elif indexes < 1 or indexes > 5:
                print("Not a valid wager!")
            elif tablecells[int(indexes)][cat-1] == 0: #cant select a tile that was already selected
                print("Not a valid wager!")
            else:
                match indexes: #there is a syntax error here according to spyder. ignore this
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
                        if pBuzz == 3:
                            print("Nobody answered! Moving on...")
                        else: # if pBuzz is anything other than 0, 1, 2 or 3 we have bigger problems
                            scores[pBuzz] = scores[pBuzz] + int(rnddiv*indexes)#adds value of the tile to player's score
                        graphics() #refreshes graphics to reflect the updated board
                    case other: #you can't wager other values than the ones that are on the board
                        print("Not a valid wager!")
        print()
    print("All questions selected!\n")

def round(num): #This function sets up rounds and then passes it off to game()
    global rnddiv
    global answer1
    global answer2
    global answer3
    global answer4
    global answer5
    
    rnddiv = 200*num
    answer1 = np.full((6,1), rnddiv*1)
    answer2 = np.full((6,1), rnddiv*2)
    answer3 = np.full((6,1), rnddiv*3)
    answer4 = np.full((6,1), rnddiv*4)
    answer5 = np.full((6,1), rnddiv*5)
    print("ROUND %d \n" % num)
    game()

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
round(1)
round(2)
print("Game over!")