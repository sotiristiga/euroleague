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


st.set_page_config(layout='wide',page_title="Search a Team",page_icon="🏀")
st.sidebar.write("If an error message appears, please refresh the page")
st.write("## Euroleague stats from 2017 to present")

def fixture_format1(Fixture):
    if Fixture<=15:
        return "First Round"
    elif Fixture>15 and Fixture<=30:
        return "Second Round"
    elif Fixture==31:
        return "PO 1"
    elif Fixture == 32:
        return "PO 2"
    elif Fixture == 33:
        return "PO 3"
    elif Fixture == 34:
        return "PO 4"
    elif Fixture == 35:
        return "PO 5"
    elif Fixture==36:
        return "Semi Final"
    elif Fixture==37:
        return "Third Place"
    elif Fixture==38:
        return "Final"
def fixture_format2(Fixture):
    if Fixture <= 15:
        return "First Round"
    elif Fixture > 15 and Fixture <= 30:
        return "Second Round"
    elif Fixture == 31:
        return "PO 1"
    elif Fixture == 32:
        return "PO 2"
    elif Fixture == 33:
        return "PO 3"
    elif Fixture == 34:
        return "PO 4"
    elif Fixture == 35:
        return "Semi Final"
    elif Fixture == 36:
        return "Third Place"
    elif Fixture == 37:
        return "Final"
def fixture_format3(Fixture):
    if Fixture <= 17:
        return "First Round"
    elif Fixture > 17 and Fixture <= 34:
        return "Second Round"
def fixture_format4(Fixture):
    if Fixture <= 17:
        return "First Round"
    elif Fixture > 17 and Fixture <= 34:
        return "Second Round"
    elif Fixture == 35:
        return "PO 1"
    elif Fixture == 36:
        return "PO 2"
    elif Fixture == 37:
        return "PO 3"
    elif Fixture == 38:
        return "PO 4"
    elif Fixture == 39:
        return "PO 5"
    elif Fixture == 40:
        return "Semi Final"
    elif Fixture == 41:
        return "Third Place"
    elif Fixture == 42:
        return "Final"

def fixture_format5(Fixture):
        if Fixture <= 17:
            return "First Round"
        elif Fixture > 17 and Fixture <= 34:
            return "Second Round"
        elif Fixture == 35:
            return "PI 1"
        elif Fixture == 36:
            return "PI 2"
        elif Fixture == 37:
            return "PO 1"
        elif Fixture == 38:
            return "PO 2"
        elif Fixture == 39:
            return "PO 3"
        elif Fixture == 40:
            return "PO 4"
        elif Fixture == 41:
            return "PO 5"
        elif Fixture == 42:
            return "Semi Final"
        elif Fixture == 43:
            return "Third Place"
        elif Fixture == 44:
            return "Final"



euroleague_2023_2024_playerstats=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/euroleague/main/euroleague_2023_2024_playerstats.csv")
euroleague_2023_2024_playerstats['idseason']=euroleague_2023_2024_playerstats['IDGAME'] + "_" + euroleague_2023_2024_playerstats['Season']
euroleague_2023_2024_playerstats[['Fixture', 'Game']] = euroleague_2023_2024_playerstats['IDGAME'].str.split('_', n=1, expand=True)
euroleague_2023_2024_playerstats['Fixture']=pd.to_numeric(euroleague_2023_2024_playerstats['Fixture'])
euroleague_2023_2024_playerstats['Round']=euroleague_2023_2024_playerstats['Fixture'].apply(fixture_format5)

euroleague_2024_2025_playerstats=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/euroleague/main/euroleague_2024_2025_playerstats.csv")
euroleague_2024_2025_playerstats['idseason']=euroleague_2024_2025_playerstats['IDGAME'] + "_" + euroleague_2024_2025_playerstats['Season']
euroleague_2024_2025_playerstats[['Fixture', 'Game']] = euroleague_2024_2025_playerstats['IDGAME'].str.split('_', n=1, expand=True)
euroleague_2024_2025_playerstats['Fixture']=pd.to_numeric(euroleague_2024_2025_playerstats['Fixture'])
euroleague_2024_2025_playerstats['Round']=euroleague_2024_2025_playerstats['Fixture'].apply(fixture_format5)

