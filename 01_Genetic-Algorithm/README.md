usage for current testing: `python pacman.py -p ANNAgent -n NUMBER_OF_RUNS`

# Pacman-Learner
Artificial Neural Network to play Pacman game that is implemented in Python.

- This code was used for a group project in my Artificial Intelligence course during my undergraduate studies.
- We extended the code from the pacman files on the Berkeley AI site.
- We constructed a Pacman AI agent which uses a multilayer perceptron artificial neural network (ANN) to determine which direction to move. The only information this agent receives is what occupies board locations surrounding it. This is fed into the input layer of the ANN.

- First starting with a stochastic approach, the networks' bias weights were initialized to random values. Then the breeder class was used to breed the fittest networks in an attempt to combine the best traits. The net result was a Pacman agent which continued to improved from generation to generation.

- After completing my undergraduate work, I decided to implement a couple other agents to see how they fair in comparison, when provided more information about the game. Those are available in the remaining folders of the [Pacman-Learner repository](https://github.com/lshort2/Pacman-Learner).

## Credit
- Huge credit to UC Berkeley for providing Intro to AI course materials online. Pacman files for the game itself were take from UC Berkeley's cs188 [site](http://ai.berkeley.edu/search.html).
- Credit to patorjk for [ascii text generator](http://patorjk.com/software/taag/#p=display&f=Graffiti&t=API). Makes organizing functions easier.

