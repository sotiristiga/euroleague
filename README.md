This file it is a R Markdown dashboard for Euroleague!


Includes Teams and Players Stats for Seasons 2019-2020, 2020-2021, 2021-2022, 2022-2023, 2023-2024(ongoing).

You must import the datasets from each season for players and results stats in the first lines after the libraries call.

The stats export from https://basketnews.com/leagues/25-euroleague/schedules.html



The summary tables appears the average values by game, when you find in commands in front of stats these character means:

Total_= Sum values from all fixtures

Average_= Average values by games played

rating_ = Compute when we descenting the stat that we want i.e. if a player has 95 rating on Pts, that means he is better than 95% of players in this stat

Team_ = Refers teams stats

Team_opp_ = Refers opponent stats



dataset_players = Includes the player stats from each game 

Columns:

# Basic stats from websites

Against =  The against team that player played

Team = The team that player played

IDGAME= the fixture and the # of the game in this fixture

Phase= The phase of Euroleague that game happened

Player = The name of player

MIN = Minutes played

PTS = Points scored

F2M = 2point Field goal made

F2A = 2point Field goal attempt

F2GP =  (F2M/F2A) *100%  #Percentage of 2 points that succeed

F3M = 3point Field goal made

F3A = 3point Field goal attempt

F3GP =  (F3M/F3A) *100% #Percentage of 3 points that succeed

FTM = Free throw made

FTA = Free throw attempt

FTP =  (FTM/FTA) *100% # Percentage of free throws that succeed

OR = Offensive Rebounds

DR = Defensive Rebounds

TR = Total Rebounds

AS = Assists

ST = Steals

TO =  Turnovers 

BLK = Blocks 

BLKR =  Blocks that conceed

PF = Fouls committed

RF = Fouls reversed

PIR = Rating from the game

Against = Against Team

HA = Home or Away game (H = Home, A = Away)

results = Win or Lose in this game his team (W = Win, L = Lose)





dataset_results= Includes the games results from each fixture.

Columns:

Fixture = # of fixture which the game happened

Phase= The phase of Euroleague that game happened

Home  = Home Team

Away = Away Team

Q1H = Points from Home team on 1st period

Q2H = Points from Home team on 2nd period

Q3H = Points from Home team on 3th period

Q4H = Points from Home team on 4th period

Q1A = Points from Away team on 1st period

Q2A = Points from Away team on 2nd period

Q3A = Points from Away team on 3th period

Q4A = Points from Away team on 4th period

EXH =  Points from Home team on extra time

EXA =  Points from Home team on extra time

Home_Points = Total points from Home team	

Away_Points = Total points from Away team

Winner	= Winner Team

Loser =  Loser Team

Home_win = Measuring if the home team win ( 0 - Lose, 1 - Win)

Away_win = Measuring if the away team win ( 0 - Lose, 1 - Win)

Season = The season that played





## Advanced Stats that are computed inside of datasets

Possesions = 0.96*(F2A + F3A - OR + TO + 0.44*FTA) # How many possesions takes a team or a player

Assist_ratio = AS / Possesions # Measures the percentage of possessions ending with an assist

As_To_Ratio = AS / TO # This measurement is particularly effective for measuring ball control.

Def_Rat = 100 * (OppPTS / OppPOS) # How many points a player or a team allows per 100 possessions. Only for teams

Off_Rat = 100 * ( PTS / Possesions) # How many points a player or a team scores per 100 possessions.

Net_rating = Off_Rat - Def_Rat # Measures the point differential per 100 possessions

