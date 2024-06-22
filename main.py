import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics
import sys

class WeatherData:
    def __init__(self, csv_file, city, date_column, min_temp_column, precip_column, date_format, first_year, middle_year, last_year):
        self.csv_file = csv_file
        self.city = city
        self.date_column = date_column
        self.min_temp_column = min_temp_column
        self.precip_column = precip_column
        self.date_format = date_format
        self.first_year = first_year
        self.middle_year = middle_year
        self.last_year = last_year

def main():
    data = WeatherData(csv_file=sys.argv[1] , city="Porto Alegre", date_column="data", 
                       min_temp_column="minima", precip_column="precip", 
                       date_format="%d/%m/%Y", first_year=1961, 
                       middle_year=2006, last_year=2016)
    
    print("---- Bem vindo ----\n\n\n")
    df = pd.read_csv(data.csv_file)
    df[data.date_column] = pd.to_datetime(df[data.date_column], format=data.date_format)
    month_input = get_month_input(both=True)
    year_input = get_year_input(data.first_year, data.last_year)
    print("Deseja ver: 1) todos os dados, 2) apenas os de precipitação, 3) apenas os de temperatura, ou 4) apenas os de umidade e vento?\n")
    mode_input = get_mode_input()
    df_dates = filter_by_date(df, data.date_column, year_input[0], year_input[1], month_input[0], month_input[1])
    filtered_df = filter_by_mode(df_dates, data.date_column, mode_input)
    print(f"\n{filtered_df.to_string(index=False)}\n")
    print(f"{get_most_rainy(df, data.date_column, data.precip_column, data.first_year, data.last_year)}")
    month_input = get_month_input(both=False)
    min_temp_avgs = get_min_temp_averages(df, data.date_column, data.min_temp_column, month_input, data.middle_year, data.last_year)
    for k, v in min_temp_avgs[0].items():
        print(f"{k} : {v}")
    print(f"\nEssa foi a media de temperatura minima no mes: {min_temp_avgs[1]}°C")
    plot_bar_graph(min_temp_avgs[0], month_input, data.middle_year, data.last_year)

def get_month_input(both):
    try:
        if both == True:
            first_input = int(input("Insira o mes de inicio: "))
            print("")
            last_input = int(input("Insira o mes de termino: "))
            print("")
            if first_input >= 1 and first_input <= 12 and last_input >= 1 and last_input <= 12:
                return [first_input, last_input]
            else:
                print("Invalid input. Please enter a valid month.")
                return get_month_input(both)
        elif both == False:
            first_input = int(input("Insira o mes: "))
            print("")
            if first_input >= 1 and first_input <= 12:
                return first_input
            else:
                print("Invalid input. Please enter a valid month.")
                return get_month_input(both)
    except:
        print("Invalid input. Please enter a valid month.")

def get_year_input(first_year, last_year):
    try:
        first_input = int(input("Insira o ano de inicio: "))
        print("")
        last_input = int(input("Insira o ano de termino: "))
        print("")
        if first_input >= first_year and first_input <= last_year and last_input >= first_year and last_input <= last_year:
            return [first_input, last_input]
        else:
            print("Invalid input. Please enter a valid year.")
            return get_year_input(first_year, last_year)
    except:
        print("Invalid input. Please enter a valid year.")

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
    
def get_most_rainy(df, date_column, precip_column, first_year, last_year):
    precip_dict = {}
    for year in range(first_year, last_year + 1):
        for month in range(1,13):
            f_df = df[(df[date_column].dt.month == month) & (df[date_column].dt.year == year)] 
            df_mean = f_df[precip_column].mean()
            precip_dict[f"{month}/{year}"] = df_mean
    
    max_value = max(precip_dict, key=precip_dict.get)
           
    return f" O mes/ano mais chuvoso foi: {max_value} com media de {str(precip_dict[max_value])} mm\n"

def get_min_temp_averages(df, date_column, min_temp_column, month, middle_year, last_year):
    month_dict = {}
    for year in range(middle_year, last_year + 1):
        f_df = df[(df[date_column].dt.month == month) & (df[date_column].dt.year == year)]
        df_mean = f_df[min_temp_column].mean()
        if np.isnan(df_mean):
            pass
        else:
            month_dict[f"{month}/{year}"] = round(df_mean, 2)
        
    return month_dict, statistics.mean(list(month_dict.values()))

def plot_bar_graph(month_dict, month, middle_year, last_year):
    array_items = np.array(list(month_dict.keys()))
    array_years = np.array(list(month_dict.values()))
    x = array_items
    y = array_years
    plt.bar(x, y, width = 0.6, color = "black")
    plt.xticks(fontsize = 7)
    plt.xlabel(f"Mes {month} no intervalo {middle_year} - {last_year}")
    plt.ylabel("Temperatura minima (°C)")
    plt.title("Temperatura minima do municipio por mes/ano")
    plt.show()
    
main()