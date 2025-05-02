import pandas as pd
import numpy as np
import re



#Creating a function that will load the trade data
def load_data():
    """
    A function that loads trade data for individual US states'trade
    with Mexico and Canada. We want to return a dataframe (for use in pandas)
    """

    
    #Read each csv file into a pandas dataframe

    #Data taken from trade.gov (2024 Data)
    canada_exports = pd.read_csv("/Users/alexvertikov/Desktop/Personal-Projects/ECON_1500_Project/data/Cured-State-Canadian-Exports - State-Canadian-Exports.csv", encoding='cp1252')
    canada_imports = pd.read_csv("/Users/alexvertikov/Desktop/Personal-Projects/ECON_1500_Project/data/Cured-State-Canadian-Imports - State-Canadian-Imports.csv", encoding='cp1252')

    mexico_exports = pd.read_csv("/Users/alexvertikov/Desktop/Personal-Projects/ECON_1500_Project/data/Cured-State-Mexican-Exports - State-Mexican-Exports.csv", encoding='cp1252')
    mexico_imports = pd.read_csv("/Users/alexvertikov/Desktop/Personal-Projects/ECON_1500_Project/data/Cured-State-Mexican-Imports.csv", encoding='cp1252')

    #Filter to get just the rows for individual states (not UNITED STATES or Unallocated)
    #Filter for rows where Product is "0--All Merchandise" and exclude UNITED STATES and Unallocated

    #Remove the rows for US, Unallocated, Puerto Rico, DC, and USVI
    canada_exports = canada_exports[
        (canada_exports["State"] != "Puerto Rico") &
        (canada_exports["State"] != "District of Columbia") &
        (canada_exports["State"] != "Virgin Islands") &
        (canada_exports["State"] != "UNITED STATES") &
        (canada_exports["State"] != 'Unallocated')
    ]

    canada_imports = canada_imports[
        (canada_imports["State"] != "Puerto Rico") &
        (canada_imports["State"] != "District of Columbia") &
        (canada_imports["State"] != "Virgin Islands") &
        (canada_imports["State"] != "UNITED STATES") &
        (canada_imports["State"] != "Unallocated")
    ]
        
    mexico_exports = mexico_exports[
        (mexico_exports["State"] != "Puerto Rico") &
        (mexico_exports["State"] != "District of Columbia") &
        (mexico_exports["State"] != "Virgin Islands") &
        (mexico_exports["State"] != "UNITED STATES") &
        (mexico_exports["State"] != "Unallocated")
    ]
        
    mexico_imports = mexico_imports[
        (mexico_imports["State"] != "Puerto Rico") &
        (mexico_imports["State"] != "District of Columbia") &
        (mexico_imports["State"] != "Virgin Islands") &
        (mexico_imports["State"] != "UNITED STATES") &
        (mexico_imports["State"] != "Unallocated")
    ]

    
    #Now, create a dataframe with just the state names (taken randmoly from canada_exports)
    all_data = pd.DataFrame({"State": canada_exports["State"].copy()})
    
        
    #Function that converts raw data values (strings with dollar signs) into numbers
    def convert_to_number(value):
        """
        If it is a string, we use regex to return a float without any commas or dollar signs
        """
        #if value is a string, we return a float ()
        if isinstance(value, str):
                #Remove $ and commas using regex
            return float(re.sub(r'[,$]', '', value))
        return value
    
    
        
    #Adding the data for exports/imports from Canada and Mexico as new columns in the dataframe
    #NOTE: the values for the export/import quantities are strings that contain dollar signs, NOT numbers

    #Use merge to safely add all the data and make sure the rows are aligned by state name 
    #We will merge the two dataframes (including the "State" column since we merge on state)
    #"How: left" signifies that we keep all rows from the left dataframe
    all_data = all_data.merge(canada_exports[["State", "2024"]], how="left", on = "State")

    #After merging, we need to rename the data column from canada_exports (since it's just called 2024)
    all_data.rename(columns = {"2024":"Canada Exports"}, inplace=True)

    #Continue the same process for other import/export dataframes
    all_data = all_data.merge(canada_imports[["State", "2024"]], how="left", on = "State")
    all_data.rename(columns = {"2024":"Canada Imports"}, inplace=True)

    all_data = all_data.merge(mexico_exports[["State", "2024"]], how="left", on = "State")
    all_data.rename(columns = {"2024":"Mexico Exports"}, inplace=True)

    all_data = all_data.merge(mexico_imports[["State", "2024"]], how="left", on = "State")
    all_data.rename(columns = {"2024":"Mexico Imports"}, inplace=True)



    #Changing the import/export column datas into floats we can work with
    #.apply() applies a function to a column (in this case the 2024 data)
    all_data["Canada Exports"] = all_data["Canada Exports"].apply(convert_to_number)
    all_data["Canada Imports"] = all_data["Canada Imports"].apply(convert_to_number)
    all_data["Mexico Exports"] = all_data["Mexico Exports"].apply(convert_to_number)
    all_data["Mexico Imports"] = all_data["Mexico Imports"].apply(convert_to_number)

        
    return all_data


