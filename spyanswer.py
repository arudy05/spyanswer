###############################################################################
# SPYANSWER! - version 1.0.2                                                  #
# an answer-and-question trivia game (like Jeopardy!) for the Spyder IDE      #
# by Adam Rudy (arudy@ualberta.ca)                                            #
# written for the ENCMP 100 Programming Contest at the University of Alberta  #
###############################################################################

import matplotlib.pyplot as plt
import matplotlib.font_manager as font
import numpy as np
import time
import sys
import json

## Global variables kept here for convenience
players = []
scores = [0,0,0]
catSet = font.FontProperties(size="16", weight="bold")
tileSet = font.FontProperties(size="24", weight="bold")
gridcolours = np.full((6,6), "#010D8C")
scorecolours = np.full((2,3), "#010D8C")

def main(): # The heart and soul (not really) of the program
    #fancy intro to the game
    print("This... ", end="")
    time.sleep(1.5)
    print("is... ")
    time.sleep(1.5) # huge ascii block coming up. woah
    print("███████╗██████╗ ██╗   ██╗ █████╗ ███╗   ██╗███████╗██╗    ██╗███████╗██████╗ ██╗\n██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║██╔════╝██║    ██║██╔════╝██╔══██╗██║\n███████╗██████╔╝ ╚████╔╝ ███████║██╔██╗ ██║███████╗██║ █╗ ██║█████╗  ██████╔╝██║\n╚════██║██╔═══╝   ╚██╔╝  ██╔══██║██║╚██╗██║╚════██║██║███╗██║██╔══╝  ██╔══██╗╚═╝\n███████║██║        ██║   ██║  ██║██║ ╚████║███████║╚███╔███╔╝███████╗██║  ██║██╗\n╚══════╝╚═╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚═╝")
    time.sleep(0.5) 
    print("Version %-11s %60s\n" % ("1.0.2", "Written by Adam Rudy"))
    
    # The menu!
    choice = menu()
    while choice != 0:
        players.clear()
        if choice == 1:
            print("\n[== Player 1 buzzes in with A ==]")
            print("[== Player 2 buzzes in with B ==]")
            print("[== Player 3 buzzes in with L ==]\n")
            print("[===== Enter player names! =====]")
            for i in range(3):
                pname = str(input("Player %d > " % (i+1)))
                players.append(pname)
            game(1, "categories.json")
            game(2, "categories1.json")
        else:
            print("Invalid choice!\n")
        choice = menu()
    print("Goodbye!")

def menu(): # The program's "main menu"
    print("[========== MAIN MENU ==========]")
    print("%5s %22s" % ("1", "Start Game"))
    print("%5s %22s" % ("0", "Exit"))
    choice = input("Select an option > ")
    while not choice.isdigit() or not choice in ("0", "1"):
        choice = input("Select an option > ")
    choice = int(choice)
    return choice

def game(num, file): #This function handles the basic gameplay loop                
    (categories, answers, questions) = loadquestions(file)
    if categories == 0:
        return
    rnddiv = 200*num
    tiles = [categories, [rnddiv*1]*6, [rnddiv*2]*6, [rnddiv*3]*6, [rnddiv*4]*6, [rnddiv*5]*6]
    print("[======= ROUND %d START!! =======]\n" % num)
    
    (tablecells, cellsum) = graphics(tiles) # initial rendering of the board
    pBuzz = 0
    pBoard = 0
    # Checking that there are still spaces on the board left
    while cellsum != 0:        
        error = False
        print("%s, it's your board!" % players[pBoard])
        cat = input("Select a category > ")
        
        try: # Error handling - making sure that cat can be an integer
            int(cat) # I realize that decimals just end up ignored -- that's fine honestly
        except ValueError:
            error = True
        if error:
            errors(1)
        elif int(cat) < 1 or int(cat) > 6: #there are only 6 categories. restart
            errors(1)
        else:
            cat = int(cat) - 1
            wager = input("For how much? > ")
            
            try: # more error handling :)
                indexes = int(wager)/rnddiv # used to check to see if the wager is actually on the board, among other things
            except ValueError:
                error = True
            
            if error:
                errors(2)
            elif indexes < 1 or indexes > 5: # wager too big or too small
                errors(2)
            elif tablecells[int(indexes)][cat] == 0: #cant select a tile that was already selected
                errors(2)
            
            else:
                match indexes:
                    case 1|2|3|4|5:
                        selected = questions[int(cat)][int(indexes-1)]
                        displayQuestion(selected) # Displays question, stores question text in a variable
                        tiles[int(indexes)][cat] = 0 #Sets the tile on the board to 0 (which will clear it on refresh)
                        pBoard = answer(selected, answers, pBoard, rnddiv, indexes)
                        (tablecells, cellsum) = graphics(tiles) #refreshes graphics to reflect the updated board
                    
                    case other: #you can't wager other values than the ones that are on the board
                        errors(2)
        print()
    print("[=== All questions selected! ===]\n")

