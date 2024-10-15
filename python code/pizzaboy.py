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
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n, sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)
from itables.streamlit import interactive_table
from itables import to_html_datatable
from streamlit.components.v1 import html
from plotly.subplots import make_subplots
from mplsoccer import PyPizza, add_image, FontManager
import streamlit as st
import openpyxl
goalkeepers=pd.read_excel('C:/Users/surve/OneDrive/Desktop/Tiganitas work/EUROLEAGUE/stats/Christos/Goalkeepers.xlsx')
centerbacks=pd.read_excel('C:/Users/surve/OneDrive/Desktop/Tiganitas work/EUROLEAGUE/stats/Christos/Center backs.xlsx')
fullwingbacks=pd.read_excel('C:/Users/surve/OneDrive/Desktop/Tiganitas work/EUROLEAGUE/stats/Christos/Full - wing backs.xlsx')
wingers=pd.read_excel('C:/Users/surve/OneDrive/Desktop/Tiganitas work/EUROLEAGUE/stats/Christos/wingers.xlsx')
cmdm=pd.read_excel('C:/Users/surve/OneDrive/Desktop/Tiganitas work/EUROLEAGUE/stats/Christos/Al CMs in Greek Super League.xlsx')
no10=pd.read_excel('C:/Users/surve/OneDrive/Desktop/Tiganitas work/EUROLEAGUE/stats/Christos/No 10.xlsx')
strikers=pd.read_excel('C:/Users/surve/OneDrive/Desktop/Tiganitas work/EUROLEAGUE/stats/Christos/Strikers.xlsx')
def player_rating_stat_higher(dataset, stat):
    dataset1 = dataset[["Player", stat]].sort_values(stat,ascending=True).reset_index()
    dataset1.drop("index", axis=1, inplace=True)
    final_dataset = dataset1.reset_index() >> mutate(Rating=(100 * (X.index + 1) / X.Player.nunique()),
                                                     Rating1=(X.Rating.round(0)))
    final_dataset.drop(stat, axis=1, inplace=True)
    final_dataset.rename(columns={'Rating1': stat}, inplace=True)
    final_dataset.drop(["index", "Rating"], axis=1, inplace=True)
    return final_dataset
def player_rating_stat_lower(dataset,stat):
    dataset1=dataset[["Player",stat]].sort_values(stat,ascending=False).reset_index()
    dataset1.drop("index",axis=1,inplace=True)
    final_dataset=dataset1.reset_index() >> mutate(Rating=(100*(X.index+1)/X.Player.nunique()),Rating1=(X.Rating.round(0)))
    final_dataset.drop(stat, axis=1, inplace=True)
    final_dataset.rename(columns={'Rating1': stat},inplace=True)
    final_dataset.drop(["index","Rating"],axis=1,inplace=True)
    return final_dataset
