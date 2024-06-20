import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics

def main():
    data_path = "data.csv"
    date_column = "data"
    date_format = "%d/%m/%Y"
    first_year = 1961
    middle_year = 2006
    last_year = 2016
    one = False
    two = True
    
    print("---- Bem vindo ----\n\n\n")
    df = read_csv(data_path)
    month_input = get_month_input(two)
    year_input = get_year_input(first_year, last_year)
    print("Deseja ver: 1) todos os dados, 2) apenas os de precipitação, 3) apenas os de temperatura, ou 4) apenas os de umidade e vento?\n")
    mode_input = get_mode_input()
    get_datetime(df, date_column, date_format)
    df_dates = filter_by_date(df, date_column, year_input[0], year_input[1], month_input[0], month_input[1])
    filtered_df = filter_by_mode(df_dates, date_column, mode_input)
    print(f"\n\n\n{filtered_df.to_string(index=False)}\n\n")
    print(f"{get_max_value(df, first_year, last_year)}")
    month_input = get_month_input(one)
    min_temp_avgs = get_min_temp_averages(middle_year, last_year, month_input, df)
    for k, v in min_temp_avgs[0].items():
        print(f"{k} : {v}")
    print(f"\n\nEssa foi...:{min_temp_avgs[1]}")
    plot_bar_graph(min_temp_avgs[0])
    
def read_csv(file):
    return pd.read_csv(file)

def get_datetime(df, column, date_format):
    df[column]= pd.to_datetime(df[column], format=date_format)
    return df[column]
    
def get_month_input(both):
    try:
        if both == True:
            first_input = int(input("Insira o mes de inicio: "))
            last_input = int(input("Insira o mes de termino: "))
            if first_input >= 1 and first_input <= 12 and last_input >= 1 and last_input <= 12:
                return [first_input, last_input]
            else:
                print("Invalid input. Please enter a valid month.")
                return get_month_input(both)
        else:
            first_input = int(input("Insira o mes: "))
            if first_input >= 1 and first_input <= 12:
                return first_input
            else:
                print("Invalid input. Please enter a valid month.")
                return get_month_input(both)
    except:
        print("Invalid input. Please enter a valid month.")

def get_mode_input():
    try:
        mode = int(input("Insira o modo: "))
        if mode >= 1 and mode <= 4:
            return mode
        else:
            return get_mode_input()
    except:
        print("Invalid input. Please enter a valid mode.")
        return get_mode_input()
def get_year_input(first_year, last_year):
    try:
        first_input = int(input("Insira o ano de inicio: "))
        last_input = int(input("Insira o ano de termino: "))
        if first_input >= first_year and first_input <= last_year and last_input >= first_year and last_input <= last_year:
            return [first_input, last_input]
        else:
            print("Invalid input. Please enter a valid year.")
            return get_year_input(first_year, last_year)
    except:
        print("Invalid input. Please enter a valid year.")

def filter_by_date(df, date_column, first_year, last_year, first_month, last_month):
    if last_month == 12 and first_month >=10:
        df = df[(df[date_column] >= f'{first_year}-{first_month}-01') & (df[date_column] < f'{last_year + 1}-01-01')]
    elif last_month == 12 and first_month < 10:
        df = df[(df[date_column] >= f'{first_year}-0{first_month}-01') & (df[date_column] < f'{last_year + 1}-01-01')]
    elif first_month < 10 and last_month < 9:
        df = df[(df[date_column] >= f'{first_year}-0{first_month}-01') & (df[date_column] < f'{last_year}-0{last_month + 1}-01')]
    elif first_month < 10 and last_month >= 9:
        df = df[(df[date_column] >= f'{first_year}-0{first_month}-01') & (df[date_column] < f'{last_year}-{last_month + 1}-01')]
    elif first_month >= 10 and last_month < 9:
        df = df[(df[date_column] >= f'{first_year}-{first_month}-01') & (df[date_column] < f'{last_year}-0{last_month + 1}-01')]
    else:
        df = df[(df[date_column] >= f'{first_year}-{first_month}-01') & (df[date_column] < f'{last_year}-{last_month + 1}-01')]
    return df
    
def filter_by_mode(df, date_column, mode):
    if mode == 1:
        return df
    elif mode == 2:
        return df[[date_column, "precip"]]
    elif mode == 3:
        return df[[date_column, "temp_media"]]
    else:
        return df[[date_column,"um_relativa", "vel_vento"]]
    
def get_max_value(df, first_year, last_year):
    precip_dict = {}
    for year in range(first_year, last_year + 1):
        for month in range(1,13):
            f_df = df[(df["data"].dt.month == month) & (df["data"].dt.year == year)] 
            df_mean = f_df["precip"].mean()
            precip_dict[f"{month}/{year}"] = df_mean
    
    max_value = max(precip_dict, key=precip_dict.get)
           
    return f" O mes/ano mais chuvoso foi: {max_value} com media de {str(precip_dict[max_value])} mm\n\n"

def get_min_temp_averages(first_year, last_year, month, df):
    month_dict = {}
    for year in range(first_year, last_year + 1):
        f_df = df[(df["data"].dt.month == month) & (df["data"].dt.year == year)]
        df_mean = f_df["minima"].mean()
        if np.isnan(df_mean):
            pass
        else:
            month_dict[f"{month}/{year}"] = round(df_mean, 2)
        
    return month_dict, statistics.mean(list(month_dict.values()))

def plot_bar_graph(some_dict):
    array_items = np.array(list(some_dict.keys()))
    array_years = np.array(list(some_dict.values()))
    x = array_items
    y = array_years
    plt.bar(x, y, width = 0.6, color = "black")
    plt.xticks(fontsize = 5)
    plt.show()
    
    

main()