euroleague_2024_2025_playerstats=euroleague_2024_2025_playerstats.loc[euroleague_2024_2025_playerstats.Fixture<=10]
euroleague_2023_2024_playerstats=euroleague_2023_2024_playerstats.loc[euroleague_2023_2024_playerstats.Fixture<=10]

euroleague_2023_2024_results=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/euroleague/main/euroleague_2023_2024_results.csv")
euroleague_2023_2024_results['idseason']=euroleague_2023_2024_results['IDGAME'] + "_" + euroleague_2023_2024_results['Season']
euroleague_2023_2024_results[['Fixture', 'Game']] = euroleague_2023_2024_results['IDGAME'].str.split('_', n=1, expand=True)
euroleague_2023_2024_results['Fixture']=pd.to_numeric(euroleague_2023_2024_results['Fixture'])
euroleague_2023_2024_results['Round']=euroleague_2023_2024_results['Fixture'].apply(fixture_format5)

euroleague_2024_2025_results=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/euroleague/main/euroleague_2024_2025_results.csv")
euroleague_2024_2025_results['idseason']=euroleague_2024_2025_results['IDGAME'] + "_" + euroleague_2024_2025_results['Season']
euroleague_2024_2025_results[['Fixture', 'Game']] = euroleague_2024_2025_results['IDGAME'].str.split('_', n=1, expand=True)
euroleague_2024_2025_results['Fixture']=pd.to_numeric(euroleague_2024_2025_results['Fixture'])
euroleague_2024_2025_results['Round']=euroleague_2024_2025_results['Fixture'].apply(fixture_format5)

euroleague_2024_2025_results=euroleague_2024_2025_results.loc[euroleague_2024_2025_results.Fixture<=10]
euroleague_2023_2024_results=euroleague_2023_2024_results.loc[euroleague_2023_2024_results.Fixture<=10]
All_Seasons=pd.concat([euroleague_2023_2024_playerstats,euroleague_2024_2025_playerstats])

All_Seasons_results=pd.concat([euroleague_2023_2024_results,euroleague_2024_2025_results])


def result_format(Win):
    if Win == 1:
        return "W"
    elif Win == 0:
        return "L"



def ha_against_format(HA):
    if HA == "A":
        return "H"
    elif HA == "H":
        return "A"


def result_against_format(results):
    if results == "W":
        return "L"
    elif results == "L":
        return "W"

def wins_against_format(results):
    if results == "W":
        return 1
    elif results=="L":
        return 0
All_Seasons["HA1"] = All_Seasons['HA'].apply(ha_against_format)
All_Seasons["Result1"] = All_Seasons['results'].apply(result_against_format)
All_Seasons["Win"]=All_Seasons['results'].apply(wins_against_format)

home_team=(All_Seasons_results[['Fixture',"Phase","Home","Away","Home_Points","Away_Points",
                                "Q1H","Q2H","Q3H","Q4H",'EXH',"Q1A","Q2A","Q3A","Q4A",'EXA','Season','Round','Home_win','idseason']]
           .rename(columns={"Home":'Team',"Away":'Against',"Home_Points":'Scored',"Away_Points":"Conceed",
                                "Q1H":'Q1S',"Q2H":'Q2S',"Q3H":'Q3S',"Q4H":'Q4S','EXH':'EXS',"Q1A":'Q1C',
                            "Q2A":'Q2C',"Q3A":'Q3C',"Q4A":'Q4C','EXA':'EXC','Home_win':'Win'}))

home_team['HA']="H"
away_team=(All_Seasons_results[['Fixture',"Phase","Home","Away","Home_Points","Away_Points",
                                "Q1H","Q2H","Q3H","Q4H",'EXH',"Q1A","Q2A","Q3A","Q4A",'EXA','Season','Round','Away_win','idseason']]
           .rename(columns={"Home":'Against',"Away":'Team',"Home_Points":'Conceed',"Away_Points":"Scored",
                                "Q1H":'Q1C',"Q2H":'Q2C',"Q3H":'Q3C',"Q4H":'Q4C','EXH':'EXC',"Q1A":'Q1S',
                            "Q2A":'Q2S',"Q3A":'Q3S',"Q4A":'Q4S','EXA':'EXS','Away_win':'Win'}))
