# Q-Learning Pacman
Another machine learning technique, Q-learning was used to dictate the actions of the pacman agent.
- After 50 training runs, Pacman solves the level with ease. SUCCESS!
![qlearning_pacman](https://user-images.githubusercontent.com/17188013/29246342-96074c7a-7fab-11e7-8c27-3b0aefb584f4.gif)
- One of the major questions my group had when first approaching a pacman solver, was, "How can we generalize the data that pacman receives?", because on a large board there are so many unique states.
- This approach uses an approximation Q-Learning agent that, with the provided extractor classes, can extract features from different states in a way that multiple states can be viewed similarly and updated at the same time. This greatly reduces the speed of learning, especially on larger maps.

## Running the Code
The following will run the game with 50 training games (no GUI displayed), followed by 10 additional games with the display on:`python pacman.py -p ApproximateQAgent -a extractor=SimpleExtractor -x 50 -n 60 -l mediumClassic`
- -x determines the number of training games
- -n determines the number of total games played
- A variety of other options are available and listed on the Berkeley [site](http://ai.berkeley.edu).

## Credit
- Credit to UC Berkeley for providing Intro to AI course materials [online](http://ai.berkeley.edu).
- Wikipedia [provides plenty of good information](https://en.wikipedia.org/wiki/Q-learning) about the topic.
- Also, big thanks to Carnegie Mellon for providing their AI lectures online! [This one](https://www.cs.cmu.edu/afs/cs/academic/class/15381-s07/www/slides/050307reinforcementLearning2.pdf), in particular, helped me understand Q-learning and how values are updated.
