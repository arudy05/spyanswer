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
import json

# Global variables kept here for convenience
players = []
scores = [0,0,0]
catSet = font.FontProperties(size="16", weight="bold")
tileSet = font.FontProperties(size="24", weight="bold")
gridcolours = np.full((6,6), "#010D8C")
scorecolours = np.full((2,3), "#010D8C")

def main(): # The heart and soul (not really) of the program
    #A fancy intro to the game
    print("This... ", end="")
    time.sleep(1.5)
    print("is... ")
    time.sleep(1.5)
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
    # Some minor error handling for if the JSON file is deemed invalid
    if categories == 0: 
        return
    rnddiv = 200*num
    tiles = [categories, [rnddiv*1]*6, [rnddiv*2]*6, [rnddiv*3]*6, [rnddiv*4]*6, [rnddiv*5]*6]
    print("[======= ROUND %d START!! =======]\n" % num)
    # Initial rendering of the board
    (tablecells, cellsum) = graphics(tiles)
    pBoard = 0
    # Checking that there are still spaces on the board left
    while cellsum != 0:        
        error = False
        print("%s, it's your board!" % players[pBoard])
        cat = input("Select a category > ")
        # Error handling - making sure that cat can be an integer
        try:
            int(cat)
        except ValueError:
            error = True
        # If there is an error or cat is not between 1 and 6 inclusive, return an error.
        if error or int(cat) < 1 or int(cat) > 6:
            errors(1)
        else:
            cat = int(cat) - 1
            wager = input("For how much? > ")
            #Error handling - making sure that the wager can be an integer
            try:
                indexes = int(wager)/rnddiv # used to check to see if the wager is actually on the board, among other things
            except ValueError:
                error = True
            # If there is an error or the index variable is not between 1 and 5 inclusive, return an error.
            if error or indexes < 1 or indexes > 5:
                errors(2)
            # If the tile was already selected, return an error
            elif tablecells[int(indexes)][cat] == 0:
                errors(2)
            # If the value of the tile is divisible by the value of the lowest possible wager, proceed
            elif indexes in (1, 2, 3, 4, 5):
                # Get the corresponding question, display it and make sure the tile cannot be selected anymore
                selected = questions[int(cat)][int(indexes-1)]
                displayQuestion(selected)
                tiles[int(indexes)][cat] = 0
                # Prompt players to buzz in and answer until one of them gets it right
                pBoard = answer(selected, answers, pBoard, rnddiv, indexes)
                (tablecells, cellsum) = graphics(tiles)
            else:
                errors(2)
        print()
    print("[=== All questions selected! ===]\n")

def loadquestions(file): # This function loads answers, categories and questions from a JSON file
    # These are not stored as global variables to avoid cheating (yes i know it's unlikely but still).
    answers = {}
    categories = []
    questions = []
    #Opens JSON file containing categories, answers and questions
    file = open(file, 'r')
    a = json.load(file)
    #Checks to make sure the JSON file is valid by looking for a specific entry
    if a["key"] != "trebek":
        errors(3)
        # Special condition that will force the game back to the menu
        return(0,0,0)
    else:
        for i in range(len(a["category"])):
            # Assigns temporary variables
            questemp = []
            b = str(i+1)
            # Gets the name of the category, stores it in a list
            categories.append(a["category"][b]["name"])
            # Gets all questions under a category and stores it in a list within the "questions" list
            for j in range(len(a["category"][b])-1):
                c = str(j+1)
                questemp.append(a["category"][b][c]["name"])
                answers[a["category"][b][c]["name"]] = set(a["category"][b][c]["answers"]) 
            questions.append(questemp) 
        #Checks to make sure that categories have an appropriate number of answers
        if len(categories) != 6 or len(questions) != 6 or len(questions[0]) != 5:
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
    #I have to individually set every single cell's text's formatting. fun
    for i in range(0,6): 
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
    #Again - individually setting every cell's text formatting.
    for i in range(0,2):
        for j in range(0,3):
            scoreText = score[(i,j)].get_text()
            if i == 0:
                scoreText.set_color("white")
                scoreText.set_fontproperties(catSet)
            else:
                scoreText.set_color("#D69F4C")
                scoreText.set_fontproperties(tileSet)
    
    #Removes graph-specific stuff and shows the "plot"
    plt.gca().get_xaxis().set_visible(False)
    plt.gca().get_yaxis().set_visible(False)
    plt.box(on=None)
    plt.show()
    return(tiles, cellsum)

def displayQuestion(selected): # This function displays questions (technically answers but whatever)
    # Puts the text of the question into an array so that it can be put into a matplotlib table
    # Also resizes the array so that matplotlib doesn't throw a fit
    text = np.array(selected) 
    text.resize(1,1)
    # Creates a figure and does all of the formatting necessary for it similar to graphics().
    plt.figure(figsize=(6,7),dpi=100,facecolor="#0567D2")
    displayQ = plt.table(text, loc='center', cellLoc='center', cellColours=np.full((1,1), "#010D8C"))
    displayQ.scale(2,26)
    displayQ.auto_set_font_size(False)
    cellText = displayQ[(0,0)].get_text()
    cellText.set_color("white")
    # Removes graph-sepcific stuff and prints the question
    cellText.set_fontproperties(catSet)
    plt.gca().get_xaxis().set_visible(False)
    plt.gca().get_yaxis().set_visible(False)
    plt.box(on=None)
    plt.show()

def answer(selected, answers, pBoard, rnddiv, indexes): # This function handles processing player answers
    # Calls the buzzer function and checks that it returns a value of either 0, 1 or 2
    pBuzz = buzzer()
    while pBuzz != 3:
        # Prompts first player to buzz in to answer
        response = input("%s, your answer? " % players[pBuzz])
        # Answers to a question are stored in a set in a dict entry name after the question
        if response in answers[selected]:
            print("That's correct!")
            break
        else:
            # Subtracts score from player who answered wrong and asks the players to buzz in again
            print("Regrettably, no.")
            scores[pBuzz] = scores[pBuzz] - int(rnddiv*indexes)
            pBuzz = buzzer()
    # Special condition for if nobody answers correctly
    if pBuzz == 3:
        print("[### No answer! Moving on... ###]")
        return pBoard
    else:
        # Adds score to player who got the question right and tells that player to pick the next question
        scores[pBuzz] = scores[pBuzz] + int(rnddiv*indexes)
        pBoard = pBuzz
        return pBoard
    
def buzzer(): # This function handles the "buzzer" for each answer.
    # A 3-second countdown before you can buzz in.
    print()
    for i in range(1,4):
        countdown = abs(4-i)
        print("\r[============== %d ==============]" % countdown, end="")
        time.sleep(1)
    print("\r[============= GO! =============]")
    
    #the idea here is that the first person to buzz in will be the first to type thus yeah
    buzz = str(input("Buzz in & press ENTER! > "))
    bnum = 0
    while True:
        # Checks that the "buzz" string contains at least one of the defined buzzer keys
        # Otherwise, assumes that nobody answered
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
        # If none of the defined buzzer keys are in the "buzz" string, this would return an IndexError.
        # If this happens, assume nobody answered and move on.
        except IndexError:
            pBuzz = 3
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