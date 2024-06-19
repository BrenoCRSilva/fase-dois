import pandas as pd

def main():
    data_path = "data.csv"
    column = "data"
    date_format = "%d/%m/%Y"
    first_year = 1961
    last_year = 2016
    
    print("---- Bem vindo ----\n\n\n")
    df = read_csv(data_path)
    month = get_month_input()
    year = get_year_input(first_year, last_year)
    print("Deseja ver: 1) todos os dados, 2) apenas os de precipitação, 3) apenas os de temperatura, ou 4) apenas os de umidade e vento?\n")
    mode = get_mode_input()
    get_datetime(df, column, date_format)
    df_dates = filter_by_date(df, column, year[0], year[1], month[0], month[1])
    filtered_df = filter_by_mode(df_dates,column, mode)
    print(f"\n{get_max_value(df, first_year, last_year)}")
    print(f"\n\n\n{filtered_df.to_string(index=False)}")
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
        f_y = int(input("Insira o ano de inicio: "))
        l_y = int(input("Insira o ano de termino: "))
        if f_y >= first_year and f_y <= last_year and l_y >= first_year and l_y <= last_year:
            return [f_y, l_y]
        else:
            print("Invalid input. Please enter a valid year.")
            return get_year_input(first_year, last_year)
    except:
        print("Invalid input. Please enter a valid year.")

def filter_by_date(df, column, first_year, last_year, m, l):
    if l == 12 and m >=10:
        df = df[(df[column] >= f'{first_year}-{m}-01') & (df[column] < f'{last_year + 1}-01-01')]
    elif l == 12 and m < 10:
        df = df[(df[column] >= f'{first_year}-0{m}-01') & (df[column] < f'{last_year + 1}-01-01')]
    elif m < 10 and l < 9:
        df = df[(df[column] >= f'{first_year}-0{m}-01') & (df[column] < f'{last_year}-0{l+1}-01')]
    elif m < 10 and l >= 9:
        df = df[(df[column] >= f'{first_year}-0{m}-01') & (df[column] < f'{last_year}-{l+1}-01')]
    elif m >= 10 and l < 9:
        df = df[(df[column] >= f'{first_year}-{m}-01') & (df[column] < f'{last_year}-0{l+1}-01')]
    else:
        df = df[(df[column] >= f'{first_year}-{m}-01') & (df[column] < f'{last_year}-{l+1}-01')]
    return df
    
def filter_by_mode(df, column, mode):
    if mode == 1:
        return df
    elif mode == 2:
        return df[[column, "precip"]]
    elif mode == 3:
        return df[[column, "temp_media"]]
    else:
        return df[[column,"um_relativa", "vel_vento"]]
    
def get_max_value(df, first_year, last_year):
    precip_dict = {}
    for year in range(first_year, last_year + 1):
        for month in range(1,13):
            f_df = df[(df["data"].dt.month == month) & (df["data"].dt.year == year)] 
            df_mean = f_df["precip"].mean()
            precip_dict[f"{month}/{year}"] = df_mean
    
    max_value = max(precip_dict, key=precip_dict.get)
           
    return f" O mes/ano mais chuvoso foi: {max_value} com media de {str(precip_dict[max_value])} mm"
    

main()