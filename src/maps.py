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
    
    return fig\
    


#In this same file, we will also create the figures for the Michigan trade pie charts

def create_pie_chart(df, title):
    """
    Creates a pie chart from Michigan's detailed import/export data from USTR
    (which now contains categories)
    """
    """
    Creates a pie chart from Michigan's detailed trade data
    
    Parameters:
    - df: DataFrame containing Michigan trade data
    - title: Title for the pie chart
    
    Returns:
    - fig: Plotly figure object
    """
    # Make a copy to avoid modifying the original
    df = df.copy()
    
    # Remove the "All Merchandise" total row
    df = df[df["Product"] != "0--All Merchandise"]
    
    # Extract the description from Product column
    df['Description'] = df['Product'].str.split('--').str[1].fillna(df['Product'])

    
    # Sort by value and get top 5 categories
    df = df.sort_values('2024', ascending=False)
    top5 = df.head(5)
    
    # Calculate "Other" category
    other_value = df.iloc[5:]['2024'].sum()
    
    # Calculate percentages
    total = df['2024'].sum()
    top5_pct = [(value / total * 100) for value in top5['2024']]
    other_pct = (other_value / total * 100)
    
    # Create labels and values for the pie chart
    labels = [f"{row[1]['Description']} ({value:.1f}%)" for row, value in zip(top5.iterrows(), top5_pct)]
    labels.append(f"Other ({other_pct:.1f}%)")
    
    values = list(top5['2024'])
    values.append(other_value)
    
    # Create the pie chart
    fig = px.pie(
        values=values,
        names=labels,
        title=title,
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    
    # Simplify text in the pie slices to just percentages
    fig.update_traces(
        textposition='inside',
        textinfo='percent',
        hoverinfo='label+percent+value',
        textfont_size=12
    )
    
    return fig
    