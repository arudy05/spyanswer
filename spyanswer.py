###############################################################################
# SPYANSWER! - version 0.8                                                    #
# an answer-and-question trivia game (like Jeopardy!) for the Spyder IDE      #
# by Adam Rudy (arudy@ualberta.ca)                                            #
# written for the ENCMP 100 Programming Contest at the University of Alberta  #
###############################################################################

import matplotlib.pyplot as plt
import matplotlib.font_manager as font
import numpy as np
import time
import sys

## Global variables kept here for efficiency, etc
categories = ["These","Are","Not","Actual","Jeopardy","Categories"]
quest = ["This is a question", "This is a question", "This is a question", "This is a question", "This is a question", "This is a question"]
questions = [quest, quest, quest, quest, quest]
scores = [0,0,0]
pBuzz = 0
catSet = font.FontProperties(size="24", weight="bold")
tileSet = font.FontProperties(size="36", weight="bold")
gridcolours = np.full((6,6), "#010D8C")
scorecolours = np.full((2,3), "#010D8C")

def main(): # The heart and soul (not really) of the program
    #fancy intro to the game
    global players
    players = []
    print("[=========== This... ===========]", end="")
    time.sleep(1.5)
    print("\r[============ is... ============]", end="")
    time.sleep(1.5) # huge ascii block coming up. woah
    print("\r███████╗██████╗ ██╗   ██╗ █████╗ ███╗   ██╗███████╗██╗    ██╗███████╗██████╗ ██╗\n██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║██╔════╝██║    ██║██╔════╝██╔══██╗██║\n███████╗██████╔╝ ╚████╔╝ ███████║██╔██╗ ██║███████╗██║ █╗ ██║█████╗  ██████╔╝██║\n╚════██║██╔═══╝   ╚██╔╝  ██╔══██║██║╚██╗██║╚════██║██║███╗██║██╔══╝  ██╔══██╗╚═╝\n███████║██║        ██║   ██║  ██║██║ ╚████║███████║╚███╔███╔╝███████╗██║  ██║██╗\n╚══════╝╚═╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚═╝")
    time.sleep(0.5) 
    print("Version %-11s %60s\n" % ("0.8", "Written by Adam Rudy"))
    
    for i in range(3):
        pname = str(input("[-------- Player %d name --------] > " % (i+1)))
        players += [pname]
    print("[== Player 1 buzzes in with A ==]")
    print("[== Player 2 buzzes in with B ==]")
    print("[== Player 3 buzzes in with L ==]\n")
    round(1)
    round(2)
    print("[========= GAME OVER! =========]") 

def round(num): #This function handles the basic gameplay loop
    rnddiv = 200*num
    col1 = [rnddiv*1] * 6
    col2 = [rnddiv*2] * 6
    col3 = [rnddiv*3] * 6
    col4 = [rnddiv*4] * 6
    col5 = [rnddiv*5] * 6
    print("[======= ROUND %d START!! =======]\n" % num)
    
    (tablecells, cellsum) = graphics(col1, col2, col3, col4, col5) # initial rendering of the board
    
    # Checking that there are still spaces on the board left
    while cellsum != 0:        
        error = False
        cat = input("[------ Select a category ------] > ")
        
        try: # Error handling - making sure that cat can be an integer
            int(cat) # I realize that decimals just end up ignored -- that's fine honestly
        except ValueError:
            error = True
        
        if cat == "exit":
            sys.exit("[========= Game ended! =========]")
        elif error:
            errors(1)
        elif int(cat) < 1 or int(cat) > 6: #there are only 6 categories. restart
            errors(1)
        else:
            cat = int(cat) - 1
            wager = input("[--------- Your wager? ---------] > ")
            
            try: # more error handling :)
                indexes = int(wager)/rnddiv # important
            except ValueError:
                error = True
            
            if error:
                errors(2)
            elif indexes < 1 or indexes > 5:
                errors(2)
            elif tablecells[int(indexes)][cat] == 0: #cant select a tile that was already selected
                errors(2)
            else:
                match indexes:
                    case 1|2|3|4|5:
                        question(cat, indexes-1)
                        pBuzz = buzzer()
                        
                        if indexes == 1:
                            col1[cat] = 0
                        elif indexes == 2:
                            col2[cat] = 0
                        elif indexes == 3:
                            col3[cat] = 0
                        elif indexes == 4:
                            col4[cat] = 0
                        else:
                            col5[cat] = 0
                        
                        if pBuzz == 3:
                            print("[### No answer! Moving on... ###]")
                        else: # if pBuzz is anything other than 0, 1, 2 or 3 we have bigger problems
                            scores[pBuzz] = scores[pBuzz] + int(rnddiv*indexes)#adds value of the tile to player's score
                        (tablecells, cellsum) = graphics(col1, col2, col3, col4, col5) #refreshes graphics to reflect the updated board
                    
                    case other: #you can't wager other values than the ones that are on the board
                        errors(2)
        print()
    print("[=== All questions selected! ===]\n")

def buzzer(): # This function handles the "buzzer" for each answer.
    # A 5-second countdown before you can buzz in.
    print()
    for i in range(1,6):
        countdown = abs(6-i)
        print("\r[============== %d ==============]" % countdown, end="")
        time.sleep(1)
    print("\r[============= GO! =============]")
    
    #the idea here is that the first person to buzz in will be the first to type thus yeah
    buzz = str(input("[-------- Buzz in now!! --------] > "))
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
            pBuzz = 3 # special condition for if no one answered at all
            break
    return pBuzz

def graphics(col1, col2, col3, col4, col5): #This function handles drawing the game's graphics.
   
    #These variables take pre-existing lists and arrange them into something usable
    tablecells = [categories, col1, col2, col3, col4, col5 ]
    scorecells = [players, scores]
    cellsum = np.sum(col1)+np.sum(col2)+np.sum(col3)+np.sum(col4)+np.sum(col5)
    
    #base figure everything goes onto this thing
    plt.figure(figsize=(12,1),dpi=100,facecolor="#0567D2")
    
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
                if str(cellText) == "Text(0, 0, '0')":
                    cellText.set_color("#010D8C")
                else:
                    cellText.set_color("#D69F4C")
                cellText.set_fontproperties(tileSet)
            
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
    return (tablecells, cellsum)

def question(cat, indexes): # This function displays answers (yes these are answers and NOT questions)
    text = np.array(questions[int(indexes)][int(cat)])
    text.resize(1,1)
    plt.figure(figsize=(6,7),dpi=100,facecolor="#0567D2")
    displayQ = plt.table(text, loc='center', cellLoc='center', cellColours=np.full((1,1), "#010D8C"))
    displayQ.scale(2,26)
    displayQ.auto_set_font_size(False)
    cellText = displayQ[(0,0)].get_text()
    cellText.set_color("white")
    cellText.set_fontproperties(catSet)
    plt.gca().get_xaxis().set_visible(False)
    plt.gca().get_yaxis().set_visible(False)
    plt.box(on=None)
    plt.show()

def errors(q): # This functions handles invalid inputs and what to return
    if q == 1:
        print("[###### Invalid category! ######]")
    elif q == 2:
        print("[####### Invalid wager!! #######]")

main()