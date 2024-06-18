import pandas as pd

def main():
    df = pd.read_csv("data.csv")
    df["data"]= pd.to_datetime(df["data"], infer_datetime_format=True)
    filtered_df = df.loc[(df['data'].dt.month == 6) & (df['data'].dt.year == 2016)]
    print(filtered_df)



def get_user_input():
    try:
        year = int(input("Enter year: "))
        month = int(input("Enter month: "))
        return year, month
    except:
        print("Invalid input. Please enter a valid year and month.")


main()