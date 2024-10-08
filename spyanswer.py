import matplotlib.pyplot as plt
import numpy as np

categories = ["Category Name","Another Category","Yet Another\nCategory","Running out\nof ideas","Please help","qwertyuiop"]
answer1 = [200,200,200,200,200,200]
answer2 = [400,400,400,400,400,400]
answer3 = [600,600,600,600,600,600]
answer4 = [800,800,800,800,800,800]
answer5 = [1000,1000,1000,1000,1000,1000]

def showgrid():
    tablecells = [categories, answer1, answer2, answer3, answer4, answer5 ]
    plt.figure(figsize=(16,9),dpi=200)
    plt.table(tablecells,loc='center',cellLoc='center').scale(1,6)
    plt.gca().get_xaxis().set_visible(False)
    plt.gca().get_yaxis().set_visible(False)
    plt.box(on=None)
    plt.show()

while sum(answer1)+sum(answer2)+sum(answer3)+sum(answer4)+sum(answer5) != 0:    
    showgrid()
    cat = int(input("Select a category (1-6, L-R): "))
    if cat < 1 or cat > 6:
        print("Not a valid category!\n")
    else:
        wager = int(input("For how much? "))
        if wager == 200:
            answer1[cat-1] = 0
        elif wager == 400:
            answer2[cat-1] = 0
        elif wager == 600:
            answer3[cat-1] = 0
        elif wager == 800:
            answer4[cat-1] = 0
        elif wager == 1000:
            answer5[cat-1] = 0
        else:
            print("Not a valid wager!\n")

print("All questions selected! Game over!")