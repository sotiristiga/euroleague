import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from math import ceil
from datetime import date
from streamlit_dynamic_filters import DynamicFilters
import urllib.request
from PIL import Image
import time
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n, sample_frac, head, arrange, mutate, group_by, summarize, DelayFunction)
from itables.streamlit import interactive_table
from itables import to_html_datatable
from streamlit.components.v1 import html
from plotly.subplots import make_subplots

st.set_page_config(layout='wide', page_title="Standings")

dataset=pd.read_csv('C:/Users/surve/OneDrive/Desktop/Tiganitas work/EUROLEAGUE/stats/basketnews stats/superleague2425.csv')

selected_ha = st.sidebar.selectbox("Home or Away games:",['Away', 'Home', 'All'],index=2)
selected_season = st.sidebar.selectbox("Season:",['All','2024-2025'],index=0)
selected_phase = st.sidebar.selectbox("Phase:",['Regular Season', 'Play offs', 'Play out','All'],index=3)
selected_wl = st.sidebar.selectbox("Result:",['Win','Draw', 'Lose','All'],index=3)
selected_round = st.sidebar.selectbox("Round:",['First Round', 'Second Round', 'All'],index=2)


if "All" in selected_ha:
    selected_ha = ['Away', 'Home',]
    dataset_filter=dataset.loc[dataset['Home_Away'].isin(selected_ha)]
    select_ha=''
else:
    dataset_filter=dataset.loc[dataset['Home_Away']==selected_ha]
    select_ha = selected_ha

if "All" in selected_season:
    selected_season = ['2016-2017', '2017-2018', '2018-2019', '2019-2020','2020-2021','2021-2022', '2022-2023','2023-2024','2024-2025']
    dataset_filter=dataset_filter.loc[dataset_filter['Season'].isin(selected_season)]
    select_season = ''
else:
    dataset_filter=dataset_filter.loc[dataset_filter['Season']==selected_season]
    select_season = selected_season

if "All" in selected_wl:
    selected_wl = ['Win','Draw', 'Lose']
    dataset_filter = dataset_filter.loc[dataset_filter['Result'].isin(selected_wl)]
    select_wl = ''
else:
    dataset_filter= dataset_filter.loc[dataset_filter['Result'] == selected_wl]
    select_wl = selected_wl

if "All" in selected_phase:
    selected_phase = ['Regular Season', 'Play offs', 'Play out']
    dataset_filter = dataset_filter.loc[dataset_filter['Phase'].isin(selected_phase)]
    select_phase = ''
else:
    dataset_filter = dataset_filter.loc[dataset_filter['Phase'] == selected_phase]
    select_phase = selected_phase

if "All" in selected_round:
    selected_round = ['First Round', 'Second Round', ]
    dataset_filter = dataset_filter.loc[dataset_filter['Round'].isin(selected_round)]
    select_round = ''
else:
    dataset_filter = dataset_filter.loc[dataset_filter['Round'] == selected_round]
    select_round = selected_round



