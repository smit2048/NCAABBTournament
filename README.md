# NCAABBTournament
Sample code for predicting the results of the NCAA basketball tournament.

Requires the two data files Stats.csv and Bracket.txt to be in the program directory

These currently contain data for the 2021 tournament. So you can see how your algorithm performs against last year's tournament result.
The data files will be updated for the 2022 tournament before it starts.

You can run the program from the command line with "Python3 Predictor.py"

How to use:
  Write your own algorithm to predict the winner of a game. Look at the function crazy(home, visitor) to see what stats are available.
  Find the lines 
  
    tourney = NCAATournament(bracket, teams)
    tourney.load()
    tourney.play(rando)
  
  and replace tourney.play(rando) with tourney.play(your_awesome_function)
  
