import random

even = random.randrange(10,20,2)

cardnum1 = ""
cardnum2 = ""

faces = {1: "As", 11: "Queen", 12: "Jack", 13: "King"}
suits = {1: "Sekop", 2: "Hati", 3: "Wajik", 4: "Keriting"}

while even>0:
  num1 = random.randint(1,13)
  num2 = random.randint(1,4)
  cardnum1 = faces.get(num1, num1)
  cardnum2 = suits[num2]
  print (cardnum1, cardnum2)
  even-=1
