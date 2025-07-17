import pandas as pd
import db_builder
import os
import data_visualization

## https://1drv.ms/w/c/b4634b89beb127d2/ERBumWK5kSxPsvVa6Z5QJWoBcDoZhPueE-87AKMkHb8GYw?e=8BI0O2

if os.path.exists("data\output.csv"):
    print("✅ Il file esiste già. Nessuna operazione eseguita.")
else:
    db_builder.build_db()

df = pd.read_csv("data/output.csv")

df = df.drop(columns=['has_at_symbol','has_explicit_port'])
print(df)

top_10_entropy = df.sort_values(by="entropy",ascending=False).head(10)
print(top_10_entropy)
top_10_link_length = df.sort_values(by="link_length",ascending=False).head(10)
print(top_10_link_length)

#data_visualization.show_correlation_matrix(df)

#togliere colonne senza dati oppure aggiungere un altro dataset



