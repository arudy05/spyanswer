###############################################################################
# SPYANSWER! - version 1.1                                                    #
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
scores = []
version = "1.1"
catSet = font.FontProperties(size="16", weight="bold")
tileSet = font.FontProperties(size="24", weight="bold")
gridcolours = np.full((6, 6), "#010D8C")

def main():  
    titlescreen(version)
    choice = menu()
    while choice != 0:
        if choice == 1:
            clearvars()
            playerSetup()
            game(1, "categories1.json")
            game(2, "categories2.json")
            gameEndScreen()
            titlescreen(version)
        if choice == 2:
            creditsScreen()
            titlescreen(version)
        else:
            pass
        choice = menu()
    print("Goodbye!")

# The program's "main menu"
def menu():
    choice = input("Select an option > ")
    while not choice.isdigit() or not choice in ("0", "1", "2"):
        choice = input("Select an option > ")
    choice = int(choice)
    return choice

# This function handles the basic gameplay loop
def game(num, file):  
    (categories, answers, questions) = loadquestions(file)
    # Some minor error handling for if the JSON file is deemed invalid
    if categories == 0:
        return
    rnddiv = 200*num
    tiles = [categories, [rnddiv*1]*6, [rnddiv*2] *
             6, [rnddiv*3]*6, [rnddiv*4]*6, [rnddiv*5]*6]
    print("[======= ROUND %d START!! =======]\n" % num)
    pBoard = 0
    # Initial rendering of the board
    (tablecells, cellsum) = graphics(tiles, pBoard)
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
        # Special command to end the current round
        if cat == "end":
            break
        # If there is an error or cat is not between 1 and 6 inclusive, return an error.
        elif error or int(cat) < 1 or int(cat) > 6:
            errors(1)
        else:
            cat = int(cat) - 1
            wager = input("For how much? > ")
            # Error handling - making sure that the wager can be an integer
            try:
                # used to check to see if the wager is actually on the board, among other things
                indexes = int(wager)/rnddiv
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
                tiles[int(indexes)][cat] = 0
                # Prompt players to buzz in and answer until one of them gets it right
                pBoard = answer(selected, answers, pBoard, rnddiv, indexes)
                (tablecells, cellsum) = graphics(tiles, pBoard)
            else:
                errors(2)
        print()
    print("[=== All questions selected! ===]\n")

# This function loads answers, categories and questions from a JSON file
def loadquestions(file):
    # These are not stored as global variables to avoid cheating (yes i know it's unlikely but still).
    answers = {}
    categories = []
    questions = []
    # Opens JSON file containing categories, answers and questions
    file = open(file, 'r')
    error = False
    try:
        a = json.load(file)
    except:
        error = True
    if error:
        errors(3)
        return (0, 0, 0)
    # Checks to make sure the JSON file is valid by looking for a specific entry
    elif a["key"] != "trebek":
        errors(3)
        # Special condition that will force the game back to the menu
        return (0, 0, 0)
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
                answers[a["category"][b][c]["name"]] = set(
                    a["category"][b][c]["answers"])
            questions.append(questemp)
        # Checks to make sure that categories have an appropriate number of answers
        if len(categories) != 6 or len(questions) != 6 or len(questions[0]) != 5:
            errors(3)
            return (0, 0, 0)
        else:
            return (categories, answers, questions)
    file.close()

# This function handles drawing the game's graphics.
def graphics(tiles, pBoard):

    # These variables take pre-existing lists and arrange them into something usable
    cellsum = (np.sum(tiles[1]) + np.sum(tiles[2]) + np.sum(tiles[3]) +
               np.sum(tiles[4]) + np.sum(tiles[5]))

    # base figure everything goes onto this thing
    plt.figure(figsize=(15, 9), dpi=100, facecolor="#191CA1")

    # Draws the grid with all the answer values and everything
    grid = plt.table(tiles, loc='upper center',
                     cellLoc='center', cellColours=gridcolours)
    grid.scale(1, 5)
    grid.auto_set_font_size(False)
    # I have to individually set every single cell's text's formatting. fun
    for i in range(0, 6):
        for j in range(0, 6):
            cellText = grid[(i, j)].get_text()
            if i == 0:
                cellText.set_color("white")
                cellText.set_fontproperties(catSet)
            else:
                # If the cell's value is 0, "hide" it.
                if str(cellText) == "Text(0, 0, '0')":
                    cellText.set_color("#010D8C")
                else:
                    cellText.set_color("#D69F4C")
                cellText.set_fontproperties(tileSet)

    # Draws the table with player scores
    showscores([players, scores], pBoard)

    # Removes graph-specific stuff and shows the "plot"
    showfigure()
    return (tiles, cellsum)