EFG = ((FGM + (0.5 * F3M)) / FGA # How a player or a team are effective on a field who attempt

FT_ratio =  FTA / FGA # Free throw ratio, Ratio of free throws attempted according to the number of shots taken.

Game_score = PTS + (0.4 * FGM) - (0.7 * FGA) - (0.4 * (FTA - FTM)) + (0.7 * OR) + (0.3 * DR) + ST + (0.7 * AS) + (0.7 * BLK) - (0.4 * PF) - TO # Have similar meaning with PIR, but it has coeffients in some stats

PIE= (PTS + FGM + FTM - FGA - FTA + DR + (.5 * OR) + AS + ST + (.5 * BLK) - PF - TO) / (PTS + GameFG + GameFT - GameFGA - GameFTA + GameDRB + (.5 * GamemORB) + GameAST + GameSTL + (.5 * GameBLK) - GamePF - GameTO) # The PIE shows the percentage of facts from a game that can be attributed to a specific player

True_shooting = PTS / (2 * (FGA + 0.44 * FTA)) # determine the overall shooting ability

Turnover_ratio = (TO * 100) / (Possesions) # Measures the percentage of possessions ending with a turnover

Usage = 100 * ((FGA + 0.44 FTA + TO) * ( Team_MP / 5)) / (MIN * (Team_FG + 0.44 * Team_FTA + Team_TO)) # Shows the percentage of possessions ending in a player's hands while on the field

OR_percent = ORB / (TeamORB + OppDRB) # Percentage of rebounds taken in attack by a player or team, based on the number of rebounds that could have been take

Assisted Field goal= AS/FGM # Ratio of field goals scored following an assist. Only for teams

Points per shoot = PTS / (FGA+FTA) # Points who take a player or a team from a shoot who attempts


Functions that I made:

- compute_stats(dataset_players,category,stat,names,ha,wl,ph,season) 

I computed the total, average and rating in a stat that I interest for a Player

dataset_players = dataset that I have made for players stats
category = Which variable want to group_by, choises -> Player
stat = The stat which I want to compute
names = Give the column name that depends from stat
ha = To check their stats if he played Home or Away (choices = "H" for home games, "A" for away games, "" for all games )
wl = To check their stats if their Team Win or Lose (choices = "W" for win games, "L" for lose games, "" for all results )
ph =  phase of Euroleague (choises = "Regular Season","Play offs","Final Four","" for all games)
season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all seasons)



- player_stats(dp,p1,ha,wl,ph,season)

Find all stats for a player with some conditions 

dataset_players = dataset that I have made for players stats

p1 = Name of Player

stat = The stat which I want to compute

ha = To check their stats if he played Home or Away (choices = "H" for home games, "A" for away games, "" for all games )

wl = To check their stats if their Team Win or Lose (choices = "W" for win games, "L" for lose games, "" for all results )

ph =  phase of Euroleague (choises = "Regular Season","Play offs","Final Four","" for all games)

season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all seasons)




- findgamestats(dataset_players,Home_Team,Away_Team,Season,Phase)

Find all stats from a game that you interest

Includes the stats of players and the summarise stats from Teams in this game

dataset_players = dataset that I have made for players stats

Home_Team = The Home Team 

Away_Team = The Away Team

Phase =  phase of Euroleague (choises = "Regular Season","Play offs","Final Four")

Season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024")



- player_stats_by_team_against(dataset_players,Player_Name,Home_Away,Win_Lose,Phase,Season)

Output the average stats of the Player against each team that he played

dataset_players = dataset that I have made for players stats

Player_Name =  The Player that you interest

Home_Away = To check their stats if he played Home or Away (choices = "H" for home games, "A" for away games, "" for all games ) 

Win_Lose = To check their stats if their Team Win or Lose (choices = "W" for win games, "L" for lose games, "" for all results )

Phase =  phase of Euroleague (choises = "Regular Season","Play offs","Final Four", "" for all phases)

Season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all Seasons)


- compute_stats_teams(dataset_players,category,stat,names,Home_Away,result,Phase,Season)

I computed the total, average and rating in a stat that I interest for a Team 


dataset_players = dataset that I have made for players stats

category = Which variable want to group_by, choises -> Team

stat = The stat which I want to compute

names = Give the column name that depends from stat

Home_Away = To check their stats if he played Home or Away (choices = "H" for home games, "A" for away games, "" for all games )

result = To check their stats if their Team Win or Lose (choices = "W" for win games, "L" for lose games, "" for all results )

Phase =  phase of Euroleague (choises = "Regular Season","Play offs","Final Four","" for all games)

Season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all Seasons)


- head_to_head_teams(dataset_players,Team1,Team2,Season,Phase)

compare two teams their stats to the tournament and between games

dataset_players =   dataset that I have made for players stats

Team1 = Select the first team

Team2 = Select the second team

Phase =  phase of Euroleague (choises = "Regular Season","Play offs","Final Four","" for all games)

