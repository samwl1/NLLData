import sys
from bs4 import BeautifulSoup
from lxml import html
from urllib.request import urlopen
from time import sleep
import requests
import pandas as pd
# "https://pointstreak.com/prostats/gamesheet_full.html?gameid=2965400"
page = requests.get("https://lscluster.hockeytech.com/game_reports/game-summary.php?game_id=1461&client_code=nll")
soup = BeautifulSoup(page.content, 'html.parser')

teams = pd.read_csv('teams.csv')
print(soup.prettify)
# tagtype = [type(item) for item in list(soup.children)]
# htmlTag = list(soup.children)[2]
# trs = soup.find_all('tr')

# stats = []
# for link in trs:
#     if "Name" in link.get_text():
#         stats.append(link.get_text())


# splits = stats[0].split()
# splits1 = splits[11:-1]
# posFO = 0
# posX = 0
# for x in splits1:
#     if x == 'FO':
#         break
#     elif x == '#':
#         posX = posFO
#     else:
#         posFO+=1
# print(posFO)

# players = {}
# splits2 = splits1[posFO+2:-1]
# splits1 = splits1[0:posX]
# statName = ['#', 'Name', 'G', 'A', 'PIM', 'S', 'SOFF', 'LB', 'T', 'CT', 'FO']
# player = {}
# print(splits1)
# idx = 0
# for item in splits1:
#     if '-' in item:
#         for char in item:
#             print(char)
#     else:



# soup.find_all('tr')[X].get_text(): 5 & 6 get the goals by quarter