tab1,tab2,tab3=st.tabs(['Standing','Player League Leaders','Players Team'])
with tab1:
    games=dataset_filter[['Team','idseason']].value_counts().reset_index()['Team'].value_counts().reset_index().rename(columns={'count':'Games'})
    wins=dataset_filter.loc[dataset_filter.Result=='Win'][['Team','idseason']].value_counts().reset_index()['Team'].value_counts().reset_index().rename(columns={'count':'Wins'})
    loses=dataset_filter.loc[dataset_filter.Result=='Lose'][['Team','idseason']].value_counts().reset_index()['Team'].value_counts().reset_index().rename(columns={'count':'Loses'})
    draws=dataset_filter.loc[dataset_filter.Result=='Draw'][['Team','idseason']].value_counts().reset_index()['Team'].value_counts().reset_index().rename(columns={'count':'Draws'})

    Team_Standings=pd.merge(games,wins,how='left',on='Team')
    Team_Standings=pd.merge(Team_Standings,draws,how='left',on='Team')
    Team_Standings=pd.merge(Team_Standings,loses,how='left',on='Team')
    Team_Standings['Wins']=Team_Standings['Wins'].fillna(0)
    Team_Standings['Loses']=Team_Standings['Loses'].fillna(0)
    Team_Standings['Draws']=Team_Standings['Draws'].fillna(0)
    Team_Standings['Points']=Team_Standings['Wins']*3+Team_Standings['Draws']*1

    teamsscored=dataset_filter.groupby(['Team','Against','idseason'])[['Goals','Own goals']].sum().reset_index().rename(columns={'Goals':'Goals Team','Own goals':'Own goals Against'})
    againstscored=teamsscored.rename(columns={'Goals Team':'Goals Against','Own goals Against':'Own goals Team'})
    againstscored.drop('Against',axis=1,inplace=True)
    againstscored=againstscored.rename(columns={'Team':'Against'})

    goals=pd.merge(teamsscored,againstscored)

    goals['Goals Scored']=goals['Goals Team']+goals['Own goals Team']
    goals['Goals Conceed']=goals['Goals Against']+goals['Own goals Against']
    total_goals=goals.groupby('Team')[['Goals Scored','Goals Conceed']].sum().reset_index()

    Team_Standings=pd.merge(Team_Standings,total_goals,how='left',on='Team').sort_values('Points',ascending=False).reset_index()
    Team_Standings.drop('index',axis=1,inplace=True)
    Team_Standings=Team_Standings.reset_index()
    Team_Standings['Rank']=Team_Standings['index']+1
    Team_Standings.drop('index',axis=1,inplace=True)
    Team_Standings=Team_Standings[['Rank','Team','Points','Games','Wins','Draws','Loses','Goals Scored','Goals Conceed']]

    interactive_table(Team_Standings.set_index('Rank'),
                          paging=False,height=960,width=20000,showIndex=True,classes="display order-column nowrap table_with_monospace_font",searching=False,fixedColumns=True,select=True,info=False,scrollCollapse=True,
            scrollX=True,scrollY=1000,fixedHeader=True,scroller=True,columnDefs=[{"className": "dt-center", "targets": "_all"}])

