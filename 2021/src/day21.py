from shared import *

# Input data is in INPUT_DATA.
#INPUT_DATA = [int(x) for x in INPUT_DATA]

player1 = tuple(parse.parse("Player 1 starting position: {:d}", INPUT_DATA[0]).fixed)[0]
player2 = tuple(parse.parse("Player 2 starting position: {:d}", INPUT_DATA[1]).fixed)[0]

# Part 1
def playGame(player1, player2, currentDie, winningScore=1000):
    scores   = { 1: 0, 2: 0}
    numRolls = 0

    def rollDie():
        nonlocal currentDie, numRolls, player1, player2
        currentDie += 1
        numRolls += 1
        if currentDie > 100: currentDie = 1
        return currentDie

    while True:
        if any([x >= winningScore for x in scores.values()]): break

        # Start with Player1
        movement1  = rollDie()
        movement1 += rollDie()
        movement1 += rollDie()
        player1  += movement1
        while player1 > 10:
            player1 -= 10
        scores[1] += player1
        #print(f"Player 1 moves {movement1} spaces to space {player1} for a total score of {scores[1]}.")

        if any([x >= winningScore for x in scores.values()]): break

        # Do Player2
        movement2  = rollDie()
        movement2 += rollDie()
        movement2 += rollDie()
        player2   += movement2
        while player2 > 10:
            player2 -= 10
        scores[2] += player2
        #print(f"Player 2 moves {movement2} spaces to space {player2} for a total score of {scores[2]}.")

    return scores, numRolls

scores, numRolls = playGame(player1, player2, 0)
print(min(scores[1], scores[2]) * numRolls)

# Part 2
@memoize
def playGame(index):
    player1, player2, score1, score2 = index

    if score1 >= 21:
        return 1, 0
    if score2 >= 21:
        return 0, 1

    win1, win2 = 0, 0

    for d1 in [1, 2, 3]:
        for d2 in [1, 2, 3]:
            for d3 in [1, 2, 3]:
                newPlayer1 = (player1 + d1 + d2 + d3) % 10
                newScore1  = score1 + newPlayer1 + 1

                # To simulate the next players turn, swap the ordering of the values.
                # Note that the returns are add2, add1. This represents the swapped player2, player2 from the arguments.
                add2, add1 = playGame((player2, newPlayer1, score2, newScore1))
                win1 += add1
                win2 += add2

    return win1, win2

wins1, wins2 = playGame((player1 - 1, player2 - 1, 0, 0))
print(max((wins1, wins2)))