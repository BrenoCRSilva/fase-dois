import pandas as pd

def main():
    
    df = pd.read_csv("data.csv")
    print(df.to_string())


def get_data_by_date():
    pass

main()