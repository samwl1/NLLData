import sys
from bs4 import BeautifulSoup
from lxml import html
from urllib.request import urlopen
from time import sleep
import requests
import pandas as pd
def fixDate(date):
    dateS = date.split(' ')
    trueDate = []
    for x in dateS:
        if x != '':
            trueDate.append(x.replace(',', ''))
            
    if trueDate[1] == 'January':
        trueDate[1] = 1
    elif trueDate[1] == 'February':
        trueDate[1] = 2
    elif trueDate[1] == 'March':
        trueDate[1] = 3
    elif trueDate[1] == 'April':
        trueDate[1] = 4
    elif trueDate[1] == 'May':
        trueDate[1] = 5
    elif trueDate[1] == 'June':
        trueDate[1] = 6
    elif trueDate[1] == 'July':
        trueDate[1] = 7
    elif trueDate[1] == 'August':
        trueDate[1] = 8
    elif trueDate[1] == 'September':
        trueDate[1] = 9
    elif trueDate[1] == 'October':
        trueDate[1] = 10
    elif trueDate[1] == 'November':
        trueDate[1] = 11
    elif trueDate[1] == 'December':
        trueDate[1] = 12
    realDate = "{year}-{month}-{day}".format(year=trueDate[3], month = trueDate[1], day = trueDate[2])
    return realDate

# inid = input("Enter the game id: ")
inid = 1461
page = requests.get("https://lscluster.hockeytech.com/game_reports/game-summary.php?game_id={id}&client_code=nll".format(id = inid))
soup = BeautifulSoup(page.content, 'html.parser')

# teams = pd.read_csv('teams.csv')
# print(soup.prettify)
# tagtype = [type(item) for item in list(soup.children)]
htmlTag = list(soup.children)[2]
trs = soup.find_all('tr')
goalieCol = ['#', "Name", 'GA', 'Mins', 'SH', 'SVS', 'PIM']
columns = ["#", "Player Name", "Position", "G", "A", "LB", "CTO", "T", "SH", "PIM", "Wd. SH", "Bl. SH (Off.)", "Bl. SH (Def)", "TSA", "FO", "Team"]
boxScoreCol = ['Date', 'Year', 'Week', 'game_id', 'team_id', 'Goals', 'Shots', 'Shot_Percent', 'Wide Shots','SH_BLK_OFF', 'SH_BLK_DEF','GB', 'TOs', 'CTOs', 'FO_Win', 'FO_Loss', 'FO_Percent','Power_Play_Goals', 'Power_Play_Opp', 'Power_Play_Percent', 'Penalty_Kill', 'Penalties', 'Pentalty_Kill_Percent', 'Saves', 'Save_Percent', 'Win', 'Q1_Score', 'Q2_Score', 'Q3_Score', 'Q4_Score', 'OT', 'OT_Score', 'Home_Away', 'Assists']

i = 0
j = 0
k = 0
rowG = 0
row = 0
# Contains general info like game id, date, etc.
gameStats = {}
# Penalty statistics for players, and team opportunities
penaltyStats = {}
# Player stats
df = pd.DataFrame(columns=columns)
# Goalie stats
gdf = pd.DataFrame(columns=goalieCol)
# Contains team ids
teamdf = pd.read_csv("teams.csv")
# box score dataframe
boxScoredf = pd.DataFrame(columns=boxScoreCol)
stats = []
entry = []
# Labels which teams are home/away
teams = {}
teamTotalentry1 = {}
goalieEntry = []
# Contains the team totals
teamTotals = {}
# Contains goals by quarter
quarters = {}
qTeamEntry = {}
qHeaders = []

flag = False
teamTotalFlag = False
goalieFlag = False
quarterFlag = False
quarterFlag2 = False
ppFlag = False
ppCountFlag = False
playerTeam = ''
qIndx = 0
qTeam = ''
placeholderPP = ''


