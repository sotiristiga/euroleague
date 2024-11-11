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
dataset2223=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2223.csv")
dataset2324=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2324.csv")
dataset2425=pd.read_csv(f"https://raw.githubusercontent.com/sotiristiga/Football_Analysis/refs/heads/main/superleague2425.csv")
dataset=pd.concat([dataset2324,dataset2425,dataset2223])

ivan=pd.concat([dataset2223,dataset2324.loc[dataset2324.Fixture<16]])
fatih=dataset2324.loc[(dataset2324.Fixture>15) & (dataset2324.Fixture<36)]
alonso=dataset2425.loc[dataset2425.Fixture<10]
vitoria=dataset2425.loc[dataset2425.Fixture<9]

def computeteamstats(dataset):
    computeTeamstats_on_games = dataset.groupby(["idseason", 'Team'])[[
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
    computeTeamstats_on_games["Dribble(%)"] = (
                100 * computeTeamstats_on_games["Dribble attempts succ"] / computeTeamstats_on_games[
            "Dribble attempts"]).round(1)
    computeTeamstats_on_games["Dribble(%)"] = computeTeamstats_on_games["Dribble(%)"].fillna(0)
    computeTeamstats_on_games["Passes(%)"] = (
                100 * computeTeamstats_on_games["Accurate passes"] / computeTeamstats_on_games["Total passes"]).round(1)
    computeTeamstats_on_games["Passes(%)"] = computeTeamstats_on_games["Passes(%)"].fillna(0)
    computeTeamstats_on_games["Crosses(%)"] = (
                100 * computeTeamstats_on_games["Accurate Crosses"] / computeTeamstats_on_games["Total Crosses"]).round(
        1)
    computeTeamstats_on_games["Crosses(%)"] = computeTeamstats_on_games["Crosses(%)"].fillna(0)
    computeTeamstats_on_games["Long balls(%)"] = (
                100 * computeTeamstats_on_games["Accurate Long balls"] / computeTeamstats_on_games[
            "Total Long balls"]).round(1)
    computeTeamstats_on_games["Long balls(%)"] = computeTeamstats_on_games["Long balls(%)"].fillna(0)
    computeTeamstats_on_games["Duels(%)"] = (
                100 * computeTeamstats_on_games["Duels won"] / computeTeamstats_on_games["Duels"]).round(1)
    computeTeamstats_on_games["Duels(%)"] = computeTeamstats_on_games["Duels(%)"].fillna(0)
    computeTeamstats_on_games["Aerial duels(%)"] = (
                100 * computeTeamstats_on_games["Aerial duels won"] / computeTeamstats_on_games["Aerial duels"]).round(
        1)
    computeTeamstats_on_games["Aerial duels(%)"] = computeTeamstats_on_games["Aerial duels(%)"].fillna(0)
    computeTeamstats_on_games["Ground duels(%)"] = (
                100 * computeTeamstats_on_games["Ground duels won"] / computeTeamstats_on_games["Ground duels"]).round(
        1)
    computeTeamstats_on_games["Ground duels(%)"] = computeTeamstats_on_games["Ground duels(%)"].fillna(0)
    computeTeamstats_on_games["Runs out(%)"] = (
                100 * computeTeamstats_on_games["Runs out succ"] / computeTeamstats_on_games["Runs out"]).round(1)
    computeTeamstats_on_games["Runs out(%)"] = computeTeamstats_on_games["Runs out(%)"].fillna(0)

    computeAgainststats_on_games = dataset.groupby(['idseason', 'Against'])[[
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
    computeAgainststats_on_games["Dribble(%)"] = (
                100 * computeAgainststats_on_games["Dribble attempts succ"] / computeAgainststats_on_games[
            "Dribble attempts"]).round(1)
    computeAgainststats_on_games["Dribble(%)"] = computeAgainststats_on_games["Dribble(%)"].fillna(0)
    computeAgainststats_on_games["Passes(%)"] = (
                100 * computeAgainststats_on_games["Accurate passes"] / computeAgainststats_on_games[
            "Total passes"]).round(1)
    computeAgainststats_on_games["Passes(%)"] = computeAgainststats_on_games["Passes(%)"].fillna(0)
    computeAgainststats_on_games["Crosses(%)"] = (
                100 * computeAgainststats_on_games["Accurate Crosses"] / computeAgainststats_on_games[
            "Total Crosses"]).round(1)
    computeAgainststats_on_games["Crosses(%)"] = computeAgainststats_on_games["Crosses(%)"].fillna(0)
    computeAgainststats_on_games["Long balls(%)"] = (
                100 * computeAgainststats_on_games["Accurate Long balls"] / computeAgainststats_on_games[
            "Total Long balls"]).round(1)
    computeAgainststats_on_games["Long balls(%)"] = computeAgainststats_on_games["Long balls(%)"].fillna(0)
    computeAgainststats_on_games["Duels(%)"] = (
                100 * computeAgainststats_on_games["Duels won"] / computeAgainststats_on_games["Duels"]).round(1)
    computeAgainststats_on_games["Duels(%)"] = computeAgainststats_on_games["Duels(%)"].fillna(0)
    computeAgainststats_on_games["Aerial duels(%)"] = (
                100 * computeAgainststats_on_games["Aerial duels won"] / computeAgainststats_on_games[
            "Aerial duels"]).round(1)
    computeAgainststats_on_games["Aerial duels(%)"] = computeAgainststats_on_games["Aerial duels(%)"].fillna(0)
    computeAgainststats_on_games["Ground duels(%)"] = (
                100 * computeAgainststats_on_games["Ground duels won"] / computeAgainststats_on_games[
            "Ground duels"]).round(1)
    computeAgainststats_on_games["Ground duels(%)"] = computeAgainststats_on_games["Ground duels(%)"].fillna(0)
    computeAgainststats_on_games["Runs out(%)"] = (
                100 * computeAgainststats_on_games["Runs out succ"] / computeAgainststats_on_games["Runs out"]).round(1)
    computeAgainststats_on_games["Runs out(%)"] = computeAgainststats_on_games["Runs out(%)"].fillna(0)

    computeAgainststats_on_games = computeAgainststats_on_games.add_prefix('opp ').rename(
        columns={'opp Against': 'Team', 'opp idseason': 'idseason'})

    computeteamstats_on_games_total = pd.merge(computeTeamstats_on_games, computeAgainststats_on_games,
                                               on=['Team', 'idseason'])

    computeteamstats_on_games_mean = computeteamstats_on_games_total.groupby('Team')[
        ['Goals', 'Assists', 'Yellow card', 'Red card', 'Shots on target',
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
         'Saves from inside box', 'Penalties saved',
         'opp Goals', 'opp Assists', 'opp Yellow card', 'opp Red card', 'opp Shots on target',
         'opp Shots off target', 'opp Shots blocked',
         'opp Dribble attempts',
         'opp Dribble attempts succ', 'opp Penalty won',
         'opp Big chances missed',
         'opp Penalty miss', 'opp Hit woodwork',
         'opp Defensive actions', 'opp Clearances',
         'opp Blocked shots', 'opp Interceptions',
         'opp Total tackles', 'opp Dribbled past',
         'opp Penalty committed', 'opp Own goals',
         'opp Last man tackle',
         'opp Error led to shot',
         'opp Clearance off line',
         'opp Error led to goal',
         'opp Touches', 'opp Accurate passes',
         'opp Total passes',
         'opp Key passes', 'opp Total Crosses',
         'opp Accurate Crosses', 'opp Total Long balls',
         'opp Accurate Long balls',
         'opp Big chances created', 'opp Duels',
         'opp Duels won',
         'opp Ground duels', 'opp Ground duels won',
         'opp Aerial duels', 'opp Aerial duels won',
         'opp Possession lost', 'opp Fouls',
         'opp Was fouled', 'opp Offsides', 'opp Saves',
         'opp Punches', 'opp Runs out', 'opp Runs out succ',
         'opp High claims',
         'opp Saves from inside box',
         'opp Penalties saved']].mean().reset_index().round(1)

    computeteamstats_on_games_mean["Dribble(%)"] = (
                100 * computeteamstats_on_games_mean["Dribble attempts succ"] / computeteamstats_on_games_mean[
            "Dribble attempts"]).round(1)
    computeteamstats_on_games_mean["Dribble(%)"] = computeteamstats_on_games_mean["Dribble(%)"].fillna(0)
    computeteamstats_on_games_mean["Passes(%)"] = (
                100 * computeteamstats_on_games_mean["Accurate passes"] / computeteamstats_on_games_mean[
            "Total passes"]).round(1)
    computeteamstats_on_games_mean["Passes(%)"] = computeteamstats_on_games_mean["Passes(%)"].fillna(0)
    computeteamstats_on_games_mean["Crosses(%)"] = (
                100 * computeteamstats_on_games_mean["Accurate Crosses"] / computeteamstats_on_games_mean[
            "Total Crosses"]).round(1)
    computeteamstats_on_games_mean["Crosses(%)"] = computeteamstats_on_games_mean["Crosses(%)"].fillna(0)
    computeteamstats_on_games_mean["Long balls(%)"] = (
                100 * computeteamstats_on_games_mean["Accurate Long balls"] / computeteamstats_on_games_mean[
            "Total Long balls"]).round(1)
    computeteamstats_on_games_mean["Long balls(%)"] = computeteamstats_on_games_mean["Long balls(%)"].fillna(0)
    computeteamstats_on_games_mean["Duels(%)"] = (
                100 * computeteamstats_on_games_mean["Duels won"] / computeteamstats_on_games_mean["Duels"]).round(1)
    computeteamstats_on_games_mean["Duels(%)"] = computeteamstats_on_games_mean["Duels(%)"].fillna(0)
    computeteamstats_on_games_mean["Aerial duels(%)"] = (
                100 * computeteamstats_on_games_mean["Aerial duels won"] / computeteamstats_on_games_mean[
            "Aerial duels"]).round(1)
    computeteamstats_on_games_mean["Aerial duels(%)"] = computeteamstats_on_games_mean["Aerial duels(%)"].fillna(0)
    computeteamstats_on_games_mean["Ground duels(%)"] = (
                100 * computeteamstats_on_games_mean["Ground duels won"] / computeteamstats_on_games_mean[
            "Ground duels"]).round(1)
    computeteamstats_on_games_mean["Ground duels(%)"] = computeteamstats_on_games_mean["Ground duels(%)"].fillna(0)
    computeteamstats_on_games_mean["Runs out(%)"] = (
                100 * computeteamstats_on_games_mean["Runs out succ"] / computeteamstats_on_games_mean[
            "Runs out"]).round(1)
    computeteamstats_on_games_mean["Runs out(%)"] = computeteamstats_on_games_mean["Runs out(%)"].fillna(0)

    computeteamstats_on_games_mean["opp Dribble(%)"] = (
                100 * computeteamstats_on_games_mean["opp Dribble attempts succ"] / computeteamstats_on_games_mean[
            "opp Dribble attempts"]).round(1)
    computeteamstats_on_games_mean["opp Dribble(%)"] = computeteamstats_on_games_mean["opp Dribble(%)"].fillna(0)
    computeteamstats_on_games_mean["opp Passes(%)"] = (
                100 * computeteamstats_on_games_mean["opp Accurate passes"] / computeteamstats_on_games_mean[
            "opp Total passes"]).round(1)
    computeteamstats_on_games_mean["opp Passes(%)"] = computeteamstats_on_games_mean["opp Passes(%)"].fillna(0)
    computeteamstats_on_games_mean["opp Crosses(%)"] = (
                100 * computeteamstats_on_games_mean["opp Accurate Crosses"] / computeteamstats_on_games_mean[
            "opp Total Crosses"]).round(1)
    computeteamstats_on_games_mean["opp Crosses(%)"] = computeteamstats_on_games_mean["opp Crosses(%)"].fillna(0)
    computeteamstats_on_games_mean["opp Long balls(%)"] = (
                100 * computeteamstats_on_games_mean["opp Accurate Long balls"] / computeteamstats_on_games_mean[
            "opp Total Long balls"]).round(1)
    computeteamstats_on_games_mean["opp Long balls(%)"] = computeteamstats_on_games_mean["opp Long balls(%)"].fillna(0)
    computeteamstats_on_games_mean["opp Duels(%)"] = (
                100 * computeteamstats_on_games_mean["opp Duels won"] / computeteamstats_on_games_mean[
            "opp Duels"]).round(1)
    computeteamstats_on_games_mean["opp Duels(%)"] = computeteamstats_on_games_mean["opp Duels(%)"].fillna(0)
    computeteamstats_on_games_mean["opp Ground duels(%)"] = (
                100 * computeteamstats_on_games_mean["opp Ground duels won"] / computeteamstats_on_games_mean[
            "opp Ground duels"]).round(1)
    computeteamstats_on_games_mean["opp Ground duels(%)"] = computeteamstats_on_games_mean[
        "opp Ground duels(%)"].fillna(0)
    computeteamstats_on_games_mean["opp Aerial duels(%)"] = (
                100 * computeteamstats_on_games_mean["opp Aerial duels won"] / computeteamstats_on_games_mean[
            "opp Aerial duels"]).round(1)
    computeteamstats_on_games_mean["opp Aerial duels(%)"] = computeteamstats_on_games_mean[
        "opp Aerial duels(%)"].fillna(0)
    computeteamstats_on_games_mean["opp Runs out(%)"] = (
                100 * computeteamstats_on_games_mean["opp Runs out succ"] / computeteamstats_on_games_mean[
            "opp Runs out"]).round(1)
    computeteamstats_on_games_mean["opp Runs out(%)"] = computeteamstats_on_games_mean["opp Runs out(%)"].fillna(0)

    computeteamstats_on_games_mean = computeteamstats_on_games_mean.loc[
        computeteamstats_on_games_mean.Team == "Panathinaikos"]

    return computeteamstats_on_games_mean

ivan_stats=computeteamstats(ivan)
fatih_stats=computeteamstats(fatih)
alonso_stats=computeteamstats(alonso)
vitoria_stats=computeteamstats(vitoria)

st.write(ivan_stats)