def goalkeepers_pizza(dataset,Select_Player,League):
    team = dataset.loc[dataset.Player == Select_Player]['Team'].unique()[0]
    nation=dataset.loc[dataset.Player==Select_Player]['Birth country'].unique()[0]
    age = dataset.loc[dataset.Player == Select_Player]['Age'].unique()[0]
    sel_dataset=dataset[["Player","xG against per 90",	"Passes per 90","Conceded goals per 90",	"Accurate passes, %","Clean sheets","Progressive passes per 90",
                        "Save rate, %",	"Accurate progressive passes, %",
                        "Prevented goals per 90",	"Lateral passes per 90",
                        "Exits per 90",	"Accurate lateral passes, %",
                        "Aerial duels per 90",	"Long passes per 90","Accurate long passes, %"]]
    colplus=["Accurate passes, %","Clean sheets","Progressive passes per 90",
                        "Save rate, %",	"Accurate progressive passes, %",
                        "Prevented goals per 90","Lateral passes per 90","Exits per 90","Accurate lateral passes, %",
                        "Aerial duels per 90",	"Long passes per 90","Accurate long passes, %"]
    colminus=["Conceded goals per 90"]
    playerratingsplus=player_rating_stat_higher(sel_dataset, "Passes per 90")
    for i in colplus:
        dfplus = player_rating_stat_higher(sel_dataset, i)
        playerratingsplus = pd.merge(playerratingsplus, dfplus)

    playerratingsminus = player_rating_stat_lower(sel_dataset, "xG against per 90")
    for i in colminus:
        dfminus = player_rating_stat_lower(sel_dataset, i)
        playerratingsminus = pd.merge(playerratingsminus, dfminus)

    player_ratings=pd.merge(playerratingsplus,playerratingsminus)
    player_ratings_select=player_ratings.loc[player_ratings.Player==Select_Player]
    goalkeeping=(player_ratings_select[["xG against per 90","Conceded goals per 90","Clean sheets", "Save rate, %","Prevented goals per 90","Exits per 90","Aerial duels per 90"]]
                 .rename(columns={"xG against per 90":"xGoals\nagainst",
                                        "Conceded goals per 90":"Conceded\ngoals",
                                        "Clean sheets":"Clean\nsheets",
                                        "Save rate, %":"Save\nrate(%)",
                                        "Prevented goals per 90":"Prevented\ngoals",
                                        "Exits per 90":"Exits",
                                        "Aerial duels per 90":"Aerial\nduels"}).melt())

    goalkeeping['Category']="Goalkeeping"
    positioning=(player_ratings_select[["Passes per 90","Accurate passes, %","Progressive passes per 90","Accurate progressive passes, %",
                                        "Lateral passes per 90",
                                        "Accurate lateral passes, %",
                                        "Long passes per 90",
                                        "Accurate long passes, %"]]
                 .rename(columns={"Passes per 90":"Passes",
                                        "Accurate passes, %":"Accurate\npasses(%)",
                                        "Progressive passes per 90":"Progressive\npasses",
                                        "Accurate progressive passes, %":"Acc.\nprogressive\npasses(%)",
                                        "Lateral passes per 90":"Lateral\npasses",
                                        "Accurate lateral passes, %":"Acc.\nlateral\npasses(%)",
                                        "Long passes per 90":"Long\npasses",
                                        "Accurate long passes, %":"Acc.\nlong\npasses(%)"}).melt())
    positioning['Category'] = "Positioning"

    all_together=pd.concat([goalkeeping,positioning])
    count_skills = all_together['Category'].value_counts().reset_index()
    goalkeeping_skills_count = count_skills.loc[count_skills.Category == 'Goalkeeping']['count'].sum()
    positioning_skills_count = count_skills.loc[count_skills.Category == 'Positioning']['count'].sum()
    slice_colors = ["#FF9300"] * goalkeeping_skills_count + ["#00B050"] * positioning_skills_count
    text_colors = ["#F2F2F2"] * (goalkeeping_skills_count + positioning_skills_count)
    baker = PyPizza(
        params=all_together.variable.to_numpy(),
        background_color="#262626",
        straight_line_color="#EBEBE9",
        straight_line_lw=1,
        last_circle_lw=0,
        other_circle_lw=0,
        inner_circle_size=20,
    )
    fig, ax = baker.make_pizza(
        all_together.value.to_numpy(),
        figsize=(7, 9),
        color_blank_space="same",
        slice_colors=slice_colors,
        value_colors=text_colors,
        value_bck_colors=slice_colors,
        blank_alpha=0.4,
        kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=1),
        kwargs_params=dict(
            color="#F2F2F2", fontsize=11, va="center"
        ),
        kwargs_values=dict(
            color="#000000",
            fontsize=11,

            zorder=3,
            bbox=dict(
                edgecolor="#000000",
                facecolor="cornflowerblue",
                boxstyle="round,pad=0.3",
                lw=1,
            ),
        ),
    )
    fig.text(
        0.515,
        0.975,
        Select_Player,
        size=16,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.515,
        0.95,
       "Team: " + team + " | Nationality: " + nation + " | Age: " + age.astype(str),
        size=14,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.515,
        0.91,
        "Percentile Rank vs "+League+" Goalkeepers | Season 2024-25 | Per 90' Stats",
        size=13,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.34,
        0.86,
        "Goalkeeping        Possession",
        size=14,

        color="#F2F2F2",
    )
    fig.patches.extend(
        [
            plt.Rectangle(
                (0.30, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#FF9300",
                transform=fig.transFigure,
                figure=fig,
            ),
            plt.Rectangle(
                (0.54, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#00B050",
                transform=fig.transFigure,
                figure=fig,
            )
        ]
    )
    figure=fig

    return figure
def centerbacks_pizza(dataset,Select_Player,League):
    team = dataset.loc[dataset.Player == Select_Player]['Team'].unique()[0]
    nation = dataset.loc[dataset.Player == Select_Player]['Birth country'].unique()[0]
    age = dataset.loc[dataset.Player == Select_Player]['Age'].unique()[0]
    sel_dataset=dataset[["Player","Goals per 90",
                                 "xG per 90",
                                 "Assists per 90",
                                 "xA per 90",
                                 "Successful attacking actions per 90",
                                 "Successful defensive actions per 90",
                                 "Defensive duels per 90",
                                 "Defensive duels won, %",
                                 "Aerial duels per 90",
                                 "Aerial duels won, %",
                                 "PAdj Interceptions",
                                 "Shots blocked per 90",
                                 "Passes per 90",
                                 "Accurate passes, %",
                                 "Progressive passes per 90",
                                 "Accurate progressive passes, %",
                                 "Dribbles per 90",
                                 "Successful dribbles, %",
                                 "Progressive runs per 90",
                                 "Long passes per 90",
                                 "Accurate long passes, %"]]
    colplus=[
            "xG per 90",
            "Assists per 90",
            "xA per 90",
            "Successful attacking actions per 90",
             "Successful defensive actions per 90",
             "Defensive duels per 90",
             "Defensive duels won, %",
             "Aerial duels per 90",
             "Aerial duels won, %",
             "PAdj Interceptions",
             "Shots blocked per 90",
             "Passes per 90",
             "Accurate passes, %",
             "Progressive passes per 90",
             "Accurate progressive passes, %",
             "Dribbles per 90",
             "Successful dribbles, %",
             "Progressive runs per 90",
             "Long passes per 90",
             "Accurate long passes, %"]

    playerratingsplus=player_rating_stat_higher(sel_dataset, "Goals per 90")
    for i in colplus:
        dfplus = player_rating_stat_higher(sel_dataset, i)
        playerratingsplus = pd.merge(playerratingsplus, dfplus)

    player_ratings=playerratingsplus
    player_ratings_select=player_ratings.loc[player_ratings.Player==Select_Player]
    attacking=(player_ratings_select[["Goals per 90",
                                        "xG per 90",
                                        "Assists per 90",
                                        "xA per 90",
                                        "Successful attacking actions per 90",
                                        ]]
                 .rename(columns={"Goals per 90":"Goals",
                                        "xG per 90":"xGoals",
                                        "Assists per 90":"Assists",
                                        "xA per 90":"xAssists",
                                  "Successful attacking actions per 90":"Succ.\natt.\nactions",}).melt())

    attacking['Category']="Attacking"
    positioning=(player_ratings_select[["Passes per 90","Accurate passes, %","Progressive passes per 90","Accurate progressive passes, %",
                                        "Dribbles per 90",
                                        "Successful dribbles, %",
                                        "Progressive runs per 90",
                                        "Long passes per 90",
                                        "Accurate long passes, %"]]
                 .rename(columns={"Passes per 90":"Passes",
                                        "Accurate passes, %":"Accurate\npasses(%)",
                                        "Progressive passes per 90":"Progressive\npasses",
                                        "Accurate progressive passes, %":"Acc.\nprogressive\npasses(%)",
                                         "Dribbles per 90": "Dribbles",
                                        "Successful dribbles, %":"Succ.\ndribbles(%)",
                                        "Progressive runs per 90":"Progressive\nruns",
                                        "Long passes per 90":"Long\npasses",
                                        "Accurate long passes, %":"Acc.\nlong\npasses(%)"}).melt())
    positioning['Category'] = "Positioning"

    defending = (player_ratings_select[["Successful defensive actions per 90",
            "Defensive duels per 90",
            "Defensive duels won, %",
            "Aerial duels per 90",
            "Aerial duels won, %",
            "PAdj Interceptions",
            "Shots blocked per 90"]].rename(columns={"Successful defensive actions per 90":"Succ.\ndef.\nactions",
                                                    "Defensive duels per 90":"Def.\nduels",
                                                    "Defensive duels won, %":"Def.\nduels\nwon(%)",
                                                    "Aerial duels per 90":"Aerial\nduels",
                                                    "Aerial duels won, %":"Aerial\nduels\nwon(%)",
                                                    "PAdj Interceptions":"PAdj\nInterceptions",
                                                    "Shots blocked per 90":"Shots\nblocked"}).melt())

    defending['Category'] = "Defending"

    all_together=pd.concat([attacking,positioning,defending])
    count_skills = all_together['Category'].value_counts().reset_index()
    attacking_skills_count = count_skills.loc[count_skills.Category == 'Attacking']['count'].sum()
    positioning_skills_count = count_skills.loc[count_skills.Category == 'Positioning']['count'].sum()
    defending_skills_count = count_skills.loc[count_skills.Category == 'Defending']['count'].sum()
    slice_colors = ["#D70232"] * attacking_skills_count + ["#00B050"] * positioning_skills_count+ ["#1A78CF"] * defending_skills_count
    text_colors = ["#F2F2F2"] * (attacking_skills_count + positioning_skills_count+defending_skills_count)
    baker = PyPizza(
        params=all_together.variable.to_numpy(),
        background_color="#262626",
        straight_line_color="#EBEBE9",
        straight_line_lw=1,
        last_circle_lw=0,
        other_circle_lw=0,
        inner_circle_size=20,
    )
    fig, ax = baker.make_pizza(
        all_together.value.to_numpy(),
        figsize=(7, 9),
        color_blank_space="same",
        slice_colors=slice_colors,
        value_colors=text_colors,
        value_bck_colors=slice_colors,
        blank_alpha=0.4,
        kwargs_slices=dict(edgecolor="#F2F2F2", zorder=3, linewidth=1),
        kwargs_params=dict(
            color="#F2F2F2", fontsize=11, va="center",
        ),
        kwargs_values=dict(
            color="#000000",

            fontsize=10,
            rotation=4,
            rotation_mode='anchor',
           zorder=3,
            bbox=dict(
                edgecolor="#000000",
                facecolor="cornflowerblue",
                boxstyle="round,pad=0.2",
                lw=1
            ),
        ),
    )
    fig.text(
        0.515,
        0.975,
        Select_Player,
        size=16,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.515,
        0.95,
        "Team: " + team + " | Nationality: " + nation + " | Age: " + age.astype(str),
        size=14,
        ha="center",

        color="#F2F2F2")
    fig.text(
        0.515,
        0.91,
        "Percentile Rank vs "+League+" Center Backs | Season 2024-25 | Per 90'",
        size=13,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.24,
        0.86,
        "Attacking          Possession          Defending",
        size=14,

        color="#F2F2F2",
    )
    fig.patches.extend(
        [
            plt.Rectangle(
                (0.205, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#D70232",
                transform=fig.transFigure,
                figure=fig,
            ),
            plt.Rectangle(
                (0.42, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#00B050",
                transform=fig.transFigure,
                figure=fig,
            ),
            plt.Rectangle(
                (0.66, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#1A78CF",
                transform=fig.transFigure,
                figure=fig,
            )
        ]
    )
    figure=fig

    return figure
def fullwingbacks_pizza(dataset,Select_Player,League):
    team = dataset.loc[dataset.Player == Select_Player]['Team'].unique()[0]
    nation = dataset.loc[dataset.Player == Select_Player]['Birth country'].unique()[0]
    age = dataset.loc[dataset.Player == Select_Player]['Age'].unique()[0]
    sel_dataset=dataset[["Player","Goals per 90",
                                 "xG per 90",
                                 "Assists per 90",
                                 "xA per 90",
                                 "Successful attacking actions per 90",
                                "Touches in box per 90",
                                 "Successful defensive actions per 90",
                                 "Defensive duels per 90",
                                 "Defensive duels won, %",
                                 "Aerial duels per 90",
                                 "Aerial duels won, %",
                                 "PAdj Interceptions",
                                 "Shots blocked per 90",
                                 "Progressive passes per 90",
                                "Accurate progressive passes, %",
                                "Dribbles per 90",
                                "Successful dribbles, %",
                                "Progressive runs per 90",
                                "Crosses per 90",
                                "Accurate crosses, %"]]
    colplus=[
            "xG per 90",
            "Assists per 90",
            "xA per 90",
            "Successful attacking actions per 90",
            "Touches in box per 90",
             "Successful defensive actions per 90",
             "Defensive duels per 90",
             "Defensive duels won, %",
             "Aerial duels per 90",
             "Aerial duels won, %",
             "PAdj Interceptions",
             "Shots blocked per 90",
             "Progressive passes per 90",
            "Accurate progressive passes, %",
            "Dribbles per 90",
            "Successful dribbles, %",
            "Progressive runs per 90",
            "Crosses per 90",
            "Accurate crosses, %"]

    playerratingsplus=player_rating_stat_higher(sel_dataset, "Goals per 90")
    for i in colplus:
        dfplus = player_rating_stat_higher(sel_dataset, i)
        playerratingsplus = pd.merge(playerratingsplus, dfplus)

    player_ratings=playerratingsplus
    player_ratings_select=player_ratings.loc[player_ratings.Player==Select_Player]
    attacking=(player_ratings_select[["Goals per 90",
                                        "xG per 90",
                                        "Assists per 90",
                                        "xA per 90",
                                        "Successful attacking actions per 90",
                                      "Touches in box per 90",
                                        ]]
                 .rename(columns={"Goals per 90":"Goals",
                                        "xG per 90":"xGoals",
                                        "Assists per 90":"Assists",
                                        "xA per 90":"xAssists",
                                  "Touches in box per 90": "Touches\nin\nbox",
                                  "Successful attacking actions per 90":"Succ.\natt.\nactions",}).melt())

    attacking['Category']="Attacking"
    positioning=(player_ratings_select[["Progressive passes per 90","Accurate progressive passes, %",
                                        "Dribbles per 90",
                                        "Successful dribbles, %",
                                        "Progressive runs per 90",
                                        "Crosses per 90",
                                        "Accurate crosses, %"]]
                 .rename(columns={"Progressive passes per 90":"Progressive\npasses","Accurate progressive passes, %":"Acc.\nprogressive\npasses(%)",
                                         "Dribbles per 90": "Dribbles",
                                        "Successful dribbles, %":"Succ.\ndribbles(%)",
                                        "Progressive runs per 90":"Progressive\nruns",
                                        "Crosses per 90":"Crosses",
                                        "Accurate crosses, %":"Acc.\ncrosses(%)"}).melt())
    positioning['Category'] = "Positioning"

    defending = (player_ratings_select[["Successful defensive actions per 90",
            "Defensive duels per 90",
            "Defensive duels won, %",
            "Aerial duels per 90",
            "Aerial duels won, %",
            "PAdj Interceptions",
            "Shots blocked per 90"]].rename(columns={"Successful defensive actions per 90":"Succ.\ndef.\nactions",
                                                    "Defensive duels per 90":"Def.\nduels",
                                                    "Defensive duels won, %":"Def.\nduels\nwon(%)",
                                                    "Aerial duels per 90":"Aerial\nduels",
                                                    "Aerial duels won, %":"Aerial\nduel\nwon(%)",
                                                    "PAdj Interceptions":"PAdj\nInterceptions",
                                                    "Shots blocked per 90":"Shots\nblocked"}).melt())

    defending['Category'] = "Defending"

    all_together=pd.concat([attacking,positioning,defending])
    count_skills = all_together['Category'].value_counts().reset_index()
    attacking_skills_count = count_skills.loc[count_skills.Category == 'Attacking']['count'].sum()
    positioning_skills_count = count_skills.loc[count_skills.Category == 'Positioning']['count'].sum()
    defending_skills_count = count_skills.loc[count_skills.Category == 'Defending']['count'].sum()
    slice_colors = ["#D70232"] * attacking_skills_count + ["#00B050"] * positioning_skills_count+ ["#1A78CF"] * defending_skills_count
    text_colors = ["#F2F2F2"] * (attacking_skills_count + positioning_skills_count+defending_skills_count)
    baker = PyPizza(
        params=all_together.variable.to_numpy(),
        background_color="#262626",
        straight_line_color="#EBEBE9",
        straight_line_lw=1,
        last_circle_lw=0,
        other_circle_lw=0,
        inner_circle_size=15,
    )
    fig, ax = baker.make_pizza(
        all_together.value.to_numpy(),
        figsize=(7, 9),
        color_blank_space="same",
        slice_colors=slice_colors,
        value_colors=text_colors,
        value_bck_colors=slice_colors,
        blank_alpha=0.4,
        kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=1),
        kwargs_params=dict(
            color="#F2F2F2", fontsize=11, va="center_baseline",
        ),
        kwargs_values=dict(
            color="#000000",


            fontsize=10,
           zorder=3,
            bbox=dict(
                edgecolor="#000000",
                facecolor="cornflowerblue",
                boxstyle="round,pad=0.2",
                lw=1
            ),
        ),
    )

    fig.text(
        0.515,
        0.975,
        Select_Player,
        size=16,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.515,
        0.95,
        "Team: " + team + " | Nationality: " + nation + " | Age: " + age.astype(str),
        size=14,
        ha="center",

        color="#F2F2F2")
    fig.text(
        0.515,
        0.91,
        "Percentile Rank vs "+League+" Full/wing backs | Season 2024-25 | Per 90'",
        size=13,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.24,
        0.86,
        "Attacking          Possession          Defending",
        size=14,

        color="#F2F2F2",
    )
    fig.patches.extend(
        [
            plt.Rectangle(
                (0.205, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#D70232",
                transform=fig.transFigure,
                figure=fig,
            ),
            plt.Rectangle(
                (0.42, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#00B050",
                transform=fig.transFigure,
                figure=fig,
            ),
            plt.Rectangle(
                (0.66, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#1A78CF",
                transform=fig.transFigure,
                figure=fig,
            )
        ]
    )
    figure=fig

    return figure
def midlfiders_pizza(dataset, Select_Player, League):
    team = dataset.loc[dataset.Player == Select_Player]['Team'].unique()[0]
    nation = dataset.loc[dataset.Player == Select_Player]['Birth country'].unique()[0]
    age = dataset.loc[dataset.Player == Select_Player]['Age'].unique()[0]
    sel_dataset = dataset[["Player", "Goals per 90",
                           "xG per 90",
                           "Assists per 90",
                           "xA per 90",
                           "Successful attacking actions per 90",
                           "Touches in box per 90",
                           "Successful defensive actions per 90",
                           "Defensive duels per 90",
                           "Defensive duels won, %",
                           "Aerial duels per 90",
                           "Aerial duels won, %",
                           "PAdj Interceptions",
                           "Shots blocked per 90",
                           "Progressive passes per 90",
                           "Accurate progressive passes, %",
                           "Dribbles per 90",
                           "Successful dribbles, %",
                           "Progressive runs per 90",
                           "Passes per 90",
                           "Accurate passes, %"]]
    colplus = [
        "xG per 90",
        "Assists per 90",
        "xA per 90",
        "Successful attacking actions per 90",
        "Touches in box per 90",
        "Successful defensive actions per 90",
        "Defensive duels per 90",
        "Defensive duels won, %",
        "Aerial duels per 90",
        "Aerial duels won, %",
        "PAdj Interceptions",
        "Shots blocked per 90",
        "Progressive passes per 90",
        "Accurate progressive passes, %",
        "Dribbles per 90",
        "Successful dribbles, %",
        "Progressive runs per 90",
        "Passes per 90",
        "Accurate passes, %"]

    playerratingsplus = player_rating_stat_higher(sel_dataset, "Goals per 90")
    for i in colplus:
        dfplus = player_rating_stat_higher(sel_dataset, i)
        playerratingsplus = pd.merge(playerratingsplus, dfplus)

    player_ratings = playerratingsplus
    player_ratings_select = player_ratings.loc[player_ratings.Player == Select_Player]
    attacking = (player_ratings_select[["Goals per 90",
                                        "xG per 90",
                                        "Assists per 90",
                                        "xA per 90",
                                        "Successful attacking actions per 90",
                                        "Touches in box per 90",
                                        ]]
                 .rename(columns={"Goals per 90": "Goals",
                                  "xG per 90": "xGoals",
                                  "Assists per 90": "Assists",
                                  "xA per 90": "xAssists",
                                  "Touches in box per 90": "Touches\nin\nbox",
                                  "Successful attacking actions per 90": "Succ.\natt.\nactions", }).melt())

    attacking['Category'] = "Attacking"
    positioning = (player_ratings_select[["Progressive passes per 90", "Accurate progressive passes, %",
                                          "Dribbles per 90",
                                          "Successful dribbles, %",
                                          "Progressive runs per 90",
                                          "Passes per 90",
                                            "Accurate passes, %"]]
                   .rename(columns={"Progressive passes per 90": "Progressive\npasses",
                                    "Accurate progressive passes, %": "Acc.\nprogressive\npasses(%)",
                                    "Dribbles per 90": "Dribbles",
                                    "Successful dribbles, %": "Succ.\ndribbles(%)",
                                    "Progressive runs per 90": "Progressive\nruns",
                                    "Passes per 90": "Passes",
                                    "Accurate passes, %": "Acc.\npasses(%)"}).melt())
    positioning['Category'] = "Positioning"

    defending = (player_ratings_select[["Successful defensive actions per 90",
                                        "Defensive duels per 90",
                                        "Defensive duels won, %",
                                        "Aerial duels per 90",
                                        "Aerial duels won, %",
                                        "PAdj Interceptions",
                                        "Shots blocked per 90"]].rename(
        columns={"Successful defensive actions per 90": "Succ.\ndef.\nactions",
                 "Defensive duels per 90": "Def.\nduels",
                 "Defensive duels won, %": "Def.\nduels\nwon(%)",
                 "Aerial duels per 90": "Aerial\nduels",
                 "Aerial duels won, %": "Aerial\nduel\nwon(%)",
                 "PAdj Interceptions": "PAdj\nInterceptions",
                 "Shots blocked per 90": "Shots\nblocked"}).melt())

    defending['Category'] = "Defending"

    all_together = pd.concat([attacking, positioning, defending])
    count_skills = all_together['Category'].value_counts().reset_index()
    attacking_skills_count = count_skills.loc[count_skills.Category == 'Attacking']['count'].sum()
    positioning_skills_count = count_skills.loc[count_skills.Category == 'Positioning']['count'].sum()
    defending_skills_count = count_skills.loc[count_skills.Category == 'Defending']['count'].sum()
    slice_colors = ["#D70232"] * attacking_skills_count + ["#00B050"] * positioning_skills_count + [
        "#1A78CF"] * defending_skills_count
    text_colors = ["#F2F2F2"] * (attacking_skills_count + positioning_skills_count + defending_skills_count)
    baker = PyPizza(
        params=all_together.variable.to_numpy(),
        background_color="#262626",
        straight_line_color="#EBEBE9",
        straight_line_lw=1,
        last_circle_lw=0,
        other_circle_lw=0,
        inner_circle_size=15,
    )
    fig, ax = baker.make_pizza(
        all_together.value.to_numpy(),
        figsize=(7, 9),
        color_blank_space="same",
        slice_colors=slice_colors,
        value_colors=text_colors,
        value_bck_colors=slice_colors,
        blank_alpha=0.4,
        kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=1),
        kwargs_params=dict(
            color="#F2F2F2", fontsize=11, va="center_baseline",
        ),
        kwargs_values=dict(
            color="#000000",

            fontsize=10,
            zorder=3,
            bbox=dict(
                edgecolor="#000000",
                facecolor="cornflowerblue",
                boxstyle="round,pad=0.2",
                lw=1
            ),
        ),
    )

    fig.text(
        0.515,
        0.975,
        Select_Player,
        size=16,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.515,
        0.95,
        "Team: " + team + " | Nationality: " + nation + " | Age: " + age.astype(str),
        size=14,
        ha="center",

        color="#F2F2F2")


    fig.text(
        0.515,
        0.91,
        "Percentile Rank vs " + League + " Midfielders | Season 2024-25 | Per 90'",
        size=13,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.24,
        0.86,
        "Attacking          Possession          Defending",
        size=14,

        color="#F2F2F2",
    )
    fig.patches.extend(
        [
            plt.Rectangle(
                (0.205, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#D70232",
                transform=fig.transFigure,
                figure=fig,
            ),
            plt.Rectangle(
                (0.42, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#00B050",
                transform=fig.transFigure,
                figure=fig,
            ),
            plt.Rectangle(
                (0.66, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#1A78CF",
                transform=fig.transFigure,
                figure=fig,
            )
        ]
    )
    figure = fig

    return figure
def no10_pizza(dataset, Select_Player, League):
    team = dataset.loc[dataset.Player == Select_Player]['Team'].unique()[0]
    nation = dataset.loc[dataset.Player == Select_Player]['Birth country'].unique()[0]
    age = dataset.loc[dataset.Player == Select_Player]['Age'].unique()[0]
    sel_dataset = dataset[["Player", "Goals per 90",
                           "xG per 90",
                           "Assists per 90",
                           "xA per 90",
                           "Successful attacking actions per 90",
                           "Touches in box per 90",
                           "Shots per 90",
                           "Shots on target, %",
                           "Successful defensive actions per 90",
                           "Defensive duels per 90",
                           "Defensive duels won, %",
                           "Aerial duels per 90",
                           "Aerial duels won, %",
                           "PAdj Interceptions",
                           "Deep completions per 90",
                            "Dribbles per 90",
                            "Successful dribbles, %",
                            "Progressive runs per 90",
                            "Smart passes per 90",
                            "Accurate smart passes, %",
                            "Key passes per 90"]]
    colplus = [
        "Goals per 90",
                           "xG per 90",
                           "Assists per 90",
                           "xA per 90",
                           "Successful attacking actions per 90",
                           "Touches in box per 90",
        "Shots per 90",
        "Shots on target, %",
                           "Successful defensive actions per 90",
                           "Defensive duels per 90",
                           "Defensive duels won, %",
                           "Aerial duels per 90",
                           "Aerial duels won, %",
                           "PAdj Interceptions",
                           "Deep completions per 90",
                            "Dribbles per 90",
                            "Successful dribbles, %",
                            "Progressive runs per 90",
                            "Smart passes per 90",
                            "Accurate smart passes, %",
                            "Key passes per 90"]

    playerratingsplus = player_rating_stat_higher(sel_dataset, "Goals per 90")
    for i in colplus:
        dfplus = player_rating_stat_higher(sel_dataset, i)
        playerratingsplus = pd.merge(playerratingsplus, dfplus)

    player_ratings = playerratingsplus
    player_ratings_select = player_ratings.loc[player_ratings.Player == Select_Player]
    attacking = (player_ratings_select[["Goals per 90",
                                        "xG per 90",
                                        "Assists per 90",
                                        "xA per 90",
                                        "Successful attacking actions per 90",
                                        "Touches in box per 90",
                                        "Shots per 90",
                                        "Shots on target, %"
                                        ]]
                 .rename(columns={"Goals per 90": "Goals",
                                  "xG per 90": "xGoals",
                                  "Assists per 90": "Assists",
                                  "xA per 90": "xAssists",
                                  "Touches in box per 90": "Touches\nin\nbox",
                                  "Successful attacking actions per 90": "Succ.\natt.\nactions",
                                  "Shots per 90":"Shots","Shots on target, %":"Shots\non\ntarget(%)"
                 }).melt())

    attacking['Category'] = "Attacking"
    positioning = (player_ratings_select[["Deep completions per 90",
                                        "Dribbles per 90",
                                        "Successful dribbles, %",
                                        "Progressive runs per 90",
                                        "Smart passes per 90",
                                        "Accurate smart passes, %",
                                        "Key passes per 90",
                                        ]]
                   .rename(columns={"Deep completions per 90": "Deep\ncompletions",
                                    "Dribbles per 90": "Dribbles",
                                    "Successful dribbles, %": "Succ.\ndribbles(%)",
                                    "Progressive runs per 90": "Progressive\nruns",
                                    "Smart passes per 90": "Smart\npasses",
                                    "Accurate smart passes, %": "Acc.\nsmart\npasses(%)",
                                    "Key passes per 90":"Key\npasses"}).melt())
    positioning['Category'] = "Positioning"

    defending = (player_ratings_select[["Successful defensive actions per 90",
                                        "Defensive duels per 90",
                                        "Defensive duels won, %",
                                        "Aerial duels per 90",
                                        "Aerial duels won, %",
                                        "PAdj Interceptions"]].rename(
        columns={"Successful defensive actions per 90": "Succ.\ndef.\nactions",
                 "Defensive duels per 90": "Def.\nduels",
                 "Defensive duels won, %": "Def.\nduels\nwon(%)",
                 "Aerial duels per 90": "Aerial\nduels",
                 "Aerial duels won, %": "Aerial\nduel\nwon(%)",
                 "PAdj Interceptions": "PAdj\nInterceptions",
                 }).melt())

    defending['Category'] = "Defending"

    all_together = pd.concat([attacking, positioning, defending])
    count_skills = all_together['Category'].value_counts().reset_index()
    attacking_skills_count = count_skills.loc[count_skills.Category == 'Attacking']['count'].sum()
    positioning_skills_count = count_skills.loc[count_skills.Category == 'Positioning']['count'].sum()
    defending_skills_count = count_skills.loc[count_skills.Category == 'Defending']['count'].sum()
    slice_colors = ["#D70232"] * attacking_skills_count + ["#00B050"] * positioning_skills_count + [
        "#1A78CF"] * defending_skills_count
    text_colors = ["#F2F2F2"] * (attacking_skills_count + positioning_skills_count + defending_skills_count)
    baker = PyPizza(
        params=all_together.variable.to_numpy(),
        background_color="#262626",
        straight_line_color="#EBEBE9",
        straight_line_lw=1,
        last_circle_lw=0,
        other_circle_lw=0,
        inner_circle_size=15,
    )
    fig, ax = baker.make_pizza(
        all_together.value.to_numpy(),
        figsize=(7, 9),
        color_blank_space="same",
        slice_colors=slice_colors,
        value_colors=text_colors,
        value_bck_colors=slice_colors,
        blank_alpha=0.4,
        kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=1),
        kwargs_params=dict(
            color="#F2F2F2", fontsize=11, va="center_baseline",
        ),
        kwargs_values=dict(
            color="#000000",

            fontsize=10,
            zorder=3,
            bbox=dict(
                edgecolor="#000000",
                facecolor="cornflowerblue",
                boxstyle="round,pad=0.2",
                lw=1
            ),
        ),
    )

    fig.text(
        0.515,
        0.975,
        Select_Player,
        size=16,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.515,
        0.95,
        "Team: " + team + " | Nationality: " + nation + " | Age: " + age.astype(str),
        size=14,
        ha="center",

        color="#F2F2F2")
    fig.text(
        0.515,
        0.92,
        "Percentile Rank vs " + League + " Attacking Midfielders (No. 10) | Season 2024-25 | Per 90'",
        size=13,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.24,
        0.86,
        "Attacking          Possession          Defending",
        size=14,

        color="#F2F2F2",
    )
    fig.patches.extend(
        [
            plt.Rectangle(
                (0.205, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#D70232",
                transform=fig.transFigure,
                figure=fig,
            ),
            plt.Rectangle(
                (0.42, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#00B050",
                transform=fig.transFigure,
                figure=fig,
            ),
            plt.Rectangle(
                (0.66, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#1A78CF",
                transform=fig.transFigure,
                figure=fig,
            )
        ]
    )
    figure = fig

    return figure
def wingers_pizza(dataset, Select_Player, League):
    team = dataset.loc[dataset.Player == Select_Player]['Team'].unique()[0]
    nation = dataset.loc[dataset.Player == Select_Player]['Birth country'].unique()[0]
    age = dataset.loc[dataset.Player == Select_Player]['Age'].unique()[0]
    sel_dataset = dataset[["Player", "Goals per 90",
                           "xG per 90",
                           "Assists per 90",
                           "xA per 90",
                           "Successful attacking actions per 90",
                           "Touches in box per 90",
                           "Shots per 90",
                           "Shots on target, %",
                           "Successful defensive actions per 90",
                           "Defensive duels per 90",
                           "Defensive duels won, %",
                           "Aerial duels per 90",
                           "Aerial duels won, %",
                           "PAdj Interceptions",
                           "Crosses per 90",
                            "Accurate crosses, %",
                            "Dribbles per 90",
                            "Successful dribbles, %",
                            "Progressive runs per 90",
                            "Smart passes per 90",
                            "Accurate smart passes, %",
                            "Key passes per 90"]]
    colplus = [
         "Goals per 90",
                           "xG per 90",
                           "Assists per 90",
                           "xA per 90",
                           "Successful attacking actions per 90",
                           "Touches in box per 90",
                           "Shots per 90",
                           "Shots on target, %",
                           "Successful defensive actions per 90",
                           "Defensive duels per 90",
                           "Defensive duels won, %",
                           "Aerial duels per 90",
                           "Aerial duels won, %",
                           "PAdj Interceptions",
                           "Crosses per 90",
                            "Accurate crosses, %",
                            "Dribbles per 90",
                            "Successful dribbles, %",
                            "Progressive runs per 90",
                            "Smart passes per 90",
                            "Accurate smart passes, %",
                            "Key passes per 90"]

    playerratingsplus = player_rating_stat_higher(sel_dataset, "Goals per 90")
    for i in colplus:
        dfplus = player_rating_stat_higher(sel_dataset, i)
        playerratingsplus = pd.merge(playerratingsplus, dfplus)

    player_ratings = playerratingsplus
    player_ratings_select = player_ratings.loc[player_ratings.Player == Select_Player]
    attacking = (player_ratings_select[["Goals per 90",
                                        "xG per 90",
                                        "Assists per 90",
                                        "xA per 90",
                                        "Successful attacking actions per 90",
                                        "Touches in box per 90",
                                        "Shots per 90",
                                        "Shots on target, %"
                                        ]]
                 .rename(columns={"Goals per 90": "Goals",
                                  "xG per 90": "xGoals",
                                  "Assists per 90": "Assists",
                                  "xA per 90": "xAssists",
                                  "Touches in box per 90": "Touches\nin\nbox",
                                  "Successful attacking actions per 90": "Succ.\natt.\nactions",
                                  "Shots per 90":"Shots","Shots on target, %":"Shots\non\ntarget(%)"
                 }).melt())

    attacking['Category'] = "Attacking"
    positioning = (player_ratings_select[["Crosses per 90",
                                        "Accurate crosses, %",
                                        "Dribbles per 90",
                                        "Successful dribbles, %",
                                        "Progressive runs per 90",
                                        "Smart passes per 90",
                                        "Accurate smart passes, %",
                                        "Key passes per 90",
                                        ]]
                   .rename(columns={"Crosses per 90": "Crosses",
                                    "Accurate crosses, %":"Accurate\ncrosses(%)",
                                    "Dribbles per 90": "Dribbles",
                                    "Successful dribbles, %": "Succ.\ndribbles(%)",
                                    "Progressive runs per 90": "Progressive\nruns",
                                    "Smart passes per 90": "Smart\npasses",
                                    "Accurate smart passes, %": "Acc.\nsmart\npasses(%)",
                                    "Key passes per 90":"Key\npasses"}).melt())
    positioning['Category'] = "Positioning"

    defending = (player_ratings_select[["Successful defensive actions per 90",
                                        "Defensive duels per 90",
                                        "Defensive duels won, %",
                                        "Aerial duels per 90",
                                        "Aerial duels won, %",
                                        "PAdj Interceptions"]].rename(
        columns={"Successful defensive actions per 90": "Succ.\ndef.\nactions",
                 "Defensive duels per 90": "Def.\nduels",
                 "Defensive duels won, %": "Def.\nduels\nwon(%)",
                 "Aerial duels per 90": "Aerial\nduels",
                 "Aerial duels won, %": "Aerial\nduel\nwon(%)",
                 "PAdj Interceptions": "PAdj\nInterceptions",
                 }).melt())

    defending['Category'] = "Defending"

    all_together = pd.concat([attacking, positioning, defending])
    count_skills = all_together['Category'].value_counts().reset_index()
    attacking_skills_count = count_skills.loc[count_skills.Category == 'Attacking']['count'].sum()
    positioning_skills_count = count_skills.loc[count_skills.Category == 'Positioning']['count'].sum()
    defending_skills_count = count_skills.loc[count_skills.Category == 'Defending']['count'].sum()
    slice_colors = ["#D70232"] * attacking_skills_count + ["#00B050"] * positioning_skills_count + [
        "#1A78CF"] * defending_skills_count
    text_colors = ["#F2F2F2"] * (attacking_skills_count + positioning_skills_count + defending_skills_count)
    baker = PyPizza(
        params=all_together.variable.to_numpy(),
        background_color="#262626",
        straight_line_color="#EBEBE9",
        straight_line_lw=1,
        last_circle_lw=0,
        other_circle_lw=0,
        inner_circle_size=15,
    )
    fig, ax = baker.make_pizza(
        all_together.value.to_numpy(),
        figsize=(7, 9),
        color_blank_space="same",
        slice_colors=slice_colors,
        value_colors=text_colors,
        value_bck_colors=slice_colors,
        blank_alpha=0.4,
        kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=1),
        kwargs_params=dict(
            color="#F2F2F2", fontsize=11, va="center_baseline",
        ),
        kwargs_values=dict(
            color="#000000",

            fontsize=10,
            zorder=3,
            bbox=dict(
                edgecolor="#000000",
                facecolor="cornflowerblue",
                boxstyle="round,pad=0.2",
                lw=1
            ),
        ),
    )

    fig.text(
        0.515,
        0.975,
        Select_Player,
        size=16,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.515,
        0.95,
        "Team: " + team + " | Nationality: " + nation + " | Age: " + age.astype(str),
        size=14,
        ha="center",

        color="#F2F2F2")
    fig.text(
        0.515,
        0.92,
        "Percentile Rank vs " + League + " Wingers | Season 2024-25 | Per 90'",
        size=13,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.24,
        0.86,
        "Attacking          Possession          Defending",
        size=14,

        color="#F2F2F2",
    )
    fig.patches.extend(
        [
            plt.Rectangle(
                (0.205, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#D70232",
                transform=fig.transFigure,
                figure=fig,
            ),
            plt.Rectangle(
                (0.42, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#00B050",
                transform=fig.transFigure,
                figure=fig,
            ),
            plt.Rectangle(
                (0.66, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#1A78CF",
                transform=fig.transFigure,
                figure=fig,
            )
        ]
    )
    figure = fig

    return figure
def strikers_pizza(dataset, Select_Player, League):
    team = dataset.loc[dataset.Player == Select_Player]['Team'].unique()[0]
    nation = dataset.loc[dataset.Player == Select_Player]['Birth country'].unique()[0]
    age = dataset.loc[dataset.Player == Select_Player]['Age'].unique()[0]
    sel_dataset = dataset[["Player", "Goals per 90",
                                    "xG per 90",
                                    "Assists per 90",
                                    "xA per 90",
                                    "Successful attacking actions per 90",
                                    "Touches in box per 90",
                                    "Shots per 90",
                                    "Goal conversion, %",
                           "Successful defensive actions per 90",
                           "Defensive duels per 90",
                           "Defensive duels won, %",
                           "Aerial duels per 90",
                           "Aerial duels won, %",
                           "PAdj Interceptions",
                           "Dribbles per 90",
                           "Successful dribbles, %",
                           "Progressive runs per 90",
                           "Smart passes per 90",
                           "Accurate smart passes, %",
                           "Passes per 90",
                           "Accurate passes, %",
                           "Deep completions per 90"
                           ]]
    colplus = ["xG per 90",
                                    "Assists per 90",
                                    "xA per 90",
                                    "Successful attacking actions per 90",
                                    "Touches in box per 90",
                                    "Shots per 90",
                                    "Goal conversion, %",
                           "Successful defensive actions per 90",
                           "Defensive duels per 90",
                           "Defensive duels won, %",
                           "Aerial duels per 90",
                           "Aerial duels won, %",
                           "PAdj Interceptions",
                           "Dribbles per 90",
                           "Successful dribbles, %",
                           "Progressive runs per 90",
                           "Smart passes per 90",
                           "Accurate smart passes, %",
                           "Passes per 90",
                           "Accurate passes, %",
                           "Deep completions per 90"]

    playerratingsplus = player_rating_stat_higher(sel_dataset, "Goals per 90")
    for i in colplus:
        dfplus = player_rating_stat_higher(sel_dataset, i)
        playerratingsplus = pd.merge(playerratingsplus, dfplus)

    player_ratings = playerratingsplus
    player_ratings_select = player_ratings.loc[player_ratings.Player == Select_Player]
    attacking = (player_ratings_select[["Goals per 90",
                                        "xG per 90",
                                        "Assists per 90",
                                        "xA per 90",
                                        "Successful attacking actions per 90",
                                        "Touches in box per 90",
                                        "Shots per 90",
                                        "Goal conversion, %"]]
                 .rename(columns={"Goals per 90": "Goals",
                                  "xG per 90": "xGoals",
                                  "Assists per 90": "Assists",
                                  "xA per 90": "xAssists",
                                  "Touches in box per 90": "Touches\nin\nbox",
                                  "Successful attacking actions per 90": "Succ.\natt.\nactions",
                                  "Shots per 90":"Shots","Goal conversion, %":"Goal\nconversion(%)"
                 }).melt())

    attacking['Category'] = "Attacking"
    positioning = (player_ratings_select[["Dribbles per 90",
                                        "Successful dribbles, %",
                                        "Progressive runs per 90",
                                        "Smart passes per 90",
                                        "Accurate smart passes, %",
                                        "Passes per 90",
                                        "Accurate passes, %",
                                        "Deep completions per 90"]]
                   .rename(columns={"Dribbles per 90": "Dribbles",
                                    "Successful dribbles, %": "Succ.\ndribbles(%)",
                                    "Progressive runs per 90": "Progressive\nruns",
                                    "Smart passes per 90": "Smart\npasses",
                                    "Accurate smart passes, %": "Acc.\nsmart\npasses(%)",
                                    "Passes per 90":"Passes",
                                    "Accurate passes, %":"Accurate\npasses(%)",
                           "Deep completions per 90":"Deep\ncompletions"
                   }).melt())
    positioning['Category'] = "Positioning"

    defending = (player_ratings_select[["Successful defensive actions per 90",
                                        "Defensive duels per 90",
                                        "Defensive duels won, %",
                                        "Aerial duels per 90",
                                        "Aerial duels won, %",
                                        "PAdj Interceptions"]].rename(
        columns={"Successful defensive actions per 90": "Succ.\ndef.\nactions",
                 "Defensive duels per 90": "Def.\nduels",
                 "Defensive duels won, %": "Def.\nduels\nwon(%)",
                 "Aerial duels per 90": "Aerial\nduels",
                 "Aerial duels won, %": "Aerial\nduel\nwon(%)",
                 "PAdj Interceptions": "PAdj\nInterceptions",
                 }).melt())

    defending['Category'] = "Defending"

    all_together = pd.concat([attacking, positioning, defending])
    count_skills = all_together['Category'].value_counts().reset_index()
    attacking_skills_count = count_skills.loc[count_skills.Category == 'Attacking']['count'].sum()
    positioning_skills_count = count_skills.loc[count_skills.Category == 'Positioning']['count'].sum()
    defending_skills_count = count_skills.loc[count_skills.Category == 'Defending']['count'].sum()
    slice_colors = ["#D70232"] * attacking_skills_count + ["#00B050"] * positioning_skills_count + [
        "#1A78CF"] * defending_skills_count
    text_colors = ["#F2F2F2"] * (attacking_skills_count + positioning_skills_count + defending_skills_count)
    baker = PyPizza(
        params=all_together.variable.to_numpy(),
        background_color="#262626",
        straight_line_color="#EBEBE9",
        straight_line_lw=1,
        last_circle_lw=0,
        other_circle_lw=0,
        inner_circle_size=15,
    )
    fig, ax = baker.make_pizza(
        all_together.value.to_numpy(),
        figsize=(7, 9),
        color_blank_space="same",
        slice_colors=slice_colors,
        value_colors=text_colors,
        value_bck_colors=slice_colors,
        blank_alpha=0.4,
        kwargs_slices=dict(edgecolor="#F2F2F2", zorder=2, linewidth=1),
        kwargs_params=dict(
            color="#F2F2F2", fontsize=11, va="center_baseline",
        ),
        kwargs_values=dict(
            color="#000000",

            fontsize=10,
            zorder=3,
            bbox=dict(
                edgecolor="#000000",
                facecolor="cornflowerblue",
                boxstyle="round,pad=0.2",
                lw=1
            ),
        ),
    )

    fig.text(
        0.515,
        0.975,
        Select_Player,
        size=16,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.515,
        0.95,
        "Team: " + team + " | Nationality: " + nation + " | Age: " + age.astype(str),
        size=14,
        ha="center",

        color="#F2F2F2")
    fig.text(
        0.515,
        0.91,
        "Percentile Rank vs " + League + " Strikers | Season 2024-25 | Per 90'",
        size=13,
        ha="center",

        color="#F2F2F2",
    )
    fig.text(
        0.24,
        0.86,
        "Attacking          Possession          Defending",
        size=14,

        color="#F2F2F2",
    )
    fig.patches.extend(
        [
            plt.Rectangle(
                (0.205, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#D70232",
                transform=fig.transFigure,
                figure=fig,
            ),
            plt.Rectangle(
                (0.42, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#00B050",
                transform=fig.transFigure,
                figure=fig,
            ),
            plt.Rectangle(
                (0.66, 0.86),
                0.025,
                0.021,
                fill=True,
                color="#1A78CF",
                transform=fig.transFigure,
                figure=fig,
            )
        ]
    )
    figure = fig

    return figure


centerbacks_pizza(centerbacks,"V. Lampropoulos",'Superleague')
goalkeepers_pizza(goalkeepers,"N. Christogeorgos",'Superleague')
fullwingbacks_pizza(fullwingbacks,"Borja González",'Superleague')
midlfiders_pizza(cmdm, "F. Bainović", 'Superleague')
no10_pizza(no10, "T. Fountas", 'Superleague')
wingers_pizza(wingers, "L. Shengelia", 'Superleague')
strikers_pizza(strikers, "A. Jung", 'Superleague')
