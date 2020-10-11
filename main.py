import requests
import csv
import datetime
from bs4 import BeautifulSoup

def save_table_on_csv():
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    name_file = "league_table_{datetime}.csv".format(datetime = now)
    with open(name_file, mode = 'w+', encoding = "utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(teams)

def get_soup():
    url = "https://www.mundodeportivo.com/resultados/futbol/laliga/clasificacion"
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def get_body_league_table():
    league_table = soup.find('table', class_ = 'table table--sport')
    return league_table.find_all('tbody')

def get_team_with_all_the_data(row):
    elements = row.find_all('td')
    div_position_name_team = elements[0].find('div', class_ = 'tflex')
    if div_position_name_team != None:
        pos_team = div_position_name_team.find('div', class_ = 'team-standing').text
        name_team = div_position_name_team.find('div', class_ = 'tflex__content').text
        points_team = elements[7].text
        return [pos_team, name_team, points_team]
    else:
        return None
            
if __name__ == "__main__":
    soup = get_soup()

    body_league_table = get_body_league_table()
    teams = []
    for team in body_league_table:
        rows = team.find_all('tr')
        for row in rows:
            team = get_team_with_all_the_data(row)
            if team != None:
                teams.append(team)

    save_table_on_csv()