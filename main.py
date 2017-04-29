#For testing purposes only
from ann import Ann
from breeding import *
import random
import operator

loveShack = Breeding()
loveShack.initialize()
for ann in loveShack.data:
    ann.setScore(randint(0, 900))

loveShack.getNextGeneration()