away_team['HA']="A"

period_points=pd.concat([home_team,away_team])

period_points["FHS"]=period_points["Q1S"]+period_points["Q2S"]
period_points["FHC"]=period_points["Q1C"]+period_points["Q2C"]
period_points["SHS"]=period_points["Q3S"]+period_points["Q4S"]
period_points["SHC"]=period_points["Q3C"]+period_points["Q4C"]
period_points["results"]=period_points["Win"].apply(result_format)
period_points['EXS'].replace(0, np.nan, inplace=True)
period_points['EXC'].replace(0, np.nan, inplace=True)
period_stats=period_points.groupby(['Team','Season'])[['Q1S',"Q1C",'Q2S',"Q2C",'FHS','FHC','Q3S',"Q3C",'Q4S',"Q4C",'SHS','SHC','EXS',"EXC"]].mean().reset_index().round(1)

finalstats=All_Seasons.groupby(['idseason','Season','Team'])[['PTS','F2M',
                              'F2A', 'F3M', 'F3A', 'FTM', 'FTA', 'OR',
                              'DR', 'TR', 'AS', 'ST', 'TO', 'BLK', 'BLKR','PF', 'RF',
                              'PIR','Possesions']].sum().reset_index()
finalstats['2P(%)']=100*(finalstats['F2M']/finalstats['F2A'])
finalstats['3P(%)']=100*(finalstats['F3M']/finalstats['F3A'])
finalstats['FT(%)']=100*(finalstats['FTM']/finalstats['FTA'])
finalstats['Offensive Rating']=100*(finalstats['PTS']/finalstats['Possesions'])
finalstats['EFG(%)']=100*(finalstats['F2M']+1.5*finalstats['F3M'])/(finalstats['F2A']+finalstats['F3A'])
finalstats['TS(%)']=100*(finalstats['PTS'])/(2*(finalstats['F2A']+finalstats['F3A']+0.44*finalstats['FTA']))
finalstats['FT Ratio']=finalstats['FTA']/(finalstats['F3A']+finalstats['F2A'])
finalstats['AS-TO Ratio']=finalstats['AS']/finalstats['TO']
finalstats['TO Ratio']=100*(finalstats['TO']/finalstats['Possesions'])
finalstats['AS Ratio']=100*(finalstats['AS']/finalstats['Possesions'])
finalstats=finalstats[['Season','Team','PTS','F2M','F2A', '2P(%)','F3M', 'F3A','3P(%)', 'FTM', 'FTA','FT(%)', 'OR','DR', 'TR',
                       'AS', 'ST', 'TO', 'BLK', 'BLKR','PF', 'RF','PIR','Possesions','Offensive Rating','EFG(%)',
                       'TS(%)','FT Ratio','AS-TO Ratio','TO Ratio','AS Ratio']].round(1)

finalstats_opp=All_Seasons.groupby(['idseason','Season','Against'])[['PTS','F2M',
                              'F2A', 'F3M', 'F3A', 'FTM', 'FTA', 'OR',
                              'DR', 'TR', 'AS', 'ST', 'TO', 'BLK', 'BLKR','PF', 'RF',
                              'PIR','Possesions']].sum().reset_index()


