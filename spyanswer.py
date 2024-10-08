import matplotlib.pyplot as plt
import numpy as np

def buzzer():
    buzz = str(input("Buzz in and press ENTER! "))
    global pBuzz
    if buzz[0] == "a":
        pBuzz = 0 #Player 1
    elif buzz[0] == "b":
        pBuzz = 1 # Player 2
    elif buzz[0] == "l":
        pBuzz = 2 # Player 3

def game():
    # Checking that there are still spaces on the board left
    while np.sum(answer1)+np.sum(answer2)+np.sum(answer3)+np.sum(answer4)+np.sum(answer5) != 0:    
        #Format and display score and grid
        tablecells = [categories, answer1, answer2, answer3, answer4, answer5 ]
        scorecells = [players, scores]
        plt.figure(figsize=(12,2),dpi=100)
        grid = plt.table(tablecells,loc='top',cellLoc='center')
        grid.scale(2,8)
        grid.auto_set_font_size(False)
        grid.set_fontsize(24)
        score = plt.table(scorecells,loc='bottom',cellLoc='center')
        score.scale(2,6)
        score.auto_set_font_size(False)
        score.set_fontsize(24)
        plt.gca().get_xaxis().set_visible(False)
        plt.gca().get_yaxis().set_visible(False)
        plt.box(on=None)
        plt.show()
        #The actual gameplay
        cat = int(input("Select a category (1-6, L-R): "))
        if cat < 1 or cat > 6:
            print("Not a valid category!")
        else:
            wager = int(input("For how much? "))
            if tablecells[int(wager/rnddiv)][cat-1] == 0:
                print("Tile already selected!")
            elif wager == rnddiv:
                buzzer()
                answer1[cat-1] = 0
                scores[pBuzz] = scores[pBuzz] + rnddiv
            elif wager == rnddiv*2:
                buzzer()
                answer2[cat-1] = 0
                scores[pBuzz] = scores[pBuzz] + rnddiv*2
            elif wager == rnddiv*3:
                buzzer()
                answer3[cat-1] = 0
                scores[pBuzz] = scores[pBuzz] + rnddiv*3
            elif wager == rnddiv*4:
                buzzer()
                answer4[cat-1] = 0
                scores[pBuzz] = scores[pBuzz] + rnddiv*4
            elif wager == rnddiv*5:
                buzzer()
                answer5[cat-1] = 0
                scores[pBuzz] = scores[pBuzz] + rnddiv*5
            else:
                print("Not a valid wager!")
        print()
    print("All questions selected! Game over!")

categories = ["These","Are","Not","Actual","Jeopardy","Categories"]
players = []
scores = [0,0,0]
pBuzz = 0
print("This.. is... JEOPARDY!\n")
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
    print("Not a valid round type!")