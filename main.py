import pandas as pd

def main():
    print("---- Bem vindo ----\n\n\n")
    data_path = "data.csv"
    column = "data"
    date_format = "%d/%m/%Y"
    first_year = 1961
    last_year = 2016
    month = get_month_input()
    year = get_year_input(first_year, last_year)
    df = read_csv(data_path)
    get_datetime(df, column, date_format)
    filtered_df = filter_data(df, column, year, month)
    print(filtered_df)
    

def read_csv(file):
    return pd.read_csv(file)

def get_datetime(df, column, date_format):
    df[column]= pd.to_datetime(df[column], format=date_format)
    return df[column]
    
def get_month_input():
    try:
        month = int(input("Insira o mes: "))
        if month >= 1 and month <= 12:
            return month
        else:
            print("Invalid input. Please enter a valid month.")
            return get_month_input()
    except:
        print("Invalid input. Please enter a valid month.")

def get_year_input(first_year, last_year):
    try:
        year = int(input("Insira o ano: "))
        if year >= first_year and year <= last_year:
            return year
        else:
            print("Invalid input. Please enter a valid year.")
            return get_year_input(first_year, last_year)
    except:
        print("Invalid input. Please enter a valid year.")

def filter_data(df, column, y, m):
    filtered_df = df.loc[(df[column].dt.month >= m) & (df[column].dt.year >= y)] #add first and last conditions to loc
    return filtered_df
    
main()