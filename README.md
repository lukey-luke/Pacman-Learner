# Pacman-Learner
This serves as a repository for a python program that can play pacman all by itself.

![qlearning_pacman](https://user-images.githubusercontent.com/17188013/29246342-96074c7a-7fab-11e7-8c27-3b0aefb584f4.gif)


## Files are organized into the following folders...
- [`01...`](https://github.com/lshort2/Pacman-Learner/tree/master/01_Genetic-Algorithm) is the code used from a group project in my undergraduate artificial intelligence course. This, agent was provided the least amount of information about the game. Each game, the breeder assigns a neural network to dictate Pacman's actions.
- [`02...`](https://github.com/lshort2/Pacman-Learner/tree/master/02_Multi-Agent) uses the class Minimax approach. This agent proved to be good at avoiding the ghosts when a depth of 3 or 4 was used.
- [`03...`](https://github.com/lshort2/Pacman-Learner/tree/master/03_Reinforcement) uses another machine learning technique, Q-Learning. This agent was provided info about the game state (pellet locations, ghost locations, and legal actions), and quickly learns which actions will provide a better score. This agent learned how to beat the classic map fairly quickly (10-20 games).

## Credit
- Huge credit to UC Berkeley for providing Intro to AI course materials online. Pacman files for the game itself were take from UC Berkeley's cs188 [site](http://ai.berkeley.edu/search.html).

