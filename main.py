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
    filtered_df = filter_data(df, column, year[0], year[1], month[0], month[1])
    print(filtered_df)
def read_csv(file):
    return pd.read_csv(file)

def get_datetime(df, column, date_format):
    df[column]= pd.to_datetime(df[column], format=date_format)
    return df[column]
    
def get_month_input():
    try:
        f_m = int(input("Insira o mes de inicio: "))
        l_m = int(input("Insira o mes de termino: "))
        if f_m >= 1 and f_m <= 12 and l_m >= 1 and l_m <= 12:
            return [f_m, l_m]
        else:
            print("Invalid input. Please enter a valid month.")
            return get_month_input()
    except:
        print("Invalid input. Please enter a valid month.")

def get_year_input(first_year, last_year):
    try:
        f_y = int(input("Insira o ano de inicio: "))
        l_y = int(input("Insira o ano de termino: "))
        if f_y >= first_year and f_y <= last_year and l_y >= first_year and l_y <= last_year:
            return [f_y, l_y]
        else:
            print("Invalid input. Please enter a valid year.")
            return get_year_input(first_year, last_year)
    except:
        print("Invalid input. Please enter a valid year.")

def filter_data(df, column, first_year, last_year, m, l):
    if m < 10 and l < 9:
        df = df[(df[column] >= f'{first_year}-0{m}-01') & (df[column] < f'{last_year}-0{l+1}-01')]
    elif m < 10 and l >= 9:
        df = df[(df[column] >= f'{first_year}-0{m}-01') & (df[column] < f'{last_year}-{l+1}-01')]
    elif m >= 10 and l < 9:
        df = df[(df[column] >= f'{first_year}-{m}-01') & (df[column] < f'{last_year}-0{l+1}-01')]
    else:
        df = df[(df[column] >= f'{first_year}-{m}-01') & (df[column] < f'{last_year}-{l+1}-01')]
    return df
    
main()