from ann import Ann
import operator
import random
from breeding import Breeding

loveShack = Breeding()
lovers = []

for i in range(0, 4):
    lovers.append(Ann())
    lovers[i].giveName("John")
    score = random.uniform(0, 100)
    lovers[i].setScore(score)
    lovers[i].Print()

print
print "Lets Make Love!!!"
print

loveShack.getGen(lovers)
loveShack.getNextGeneration()


