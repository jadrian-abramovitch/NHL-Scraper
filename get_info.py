import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
from matplotlib import pylab
from numpy import arange,array,ones
from scipy import stats
from pylab import figure, axes, pie, title, show

#dictionary to switch between team code and team name, thanks wikipedia
teamCodes = {'AFM' : 'Atlanta Flames',
'ANA' : 'Anaheim Ducks',
'ARI' :'Arizona Coyotes',
'ATL' : 'Atlanta Thrashers',
'BOS' : 'Boston Bruins',
'BRK' : 'Brooklyn Americans',
'BUF' : 'Buffalo Sabres',
'CAR' : 'Carolina Hurricanes',
'CGS' : 'California Golden Seals',
'CGY' : 'Calgary Flames',
'CHI' : 'Chicago Blackhawks',
'CBJ' : 'Columbus Blue Jackets',
'CLE' : 'Cleveland Barons',
'CLR' : 'Colorado Rockies',
'COL' : 'Colorado Avalanche',
'DAL' : 'Dallas Stars',
'DFL' : 'Detroit Falcons',
'DCG' : 'Detroit Cougars',
'DET' : 'Detroit Red Wings',
'EDM' : 'Edmonton Oilers',
'FLA' : 'Florida Panthers',
'HAM' : 'Hamilton Tigers',
'HFD' : 'Hartford Whalers',
'KCS' : 'Kansas City Scouts',
'LAK' : 'Los Angeles Kings',
'MIN' : 'Minnesota Wild',
'MMR' : 'Montreal Maroons',
'MNS' : 'Minnesota North Stars',
'MTL' : 'Montréal Canadiens',
'MWN' : 'Montreal Wanderers',
'NSH' : 'Nashville Predators',
'NJD' : 'New Jersey Devils',
'NYA' : 'New York Americans',
'NYI' : 'New York Islanders',
'NYR' : 'New York Rangers',
'OAK' : 'Oakland Seals',
'OTT' : 'Ottawa Senators',
'PHI' : 'Philadelphia Flyers',
'PHX' : 'Phoenix Coyotes',
'PIR' : 'Pittsburgh Pirates',
'PIT' : 'Pittsburgh Penguins',
'QUA' : 'Philadelphia Quakers',
'QUE' : 'Quebec Nordiques',
'QBD' : 'Quebec Bulldogs',
'SEN' : 'Ottawa Senators (original)',
'SJS' : 'San Jose Sharks',
'SLE' : 'St. Louis Eagles',
'STL' : 'St. Louis Blues',
'TAN' : 'Toronto Arenas',
'TBL' : 'Tampa Bay Lightning',
'TOR' : 'Toronto Maple Leafs',
'TSP' : 'Toronto St. Patricks',
'VAN' : 'Vancouver Canucks',
'VGK' : 'Vegas Golden Knights',
'WIN' : 'Winnipeg Jets (original)',
'WPG' : 'Winnipeg Jets',
'WSH' : 'Washington Capitals'}


# set to the same file path as scraper.py to access the information gathered
file_path = ""
            

def team_player_info(team, year):
    ## Gets all player info for a specific season
    ## String 'team' should be the entire team name (e.g. 'Toronto Maple Leafs').
    ## Int Year should be the year in which the season started.
    
    row = pd.DataFrame(columns = ['Index', 'Player', 'Season', 'Team', 'Pos', 'GP', 'G', 'A', 'P', '+/-', 'PIM', 'P/GP', 'PPG', 'PPP', 'SHG', 'SHP', 'GWG', 'OTG', 'S', 'S%', 'TOI/GP', 'Shifts/GP', 'FOW%'])
    start_str = str(year)
    end_str = str(year + 1)
    
    ## Change to where all of the player info is stored
    df = pd.read_csv(file_path + start_str + "" + end_str + ".csv", index_col=[0])
    
    number_rows, number_cols = df.shape
    if ((team == df['Team']).any()):
        row_index = df.index[df['Team'].str.contains(team)].tolist()

    for i in row_index:
        row = row.append(df.iloc[i-1])
    
    return row


        
