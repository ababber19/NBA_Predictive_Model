### CREATES CSV FILE CONTAINING ALL NBA SEASONS' (1950-51: 2019:20) STATISTICS
    # CAN CREATE THREE DIFFERENT CSV FILES; STATS_PER_GAME, STATS_PER_36_MINUTES, STATS_PER_100_POSSESSIONS
    # DETERMINED BY "typeOfStats" VARIABLE





# Imports all libraries used in program
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
from itertools import compress
import time
import numpy as np


# Indicates start time of program
allStartTime = time.time()



rookieStats = pd.DataFrame()

# Pandas df that will contain all players statistics
allSeasonsStats = pd.DataFrame()

# Pandas df that will contain the time it takes for each season to complete
time_df = pd.DataFrame(columns=["Season", "Time", "NumPlayers", "NumRookies"])


# Indicates the type of statistics being analyzed (per game, per possession, per 36 minutes)
# Should be either "game", "minute", "poss"
typeOfStats = "poss"

# For-loop that goes through each season, scrapes the data, and adds the data to the "allSeasonStats" df
# If using per game or per 36 minutes, starts from 1951
# If using per 100 possessions, starts from 1974
for year in range(1974, 2021):
    # url page we are scrapping
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_{typeOfStats}.html"
    # html of page we are scrapping
    page = urllib.request.urlopen(url)


    # Time that this specific season has started
    seasonStartTime = time.time()


    # passes it to soup object using "hmtl.parser" as the parser
    soup = BeautifulSoup(page, "html.parser")

    # This sets up the column headers for all statistics, and gets rid of the "rank" variable
    header = [th.getText() for th in soup.findAll("tr", limit = 2)[0].findAll("th")]
    header = header[1:]

    # This sets up all of the rows (statistics of each column), and gets rid of the basketball-reference "rank" variable
    rows = soup.findAll('tr')[1:]
    playerStats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]


    
    # Creates a pandas dataframe with all of the data and column header
    oneSeasonStats = pd.DataFrame(playerStats, columns = header)
    # Sets the year to the year the season ended (e.g., 1950-1951 season --> 1951)
    oneSeasonStats["year"] = year
    # Initializes all players "isRookie" to False
    oneSeasonStats["isRookie"] = False
    oneSeasonStats["isSoph"] = False
    
    # If there are no rookie players (first year of NBA), all players are considered rookies
    if len(rookieStats) == 0:
        oneSeasonStats["isRookie"] = True

    # If this is the second year of the NBA...
    elif len(allSeasonsStats) == 0:
        # For-loop to determine which players are rookies
        for player in oneSeasonStats["Player"].unique():
            # If the player has not played in the NBA before, the player is considered a rookie
            # Checked by seeing if player is in "rookieStats" df
            if player not in rookieStats["Player"].unique():
                # Goes through "oneSeasonStats", and sets all these players' "isRookie" var to True
                oneSeasonStats["isRookie"].mask(oneSeasonStats["Player"] == player, True, inplace = True)
        
            else:
                oneSeasonStats["isSoph"].mask(oneSeasonStats["Player"] == player, True, inplace = True)

    # Otherwise...
    else:
        # For-loop to determine which players are rookies
        for player in oneSeasonStats["Player"].unique():
            # If the player has not played in the NBA before, the player is considered a rookie
            # Checked by seeing if player is in "rookieStats" df
            if player not in rookieStats["Player"].unique():
                # Goes through "oneSeasonStats", and sets all these players' "isRookie" var to True
                oneSeasonStats['isRookie'].mask(oneSeasonStats['Player'] == player, True, inplace = True)
            
            # If the player has only played their rookie year, then the player is considered a soph (sophomore)
            elif player not in allSeasonsStats["Player"].unique():
                # Goes through "oneSeasonStats", and sets all these players' "isSoph" var to True
                oneSeasonStats["isSoph"].mask(oneSeasonStats["Player"] == player, True, inplace = True)



    # Drops any empty rows based on "na" player values
    oneSeasonStats = oneSeasonStats.dropna(subset = ["Player"])
    # Concats this season with all seasons ever played
    allSeasonsStats = pd.concat([allSeasonsStats, oneSeasonStats[oneSeasonStats["isRookie"] == False]])

    # Concats this season rookies with all rookies
    rookieStats = pd.concat([rookieStats, oneSeasonStats[oneSeasonStats["isRookie"] == True]])
    
    
    
    # Creates a temp dictionary containing information about how long compiling of this season took
    tempDict = {"Season": [year], "Time": [(time.time() - seasonStartTime)], "NumPlayers": [len(oneSeasonStats)], "NumRookies": [oneSeasonStats["isRookie"].values.sum()]}
    # Converts dictionary to pandas df
    tempDF = pd.DataFrame(data = tempDict)
    
    # Combines this df with "time_df", which contains how long each season took to compile
    time_df = pd.concat([time_df, tempDF])



    # Prints information to console to check performance while program is still compiling
    print("\n\nSeason {} finished!".format(year))
    print("--- %s seconds ---" % (time.time() - seasonStartTime))
    print("Number of players: {}".format(len(oneSeasonStats)))
    print("Number of rookies: {}".format(oneSeasonStats["isRookie"].values.sum()))


# Combines rookieStats and allSeasonStats, and exports players' statistics as a csv
allSeasonsStats = pd.concat([allSeasonsStats, rookieStats])
allSeasonsStats.set_index("Player", inplace = True)
allSeasonsStats.to_csv(f"allSeasonStatsPer{typeOfStats}.csv")

# Exports time information as a csv
time_df.set_index("Season", inplace = True)
time_df.to_csv(f"timeTakenPer{typeOfStats}.csv")

# Prints to console how long the full program took to run
print("--- %s seconds ---" % (time.time() - allStartTime))