def loadquestions(file): # This function loads answers, categories and questions from a JSON file
    answers = {} # this cannot be a global variable purely because it would be too easily accessible from Spyder's variable explorer
    categories = []
    questions = []
    file = open(file, 'r') # the file that contains categories, answers, and questions
    a = json.load(file)
    if a["key"] != "trebek": # checks to make sure that the JSON file is valid by looking for a "key" of sorts
        errors(3)
        return(0,0,0)
    else:
        for i in range(len(a["category"])):
            questemp = [] # temporary variable, cleared every iteration
            b = str(i+1)
            categories.append(a["category"][b]["name"]) # fetches all categories and puts them in a list
            for j in range(len(a["category"][b])-1):
                c = str(j+1)
                questemp.append(a["category"][b][c]["name"]) # fetches all questions for a category and puts them in a temporary list
                answers[a["category"][b][c]["name"]] = set(a["category"][b][c]["answers"]) 
            questions.append(questemp) # adds this category's questions as a new list within the questions list
        if len(categories) != 6 or len(questions) != 6:
            errors(3)
            return(0,0,0)
        else:
            return (categories, answers, questions)
    file.close()

def graphics(tiles): #This function handles drawing the game's graphics.
   
    #These variables take pre-existing lists and arrange them into something usable
    scorecells = [players, scores]
    cellsum = np.sum(tiles[1]) + np.sum(tiles[2]) + np.sum(tiles[3]) + np.sum(tiles[4]) + np.sum(tiles[5])
    
    #base figure everything goes onto this thing
    plt.figure(figsize=(15,9),dpi=100,facecolor="#0567D2")
    
    #Draws the grid with all the answer values and everything
    grid = plt.table(tiles,loc='upper center',cellLoc='center',cellColours=gridcolours)
    grid.scale(1,5)
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
    score = plt.table(scorecells,loc='lower center',cellLoc='center',cellColours=scorecolours)
    score.scale(1,4)
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
    return(tiles, cellsum)

def displayQuestion(selected): # This function displays questions (technically answers but whatever)
    text = np.array(selected) # puts the text into an array to be put into a matplotlib table
    text.resize(1,1)
    plt.figure(figsize=(6,7),dpi=100,facecolor="#0567D2")
    displayQ = plt.table(text, loc='center', cellLoc='center', cellColours=np.full((1,1), "#010D8C"))
    displayQ.scale(2,26)
    displayQ.auto_set_font_size(False)
    cellText = displayQ[(0,0)].get_text() #at least we only have to do this once instead of multiple times
    cellText.set_color("white")
    cellText.set_fontproperties(catSet)
    plt.gca().get_xaxis().set_visible(False)
    plt.gca().get_yaxis().set_visible(False)
    plt.box(on=None)
    plt.show()

def answer(selected, answers, pBoard, rnddiv, indexes): # This function handles processing player answers
    pBuzz = buzzer() # The buzzer function
    while pBuzz != 3:
        response = input("%s, your answer? " % players[pBuzz]) # prompts player for an answer
        responseCheck = False
        if response in answers[selected]: # checks all possible answers (set stored in a dict key named after the corresponding question)
            print("That's correct!")
            break
        else:
            print("Regrettably, no.")
            scores[pBuzz] = scores[pBuzz] - int(rnddiv*indexes) # subtracts score from player
            pBuzz = buzzer()
    if pBuzz == 3:
        print("[### No answer! Moving on... ###]")
        return pBoard
    else: # if pBuzz is anything other than 0, 1, 2 or 3 we have bigger problems
        scores[pBuzz] = scores[pBuzz] + int(rnddiv*indexes)#adds value of the tile to player's score
        pBoard = pBuzz
        return pBoard
    

def buzzer(): # This function handles the "buzzer" for each answer.
    # A 5-second countdown before you can buzz in.
    print()
    for i in range(1,6):
        countdown = abs(6-i)
        print("\r[============== %d ==============]" % countdown, end="")
        time.sleep(1)
    print("\r[============= GO! =============]")
    
    #the idea here is that the first person to buzz in will be the first to type thus yeah
    buzz = str(input("Buzz in & press ENTER! > "))
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

def errors(q): # This functions handles invalid inputs and what to return
    if q == 1:
        print("[###### Invalid category! ######]\n")
    elif q == 2:
        print("[####### Invalid wager!! #######]\n")
    elif q == 3:
        print("[##### Invalid JSON file!! #####]\n")

main()