def team_info(team, year):
    ## Gets one teams stats for a specific year.
    ## String 'team' should be the entire team name (e.g. 'Toronto Maple Leafs').
    ## Int Year should be the year in which the season started.
    
    start_str = str(year)
    end_str = str(year+1)
    
    ## Change to where all of the team info is stored
    df = pd.read_csv(file_path + start_str + '' + end_str + '.csv')
    if((team == df['Team']).any()):
        row_index = df[df['Team']==team].index.item()
        info = df.iloc[row_index][9]
    return info



def all_team_standings(year):
    ## Returns points and standing of all teams for the given year
    ## Int Year should be the year in which the season started.

    start_str = str(year)
    end_str = str(year+1)
    
    ## Change to where all of the team info is stored
    df = pd.read_csv(file_path + start_str + '' + end_str + '.csv')
    df.set_index('Index', inplace=True)
    df = df.drop(columns = ['Unnamed: 0', 'Season', 'GP', 'W', 'L', 'T', 'OT', 'ROW', 'P%', 'GF', 'GA', 'S/O Win', 'GF/GP', 'GA/GP', 'PP%', 'PK%', 'Shots/GP', 'SA/GP', 'FOW%'])
    return df



def points_deviation(year, removeOutliers=False, percent=False, removeDefense=False):
    ## Returns the deviation of points scored by players on the team vs their teams points in a dataframe
    ## Int Year should be the year in which the season started.
    ## removeOutliers will take remove any players who played less than 20 games


    deviation = []
    df = all_team_standings(year)
    
    number_rows, number_cols = df.shape
    for i in range(number_rows):
        team = df.iloc[i][0]
        #Uses the dictionary to convert between 3 letter code and full team name
        temp = team_player_info(list(teamCodes.keys())[list(teamCodes.values()).index(team)], year)
        
        if removeOutliers:
            
            if ((20 > temp['GP']).any()):
                row_index = temp.index[temp['GP']<20].tolist()
                temp.drop(row_index, inplace=True)

        if removeDefense:
            row_index = temp.index[temp['Pos']=='D'].tolist()
            temp.drop(row_index, inplace=True)
                
        if percent:
            total = temp['G'].sum()
            temp.sort_values('G', ascending=False, inplace=True)
            plyr_percent = []
            for j in range(num_top_plyrs):
                plyr_percent.append((temp[stat].iloc[j])/total)
            deviation.append(np.std(plyr_percent['G']))
        else:
            deviation.append(np.std(temp['G']))
        
    df['STD'] = deviation
    return df   
        
        
def deviation_graphs(start_year, end_year):
    ## Saves graphs to of team points vs standard deviation of player points
    ## Makes a graph for each year specified for the start and end years
    for year in range(start_year, end_year+1):
        x = (points_deviation(year, removeOutliers=True, percent=True, removeDefense=True))
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x['STD'],x['P'])
        line = slope*(x['STD'])+intercept
        
        plt.xlabel("Deviation of Points")
        plt.ylabel("Team Points")
        
        year_str = str(year)
        plt.title("Team Standings vs Deviation of Points Scored by Players in Year: " + year_str)
        plt.plot(x['STD'],x['P'],'o', x['STD'], line)
        
        r_squared = round(r_value**2, 3)
        display_text = "R^2: " + str(r_squared)
        if year == 2012 or year == 2018:
            plt.text(9, 74, display_text,fontsize=10 )
        else:
            plt.text(16, 105, display_text,fontsize=10 )

        #Change to where you wish to save the files
        plt.savefig(file_path + year_str + ".png")
        plt.close()

