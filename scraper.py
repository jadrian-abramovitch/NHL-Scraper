from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import math
import re


## set file path where to save all data, E.g. 'C:\Documents\foldername'
file_path = ""


def click_next():
    ## click button to go to the next page of players
    button = browser.find_element_by_xpath("//div[@class = '-next']/button[@class = '-btn']").click()

 
def get_player_info(first_row, last_row):
    ## get all info from a specific page of player statistics, returns a dataframe
    df = pd.DataFrame(columns = ['Index', 'Player', 'Season', 'Team', 'Pos', 'GP', 'G', 'A', 'P', '+/-', 'PIM', 'P/GP', 'PPG', 'PPP', 'SHG', 'SHP', 'GWG', 'OTG', 'S', 'S%', 'TOI/GP', 'Shifts/GP', 'FOW%'])
    
    first_row = first_row
    last_row = last_row
    for row in range(first_row, last_row+1):
    
        row_string = str(row)
        element = [] 
        for column in range(1,24):
            column_string = str(column)

            ## nhl site differentiates even and odd rows, the following sorts this out
            if row % 2 == 0:
                temp = browser.find_elements_by_xpath("//div[@class = 'rt-tr -even']/div[@class = 'rt-td' and @role = 'gridcell']/div[text()='"+ row_string +"']/../../div[" + column_string + "]")
                
            else:
                temp = browser.find_elements_by_xpath("//div[@class = 'rt-tr -odd']/div[@class = 'rt-td' and @role = 'gridcell']/div[text()='"+ row_string +"']/../../div[" + column_string + "]")
                
            if temp:
                element.append(temp[0].text)
            
        if element:
            df = df.append({'Index':element[0], 'Player':element[1], 'Season':element[2], 'Team':element[3], 'Pos':element[4], 'GP':element[5], 'G':element[6], 'A':element[7], 'P':element[8], '+/-':element[9], 'PIM':element[10], 'P/GP':element[11], 'PPG':element[12], 'PPP':element[13], 'SHG':element[14], 'SHP':element[15], 'GWG':element[16], 'OTG':element[17], 'S':element[18], 'S%':element[19], 'TOI/GP':element[20], 'Shifts/GP':element[21], 'FOW%':element[22]},  ignore_index=True)

    df.set_index('Index', inplace=True)
    return(df)



def get_team_info(first_row, last_row):
    df = pd.DataFrame(columns = ['Index', 'Team', 'Season', 'GP', 'W', 'L', 'T', 'OT', 'P', 'ROW', 'P%', 'GF', 'GA', 'S/O Win', 'GF/GP', 'GA/GP', 'PP%', 'PK%', 'Shots/GP', 'SA/GP', 'FOW%'])

    for row in range(first_row, last_row+1):
        row_string = str(row)
        element = []
        for column in range(1,22):
            column_string = str(column)
            ## nhl site differentiates even and odd rows, the following sorts this out
            if row % 2 == 0:
                temp = browser.find_elements_by_xpath("//div[@class = 'rt-tr -even']/div[@class = 'rt-td' and @role = 'gridcell']/div[text()='"+ row_string +"']/../../div[" + column_string + "]")
            else:
                temp = browser.find_elements_by_xpath("//div[@class = 'rt-tr -odd']/div[@class = 'rt-td' and @role = 'gridcell']/div[text()='"+ row_string +"']/../../div[" + column_string + "]")

            if temp:
                ##check to make sure temp is not empty
                check = str(temp[0])
                if re.match(r'©', check):
                    ##Accent aigu breaks scraper
                    temp[0] == "Montréal Canadiens"
                
                element.append(temp[0].text)

        if element:
            ##check to make sure element is not empty
            df = df.append({'Index':element[0], 'Team':element[1], 'Season':element[2], 'GP':element[3], 'W':element[4], 'L':element[5], 'T':element[6], 'OT':element[7], 'P':element[8], 'ROW':element[9], 'P%':element[10], 'GF':element[11],'GA':element[12], 'S/O Win':element[13], 'GF/GP':element[14], 'GA/GP':element[15], 'PP%':element[16], 'PK%':element[17], 'Shots/GP':element[18], 'SA/GP':element[19], 'FOW%':element[20]},  ignore_index=True)

    return(df)
            


def all_players(number_players):
    ## iterate through all of the players you want, calling get_info for each page
    data = pd.DataFrame(columns = ['Player', 'Season', 'Team', 'Pos', 'GP', 'G', 'A', 'P', '+/-', 'PIM', 'P/GP', 'PPG', 'PPP', 'SHG', 'SHP', 'GWG', 'OTG', 'S', 'S%', 'TOI/GP', 'Shifts/GP', 'FOW%'])
    pages = math.ceil(number_players/50)
    for i in range(0, pages-1):
        data = data.append(get_player_info((i*50+1), (i+1)*50))
        if len(data)%50 == 0:
            click_next()
        else:
            return(data)
    data = data.append(get_player_info((pages-1)*50+1, number_players))
    return(data)

def all_teams(number_teams):
    ## iterate through all of the players you want, calling get_info for each page
    data = pd.DataFrame(columns = ['Index', 'Team', 'Season', 'GP', 'W', 'L', 'T', 'OT', 'P', 'ROW', 'P%', 'GF', 'GA', 'S/O Win', 'GF/GP', 'GA/GP', 'PP%', 'PK%', 'Shots/GP', 'SA/GP', 'FOW%'])
    data = data.append(get_team_info(1, number_teams))
    return(data)




def all_teams_all_seasons(number_seasons):

    
    for i in range(number_seasons):
        first_year = 1917
        start = first_year + i
        end = start + 1
        start_str = str(start)
        end_str = str(end)
        url = "http://www.nhl.com/stats/team?reportType=season&seasonFrom=" + start_str + "" + end_str + "&seasonTo=" + start_str + "" + end_str + "&gameType=2&filter=gamesPlayed,gte,1&sort=points,wins"
        browser.get(url)
        frame = all_teams(31)
        print(frame)

        ##set to your xpath where you want to save all of the files
        frame.to_csv(file_path + start_str + '' + end_str + '.csv')


def all_players_all_seasons(number_seasons):

    for i in range(number_seasons):
        ## set to the first year you want. First season all time is 1917
        first_year = 1917
        start = first_year + i
        end = start + 1
        start_str = str(start)
        end_str = str(end)
        url = "http://www.nhl.com/stats/player?reportType=season&seasonFrom=" + start_str + "" + end_str + "&seasonTo=" + start_str + "" + end_str + "&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists"
        browser.get(url)
        frame = all_players(1000)
        print(frame)

        ##set to your xpath where you want to save all of the files
        frame.to_csv(file_path + start_str + '' + end_str + '.csv')

browser = webdriver.Chrome()
all_teams_all_seasons(102)