Season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all Seasons)



- Games_summary(dataset_results,Team1,season) 

The total games that a team played in all tournament, away, home and how wins or Loses made it in all tournament and at home or away games


dataset_results = Includes the games results from each fixture

Team1 =  The team that I want

season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all Seasons)


- Games_summary_between_teams(dataset_results,Team1,Team2,Season)

Total games between these 2 teams in all tournamert, for each phase, how many home and away games played and which have most wins between these 2

dataset_results = Includes the games results from each fixture

Team1 = Select the first team

Team2 = Select the second team

Season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all Seasons)



- Games_summary_between_teams(dataset_results,Team1,Team2,Season)

Total games between these 2 teams in all tournamert, for each phase, how many home and away games played and which have most wins between these 2

dataset_results = Includes the games results from each fixture

Team1 = Select the first team

Team2 = Select the second team

season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all Seasons)



- search_team(dt,Team1,ph,ha,result,season)

Find all stats for a team with some conditions 

dt =   dataset that I have made for players stats

Team1 = The team that I want
 
ph =  phase of Euroleague (choises = "Regular Season","Play offs","Final Four","" for all games)

ha = To check their stats if he played Home or Away (choices = "H" for home games, "A" for away games, "" for all games )

result= To check their stats if their Team Win or Lose (choices = "W" for win games, "L" for lose games, "" for all results )

season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all Seasons)


- teamplayersstats(dataset_players,ha,wl,ph,season,Team)

The avarege stats from all players for each Team

dataset_players =   dataset that I have made for players stats

ha = To check their stats if he played Home or Away (choices = "H" for home games, "A" for away games, "" for all games )

wl= To check their stats if their Team Win or Lose (choices = "W" for win games, "L" for lose games, "" for all results )

ph =  phase of Euroleague (choises = "Regular Season","Play offs","Final Four","" for all games)

season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all Seasons)

Team1 = The team that I want


- compare_teams=function(Team1,season,phase,ha,Result)

Computes the stats for the Team that you interest and use for the comparison of two teams. It could be the same team when you want to chech stats with different conditions

Team1 = The team that I want

season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all Seasons)

ph =  phase of Euroleague (choises = "Regular Season","Play offs","Final Four","" for all games)

season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all Seasons)


- compute_best_stats(dataset_players,stat,season)

Output the 5 highest values of Players in this stat category in a game

dataset_players =   dataset that I have made for players stats

stat = The stat which I want to compute

season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all Seasons)



- compute_best_stats_teams(dataset_players,stat,season)

Output the 5 highest values of Teams in this stat category in a game

dataset_players =   dataset that I have made for players stats

stat = The stat which I want to compute

season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all Seasons)


- period_points(dataset_results,Team_select,Season,Phase,ha,result)

Compute the average points that a team scored & conceed in every quarter, first & second half and extra time)

dataset_results = Includes the games results from each fixture

Team_select = The team that I want

Season = season that interest (choises = "2019-2020", "2020-2021", "2021-2022", "2022-2023", "2023-2024", "" for all Seasons)

Phase =  phase of Euroleague (choises = "Regular Season","Play offs","Final Four","" for all games)

ha = To check their stats if he played Home or Away (choices = "H" for home games, "A" for away games, "" for all games )

result= To check their stats if their Team Win or Lose (choices = "W" for win games, "L" for lose games, "" for all results )





R markdown dashboard output


The output is a browser page that includes 4 different tabs

The first tab concern on the players and their stats, the second refers to stats of a game, the thrd to team stats and the last dealing with fantasy euroleague

In the first tab we have 5 new tabs

Basic stats: In this tab there are the top 5 players for their average values

You can use and some conditions for the phase & season you interest, what the player made at home or away games and wins or loses 

The function which used -> compute_stats(dataset_players,category,stat,names,ha,wl,ph,season) 

