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

# teams = pd.read_csv('teams.csv')
# print(soup.prettify)
# tagtype = [type(item) for item in list(soup.children)]
htmlTag = list(soup.children)[2]
trs = soup.find_all('tr')
gameStats = {}
goalieCol = ['#', "Name", 'GA', 'Mins', 'SH', 'SVS', 'PIM']
columns = ["#", "Player Name", "Position", "G", "A", "LB", "CTO", "T", "SH", "PIM", "Wd. SH", "Bl. SH (Off.)", "Bl. SH (Def)", "TSA", "FO"]
df = pd.DataFrame(columns=columns)
gdf = pd.DataFrame(columns=goalieCol)

stats = []
i = 0
j = 0
k = 0
rowG = 0
row = 0
entry = []
teams = {}
teamTotalentry1 = []
goalieEntry = []
teamTotals = {}
flag = False
teamTotalFlag = False
goalieFlag = False
for link in trs:
    children = list(link.children)
    
   
    for child in children:
        
        kid = child.getText()
        
        if 'GAME SUMMARY' in kid:
            gameStats['Game Summary'] = kid
        # elif kid in columns and i == 0:
            
        #     continue
        elif 'VISITORS' in kid and len(kid) <= 40:
            nameSplit = kid.split(':')
            teams[nameSplit[0]] = nameSplit[1].strip()
        elif 'HOME' in kid and len(kid) <= 40:
            nameSplit = kid.split(':')
            teams[nameSplit[0]] = nameSplit[1].strip()
        elif 'PLAYERS' in kid and len(kid) == len('players'):
            flag = True
            continue
        elif 'TEAM TOTAL' in kid and len(kid) == len('team total'):
            flag = False
            teamTotalFlag = True
        elif 'Goalies' in kid and len(kid) <= 20:
            goalieFlag = True
        # elif goalieFlag and (rowG==2 or rowG==4):
        #     goalieFlag = False
        elif goalieFlag and (kid != '\n' or kid != '' or kid != ' ' or kid != '\t'):
            kid = kid.replace('\n', '')
            kid = kid.replace(' ', '')
            kid = kid.replace('\xa0', '')
            kid = kid.replace('\t', '')

            flag3 = True
            for x in goalieCol:
                if x in kid and ',' not in kid:                       
                    flag3 = False
                    break

            if kid == '' and flag3:
                continue
            if k == 6:
                goalieEntry.append(kid)
                k = 0
                gdf.loc[rowG] = goalieEntry
                goalieEntry = []
                rowG+=1
                if(rowG == 2 or rowG == 4):
                    goalieFlag = False
                continue
                
            if (':' in kid or ',' in kid) and flag3:
                if k == 6:
                    goalieEntry.append(kid)
                    k = 0
                    gdf.loc[rowG] = goalieEntry
                    goalieEntry = []
                    rowG+=1
                else:
                    goalieEntry.append(kid)
                    k+=1

            elif flag3 and kid != '-':
                goalieEntry.append(int(kid))
                k+=1
            elif flag3:
                goalieEntry.append(kid)
                k+=1


        elif teamTotalFlag and (kid != '\n' or kid != '' or kid != ' ' or kid != '\t'):
            kid = kid.replace('\n', '')
            kid = kid.replace(' ', '')
            kid = kid.replace('\xa0', '')
            kid = kid.replace('\t', '')
            
            flag2 = True
            for x in columns:
                if x in kid and ',' not in kid and j!=2:                       
                    flag2 = False
                    break

            if kid == '' and flag2:
                continue
            

            elif j == 11:
                if not flag2:
                    continue
                if j == 11:
                    teamTotalentry1.append(kid)
                    if len(teamTotals) == 0:
                        teamTotals[teams["VISITORS"]] = teamTotalentry1
                    else:
                        teamTotals[teams["HOME"]] = teamTotalentry1
                    teamTotalentry1 = []
                    teamTotalFlag = False
                    j=0
                else:
                    teamTotalentry1.append(kid)
                    j+=1
            else:
                if not flag2:
                    continue
                if '/' in kid:
                    teamTotalentry1.append(kid)
                else:
                    num = int(kid)
                    teamTotalentry1.append(num)
                j+=1
        elif flag and (kid != '\n' or kid != '' or kid != ' ' or kid != '\t'):
            if kid in columns and i != 2:
                continue
            else:    
            
                kid = kid.replace('\n', '')
                kid = kid.replace(' ', '')
                kid = kid.replace('\xa0', '')
                kid = kid.replace('\t', '')
                
                flag2 = True
                for x in columns:
                    if x in kid and ',' not in kid and i!=2:                       
                        flag2 = False
                        break

                if kid == '' and flag2:
                    continue
                elif i == 0 or i == 1 or i == 2 or i == 14:
                    if not flag2:
                        continue
                    if i == 14:
                        entry.append(kid)
                        df.loc[row] = entry
                        entry = []
                        row+=1
                        i=0
                    else:
                        entry.append(kid)
                        i+=1
                else:
                    if not flag2:
                        continue
                    if '/' in kid:
                        entry.append(kid)
                    else:
                        num = int(kid)
                        entry.append(num)
                    i+=1

      
print(gdf)
# splits = gameStats['Game Summary'].split('\n')
# fixedSplits = []
# for split in splits:
#     if '' == split:
#         continue
#     else:
#         fixedSplits.append(split.replace('\t', ''))
# gameStats['Game Summary'] = fixedSplits
