'''
nes = open("won1_input.txt").read().splitlines()

data = []
for i in range(0, len(nes)):
    data.append([])
    for j in range(0, len(nes[0])):
        data[i].append(int (nes[i][j]))

for i in range(0, len(data)):
    for j in range(0, len(data[i])):
#        print data[i][j],
#    print '\n'

'''

lines = [line.rstrip('\n') for line in open('won1_labels.txt')]
labels = []
for line in lines:
    line = line.strip().split(' ')
    labels.append(line)
data = []
for line in lines:
    number_strings = line.split() # Split the line on runs of whitespace
    numbers = [float(n) for n in number_strings] # Convert to integers
    data.append(numbers) # Add the "row" to your list.

for i in range(0, len(data)):
    for j in range(0, len(data[i])):
        print data[i][j],
    print ''