with tab2:
    games=dataset_filter['Player'].value_counts().reset_index().rename(columns={'count':'Games'})
    computeplayerstats=dataset_filter.groupby('Player')[['Minutes played',
       'Goals', 'Assists', 'Yellow card', 'Red card', 'Shots on target',
       'Shots off target', 'Shots blocked', 'Dribble attempts',
       'Dribble attempts succ', 'Penalty won', 'Big chances missed',
       'Penalty miss', 'Hit woodwork', 'Defensive actions', 'Clearances',
       'Blocked shots', 'Interceptions', 'Total tackles', 'Dribbled past',
       'Penalty committed', 'Own goals', 'Last man tackle',
       'Error led to shot', 'Clearance off line', 'Error led to goal',
       'Touches', 'Accurate passes', 'Total passes',
       'Key passes', 'Total Crosses', 'Accurate Crosses', 'Total Long balls',
       'Accurate Long balls', 'Big chances created', 'Duels', 'Duels won',
       'Ground duels', 'Ground duels won', 'Aerial duels', 'Aerial duels won',
       'Possession lost', 'Fouls', 'Was fouled', 'Offsides', 'Saves',
       'Punches', 'Runs out', 'Runs out succ', 'High claims',
       'Saves from inside box', 'Penalties saved']].sum().reset_index()
    computeplayerstats["Dribble(%)"]=(100*computeplayerstats["Dribble attempts succ"]/computeplayerstats["Dribble attempts"]).round(3)
    computeplayerstats["Dribble(%)"]=computeplayerstats["Dribble(%)"].fillna(0)
    computeplayerstats["Passes(%)"] = (100 * computeplayerstats["Accurate passes"] / computeplayerstats["Total passes"]).round(3)
    computeplayerstats["Passes(%)"] = computeplayerstats["Passes(%)"].fillna(0)
    computeplayerstats["Crosses(%)"] = (100 * computeplayerstats["Accurate Crosses"] / computeplayerstats["Total Crosses"]).round(3)
    computeplayerstats["Crosses(%)"] = computeplayerstats["Crosses(%)"].fillna(0)
    computeplayerstats["Long balls(%)"] = (100 * computeplayerstats["Accurate Long balls"] / computeplayerstats["Total Long balls"]).round(3)
    computeplayerstats["Long balls(%)"] = computeplayerstats["Long balls(%)"].fillna(0)
    computeplayerstats["Duels(%)"] = (100 * computeplayerstats["Duels won"] / computeplayerstats["Duels"]).round(3)
    computeplayerstats["Duels(%)"] = computeplayerstats["Duels(%)"].fillna(0)
    computeplayerstats["Aerial duels(%)"] = (100 * computeplayerstats["Aerial duels won"] / computeplayerstats["Aerial duels"]).round(3)
    computeplayerstats["Aerial duels(%)"] = computeplayerstats["Aerial duels(%)"].fillna(0)
    computeplayerstats["Runs out(%)"] = (100 * computeplayerstats["Runs out succ"] / computeplayerstats["Runs out"]).round(3)
    computeplayerstats["Runs out(%)"] = computeplayerstats["Runs out(%)"].fillna(0)
    computeplayerstats=pd.merge(computeplayerstats,games)
    selected_stats=st.selectbox("Category:",['Games','Minutes played',
       'Goals', 'Assists', 'Yellow card', 'Red card', 'Shots on target',
       'Shots off target', 'Shots blocked','Dribble attempts succ', 'Dribble attempts',
        'Penalty won', 'Big chances missed',
       'Penalty miss', 'Hit woodwork', 'Defensive actions', 'Clearances',
       'Blocked shots', 'Interceptions', 'Total tackles', 'Dribbled past',
       'Penalty committed', 'Own goals', 'Last man tackle',
       'Error led to shot', 'Clearance off line', 'Error led to goal',
       'Touches', 'Accurate passes', 'Total passes',
       'Key passes', 'Accurate Crosses','Total Crosses', 'Accurate Long balls', 'Total Long balls',
        'Big chances created','Duels won', 'Duels',
        'Ground duels won','Ground duels', 'Aerial duels won','Aerial duels',
       'Possession lost', 'Fouls', 'Was fouled', 'Offsides', 'Saves',
       'Punches', 'Runs out succ', 'Runs out','High claims',
       'Saves from inside box', 'Penalties saved'])
    regex1='Player|' + selected_stats

    outputtable=computeplayerstats.filter(regex=regex1).sort_values(selected_stats,ascending=False).reset_index()
    outputtable.drop('index',axis=1,inplace=True)
    outputtable=outputtable.reset_index()
    outputtable['Rank']=outputtable['index']+1
    interactive_table(
        outputtable[['Rank','Player',selected_stats]].set_index('Rank'),
        paging=False, height=900, width=2000, showIndex=True,
        classes="display order-column nowrap table_with_monospace_font", searching=True,
        fixedColumns=True, select=True, info=False, scrollCollapse=True,
        scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
        columnDefs=[{"className": "dt-center", "targets": "_all"}])