for link in trs:
    children = list(link.children)
    for child in children:
        kid = child.getText()
        if 'GAME SUMMARY' in kid:
            gameStats['Game Summary'] = kid
        elif 'VISITORS' in kid and len(kid) <= 40:
            nameSplit = kid.split(':')
            teams[nameSplit[0]] = nameSplit[1].strip()
            playerTeam = nameSplit[1].strip().title()
        elif 'SCORING' in kid and len(kid) <= 10:
            quarterFlag = True
        elif 'SHOTS' in kid and len(kid) < 10:
            quarterFlag = False
        elif 'HOME' in kid and len(kid) <= 40:
            nameSplit = kid.split(':')
            teams[nameSplit[0]] = nameSplit[1].strip()
            playerTeam = nameSplit[1].strip().title()
        elif 'PLAYERS' in kid and len(kid) == len('players'):
            flag = True
            continue
        elif 'TEAM TOTAL' in kid and len(kid) == len('team total'):
            flag = False
            teamTotalFlag = True
        elif 'Scoring' in kid and len(kid) <= 30:
            if ppFlag == True:
                varSplit = kid.split(' ')
                if len(varSplit) == 3:
                    placeholderPP = "{t1} {t2}".format(t1=varSplit[0], t2 = varSplit[1])
                else:
                    placeholderPP = varSplit[0]
                penaltyStats[placeholderPP] = {}
            else:
                varSplit = kid.split(' ')
                if len(varSplit) == 3:
                    placeholderPP = "{t1} {t2}".format(t1=varSplit[0], t2 = varSplit[1])
                else:
                    placeholderPP = varSplit[0]
                penaltyStats[placeholderPP] = {}
                ppFlag = True 
            
        elif 'Penalties' in kid:
            kid = kid.replace('\n', '')
            kid = kid.replace('\xa0', '')
            kid = kid.replace('\t', '')
            ppFlag = False
            
            if ppCountFlag == True:
                ph = penaltyStats[placeholderPP]['Opportunities']
                phn = placeholderPP
                varSplit = kid.split(' ')
                if len(varSplit) > 2:
                    placeholderPP = "{t1} {t2}".format(t1=varSplit[0], t2 = varSplit[1])
                else:
                    placeholderPP = varSplit[0]
                penaltyStats[placeholderPP]['Opportunities'] = 0
                penaltyStats[placeholderPP]['Opportunities'] = ph
                placeholderPP = phn
                penaltyStats[placeholderPP]['Opportunities'] = 0
            else:
                varSplit = kid.split(' ')
                placeholderPP = varSplit[0]
                ppCountFlag = True
                penaltyStats[placeholderPP]['Opportunities'] = 0
        elif 'Penalty Shots' in kid or ('PP' in kid and 'PIM' in kid and 'PTS' in kid):
            ppCountFlag = False
        elif 'Goalies' in kid and len(kid) <= 20:
            goalieFlag = True
        elif ppCountFlag and (kid != '\n' or kid != '' or kid != ' ' or kid != '\t'):
            kid = kid.replace('\n', '')
            kid = kid.replace('\xa0', '')
            kid = kid.replace('\t', '')
            if kid == ' ' or kid =='':
                continue
            elif '(PS)' in kid or '(PP)' in kid:
                penaltyStats[placeholderPP]['Opportunities'] = penaltyStats[placeholderPP]['Opportunities'] +1
            else:
                continue

        elif ppFlag and (kid != '\n' or kid != '' or kid != ' ' or kid != '\t'):
            kid = kid.replace('\n', '')
            kid = kid.replace('\xa0', '')
            kid = kid.replace('\t', '')
            if kid == ' ' or kid =='':
                continue
            else:
                
                s1 = kid.split('.')
                
                s2 = s1[1].split(',')
                
                if 'PP' in s2[-1]:
                    if s2[0] in penaltyStats[placeholderPP]:
                        penaltyStats[placeholderPP][s2[0]] =  penaltyStats[placeholderPP][s2[0]]+1
                    else:
                        penaltyStats[placeholderPP].setdefault(s2[0], 1)
                


        elif quarterFlag and (kid != '\n' or kid != '' or kid != ' ' or kid != '\t'):
            kid = kid.replace('\n', '')
            kid = kid.replace('\xa0', '')
            kid = kid.replace('\t', '')
            if qIndx == 0 and qTeam == '' and kid != '' and kid != ' ' and quarterFlag2:
                qTeam = kid
            else:
                kid = kid.replace(' ', '')
            

                if 'Total' in kid and len(kid) <= 10:
                    quarterFlag2 = True
                    continue
                if (not quarterFlag2) and kid != '' and kid != ' ' and kid != 'SCORING':
                    qHeaders.append(kid)
            
                if kid == '' and quarterFlag2:
                    continue

                
                elif quarterFlag2:
                    if qIndx == len(qHeaders):
                        
                        qTeamEntry['Total'] = int(kid)
                        quarters[qTeam] = qTeamEntry
                        qTeamEntry = {}
                        qIndx = 0
                        qTeam = ''
                    else:
                    
                        if kid == qTeam:
                            continue
                        else:
                            qTeamEntry[qHeaders[qIndx]] = kid
                            qIndx+=1


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
                if '(W)' in kid:
                    kid.replace('(W)', '')
                if '(L)' in kid:
                    kid.replace('(L)', '')
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
                    teamTotalentry1[columns[j+3]] = kid
                    if len(teamTotals) == 0:
                        teamTotals[teams["VISITORS"]] = teamTotalentry1
                    else:
                        teamTotals[teams["HOME"]] = teamTotalentry1
                    teamTotalentry1 = {}
                    teamTotalFlag = False
                    j=0
                else:
                    teamTotalentry1[columns[j+3]] = kid
                    j+=1
            else:
                if not flag2:
                    continue
                if '/' in kid:
                    teamTotalentry1[columns[j+3]] = kid
                else:
                    num = int(kid)
                    teamTotalentry1[columns[j+3]] = num
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
                    if 'C'==kid or 'A'==kid:
                        flag2 = False
                        break

                if kid == '' and flag2:
                    continue
                elif i == 0 or i == 1 or i == 2 or i == 14:
                    if not flag2:
                        continue
                    if i == 14:
                        entry.append(kid)
                        entry.append(playerTeam)
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


