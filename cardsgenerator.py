import random
num1 = random.randint(1,13)
num2 = random.randint(1,4)
cardnum1 = ""
cardnum2 = ""

faces = {1: "Ace of", 11: "Queen of", 12: "Jack of", 13: "King of"} # it's usually J Q K, though
cardnum1 = faces.get(num1, num1)
suits = {1: "Spades", 2: "Hearts", 3: "Diamonds", 4: "Clubs"}
cardnum2 = suits[num2]

print (cardnum1, cardnum2)
