import legitimate_cleaner
import phishing_cleaner
import math
import ipaddress
import tldextract
import pandas as pd
import re
from urllib.parse import urlparse


sensitive_keywords = [
    'login', 'secure', 'update', 'verify', 'account', 'bank', 'password',
    'signin', 'confirm', 'validate', 'submit', 'security',
    'pay', 'payment', 'billing', 'invoice', 'transaction',
    'urgent', 'alert', 'warning', 'unusual', 'locked', 'suspended',
    'identity', 'credentials', 'authentication', 'recovery',
    'reset', 'support', 'access', 'admin', 'verifyidentity',
    'reverify', 'pin', 'code', 'token', '2fa', 'passcode',
    'ssn', 'social', 'securitynumber','paypal', 'apple', 'google', 'microsoft', 'amazon', 'facebook', 'instagram', 'dropbox', 'outlook', 'office365'
]

regex_sensitive_keywords = '|'.join(sensitive_keywords)

def is_ip_address(link):
    try:
        ipaddress.ip_address(link)
        return 1
    except ValueError:
        return 0
    
def count_subdomains(url):
    try:
        extracted = tldextract.extract(url)
        if extracted.subdomain:
            return len(extracted.subdomain.split('.'))
        else:
            return 0
    except:
        return 0

def has_explicit_port(url):
    try:
        parsed_url = urlparse(url)
        return 1 if parsed_url.port is not None else 0
    except Exception as e:
        return -1
    
def shannon_entropy(s):
    if not s:
        return 0
    probabilities = [s.count(c) / len(s) for c in set(s)]
    return -sum(p * math.log2(p) for p in probabilities)

def build_db():

    print("Creazione df \n")
    legitimateDF = legitimate_cleaner.create_legitimate_df()
    phishingDF = phishing_cleaner.create_phishing_df()
    combined_df = pd.concat([legitimateDF, phishingDF], ignore_index=True)

    print("creazione colonna link_length\n")
    combined_df["link_length"] = combined_df["link"].apply(len)

    print("creazione colonna dot_count\n")
    combined_df["dot_count"] = combined_df["link"].str.count(r'\.')

    print("creazione colonna is_ip\n")
    combined_df["is_ip"] = combined_df["link"].apply(is_ip_address)

    print("creazione colonna has_at_symbol\n")
    combined_df['has_at_symbol'] = combined_df['link'].str.contains('@').astype(int)

    print("creazione colonna count_hyphens\n")
    combined_df['count_hyphens'] = combined_df['link'].str.count('-')
    
    print("creazione colonna num_subdomains\n")
    combined_df["num_subdomains"] = combined_df["link"].apply(count_subdomains)

    print("creazione colonna has_subdomains\n")
    combined_df['has_subdomain'] = (combined_df['num_subdomains'] > 1).astype(int)
    
    print("creazione colonna count_sensitive_keyword\n")
    combined_df['count_sensitive_keyword'] = combined_df['link'].str.findall(regex_sensitive_keywords,flags=re.IGNORECASE).str.len()
    
    print("creazione colonna has_explicit_port\n")
    combined_df['has_explicit_port'] = combined_df['link'].apply(has_explicit_port)

    print("creazione colonna has_https\n")
    combined_df['has_https'] = combined_df['link'].str.startswith('https').astype(int)

    print("creazione colonna entropy\n")
    combined_df['entropy'] = combined_df['link'].apply(shannon_entropy)

    print("creazione output csv\n")
    combined_df.to_csv('data/output.csv', index=False)

    print("fine\n")
