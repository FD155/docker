# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 15:02:37 2022

@author: fdoronzo
"""

import pandas as pd
import streamlit as st
import plotly_express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


st.title("“Atelier Docker M2 SISE")
st.subheader("Exploration des données des résultats des étudiants de deux écoles portugaises")
file_path = st.file_uploader("chargement du fichiers")

@st.cache(persist=True)
 
def upload(file):
    dataframe = pd.read_csv(file, sep = ';')
    return dataframe


def histchart(data):
    result = data.groupby(['guardian','schoolsup']).size().reset_index(name='counts')
    fig = px.bar(result,x = "guardian",y="counts",height = 400,color='schoolsup')
    return fig

def piechart(df):       
    resultM = df.groupby(['reason']).size().reset_index(name='counts')
    resultF = df.groupby(['age']).size().reset_index(name='counts')   
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=resultM.reason, values=resultM.counts, name="Raison"),
                  1, 1)
    fig.add_trace(go.Pie(labels=resultF.age, values=resultF.counts, name="Raison"),
                  1, 2)  
    
    fig.update_layout(
        title_text=("Plus d'information sur l'étudiant"))
    return fig


def boxplot(df):       
    categories_count = ['G1', 'G2', 'G3']
    chosen_count = st.selectbox(
       'Quel trimestre ?', categories_count)
    fig = px.box(df, x='studytime', y=chosen_count, color='schoolsup', notched=True)
    return fig


if file_path is not None:
    data = upload(file_path)
    genre = st.sidebar.radio(
             "Genre",
            ('Tout', 'Homme', 'Femme'))
    if genre == 'Femme':
        data = data.loc[data['sex']=='F',:]
    elif genre == 'Homme':
        data = data.loc[data['sex']=='M',:]  
    
    sorti = st.sidebar.radio(
             "Temps passé avec les amis",
            ('Aucun', 'Très peu', 'Peu','Moyennement','Souvent','Très souvent'))
    if sorti == 'Très peu':
        data = data.loc[data['goout']==1,:]
    elif sorti == 'Peu':
        data = data.loc[data['goout']==2,:]
    elif sorti == 'Moyennement':
        data = data.loc[data['goout']==3,:]
    elif sorti == 'Souvent':
        data = data.loc[data['goout']==4,:]
    elif sorti == 'Très souvent':
        data = data.loc[data['goout']==5,:]

    st.write(data)
    hist = histchart(data)
    st.write(hist)
    pie = piechart(data)
    st.write(pie)
    boxplot = boxplot(data)
    st.plotly_chart(boxplot)
#toto loco    
