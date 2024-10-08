import matplotlib.pyplot as plt

def game():
    while sum(answer1)+sum(answer2)+sum(answer3)+sum(answer4)+sum(answer5) != 0:    
        tablecells = [categories, answer1, answer2, answer3, answer4, answer5 ]
        plt.figure(figsize=(12,6),dpi=100)
        grid = plt.table(tablecells,loc='center',cellLoc='center')
        grid.scale(1,6)
        grid.auto_set_font_size(False)
        grid.set_fontsize(16)
        plt.gca().get_xaxis().set_visible(False)
        plt.gca().get_yaxis().set_visible(False)
        plt.box(on=None)
        plt.show()
        cat = int(input("Select a category (1-6, L-R): "))
        if cat < 1 or cat > 6:
            print("Not a valid category!")
        else:
            wager = int(input("For how much? "))
            if tablecells[int(wager/rnddiv)][cat-1] == 0:
                print("Tile already selected!")
            elif wager == rnddiv:
                answer1[cat-1] = 0
            elif wager == rnddiv*2:
                answer2[cat-1] = 0
            elif wager == rnddiv*3:
                answer3[cat-1] = 0
            elif wager == rnddiv*4:
                answer4[cat-1] = 0
            elif wager == rnddiv*5:
                answer5[cat-1] = 0
            else:
                print("Not a valid wager!")
        print()
    print("All questions selected! Game over!")

categories = ["These","Are","Not","Actual","Jeopardy","Categories"]
print("This.. is... JEOPARDY!")
rnd = int(input("What round would you like to play? "))
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