Games(G - the only variable that I haven't the average),
Minutes(Average_MIN),
Points(Average_PTS),
Game_score,
Average Possesions,
Offensive Rating,
Defensive Rebounds(Average_DR),
Offensive Rebounds(Average_OR),
Offensive Rebound(%)(OR_percent)
Total Rebounds(Average_TR),
Assists(Average_AS),
Assists_ratio,
Assists vs Turnover ratio (As_To_Ratio),
Steals(Average_ST),
Blocks(Average_BLK),
Blocks reversed(Average_BLKR),
Personal Fouls(Average_PF),
Reversed Fouls(Average_RF),
Turnovers(Average_TO),
Turnover ratio(TO_ratio),
PIR(Average_PIR),
PIE(Average_PIE)

Shooting stats: In this tab there are the top 5 players for their average values on 

You can use and some conditions for the phase & season you interest, what the player made at home or away games and wins or loses 

The function which used -> compute_stats(dataset_players,category,stat,names,ha,wl,ph,season) 

Points per Shoot,
Free throws made(Average_FTM),
Free throws attempt(Average_FTA),
Percentage on free throws (PFT),
Percent_attempt_FT # Percent of the attempts that was Free Throws
2 Points Field goal made(Average_F2M),
2 Points Field goal attempt(Average_F2A),
Percentage on 2 Points Field goal (P2),
Percent_attempt_P2 # Percent of the attempts that was 2 Points shots
3 Points Field goal made(Average_F3M),
3 Points Field goal attempt(Average_F3A),
Percentage on 3 Points Field goal (P3)
Percent_attempt_P3 # Percent of the attempts that was 3 Points shots
Free throw ratio(FT_ratio),
Usage,
EFG,
True shooting

Record stats: Includes the 5 best values that a Player had in a game. Refers to stats

PTS,
MIN,
PIR,
AS,
F2M,
F2A,
F3M,
F3A,
FTM,
FTA,
OR,
OR_percent
DR,
TR,
TO,
ST,
BLK,
BLKR,
RF,
Game_score,
PIR,
Usage,
PIE

The function which used ->

Search Player: You can find the stats of a player that you interest, you can use and some conditions for the phase & season you interest, what the player made at home or away games and wins or loses 

The function which used -> player_stats(dp,p1,ha,wl,ph,season)

In this page you can find:

- All the teams that he played
- The total games that he played in each team
- The average stats of the player 

Compare Players: You can compare two players for their stats, you can use and some conditions for the phase & season you interest, what the player made at home or away games and wins or loses 

The function which used -> player_stats(dp,p1,ha,wl,ph,season)

In this page you can find:

- All the teams that they played
- The total games that he played in each team
- The average stats of the players


Player stats by team: You can find all stats of the players for each team, you can use and some conditions for the phase & season you interest, what the player made at home or away games and wins or loses 

The function which used -> teamplayersstats(dataset_players,ha,wl,ph,season,Team)


Player stats against each team: You can find all stats from a player with all opponents teams that he played, you can use and some conditions for the phase & season you interest, what the player made at home or away games and wins or loses 

The function which used -> player_stats_by_team_against(dataset_players,Player_Name,Home_Away,Win_Lose,Phase,Season)


Player stats by a game: You can find the stats of each player in every game that he played

In Second tab, Find stats for a game, is only the stats of players and teams in the game that you select 

The function which used -> findgamestats(dataset_players,Home_Team,Away_Team,Season,Phase)



In the Third tab we have 6 new tabs

Team ranking: Have some ranking stats such as

The function which used -> compute_stats_teams(dataset_players,category,stat,names,Home_Away,result,Phase,Season)

Games (G)
Team average points
Team average points conceed 
Difference between Team average points  & Team average points conceed (Diff)
Wins
Loses
Percentage of wins (Win_Per)

You can use and some conditions for the phase & season you interest, what the player made at home or away games and wins or loses 

Team Basic stats: Have the other basic stats per game such as

The function which used -> compute_stats_teams(dataset_players,category,stat,names,Home_Away,result,Phase,Season)

Assists(AS),
Opponent Assists(opp_AS),
Defensive Rebounds(DR),
Opponent Defensive Rebounds(opp_DR),
Offensive Rebounds(OR),
Opponent Offensive Rebounds(opp_OR),
Total Rebounds(TR),
Opponent Total Rebounds(opp_TR),
Steals(ST),
Opponent Steals(opp_ST),
Turnovers(TO),
Opponent Turnovers(opp_TO),
Blocks(BLK),
Opponent Blocks(opp_BLK),
Personal Fouls(PF),
Opponent Personal Fouls(opp_PF)

You can use and some conditions for the phase & season you interest, what the player made at home or away games and wins or loses 

Team Shooting stats: Have the shootings stats per game such as

2 Points Field goal made(F2M),
2 Points Field goal attempt(F2A),
Percentage on 2 Points Field goal (P2),
3 Points Field goal made(F3M),
3 Points Field goal attempt(F3A),
Percentage on 3 Points Field goal (P3),
Free throws made(FTM),
Free throws attempt(FTA),
Percentage on free throws (PFT),
Opponent 2 Points Field goal made(opp_F2M),
Opponent 2 Points Field goal attempt(opp_F2A),
Opponent Percentage on 2 Points Field goal (opp_P2),
Opponent 3 Points Field goal made(opp_F3M),
Opponent 3 Points Field goal attempt(opp_F3A),
Opponent Percentage on 3 Points Field goal (opp_P3),
Opponent Free throws made(opp_FTM),
Opponent Free throws attempt(opp_FTA),
Opponent Percentage on free throws (opp_PFT)

You can use and some conditions for the phase & season you interest, what the player made at home or away games and wins or loses 



Team Advanced stats: Have the advanced stats per game for all teams such as

The function which used -> compute_stats_teams(dataset_players,category,stat,names,Home_Away,result,Phase,Season)

Assisted Field goal (ASSISTED_FG)
Assists vs Turnover ratio (As_To_RATIO)
EFG
Free throw ratio(FT_ratio),
Average Possesions (POS),
Average Possesions of opponents (OPP_POS)
Offensive Rating(OFF_RAT)
Defensive Rating(DEF_RAT)
Net Rating (NET_RAT)
Turnover ratio(TO_ratio),
True shooting(TRUESHOT),
PIR
PIR opponent (PIR_opp)

You can use and some conditions for the phase & season you interest, what the player made at home or away games and wins or loses 


Head to Head: compare two teams their stats to the tournament and between games. Also, have and total games that played in each phase & season and which has the most wins or loses total & what happen at home and away games

The functions which used -> head_to_head_teams(dataset_players,Team1,Team2,Season,Phase)
                         -> Games_summary_between_teams(dataset_results,Team1,Team2,Season)


Compare Team: You can find the stats of a team that you interest and compare with another team, it is useful for compare the same team with different conditions.
Also, it has period points from each team that you select and finding in how many stats the one team is better than another.

You can use and some conditions for the phase & season you interest and what the team made at home or away games and wins or loses

The functions which used -> compare_teams=function(Team1,season,phase,ha,Result)
                         -> period_points(dataset_results,Team_select,Season,Phase,ha,result)



Search Team: You can find the stats of a team that you interest, you can use and some conditions for the phase & season you interest and what the team made at home or away games and wins or loses

The functions which used -> search_team(dt,Team1,ph,ha,result,season)
                         -> period_points(dataset_results,Team_select,Season,Phase,ha,result)


Record basic stats: Includes  both the 5 best and worst values that a team had in a game. Refers to stats

PTS,
AS,
F2M,
F2A,
P2,
F3M,
F3A,
P3,
FTM,
FTA,
PFT,
OR,
DR,
TR,
TO,
ST,
BLK,
PIR,
PF,
POS(Possesions),
ASR(Assists Ratio),
ASFG(Assisted Field goal),
ASTOR(Assists-Turnover Ratio),
TOR(Turnover Ratio),
EFG
FTR(Free Throw Ratio)
TS(True Shooting)
OFR(Offensive Rating)


Record basic stats: Includes  both the 5 best and worst values that a team had in a game. Refers to stats

POS(Possesions),
ASR(Assists Ratio),
ASFG(Assisted Field goal),
ASTOR(Assists-Turnover Ratio),
TOR(Turnover Ratio),
EFG
FTR(Free Throw Ratio)
TS(True Shooting)
OFR(Offensive Rating)

The functions which used -> compute_best_stats_teams=function(dataset_players,stat,season)




If you find something wrong or you want to discuss it, it's pleasure to contact with me to my LinkedIn profile 

Also, if you have any different ideas to improve or to insert, I wil be available to hear you

The next step is to insert more Euroleague to the project.
 
