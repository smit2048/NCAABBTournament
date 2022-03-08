# Predictor.py - sample code to show NCAA Basketball tournament prediction
#   requires a file named Stats.csv for team stats, and Bracket.txt for the matchups
import csv
import random

class BasketballTeam:
    def __init__(self, stats):
        self.name = stats[1]
        self.wins = int(stats[3])
        self.loses = int(stats[4])
        self.SOS = float(stats[7])
        self.pointsScored = int(stats[18])
        self.pointsAllowed = int(stats[19])
        self.fieldGoals = int(stats[22])
        self.fieldGoalsAttempted = int(stats[23])
        self.threePointShots = int(stats[25])
        self.threePointShotsAttempted = int(stats[26])
        self.freeThrows = int(stats[28])
        self.freeThrowsAttempted = int(stats[29])
        self.offensiveRebounds = int(stats[31])
        self.totalRebounds = int(stats[32])
        self.assists = int(stats[33])
        self.steals = int(stats[34])
        self.blocks = int(stats[35])
        self.turnovers = int(stats[36])
        self.personalFouls = int(stats[37])

    def __str__(self):
        return (self.name)


class NCAATournament:
    def __init__(self, bracket, teams):
        self.east = []
        self.west = []
        self.midwest = []
        self.south = []
        self.teams = teams
        self.bracket = bracket

    # load the data for a tournament
    def load(self):
        # convert the team names in the bracket in to Basketball teams in an inefficient way
        bbTeams = []
        for teamName in self.bracket:
            for team in self.teams:
                if team.name == teamName:
                    bbTeams.append(team)

        # break teams into their regions
        # the "region" concept is a mess, sometimes the NCAA uses north, south, east, west,
        # sometimes they use city names Atlanta, Indianapolis, etc
        for x in range(0, 16):
            self.west.append(bbTeams[x])
        for x in range(16, 32):
            self.east.append(bbTeams[x])
        for x in range(32, 48):
            self.south.append(bbTeams[x])
        for x in range(48, 64):
            self.midwest.append(bbTeams[x])

    def play(self, func):
        # The NCAA tournament is really 4 different 16 team regional tourmaments
        # followed by one 4 team tournament
        westWinner = FWSETourney(self.west, func)
        eastWinner = FWSETourney(self.east, func)
        southWinner = FWSETourney(self.south, func)
        midwestWinner = FWSETourney(self.midwest, func)

        finals = [westWinner[0], eastWinner[0], midwestWinner[0], southWinner[0]]
        print(f'\nFinal Four: {westWinner[0]}, {eastWinner[0]}, {midwestWinner[0]}, {southWinner[0]}')
        winner = FWSETourney(finals, func)
        print(f'Winner -> {winner[0]}\n')

    def __str__(self):
        return self.teams


spaces = {16: 0, 8: 4, 4: 8, 2: 12}

# First plays Worst Single Elimination tournament, like NCAA basketball
#   input: teams: list of teams in the tournament, in order of matchups
#          matchup: function that determines which team wins
#   returns: the winner
def FWSETourney(teams, matchup):
    numTeams = len(teams)
    if numTeams == 1:
        return teams

    # Play the games, adding the winners to the winner list
    winners = []
    while (len(teams) > 0):
        home = teams.pop(0)
        visitor = teams.pop(0)
        print(f'{" " * spaces[numTeams]}', end='')
        winners.append(matchup(home, visitor))

    return FWSETourney(winners, matchup)


# example function, pick a random winner
def rando(home, visitor):
    result = random.random()
    if result > .5:
        print(f'{home.name} beat {visitor.name}')
        return home
    else:
        print(f'{visitor.name} beat {home.name}')
        return visitor


# nonsensical function that uses all the stats
def crazy(home, visitor):
    homeScore = ((home.wins / 31) + (home.SOS / 13.89) + (home.pointsScored / 2911)
        + (home.fieldGoals / 1079) + (home.threePointShots / 348)
        + (home.freeThrows / 513) + (home.offensiveRebounds / 458) + (home.totalRebounds / 1343)
        + (home.assists / 601) + (home.steals / 299) + (home.blocks / 168) - (home.turnovers / 498)
        - (home.pointsAllowed / 1100) - (home.personalFouls / 620))
    visitorScore = ((visitor.wins / 31) + (visitor.SOS / 13.89) + (visitor.pointsScored / 2911)
        + (visitor.fieldGoals / 1079) + (visitor.threePointShots / 348)
        + (visitor.freeThrows / 513) + (visitor.offensiveRebounds / 458) + (visitor.totalRebounds / 1343)
        + (visitor.assists / 601) + (visitor.steals / 299) + (visitor.blocks / 168) - (visitor.turnovers / 498)
        - (visitor.pointsAllowed / 1100) - (visitor.personalFouls / 620))
    if homeScore > visitorScore:
        print(f'{home.name} beat {visitor.name}')
        return home
    else:
        print(f'{visitor.name} beat {home.name}')
        return visitor


if __name__ == '__main__':
    # first open the csv stat file convert it to a list of teams
    teams = []
    with open('Stats.csv', 'r') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            teams.append(BasketballTeam(line))

    # now open the bracket file
    with open('Bracket.txt') as file:
        bracket = [name.strip() for name in file]

    tourney = NCAATournament(bracket, teams)
    tourney.load()
    tourney.play(rando)

    tourney.load()
    tourney.play(crazy)
