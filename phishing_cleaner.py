import pandas as pd

# inserimento nuova colonna con "is_phishing"
def create_phishing_df():
    df = pd.read_csv("ALL-phishing-domains.lst", header=None, names=["link"])
    df["is_phishing"] = 1
    return df


