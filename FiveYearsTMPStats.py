import numpy as np
import pandas as pd
import time

# Finds the start time for the program
startTime = time.time()


# Indicates the type of statistics being analyzed (per game, per possession, per 36 minutes)
# SHOULD ALWAYS BE GAME
typeOfStats = "game"

# Imports Seasons Stats, sorts df by columns "Player" and "year"
allSeasonStats = pd.read_csv(f"allSeasonStatsPer{typeOfStats}.csv").sort_values(["Player", "year"])

# Calculates the players' season minutes played (SMP)
allSeasonStats["SMP"] = allSeasonStats["G"] * allSeasonStats["MP"]


# Initializes rookieStats df, which will contain only the first two years' statistics of each player
# Will also contain FYMP; explained below
rookieStats = pd.DataFrame()
rookieStats = allSeasonStats[(allSeasonStats["isRookie"] == True) | (allSeasonStats["isSoph"] == True)]

# Initializes FYMP (five year minutes played) statistic to 0
rookieStats["FYMP"] = 0



# For loop to determine FYMP statistic for each player
for player in rookieStats["Player"].unique():
    # Finds the rookie year of the player
    rookieYear = int(rookieStats[rookieStats["Player"] == player][0:1].year)
    
    # Calculates the FYMP value of the player
    fympVal = ((allSeasonStats[allSeasonStats["Player"] == player][allSeasonStats["year"] > (rookieYear + 1)][allSeasonStats["year"] < (rookieYear + 7)]).sum()["SMP"])

    # Adds this statistic to player in "rookieStats" df
    rookieStats["FYMP"].mask(rookieStats["Player"] == player, fympVal, inplace = True)


# Prints the time the program took to run
print("--- %s seconds ---" % (time.time() - startTime))


# Exports "rookieStats" df
# Sets index of player to avoid exporting the default pandas index to the csv
rookieStats.set_index("Player", inplace = True)
rookieStats.to_csv(f"firstTwoYearsStatsPer{typeOfStats}.csv")