splits = gameStats['Game Summary'].split('\n')
fixedSplits = []
for split in splits:
    if '' == split:
        continue
    else:
        fixedSplits.append(split.replace('\t', ''))
gameStats['Game Summary'] = fixedSplits
gameid = (fixedSplits[0].split('Y'))[1]
gameDate = (fixedSplits[1].split('-'))[0]
gameYear = (gameDate.split(','))[2]
gameStats['Game ID'] = int(gameid) - 1460
gameStats['Game Year'] = int(gameYear)
gameStats['Game Date'] = fixDate(gameDate)
fTeamTotals = {}
for x in teamTotals.keys():
    fTeamTotals[x.title()] = teamTotals[x]
fTeams = {}
for x in teams.keys():
    fTeams[x.title()] = teams[x].title()

savesentry1 = 0
goalsMatch1 = 0
savesentry2 = 0
goalsMatch2 = 0
winCheck = 0
for gidx in range(4):
    s = gdf['SVS']
    g = gdf['GA']
    w = gdf['Name']
    if gidx == 1 or gidx == 0:
        if '(W)' in w[gidx]:
            winCheck = 1
        if s[gidx] == '-':
            pass
        else:
            savesentry1+=s[gidx]
        if g[gidx] == '-':
            pass
        else:
            goalsMatch1+=g[gidx]
    else:
        if '(W)' in w[gidx]:
            winCheck = 2
        if s[gidx] == '-':
            pass
        else:
            savesentry2+=s[gidx]
        if g[gidx] == '-':
            pass
        else:
            goalsMatch2+=g[gidx]


