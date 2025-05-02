import plotly.express as px
import numpy as np
import pandas as pd

def create_map(df):
    """"
    This is a function that will generate and synthesize the actual map we are using
    Specifically, we will be making use of the plotly objects.

    This function intakes our all_data df
    """

    # Adding a state codes dictionary for mapping
    state_codes = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 
        'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
        'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 
        'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
        'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 
        'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
        'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 
        'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 
        'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
        'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC'
    }
    
    #Add state codes to the dataframe, map will change the "State" column of the original df to "state_code"
    df_map = df.copy()
    df_map["state_code"] = df_map["State"].map(state_codes)

    
    # Create diverging color scale (red for negative, green for positive)
    max_abs_value = max(abs(df_map["Total Balance"].min()), abs(df_map["Total Balance"].max()))

    # Ensure there's a good range for the color scale
    if max_abs_value < 50:
        max_abs_value = 50  # Set a minimum range of -50 to 50 million

    
    fig = px.choropleth(
        df_map,
        locations='state_code',
        locationmode='USA-states',
        color="Total Balance",
        color_continuous_scale=[
            (0, 'darkred'),
            (0.5, 'white'),
            (1, 'darkgreen')
        ],
        range_color=[-max_abs_value, max_abs_value],
        scope='usa',
        labels={
            "Canada Exports": "Canada Exports(million $)",  
            "Canada Imports": "Canada Imports(million $)",
            "Mexico Exports": "Mexico Exports (million $)",
            "Mexico Imports": "Mexico Imports (million $)",  
            "Total Balance": "Trade Balance (million $)"
                },

        #These are the information that will appear 
        hover_data={
            "state_code": False,
            'State': True, 
            'Canada Exports': True, 
            'Canada Imports': True, 
            'Mexico Exports': True, 
            'Mexico Imports': True, 
            "Total Balance": True
        }
    )
    
    fig.update_layout(
        title="US States' Absolute Trade Balance with Canada and Mexico under selected tariff rates. Hover over each state for granular data.",
        geo=dict(
            showlakes=True,
            lakecolor='rgb(255, 255, 255)',
        ),
        coloraxis_colorbar=dict(
            title='Trade Balance (million $)',
            tickprefix='$',
            tickformat=',.0f'
        )
    )
    
    return fig