# This function displays questions (technically answers but whatever)
def displayQuestion(selected):
    # Puts the text of the question into an array so that it can be put into a matplotlib table
    # Also resizes the array so that matplotlib doesn't throw a fit
    text = np.array(selected)
    text.resize(1, 1)

    # Creates a figure and does all of the formatting necessary for it similar to graphics().
    plt.figure(figsize=(15, 9), dpi=100, facecolor="#191CA1")
    displayQ = plt.table(text, loc='upper center', cellLoc='center',
                         cellColours=np.full((1, 1), "#010D8C"))
    displayQ.scale(1, 30)
    displayQ.auto_set_font_size(False)
    cellText = displayQ[(0, 0)].get_text()
    cellText.set_color("white")
    showscores([players, scores], 3)
    cellText.set_fontproperties(tileSet)
    showfigure()

# This function handles processing player answers
def answer(selected, answers, pBoard, rnddiv, indexes):
    # Calls the buzzer function and checks that it returns a value of either 0, 1 or 2
    displayQuestion(selected)
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
            displayQuestion(selected)
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

# This function handles the "buzzer" for each answer.
def buzzer():
    # A 3-second countdown before you can buzz in.
    print()
    for i in range(1, 4):
        countdown = abs(4-i)
        print("\r[============== %d ==============]" % countdown, end="")
        time.sleep(1)
    print("\r[============= GO! =============]")

    # the idea here is that the first person to buzz in will be the first to type thus yeah
    buzz = str(input("Buzz in & press ENTER! > "))
    bnum = 0
    while True:
        # Checks that the "buzz" string contains at least one of the defined buzzer keys
        # Otherwise, assumes that nobody answered
        try:
            if buzz[bnum] == "a":
                pBuzz = 0  # Player 1
                break
            elif buzz[bnum] == "b":
                pBuzz = 1  # Player 2
                break
            elif buzz[bnum] == "l":
                pBuzz = 2  # Player 3
                break
            else:
                bnum = bnum+1
        # If none of the defined buzzer keys are in the "buzz" string, this would return an IndexError.
        # If this happens, assume nobody answered and move on.
        except IndexError:
            pBuzz = 3
            break
    return pBuzz

# This functions handles invalid inputs and what to return
def errors(q):
    if q == 1:
        print("##### Invalid category!")
    elif q == 2:
        print("##### Invalid wager!")
    elif q == 3:
        print("##### Invalid JSON file!")

# This function displays the title screen
def titlescreen(version):
    # Defining fonts to be used
    titleSet = font.FontProperties(size="16", family="monospace")
    textSet = font.FontProperties(size="24", weight="bold", family="monospace")
    asciiTitle = "███████╗██████╗ ██╗   ██╗ █████╗ ███╗   ██╗███████╗██╗    ██╗███████╗██████╗ ██╗\n██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║██╔════╝██║    ██║██╔════╝██╔══██╗██║\n███████╗██████╔╝ ╚████╔╝ ███████║██╔██╗ ██║███████╗██║ █╗ ██║█████╗  ██████╔╝██║\n╚════██║██╔═══╝   ╚██╔╝  ██╔══██║██║╚██╗██║╚════██║██║███╗██║██╔══╝  ██╔══██╗╚═╝\n███████║██║        ██║   ██║  ██║██║ ╚████║███████║╚███╔███╔╝███████╗██║  ██║██╗\n╚══════╝╚═╝        ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚═╝"

    # Formatting the figure accordingly
    fig = plt.figure(figsize=(15, 9), dpi=100, facecolor="#191CA1")
    ax = fig.add_subplot()
    ax.axis([0, 10, 0, 10])
    # Text elements on the menu
    ax.text(5, 8, asciiTitle, va="center", ha="center", color="#D69F4C",
            linespacing=1.1, fontproperties=titleSet)
    ax.text(9.5, 6.5, "Version " + version, va="center", ha="right",
            color="white", fontproperties=titleSet)
    ax.text(5, 2, "1 - Start Game\n2 ---- Credits\n0 ------- Quit",
            va="center", ha="center", color="white", fontproperties=textSet,
            linespacing=1.5)
    showfigure()