def generateBoxScore(hoa, team, week):
    opponent = ''
    for t in fTeams.keys():
        if fTeams[t] == team:
            pass
        else:
            opponent = fTeams[t]
    bsentry = []
    bsentry.append(gameStats['Game Date'])
    bsentry.append(gameStats['Game Year'])
    bsentry.append(int(week))
    bsentry.append(gameStats['Game ID'])
    teamid = teamdf.loc[teamdf['City'] == team].iloc[0]['team_id']
    bsentry.append(teamid)
    bsentry.append(int(fTeamTotals[team]['G']))
    bsentry.append(int(fTeamTotals[team]['SH']))
    bsentry.append(int(fTeamTotals[team]['G'])/int(fTeamTotals[team]['SH']))
    bsentry.append(int(fTeamTotals[team]['Wd. SH']))
    bsentry.append(int(fTeamTotals[team]['Bl. SH (Off.)']))
    bsentry.append(int(fTeamTotals[team]['Bl. SH (Def)']))
    bsentry.append(int(fTeamTotals[team]['LB']))
    bsentry.append(int(fTeamTotals[team]['T']))
    bsentry.append(int(fTeamTotals[team]['CTO']))
    fos = fTeamTotals[team]['FO'].split('/')
    foWin = int(fos[0])
    foLoss = int(fos[1]) - foWin
    foPerc = foWin/int(fos[1])
    bsentry.append(foWin)
    bsentry.append(foLoss)
    bsentry.append(foPerc)
    ppg = 0
    ppopp = penaltyStats[team]['Opportunities']
    pk = 0
    pkp = 0
    penalties = 0
    for teampp in penaltyStats:
        if teampp == team:
            for item in penaltyStats[team]:
                if item == 'Opportunities':
                    break
                else:
                    ppg+=penaltyStats[team][item]
        else:
            for item in penaltyStats[teampp]:
                if item == 'Opportunities':
                    pkp = 1 - (pk/int(penaltyStats[teampp]['Opportunities']))
                    pk = int(penaltyStats[teampp]['Opportunities'])-pk
                    penalties = int(penaltyStats[teampp]['Opportunities'])
                else:
                    pk+=penaltyStats[teampp][item]
    bsentry.append(ppg)
    bsentry.append(ppopp)
    bsentry.append(ppg/ppopp)                                       
    bsentry.append(pk)
    bsentry.append(penalties)
    bsentry.append(pkp)
    numTeamCheck = 0
    if goalsMatch1 == fTeamTotals[team]['G']:
        numTeamCheck = 2
        bsentry.append(savesentry2)
        bsentry.append(savesentry2/int(fTeamTotals[opponent]['G']))
    else:
        bsentry.append(savesentry1)
        bsentry.append(savesentry1/int(fTeamTotals[opponent]['G']))
        numTeamCheck = 1
    if winCheck == numTeamCheck:
        bsentry.append(1)
    else:
        bsentry.append(0)
        qKey = ''
    for q in quarters.keys():
        if team in q:
            qKey = q
    for qs in quarters[qKey].keys():
        bsentry.append(int(quarters[qKey][qs]))
    bsentry.append(hoa)
    bsentry.append(fTeamTotals[team]['A'])
    return bsentry


def generatePlayerStat(name, week, tIdx):
    pnSplit = name.split(',')
    psentry = []
    psentry.append(gameStats['Game Year'])
    psentry.append(int(week))
    psentry.append(gameStats['Game ID'])
    tidrow = teamdf[teamdf['City'] == df.iloc[tIdx]['Team']]
    psentry.append(tidrow['team_id'].iloc[0])
    psentry.append(pnSplit[1])
    psentry.append(int(df['G'].iloc[tIdx]))
    psentry.append(int(df['SH'].iloc[tIdx]))
    psentry.append(int(df['G'].iloc[tIdx]))
    

# 'Date', 'Year', 'Week', 'game_id', 'team_id', 'Goals', 'Shots', 'Shot_Percent', 
# 'Wide Shots','SH_BLK_OFF', 'SH_BLK_DEF','GB', 'TOs', 'CTOs', 'FO_Win', 'FO_Loss', 
# 'FO_Percent','Power_Play_Goals', 'Power_Play_Opp', 'Power_Play_Percent', 'Penalty_Kill', 
# 'Penalties', 'Pentalty_Kill_Percent', 'Saves', 'Save_Percent', 'Win', 'Q1_Score', 
# 'Q2_Score', 'Q3_Score', 'Q4_Score', 'OT', 'OT_Score', 'Home_Away', 'Assists'