finalstats_opp['2P(%)']=100*(finalstats_opp['F2M']/finalstats_opp['F2A'])
finalstats_opp['3P(%)']=100*(finalstats_opp['F3M']/finalstats_opp['F3A'])
finalstats_opp['FT(%)']=100*(finalstats_opp['FTM']/finalstats_opp['FTA'])
finalstats_opp['Offensive Rating']=100*(finalstats_opp['PTS']/finalstats_opp['Possesions'])
finalstats_opp['EFG(%)']=100*(finalstats_opp['F2M']+1.5*finalstats_opp['F3M'])/(finalstats_opp['F2A']+finalstats_opp['F3A'])
finalstats_opp['TS(%)']=100*(finalstats_opp['PTS'])/(2*(finalstats_opp['F2A']+finalstats_opp['F3A']+0.44*finalstats_opp['FTA']))
finalstats_opp['FT Ratio']=finalstats_opp['FTA']/(finalstats_opp['F3A']+finalstats_opp['F2A'])
finalstats_opp['AS-TO Ratio']=finalstats_opp['AS']/finalstats_opp['TO']
finalstats_opp['TO Ratio']=100*(finalstats_opp['TO']/finalstats_opp['Possesions'])
finalstats_opp['AS Ratio']=100*(finalstats_opp['AS']/finalstats_opp['Possesions'])
finalstats_opp=finalstats_opp[['Season','Against','PTS','F2M','F2A', '2P(%)','F3M', 'F3A','3P(%)', 'FTM', 'FTA','FT(%)', 'OR','DR', 'TR',
                       'AS', 'ST', 'TO', 'BLK', 'BLKR','PF', 'RF','PIR','Possesions','Offensive Rating','EFG(%)',
                       'TS(%)','FT Ratio','AS-TO Ratio','TO Ratio','AS Ratio']].round(1)
finalstats_opp=finalstats_opp.add_prefix('opp ').rename(columns={'opp Against':'Team','opp Season':'Season'})

gamesstats=pd.merge(finalstats,finalstats_opp)
allstats_in_a_game=pd.merge(period_points,gamesstats,on=['Season','Team'])






finalstats=allstats_in_a_game.groupby(['Season','Team'])[['PTS','F2M',
                              'F2A', 'F3M', 'F3A', 'FTM', 'FTA', 'OR',
                              'DR', 'TR', 'AS', 'ST', 'TO', 'BLK', 'BLKR','PF', 'RF',
                              'PIR','Possesions']].mean().reset_index()
finalstats['2P(%)']=100*(finalstats['F2M']/finalstats['F2A'])
finalstats['3P(%)']=100*(finalstats['F3M']/finalstats['F3A'])
finalstats['FT(%)']=100*(finalstats['FTM']/finalstats['FTA'])
finalstats['Offensive Rating']=100*(finalstats['PTS']/finalstats['Possesions'])
finalstats['EFG(%)']=100*(finalstats['F2M']+1.5*finalstats['F3M'])/(finalstats['F2A']+finalstats['F3A'])
finalstats['TS(%)']=100*(finalstats['PTS'])/(2*(finalstats['F2A']+finalstats['F3A']+0.44*finalstats['FTA']))
finalstats['FT Ratio']=finalstats['FTA']/(finalstats['F3A']+finalstats['F2A'])
finalstats['AS-TO Ratio']=finalstats['AS']/finalstats['TO']
finalstats['TO Ratio']=100*(finalstats['TO']/finalstats['Possesions'])
finalstats['AS Ratio']=100*(finalstats['AS']/finalstats['Possesions'])
finalstats=finalstats[['Team','Season','PTS','F2M','F2A', '2P(%)','F3M', 'F3A','3P(%)', 'FTM', 'FTA','FT(%)', 'OR','DR', 'TR',
                       'AS', 'ST', 'TO', 'BLK', 'BLKR','PF', 'RF','PIR','Possesions','Offensive Rating','EFG(%)',
                       'TS(%)','FT Ratio','AS-TO Ratio','TO Ratio','AS Ratio']].round(1)

finalstats_opp=allstats_in_a_game.groupby(['Season','Against'])[['PTS','F2M',
                              'F2A', 'F3M', 'F3A', 'FTM', 'FTA', 'OR',
                              'DR', 'TR', 'AS', 'ST', 'TO', 'BLK', 'BLKR','PF', 'RF',
                              'PIR','Possesions']].mean().reset_index()


