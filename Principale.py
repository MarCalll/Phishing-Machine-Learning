import legitimate_cleaner
import phishing_cleaner
import pandas as pd

## https://1drv.ms/w/c/b4634b89beb127d2/ERBumWK5kSxPsvVa6Z5QJWoBcDoZhPueE-87AKMkHb8GYw?e=8BI0O2

legitimateDF = legitimate_cleaner.create_legitimate_df()
phishingDF = phishing_cleaner.create_phishing_df()
combined_df = pd.concat([legitimateDF, phishingDF], ignore_index=True)

combined_df["link_length"] = combined_df["link"].apply(len)

print(combined_df)