#Importing packages
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

#Importing functions from the other pilots
from data_loader import load_data, calculate_balance, impact_calculator
from maps import create_map

             ####
###     ABOVE THE MAP    ####
             ####


#Setting the streamlit page configuration
st.set_page_config(layout="wide", page_title="North American Trade Visualization")

#Creating Title
st.title("An Interactive Visualization of 2024 North American Trade for U.S. States")

#Header for a subtitle
st.subheader("Created by Alex Vertikov as a Final Project for the Spring 2025 Iteration of ECON 1500 at Brown University, taught by Professor Fernando Duarte. Please see the README for more details on the motivation and implementation of this project.")



             ####
###           MAP    ####
             ####

#Creating a container for the map (so that we can edit out of order on the page.)
#All of the map creation is now in the container located below the tariff slider
map_container = st.container()


             ####
###     BELOW THE MAP    ####
             ####

#Subheader for the tarriff rate slider
st.subheader("Tarriff Rate Slider (Simple Model)")

#Creating the streamlit slider
tariff_rate = st.slider(
    "Select a hypothetical tariff rate for North American trade:",
    min_value=0,
    max_value=50,
    value=0,  # Default value
    step=5,
    help="Adjust to see projected effects of different tariff rates on absolute state trade balances"
)

#Adding explanation text in markdown
st.markdown("""
The tarriff rate slider assumes that tarriffs on Mexico and Canada are equal and will be equally reciprocated. For information
on the model used to calculate the proposed changes in trade, please see README.md. The map will update for the
proposed trade balances for each state under your selected rate.
            """)




#### AFTER TARRIFF SLIDER ####

#Loading and processing data
@st.cache_data

def get_processed_data(tariff_rate):
    """"
    A function to process the data and give us our final dataframe
    """
    #Extracting the all_data dataframe
    df = load_data()

    #We need to call calculate_balance on all_data
    df = calculate_balance(df)

    #If the tariff rate is non-zero, we apply it too
    if tariff_rate > 0:
        df = impact_calculator(df, tariff_rate)

    return df

#The final dataframe
trade_data = get_processed_data(tariff_rate)

#Printing the final dataframe for error checking
print(trade_data)

#Copying the dataframe
ranking_data = trade_data.copy()

#Ranking the columns by total deficits
ranking_data = ranking_data.sort_values(by="Total Balance", ascending=False)

print(ranking_data)


#We open the map_container so that we can write the code in the map portion of the file
with map_container:
    #Creating and displaying the map
    fig = create_map(trade_data)

    st.plotly_chart(fig, use_container_width=True)


#Creating a header for takeaways
st.subheader("Takeaways")

st.markdown("""
            At the status quo, we see that there are very few states with significant trade surpluses with Mexico and Canada.
            We also see that there are very many (especially the largest ones) with significant deficits. 
            Michigan has by far the greatest absolute balance of trade, with a whopping whopping 79.6 billion dollar deficit  
            and massive deficits for both Canada and Mexico individually. We see the state with the highest trade surplus is
            Oregon, and they only have a surplus of 4.88 billion dollars.

            Even under this extremely simple model, we see that increased tariffs would result in greatly increasing 
            US States' balance of trade with the US. Under a 20% North American tarriff rate, Michigan would have a projected
            trade deficit of 54.77 billion dollars, significantly decreased from the 0% rate. We also see that under the
            20% tariff rate, Texas has a projected trade surplus of 23.37 billion dollars. This is a marked increase that
            demonstrates the strong impact of higher North American tariffs on individual states' trade surpluses with
            Mexico and Canada.


            The greater effects of these trade choices on other economic indicators (GDP, unemployment, etc)
            are not projected in this model or visualization, and cannot be deduced from solely looking 
            at the balance of trade for each state. Those factors must also be considered in implementing trade
            policy, which goes beyond the purpose of this model.

            """)


#Potentially create another map with a new slider for a more complex model.