finalstats_opp['2P(%)']=100*(finalstats_opp['F2M']/finalstats_opp['F2A'])
finalstats_opp['3P(%)']=100*(finalstats_opp['F3M']/finalstats_opp['F3A'])
finalstats_opp['FT(%)']=100*(finalstats_opp['FTM']/finalstats_opp['FTA'])
finalstats_opp['Offensive Rating']=100*(finalstats_opp['PTS']/finalstats_opp['Possesions'])
finalstats_opp['EFG(%)']=100*(finalstats_opp['F2M']+1.5*finalstats_opp['F3M'])/(finalstats_opp['F2A']+finalstats_opp['F3A'])
finalstats_opp['TS(%)']=100*(finalstats_opp['PTS'])/(2*(finalstats_opp['F2A']+finalstats_opp['F3A']+0.44*finalstats_opp['FTA']))
finalstats_opp['FT Ratio']=finalstats_opp['FTA']/(finalstats_opp['F3A']+finalstats_opp['F2A'])
finalstats_opp['AS-TO Ratio']=finalstats_opp['AS']/finalstats_opp['TO']
finalstats_opp['TO Ratio']=100*(finalstats_opp['TO']/finalstats_opp['Possesions'])
finalstats_opp['AS Ratio']=100*(finalstats_opp['AS']/finalstats_opp['Possesions'])
finalstats_opp=finalstats_opp[['Against','Season','PTS','F2M','F2A', '2P(%)','F3M', 'F3A','3P(%)', 'FTM', 'FTA','FT(%)', 'OR','DR', 'TR',
                       'AS', 'ST', 'TO', 'BLK', 'BLKR','PF', 'RF','PIR','Possesions','Offensive Rating','EFG(%)',
                       'TS(%)','FT Ratio','AS-TO Ratio','TO Ratio','AS Ratio']].round(1).rename(columns={'Against':'Team'})

finalstats_opp_for_rating=finalstats_opp.add_prefix("opp ").rename(columns={'opp Team':'Team','opp Offensive Rating':'Defensive Rating','opp Season':'Season'})

gamesstats=pd.merge(finalstats,finalstats_opp_for_rating)
gamesstats=pd.merge(gamesstats,period_stats,on=['Team','Season'])

gamesstats2324PAN=gamesstats.loc[(gamesstats.Season=="2023-2024")&(gamesstats.Team.isin(['PAN','OLY']))]
gamesstats2425PAN=gamesstats.loc[(gamesstats.Season=="2024-2025")&(gamesstats.Team.isin(['PAN','OLY']))]
gamestatsPAN=pd.concat([gamesstats2324PAN,gamesstats2425PAN])

interactive_table(gamestatsPAN.set_index('Team'),
    paging=False, height=900, width=2000, showIndex=True,
    classes="display order-column nowrap table_with_monospace_font", searching=False,
    fixedColumns=True, select=True, info=False, scrollCollapse=True,
    scrollX=True, scrollY=1000, fixedHeader=True, scroller=True, filter='bottom',
    columnDefs=[{"className": "dt-center", "targets": "_all"}])


st.write(All_Seasons.loc[(All_Seasons.Team=='PAN')& (All_Seasons.Season=='2023-2024')][['idseason','results']].value_counts().reset_index()['results'].value_counts())
st.write(All_Seasons.loc[(All_Seasons.Team=='OLY')& (All_Seasons.Season=='2023-2024')][['idseason','results']].value_counts().reset_index()['results'].value_counts())

pts=gamestatsPAN[['Team','Season','PTS','opp PTS']].melt(id_vars=['Team','Season'])
st.write(pts)

pts_bar=px.bar(pts,x='Season',y='value',color="variable", barmode='group',facet_col='Team',
             height=1000,width=2000, text_auto=True,color_discrete_sequence= ['darkorange','black'],labels={'value':'Avg. Points per game','variable':''},title='')
pts_bar.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
pts_bar.update_layout(plot_bgcolor='white',font_size=18)
st.write(pts_bar)