def all_years_deviation_graphs(start_year, end_year):
    # Saves one graph of team points vs standard deviation of player points that includes all years specified
    
    x = pd.DataFrame(columns = ['Team','P', 'STD'])
    points = np.array([])
    deviation = np.array([])
    
    for year in range(start_year, end_year+1):
        #change removeOutliers if you wish to include players who have played less than 20 games in the specified year
        temp = points_deviation(year, removeOutliers = True)
        x = x.append(temp)
        points = np.append(points, temp['P'])
        deviation = np.append(deviation, temp['STD'])



    slope, intercept, r_value, p_value, std_err = stats.linregress(deviation, points)
    line = slope*(deviation)+intercept    

    plt.xlabel("Deviation of Goals %")
    plt.ylabel("Team Points")
        
    year_str = str(year)
    plt.title("Team Standings vs Deviation of Goals % Scored by Forwards 2005-2018")
    plt.plot(deviation, points,'o', deviation, line)
        
    r_squared = round(r_value**2, 3)
    display_text = "R^2: " + str(r_squared)
    plt.text(4, 105, display_text,fontsize=10 )
    
    # Change to where you wish to save the file
    plt.savefig(file_path)
    plt.close()
    
def topx_percent(year, num_top_plyrs, stat, removeOutliers = True, removeDefense = True):
    # Returns a dataframe of the top x players stats expressed as a % of the team total vs their teams points in the standings
    # Int Year is the year in which the season started
    # Int num_top_plyrs is how many of the team leaders you wish to look at
    # Str stat is the individual player stat you wish to observe, typically 'G' or 'P'
    # Bool removeOutliers removes any players who played less than 20 games in a season if set to True
    # Bool removeDefense removes defensemen, thus allowing you to only view forwards if set to True
    topx = []
    df = all_team_standings(year)
    number_rows, number_cols = df.shape
    for i in range(number_rows):
        team = df.iloc[i][0]
        temp = team_player_info(list(teamCodes.keys())[list(teamCodes.values()).index(team)], year)

        total_goals = temp[stat].sum()
        if removeOutliers:
            if ((20 > temp['GP']).any()):
                row_index = temp.index[temp['GP']<20].tolist()
                temp.drop(row_index, inplace=True)
        if removeDefense:
            row_index = temp.index[temp['Pos']=='D'].tolist()
            temp.drop(row_index, inplace=True)

        ##here
        temp.sort_values(stat, ascending=False, inplace=True)
        plyr_percent = []
        ##for j in range(num_top_plyrs):
        ##   plyr_percent.append((temp[stat].iloc[j])/total_goals)

        #topx.append(sum(plyr_percent))
        topx.append(total_goals)
    df['Topx'] = topx
    return df
    
def all_years_percent_graphs(start_year, end_year):
    # Saves a graph of % of a stat for the top x players vs team points in the standings for all specified years

    # Set to the number of top players per team you wish to compare
    num_top_plyrs = 3
    
    # Set to the stat you wish to compare on
    stat = 'G'
    
    x = pd.DataFrame(columns = ['Team','P', 'Topx'])
    points = np.array([])
    topx = np.array([])
    for year in range(start_year, end_year+1):
        temp = topx_percent(year, num_top_plyrs, stat)
        x = x.append(temp)
        points = np.append(points, temp['P'])
        topx = np.append(topx, temp['Topx'])

    slope, intercept, r_value, p_value, std_err = stats.linregress(topx, points)
    line = slope*(topx)+intercept    

    ##plt.xlabel("Top" + str(num_top_plyrs) + " " + stat + "%")
    plt.xlabel("Goals Scored")
    plt.ylabel("Team Points")
        
    year_str = str(year)
    plt.title("Team Standings vs Goals Scored")
    ##plt.title("Team Standings vs " + stat + "% for top " + str(num_top_plyrs) + " forwards 2005-2018")
    plt.plot(topx, points,'o', topx, line)
        
    r_squared = round(r_value**2, 3)
    display_text = "R^2: " + str(r_squared)

    # adjust the first value to somewhere on the x-axis of you graph so it appears on the graph
    plt.text(150, 105, display_text,fontsize=10 )

    # Set to where you wish to save the graph 
    plt.savefig(file_path)
    plt.close()
    

##print(all_team_standings(2015))
pd.set_option('display.max_columns', 30)
all_years_deviation_graphs(2005, 2018)
#all_years_percent_graphs(2005,2018)
