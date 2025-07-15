import pandas as pd

# inserimento nuova colonna con "is_phishing"
def create_legitimate_df():
    df = pd.read_csv("top-1m.csv", header=None, names=["link"])
    df["is_phishing"] = 0
    df = df[:500000]
    return df