quarter=gamestatsPAN[['Team','Season','Q1S',"Q1C",'Q2S',"Q2C",'Q3S',"Q3C",'Q4S',"Q4C"]].melt(id_vars=['Team','Season'])
quarter['variable']=quarter['variable'].str.replace('S'," Scored")
quarter['variable']=quarter['variable'].str.replace('C'," Conceded")
quarter[['period','variable1']]=quarter['variable'].str.split(' ', expand=True)


period_bar=px.bar(quarter.loc[quarter.Team=='OLY'],x='Season',y='value',color="variable1", barmode='group',facet_col='period',
             height=1000,width=2000, text_auto=True,color_discrete_sequence= ['darkorange','black'],labels={'value':'Avg. Period Points per game','variable1':'','period':'Period'},title='Olympiacos')
period_bar.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
period_bar.update_layout(plot_bgcolor='white',font_size=18)
st.write(period_bar)

period_bar=px.bar(quarter.loc[quarter.Team=='PAN'],x='Season',y='value',color="variable1", barmode='group',facet_col='period',
             height=1000,width=2000, text_auto=True,color_discrete_sequence= ['darkorange','black'],labels={'value':'Avg. Period Points per game','variable1':'','period':'Quarter'},title='Panathinaikos')
period_bar.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
period_bar.update_layout(plot_bgcolor='white',font_size=18)
st.write(period_bar)

shot=gamestatsPAN[['Team','Season','F2M','F2A', '2P(%)','F3M', 'F3A','3P(%)', 'FTM', 'FTA','FT(%)']].melt(id_vars=['Team','Season'])
shot['variable']=shot['variable'].str.replace('F2','2P')
shot['variable']=shot['variable'].str.replace('F3','3P')
shot['variable']=shot['variable'].str.replace('M',' Made')
shot['variable']=shot['variable'].str.replace('A',' Attempt')
shot['variable']=shot['variable'].str.replace('(%)',' Percentage(%)')
shot[['Shot','Type']]=shot['variable'].str.split(' ', expand=True)

shot_bar=px.bar(shot.loc[shot.Team=='OLY'],x='Season',y='value',color="Type", barmode='group',facet_col='Shot',
             height=1000,width=2000, text_auto=True,color_discrete_sequence= ['darkorange','black','goldenrod'],
                labels={'value':'Avg. per game','variable1':'','Type':''},title='Olympiacos')
shot_bar.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
shot_bar.update_layout(plot_bgcolor='white',font_size=18)
st.write(shot_bar)

shot_bar=px.bar(shot.loc[shot.Team=='PAN'],x='Season',y='value',color="Type", barmode='group',facet_col='Shot',
             height=1000,width=2000, text_auto=True,color_discrete_sequence= ['darkorange','black','goldenrod'],
                labels={'value':'Avg. per game','variable1':'','Type':''},title='Panathinaikos')
shot_bar.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
shot_bar.update_layout(plot_bgcolor='white',font_size=18)
st.write(shot_bar)

opp_shot=gamestatsPAN[['Team','Season','opp F2M','opp F2A', 'opp 2P(%)','opp F3M', 'opp F3A','opp 3P(%)', 'opp FTM', 'opp FTA','opp FT(%)']].melt(id_vars=['Team','Season'])
opp_shot['variable']=opp_shot['variable'].str.replace('F2','2P')
opp_shot['variable']=opp_shot['variable'].str.replace('F3','3P')
opp_shot['variable']=opp_shot['variable'].str.replace('M',' Made')
opp_shot['variable']=opp_shot['variable'].str.replace('A',' Attempt')
opp_shot['variable']=opp_shot['variable'].str.replace('(%)',' Percentage(%)')
opp_shot['variable']=opp_shot['variable'].str.replace('opp ','')
opp_shot[['Shot','Type']]=opp_shot['variable'].str.split(' ', expand=True)

opp_shot_bar=px.bar(opp_shot.loc[opp_shot.Team=='OLY'],x='Season',y='value',color="Type", barmode='group',facet_col='Shot',
             height=1000,width=2000, text_auto=True,color_discrete_sequence= ['darkorange','black','goldenrod'],
                    labels={'value':'Avg. per game','variable1':'','Type':''},title='Olympiacos')
