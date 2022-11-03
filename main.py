# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 19:03:11 2022

@author: Mitchell Gaming PC
"""

import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import altair as alt

col1, col2, col3 = st.columns(3)

with col1:
    st.write(' ')

with col2:
    st.header('County-level Health Data for NC')
    url = 'https://nciom.org/nc-health-data/map/'
    st.write(f'Data obtained from: {url}')

with col3:
    st.write(' ')
    

col1, col2 = st.columns(2)

df = pd.read_excel('County Health Data 2021.xlsx')

melted = pd.melt(df, ['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2','Unnamed: 3','Unnamed: 4', 'Data year', 'Data Notes'])

melted = melted.rename({'Unnamed: 0':'feature', 'Unnamed: 1': 'feature_longer', 'Unnamed: 2':'source', 'Unnamed: 3':'link','Unnamed: 4':'etc',
                       'Data year':'data_year', 'Data Notes':'data_notes', 'variable':'county'}, axis = 1)

data_options = ['Life expectancy', 'Food Insecurity', 'Unemployment']

with col2:
    selected_attr = st.selectbox(label = 'Select an attribute to view:', options = data_options)
    
    county_options = melted['county'].unique()
    
    selected_county = st.selectbox(label = 'Select a county to highlight:', options = county_options)
    
    
    selected_data = melted[melted['feature'] == selected_attr]
    
    plot1 = alt.Chart(selected_data).mark_bar().encode(
        alt.X("value:Q", bin=True),
        y='count()',
    ).properties(title = 'Distribution of {}'.format(selected_attr.lower()),
                 width = 850,
                 height = 425)
    
    
    st.altair_chart(plot1)



    
with col1:
    colors = ['red' if x == 'Alamance' else 'blue' for x in selected_data.sort_values(by = 'value', ascending = False).county]

    def apply_color(county):
        if county == selected_county:
            return 'Selected County'
        else:
            return 'All Others'

    selected_data['color'] = selected_data['county'].map(apply_color)


    plot2 = alt.Chart(selected_data.sort_values(by = 'value', ascending = False)).mark_bar().encode(
        alt.Y("county", sort='-x', axis=alt.Axis(labels = False)),
        alt.X("value:Q"),
    color = alt.Color('color', legend=alt.Legend(
            legendX=0, legendY=-500,
            direction='vertical'))).properties(
        width=850,
        height=600
    )
                
    st.altair_chart(plot2)