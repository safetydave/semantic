# semantic
Solving semantic puzzles, like https://semantle.com

Solution components comprise:

* Two vocabulary options - english words set and unigram frequency
* Two semantic models - word2vec and USE
* Two solver/search strategies - cohort and gradient

These are then combined in a variety of different notebooks:

* Notebook for playing online
* Notebooks exploring how each solver/search works
* Notebook comparing solvers and human guesses
* Notebook for statistically testing performance

And also use some utilities:

* Semantle simulator to stand in for a remote game
* Performance measurement utilities

Resources (download to `data` folder):

* english words (unigram freq) https://www.kaggle.com/datasets/rtatman/english-word-frequency
* word2vec semantic model https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing
