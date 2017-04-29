from ann import Ann
from breeding import *
import random
import operator

loveShack = Breeding()
lovers = []

for i in range(0, ANN_COUNT):
    lovers.append(Ann())
    lovers[i].giveName("Tina")
    score = random.uniform(0, 500)
    lovers[i].setScore(score)

loveShack.setGen(lovers)
loveShack.getNextGeneration()
