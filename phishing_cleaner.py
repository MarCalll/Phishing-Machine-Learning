import pandas as pd

# inserimento nuova colonna con "is_phishing"
def create_phishing_df(url):
    df = pd.read_csv(url, header=None, names=["link"])
    df["is_phishing"] = 1
    return df