opp_shot_bar.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
opp_shot_bar.update_layout(plot_bgcolor='white',font_size=18)
st.write(opp_shot_bar)

opp_shot_bar=px.bar(opp_shot.loc[opp_shot.Team=='PAN'],x='Season',y='value',color="Type", barmode='group',facet_col='Shot',
             height=1000,width=2000, text_auto=True,color_discrete_sequence= ['darkorange','black','goldenrod'],
                    labels={'value':'Avg. per game','variable1':'','Type':''},title='Panathinaikos')
opp_shot_bar.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
opp_shot_bar.update_layout(plot_bgcolor='white',font_size=18)
st.write(opp_shot_bar)

attack_stats=gamestatsPAN[['Team','Season','AS','TO','OR','opp DR','RF']].melt(id_vars=['Team','Season'])
gamestatsPAN[['Team','Season','AS-TO Ratio']]
attack_bar=px.bar(attack_stats.loc[attack_stats.Team=='OLY'],x='variable',y='value',color="Season", barmode='group',
             height=1000,width=2000, text_auto=True,color_discrete_sequence= ['darkorange','black'],labels={'value':'Avg. per game','variable':'','period':'Quarter'},
                  title='Olympiacos')
attack_bar.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
attack_bar.update_layout(plot_bgcolor='white',font_size=18)
st.write(attack_bar)


attack_bar=px.bar(attack_stats.loc[attack_stats.Team=='PAN'],x='variable',y='value',color="Season", barmode='group',
             height=1000,width=2000, text_auto=True,color_discrete_sequence= ['darkorange','black'],labels={'value':'Avg. per game','variable':'','period':'Quarter'},
                title='Panathinaikos')
attack_bar.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
attack_bar.update_layout(plot_bgcolor='white',font_size=18)
st.write(attack_bar)

defence_stats=gamestatsPAN[['Team','Season','opp AS','opp TO','opp OR','DR','PF']].melt(id_vars=['Team','Season'])

defence_bar=px.bar(defence_stats.loc[defence_stats.Team=='OLY'],x='variable',y='value',color="Season", barmode='group',
             height=1000,width=2000, text_auto=True,color_discrete_sequence= ['darkorange','black'],labels={'value':'Avg. per game','variable':'','period':'Quarter'},title='Olympiacos')
defence_bar.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
defence_bar.update_layout(plot_bgcolor='white',font_size=18)
st.write(defence_bar)

defence_bar=px.bar(defence_stats.loc[defence_stats.Team=='PAN'],x='variable',y='value',color="Season", barmode='group',
             height=1000,width=2000, text_auto=True,color_discrete_sequence= ['darkorange','black'],labels={'value':'Avg. per game','variable':'','period':'Quarter'},title='Panathinaikos')
defence_bar.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
defence_bar.update_layout(plot_bgcolor='white',font_size=18)
st.write(defence_bar)

dorat=gamestatsPAN[['Team','Season','Offensive Rating','Defensive Rating']]
dorat['Net Rating']=dorat['Offensive Rating'] - dorat['Defensive Rating']
dorat=dorat.melt(id_vars=['Team','Season'])

dorat_bar=px.bar(dorat.loc[dorat.Team=='PAN'],x='variable',y='value',color="Season", barmode='group',
             height=1000,width=2000, text_auto=True,color_discrete_sequence= ['darkorange','black'],labels={'value':'Avg. per game','variable':'','period':'Quarter'},title='Panathinaikos')
dorat_bar.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
dorat_bar.update_layout(plot_bgcolor='white',font_size=18)
st.write(dorat_bar)

dorat_bar=px.bar(dorat.loc[dorat.Team=='OLY'],x='variable',y='value',color="Season", barmode='group',
             height=1000,width=2000, text_auto=True,color_discrete_sequence= ['darkorange','black'],labels={'value':'Avg. per game','variable':'','period':'Quarter'},title='Olympiacos')
dorat_bar.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
dorat_bar.update_layout(plot_bgcolor='white',font_size=18)
st.write(dorat_bar)
