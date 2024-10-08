import matplotlib.pyplot as plt

def game():
    while sum(answer1)+sum(answer2)+sum(answer3)+sum(answer4)+sum(answer5) != 0:    
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
        #the gameplay
        cat = int(input("Select a category (1-6, L-R): "))
        if cat < 1 or cat > 6:
            print("Not a valid category!")
        else:
            wager = int(input("For how much? "))
            if tablecells[int(wager/rnddiv)][cat-1] == 0:
                print("Tile already selected!")
            elif wager == rnddiv:
                answer1[cat-1] = 0
                scores[0] = scores[0] + rnddiv
            elif wager == rnddiv*2:
                answer2[cat-1] = 0
                scores[0] = scores[0] + rnddiv*2
            elif wager == rnddiv*3:
                answer3[cat-1] = 0
                scores[0] = scores[0] + rnddiv*3
            elif wager == rnddiv*4:
                answer4[cat-1] = 0
                scores[0] = scores[0] + rnddiv*4
            elif wager == rnddiv*5:
                answer5[cat-1] = 0
                scores[0] = scores[0] + rnddiv*5
            else:
                print("Not a valid wager!")
        print()
    print("All questions selected! Game over!")

categories = ["These","Are","Not","Actual","Jeopardy","Categories"]
players = []
scores = [0,0,0]
print("This.. is... JEOPARDY!\n")
for i in range(3):
    pname = str(input("Player %i: " % (i+1)))
    players += [pname]
rnd = int(input("What round would you like to play? "))
print()
if rnd == 1:
    answer1 = [200,200,200,200,200,200]
    answer2 = [400,400,400,400,400,400]
    answer3 = [600,600,600,600,600,600]
    answer4 = [800,800,800,800,800,800]
    answer5 = [1000,1000,1000,1000,1000,1000]
    rnddiv = 200
    game()
elif rnd == 2:
    answer1 = [400,400,400,400,400,400]
    answer2 = [800,800,800,800,800,800]
    answer3 = [1200,1200,1200,1200,1200,1200]
    answer4 = [1600,1600,1600,1600,1600,1600]
    answer5 = [2000,2000,2000,2000,2000,2000]
    rnddiv = 400
    game()
else:
    print("Not a valid round type!")