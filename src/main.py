#Importing packages
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

#Importing functions from the other pilots
from data_loader import load_data, calculate_balance, impact_calculator, load_detailed_data
from maps import create_map, create_pie_chart

             ####
###     ABOVE THE MAP    ####
             ####


#Setting the streamlit page configuration
st.set_page_config(layout="wide", page_title="North American Trade Visualization")

#Creating Title
st.title("An Interactive Visualization of 2024 North American Trade for U.S. States")

#Header for a subtitle
st.subheader("Created by Alex Vertikov as a Final Project for the Spring 2025 Iteration of ECON 1500 at Brown University, taught by Professor Fernando Duarte. Please see the README.md file in (https://github.com/alexvertikov/NA-Trade-Visualization) for more details on the motivation and implementation of this project.")



             ####
###           MAP    ####
             ####

#Creating a container for the map (so that we can edit out of order on the page.)
#All of the map creation is now in the container located below the tariff slider
map_container = st.container()


             ####
###     BELOW THE MAP (TARIFF SLIDER)    ####
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



        ####
#### AFTER TARRIFF SLIDER ####
        ####

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
            Michigan has by far the greatest absolute balance of trade, with a whopping whopping 79.6 billion dollar deficit and massive
            deficits for both Canada and Mexico individually. We see the state with the highest trade surplus is
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


                    ####  
        #### STATE RANKING SECTION #####
                    ####


# Create a section for ranking tables
st.subheader("State Trade Balance Rankings")

# Get data for the current state of trade (0% tariff)
data = get_processed_data(0)

# Create columns for side-by-side tables
col1, col2 = st.columns(2)
with col1:
    # Using markdown with ### makes it smaller than the subheader above
    st.markdown("##### Top 3 States with Trade Surplus")
    
    # Create a custom DataFrame for top 3 states
    surplus_data = pd.DataFrame({
        "State": ["Oregon", "New Hampshire", "Nebraska"],
        "Trade Balance": ["$4.88B", "$2.95B", "$2.78B"],
        "Key Industries/Motivators": [
            "Semiconductor and electronics manufacturing exports",
            "Computer and electronic equipment exports",
            "Agricultural exports, especially corn and soybeans"
        ]
    })
    
    # Display the table without index
    st.table(surplus_data.set_index('State'))
    
with col2:
    # Using markdown with ### makes it smaller than the subheader above
    st.markdown("##### Top 3 States with Trade Deficit")
    
    # Create a custom DataFrame for bottom 3 states
    deficit_data = pd.DataFrame({
        "State": ["Michigan", "Illinois", "Texas"],
        "Trade Balance": ["-$79.65B", "-$50.32B", "-$36.11B"],
        "Key Industries/Motivators": [
            "Automotive imports from Mexico and Canada",
            "Machinery and transportation equipment imports",
            "Despite energy exports, large imports of manufactured goods"
        ]
    })
    
    # Display the table without index
    st.table(deficit_data.set_index('State'))






                    ####  
        #### MICHIGAN CASE STUDY #####
                    ####



st.subheader("A Case Study: Michigan")

st.markdown("""
            As we see in the takeaways section, Michigan stands out for having an exceptionally high trade deficit with Mexico and Canada.
            From the map, Michigan's deep red is a clear outlier, and since Michigan has also struggled with many of the social issues that have motivated this project,
            it is worth examining in particular detail. 

            Michigan, especially in its urban centers, has seen great social harms from deindustrialization, with unemployment, urban decay,
            crime, municipal poverty, and high opioid use raising political attention in recent years.
            """

)

#Creating a new set of columns
col3, col4, = st.columns(2)

with col3:
    #Inserting an image of an abandoned automobile plant (width of 500 pixels)
    st.image("https://upload.wikimedia.org/wikipedia/commons/f/f7/Packard_Plant_Ruins.jpg",
         caption = "The ruins of the Packard Automative Plant in Detroit, MI (Photo by Csmcm, CC-BY-SA 3.0 from Wikimedia Commons).", 
         width = 500)

with col4:
    #Basic population statisics for Michigan cities
    st.markdown("""
    #### Major Michigan Cities Population Decline
    - Detroit: 1,850,000 (1950) → 639,000 (2020) = 66% decline
    - Flint: 196,000 (peak) → 81,000 (2020) = 59% decline
    - Saginaw: 98,000 (peak) → 44,000 (2020) = 55% decline
    """)

#Title for the pie charts
st.markdown("""
    #### Pie Charts Showing Good-Specific Breakdowns of Michigan's Imports/Exports with Canada and Mexico
"""
     
)
  ###
  #### PIE CHARTS ####
  ###


# Create 2x2 grid for the charts
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# Load Michigan detailed trade data
mexico_imports_df = load_detailed_data("MI-DetailedMexicoImports - MI-DetailedMexicoImports.csv")
mexico_exports_df = load_detailed_data("MI-DetailedMexicanExports - MI-DetailedMexicanExports.csv")
canada_imports_df = load_detailed_data("MI-DetailedCanadaImports - MI-DetailedCanadaImports.csv")
canada_exports_df = load_detailed_data("MI-CanadaDetailedExports - MI-CanadaDetailedExports.csv")
    
with row1_col1:
        # Michigan imports from Mexico
        fig1 = create_pie_chart(
            mexico_imports_df,
            "Breakdown of Michigan Imports from Mexico"
        )
        st.plotly_chart(fig1, use_container_width=True)
    
with row1_col2:
        # Michigan exports to Mexico
        fig2 = create_pie_chart(
            mexico_exports_df,
            "Breakdown of Michigan Exports to Mexico"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
with row2_col1:
        # Michigan imports from Canada
        fig3 = create_pie_chart(
            canada_imports_df,
            "Breakdown of Michigan Imports from Canada"
        )
        st.plotly_chart(fig3, use_container_width=True)
    
with row2_col2:
        # Michigan exports to Canada
        fig4 = create_pie_chart(
            canada_exports_df,
            "Breakdown of Michigan Exports to Canada"
        )
        st.plotly_chart(fig4, use_container_width=True)



st.markdown("""
            From analyzing this granular data, we see that huge imports for the automotive industries
            are the primary driver of Michigan's large trade deficits. Even as Michigan enjoys a particularly 
            close trade relationship with Canada due to their immediate proximity, we see that automative trade 
            forms an overwhelming part of Michigan's international trade, especially with imports from Mexico and 
            exports to Canada.  The data clearly shows how Michigan's trade is overwhelmingly concentrated in the 
            automotive sector with both trading partners, and yet there imports significantly outweigh
            exports. Within this context, the post-NAFTA supply chain integration is especially noticable,
            yet it seems that Michigan has not achieved any desired economic diversification or production
            leading to increased North American imports.
            """
)