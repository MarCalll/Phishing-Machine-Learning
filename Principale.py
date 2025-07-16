import legitimate_cleaner
import phishing_cleaner
import db_builder
import pandas as pd
import re 

## https://1drv.ms/w/c/b4634b89beb127d2/ERBumWK5kSxPsvVa6Z5QJWoBcDoZhPueE-87AKMkHb8GYw?e=8BI0O2

legitimateDF = legitimate_cleaner.create_legitimate_df()
phishingDF = phishing_cleaner.create_phishing_df()
combined_df = pd.concat([legitimateDF, phishingDF], ignore_index=True)

combined_df["link_length"] = combined_df["link"].apply(len)
combined_df["dot_count"] = combined_df["link"].str.count(r'\.')
combined_df["is_ip"] = combined_df["link"].apply(db_builder.is_ip_address)

combined_df['has_at_symbol'] = combined_df['link'].str.contains('@').astype(int)
combined_df['count_hyphens'] = combined_df['link'].str.count('-')
combined_df["num_subdomains"] = combined_df["link"].apply(db_builder.count_subdomains)
combined_df['count_sensitive_keyword'] = combined_df['link'].str.findall(db_builder.regex_sensitive_keywords,flags=re.IGNORECASE).str.len()
combined_df['has_explicit_port'] = combined_df['link'].apply(db_builder.has_explicit_port)

#print(link_con_sensitive_word)
print(combined_df)