# This function dispplays credits and acknowledgements
def creditsScreen():  
    yap = 'SPYANSWER! (a portmanteau of "Spyder" and "answer"):\nan answer-and question trivia game based off of the "Jeopardy!" game show\ncreated for the ENCMP 100 Programming Contest at the University of Alberta\nduring the 2024 winter term and written by Adam Rudy (arudy@ualberta.ca).\n\nJeopardy! was created by Merv Griffin and is a registered trademark of\nJeopardy Productions, Inc. - an entity which I am in no way, shape or form\nassociated with. This program was created as an homage to the show and aims \nto recreate it as faithfully as possible (within reason).'
    fig = plt.figure(figsize=(15, 9), dpi=100, facecolor="#191CA1")
    ax = fig.add_subplot()
    ax.axis([0, 10, 0, 10])
    ax.text(5, 6, yap, fontproperties=catSet, ha="center", va="center",
            color="white", linespacing=1.5)
    ax.text(5, 2, "Press ENTER to return to the title screen.",
            fontproperties=catSet, ha="center", va="center",
            color="white", linespacing=1.5)
    showfigure()
    input("Press ENTER to return to the title screen.")

# This function sets up the "score" table
def showscores(scorecells, pBoard):  
    # Formatting the table
    score = plt.table(scorecells, loc='lower center', cellLoc='center',
                      edges="BT")
    score.scale(1, 4)
    score.auto_set_font_size(False)
    # Set cell/text formatting
    for i in range(0, 2):
        for j in range(0, 3):
            scoreText = score[(i, j)].get_text()
            score[(i, j)].set(edgecolor="black", linewidth=3)
            if i == 0:
                # Player names are white
                scoreText.set_color("white")
                scoreText.set_fontproperties(catSet)
            else:
                # Scores are yellow
                scoreText.set_color("#D69F4C")
                scoreText.set_fontproperties(tileSet)
            if j == pBoard:
                score[(i, j)].set(edgecolor="#D69F4C", linewidth=3)
            else:
                score[(i, j)].set(edgecolor="black", linewidth=3)

# A handful of lines that get repeated in a lot of places and thus get their own function.
def showfigure():
    plt.gca().get_xaxis().set_visible(False)
    plt.gca().get_yaxis().set_visible(False)
    plt.box(on=None)
    plt.show()

# This function gets player names in a more "interactive" format
def playerSetup():  
    print("[===== Enter player names! =====]")
    keys = ["A", "B", "L"]
    for i in range(3):

        fig = plt.figure(figsize=(15, 9), dpi=100, facecolor="#191CA1")
        ax = fig.add_subplot()
        ax.axis([0, 10, 0, 10])
        showscores([players, scores], i)
        words = "Player %d buzzes in with %s" % (i+1, keys[i])
        ax.text(5, 5, words, ha="center",
                fontproperties=tileSet, color="white")
        showfigure()

        pname = str(input("Player %d > " % (i+1)))
        players.insert(i, pname)
        players.pop(3)

# This function displays final scores and indicates the winner of the game
def gameEndScreen():  
    # Create base figure
    fig = plt.figure(figsize=(15, 9), dpi=100, facecolor="#191CA1")
    ax = fig.add_subplot()
    ax.axis([0, 10, 0, 10])

    print("[========= GAME OVER!! =========]")
    # Checks to see if there is a tie between players.
    case = [i for i, val in enumerate(scores) if val == max(scores)]
    if len(case) == 1:
        words = "%s wins the game!" % players[case[0]]
        index = case[0]
    elif len(case) == 2:
        words = "There is a tie between\n%s and %s." % (
            players[case[0]], players[case[1]])
        index = 3
    else:
        words = "There is a three way tie! How absurd!"
        index = 3
    # Finishes figure, outputs it and waits 5 seconds before ending the function.
    showscores([players, scores], index)
    ax.text(5, 5, words, ha="center", fontproperties=tileSet, color="white")
    showfigure()
    time.sleep(5)

# Clears players and scores variables and prepares them for use in a game
def clearvars():  
    players.clear()
    scores.clear()
    for i in range(3):
        players.append("")
        scores.append(0)


main()
