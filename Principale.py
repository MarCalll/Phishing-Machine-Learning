import pandas as pd

import db_builder
import os
import data_visualization
import machine_learning

df = None

df = db_builder.build_db()
df = db_builder.remove_duplicates(df)
print(df)

data_visualization.show_correlation_matrix(df)
#Le correlazioni con la variabile target sono generalmente deboli (tutte < 0.15), suggerendo che nessuna feature da sola è un predittore forte di phishing,
# ma insieme possono essere utili in un modello di machine learning.

machine_learning.set_df(df)
machine_learning.run_randomforestclassifier()
machine_learning.run_xgboost()
machine_learning.run_lightGBM()
machine_learning.run_catboost()
machine_learning.run_extraTrees()
machine_learning.run_LogReg()
machine_learning.run_autoGluon(df)

legitimate_test_domains = [
    "google.com",                          # Brand noto, dominio semplice
    "github.com",                          # Servizio sviluppatori famoso
    "stackoverflow.com",                   # Community tecnica
    "medium.com",                          # Piattaforma blogging
    "auth0.com",                           # Servizio auth - nome sospetto
    "vercel.app",                          # TLD .app + nome breve
    "account.google.com",                  # Sottodominio con "account"
    "security.ubuntu.com"                  # Sottodominio con "security"
]

for ele in legitimate_test_domains:
    custom_df = db_builder.test_custom_domain(ele)
    machine_learning.predict_dominio(custom_df)