with tab3:
    games = dataset_filter[['Player','Team']].value_counts().reset_index().rename(columns={'count': 'Games'})
    computeplayerstats = dataset_filter.groupby(['Player','Team'])[['Minutes played',
                                                           'Goals', 'Assists', 'Yellow card', 'Red card',
                                                           'Shots on target',
                                                           'Shots off target', 'Shots blocked', 'Dribble attempts',
                                                           'Dribble attempts succ', 'Penalty won', 'Big chances missed',
                                                           'Penalty miss', 'Hit woodwork', 'Defensive actions',
                                                           'Clearances',
                                                           'Blocked shots', 'Interceptions', 'Total tackles',
                                                           'Dribbled past',
                                                           'Penalty committed', 'Own goals', 'Last man tackle',
                                                           'Error led to shot', 'Clearance off line',
                                                           'Error led to goal',
                                                           'Touches', 'Accurate passes', 'Total passes',
                                                           'Key passes', 'Total Crosses', 'Accurate Crosses',
                                                           'Total Long balls',
                                                           'Accurate Long balls', 'Big chances created', 'Duels',
                                                           'Duels won',
                                                           'Ground duels', 'Ground duels won', 'Aerial duels',
                                                           'Aerial duels won',
                                                           'Possession lost', 'Fouls', 'Was fouled', 'Offsides',
                                                           'Saves',
                                                           'Punches', 'Runs out', 'Runs out succ', 'High claims',
                                                           'Saves from inside box',
                                                           'Penalties saved']].sum().reset_index()
    computeplayerstats["Dribble(%)"] = (
                100 * computeplayerstats["Dribble attempts succ"] / computeplayerstats["Dribble attempts"]).round(3)
    computeplayerstats["Dribble(%)"] = computeplayerstats["Dribble(%)"].fillna(0)
    computeplayerstats["Passes(%)"] = (
                100 * computeplayerstats["Accurate passes"] / computeplayerstats["Total passes"]).round(3)
    computeplayerstats["Passes(%)"] = computeplayerstats["Passes(%)"].fillna(0)
    computeplayerstats["Crosses(%)"] = (
                100 * computeplayerstats["Accurate Crosses"] / computeplayerstats["Total Crosses"]).round(3)
    computeplayerstats["Crosses(%)"] = computeplayerstats["Crosses(%)"].fillna(0)
    computeplayerstats["Long balls(%)"] = (
                100 * computeplayerstats["Accurate Long balls"] / computeplayerstats["Total Long balls"]).round(3)
    computeplayerstats["Long balls(%)"] = computeplayerstats["Long balls(%)"].fillna(0)
    computeplayerstats["Duels(%)"] = (100 * computeplayerstats["Duels won"] / computeplayerstats["Duels"]).round(3)
    computeplayerstats["Duels(%)"] = computeplayerstats["Duels(%)"].fillna(0)
    computeplayerstats["Ground duels(%)"] = (
            100 * computeplayerstats["Ground duels won"] / computeplayerstats["Ground duels"]).round(3)
    computeplayerstats["Ground duels(%)"] = computeplayerstats["Ground duels(%)"].fillna(0)
    computeplayerstats["Aerial duels(%)"] = (
                100 * computeplayerstats["Aerial duels won"] / computeplayerstats["Aerial duels"]).round(3)
    computeplayerstats["Aerial duels(%)"] = computeplayerstats["Aerial duels(%)"].fillna(0)
    computeplayerstats["Runs out(%)"] = (
                100 * computeplayerstats["Runs out succ"] / computeplayerstats["Runs out"]).round(3)
    computeplayerstats["Runs out(%)"] = computeplayerstats["Runs out(%)"].fillna(0)
    selected_Team = st.selectbox("Team:", dataset_filter['Team'].unique())
    computeplayerstats = pd.merge(computeplayerstats, games)
    teamstats=computeplayerstats.loc[computeplayerstats.Team==selected_Team ][['Player','Games','Minutes played',
                                                           'Goals', 'Assists', 'Yellow card', 'Red card',
                                                           'Shots on target',
                                                           'Shots off target', 'Shots blocked', 'Dribble attempts succ','Dribble attempts',
                                                           "Dribble(%)", 'Penalty won', 'Big chances missed',
                                                           'Penalty miss', 'Hit woodwork', 'Defensive actions',
                                                           'Clearances',
                                                           'Blocked shots', 'Interceptions', 'Total tackles',
                                                           'Dribbled past',
                                                           'Penalty committed', 'Own goals', 'Last man tackle',
                                                           'Error led to shot', 'Clearance off line',
                                                           'Error led to goal',
                                                           'Touches', 'Accurate passes', 'Total passes',"Passes(%)",
                                                           'Key passes', 'Accurate Crosses','Total Crosses', "Crosses(%)",
                                                           'Accurate Long balls','Total Long balls',"Long balls(%)", 'Big chances created', 'Duels won','Duels',"Duels(%)",
                                                           'Ground duels won','Ground duels', "Ground duels(%)", 'Aerial duels won','Aerial duels',"Aerial duels(%)",
                                                           'Possession lost', 'Fouls', 'Was fouled', 'Offsides','Saves',
                                                           'Punches', 'Runs out succ','Runs out',  "Runs out(%)",'High claims','Saves from inside box','Penalties saved']]
    interactive_table(
        teamstats.sort_values('Minutes played',ascending=False).set_index('Player'),
        paging=False, height=900, width=2000, showIndex=True,
        classes="display order-column nowrap table_with_monospace_font", searching=True,
        fixedColumns=True, select=True, info=False, scrollCollapse=True,
        scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
        columnDefs=[{"className": "dt-center", "targets": "_all"}])