#A function that will calculate the balance of trade for each state with Mexico+Canada
def calculate_balance(df):
    """
    Using the values within the dataframe (Canada export/imports and Mexico exports/imports)
    calculate the balance of trade for each state with Mexico and Canada combined.
    We will have to call this function on our all_data df
    """

    #First, create an extra column which calculates the balance of trade with Canada and Mexico
    df["Canada Balance"] = df["Canada Exports"] - df["Canada Imports"]
    df["Mexico Balance"] = df["Mexico Exports"] - df["Mexico Imports"]


    #Create a third column that calculates total balance
    df["Total Balance"] = df["Mexico Balance"] + df["Canada Balance"]
       
    return df



def impact_calculator(df, rate):
    """"
    A function that intakes a tarriff rate and dataframe and uses a model
    (either Penn Model or my own) to calculate the proposed effect on imports and exports.
    This specific (simple) model is inspired by 

    The function will intake a dataframe (similar to all_data) and tarriff rate (given from the slider)
    and update the dataframe with the projected import/export volumes

    For simplification, we assume that in 2024 all goods were subject to a 0% tarriff rate.
    """

    #Making a copy of our dataframe
    projected_df = df.copy()

    if (rate == 0):
        #If the rate is 0, nothing changes (assume that there is currently 0% tarriff, as was the case for USMCA compliant goods in 2024)
        return projected_df
    
    #Converting the tarriff rate to a decimal
    dec_rate = rate / 100


    #VERY simple model
    #Assume import elasticity of -0.7 and export elasticity of -1.0 (since reciprocal tarriffs would reduce exports)

    #In economic literature, 0.7 is standard (cite a paper)
    import_elasticity = -0.7

    #For export elasticity, we have between 0.5 and 1.5
    export_elasticity = 1.0
    
    #Simple calculations to apply the elasticity onto the imports (0.7 times the tarriff rate will be the percent decrease in imports)
    projected_df["Canada Imports"] = df["Canada Imports"] * (1 + (import_elasticity * dec_rate))
    projected_df["Mexico Imports"] = df["Mexico Imports"] * (1 + (import_elasticity * dec_rate))
    
    #Simple calculations to apply the elasticity onto the exports (1.0 times the tarriff rate will be the percent increase in exports)
    projected_df["Canada Exports"] = df["Canada Exports"] * (1 + (export_elasticity * dec_rate))
    projected_df["Mexico Exports"] = df["Mexico Exports"] * (1 + (export_elasticity * dec_rate))
    
    #Because we changed the import/export columns, we need to call calculate_balance again
    #to recalculate the individual and total balances
    projected_df = calculate_balance(projected_df)
    
    return projected_df