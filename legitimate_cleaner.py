import pandas as pd
import tldextract

# inserimento nuova colonna con "is_phishing"
def create_legitimate_df():
    df = pd.read_csv("data/top-1m.csv", header=None, names=["link"])
    df["is_phishing"] = 0
    df = df[:464746]
    return df
