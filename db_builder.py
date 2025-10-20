import legitimate_cleaner
import phishing_cleaner
import math
import ipaddress
import tldextract
import pandas as pd
import re
from urllib.parse import urlparse

sensitive_keywords = [
    'login', 'secure', 'update', 'verify', 'account', 'bank', 'password','signin', 'confirm', 'validate', 'submit', 'security',
    'pay', 'payment', 'billing', 'invoice', 'transaction', 'urgent', 'alert', 'warning', 'unusual', 'locked', 'suspended', 'identity', 'credentials', 'authentication', 'recovery',
    'reset', 'support', 'access', 'admin', 'verifyidentity', 'reverify', 'pin', 'code', 'token', '2fa', 'passcode',
    'ssn', 'social', 'securitynumber','paypal', 'apple', 'google', 'microsoft', 'amazon', 'facebook', 'instagram', 'dropbox', 'outlook', 'office365'
]

free_hosting_services = ['weebly', 'wix', 'wordpress', 'blogspot', 'blogger', '000webhost', 'infinityfree', 'freehostia', 'byethost', 'site123', 'webnode', 'yolasite', 'simple-site',
                                'github.io', 'gitlab.io', 'netlify.app', 'vercel.app', 'herokuapp.com', 'firebaseapp.com', 'aws.amazon.com', 'googleusercontent.com', 'pages.dev', 
                                'my-free.website', 'free.nf', 'cu.cc', 'cz.cc', 'co.nf', 'tk', 'ml', 'ga', 'cf', 'altervista.org', 'tripod.com', 'angelfire.com', 'geocities.com', 
                                'bravesites.com', 'webs.com', 'yola.com', 'webstarts.com', 'ucoz.com', 'jimdo.com', 'sitey.com', '000webhostapp.com', 'weebly.com', 'weeblysite.com', 
                                'godaddysites.com', 'repl.co', 'glitch.me', 'duckdns.org', 'azurewebsites.net', 'atwebpages.com', '16mb.com', 'webcindario.com', 'freewebhostmost.com', 
                                'great-site.net', 'myportfolio.com', 'temporary.link', 'webspace.re', 'tonohost.com', 'hyperphp.com', 'moonfruit.com', 'brizy.site', 'easy.co', 'workers.dev', 
                                'appspot.com', 'webflow.io', 'c1.biz', '.ml', '.ga', '.tk', '.cf', '.gq'
]

tldsdict0 = {}
tldsdict1 = {}
tldsdictglobal = {}

regex_sensitive_keywords = '|'.join(sensitive_keywords)
regex_free_hosting_keywords = '|'.join(free_hosting_services)

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
    
def shannon_entropy(clean_domain):

    if not clean_domain or len(clean_domain) == 1:
        return 0.0

    probs = [clean_domain.count(c) / len(clean_domain) for c in set(clean_domain)]
    entropy = -sum(p * math.log2(p) for p in probs)

    return round(entropy, 6)

def build_db():
    github_Phishing_Domain_Database_phishingURL = "data/ALL-phishing-domains.lst"
    open_phish_data_URL = "data/openphishdata.txt"
    print("Creazione df \n")
    legitimateDF = legitimate_cleaner.create_legitimate_df()
    phishingDF1 = phishing_cleaner.create_phishing_df(github_Phishing_Domain_Database_phishingURL)
    phishingDF2 = phishing_cleaner.create_phishing_df(open_phish_data_URL)
    combined_df = pd.concat([legitimateDF, phishingDF1,phishingDF2], ignore_index=True)

    new_df = build_columns(combined_df)
    print("Salvataggio csv")
    new_df.to_csv("data/output.csv", index=False)

    return new_df

def remove_duplicates(df):
    df_clean = df.drop_duplicates(subset=['full_domain', 'clean_domain', 'top_level_domain'], keep='first')
    phishing_count = df_clean['is_phishing'].sum()
    legitimate_count = (df_clean['is_phishing'] == 0).sum()

    print(f"Phishing: {phishing_count}")
    print(f"Legittimi: {legitimate_count}")

    return df_clean

def extract_domain(url):
    ext = tldextract.extract(url)
    domain = ext.domain
    return f"{domain}"

def extract_full_domain(url):
    ext = tldextract.extract(url)
    domain = ext.domain
    subdomain = ext.subdomain
    suffix = ext.suffix

    if subdomain:
        return f"{subdomain}.{domain}.{suffix}"
    else:
        return f"{domain}.{suffix}"

def extract_TLD(url):
    ext = tldextract.extract(url)
    suffix = ext.suffix
    return f"{suffix}"
    
def build_tld_ratio(row):
    global tldsdict0,tldsdict1
    top_level_domain = row['top_level_domain']
    is_phishing = row['is_phishing']
    if is_phishing == 0:
        tldsdict0[top_level_domain] = tldsdict0.get(top_level_domain, 0) + 1
    else:
        tldsdict1[top_level_domain] = tldsdict1.get(top_level_domain, 0) + 1

def build_global_tld_ratio():
    totaletlds = sum(tldsdict0.values()) + sum(tldsdict1.values())
    global tldsdictglobal
    for k, v in tldsdict0.items():
        tldsdictglobal[k] = v

    for k, v in tldsdict1.items():
        tldsdictglobal[k] = tldsdictglobal.get(k, 0) + v
    
    for k, v in tldsdictglobal.items():
        tldsdictglobal[k] = v / totaletlds

def set_tld_ratio(tld):
    idratio = tldsdictglobal[tld]
    return idratio

def build_columns(df):

    print("creazione colonne...\n")

    df['full_domain'] = df['link'].apply(extract_full_domain)

    df["clean_domain"] = df["link"].apply(extract_domain)

    df["top_level_domain"] = df["link"].apply(extract_TLD)

    df['domain_length'] = df['clean_domain'].str.len()

    df['count_digits'] = df['clean_domain'].str.count(r'\d')

    df["is_ip"] = df["link"].apply(is_ip_address)

    df['has_at_symbol'] = df['clean_domain'].str.contains('@').astype(int)
    
    df['count_hyphens'] = df['clean_domain'].str.count('-')

    df['count_special_chars'] = df['clean_domain'].apply(lambda x: len(re.findall(r'[^a-zA-Z0-9]', x)))

    df["num_subdomains"] = df["clean_domain"].apply(count_subdomains)

    df['free_hosting_keyword'] = df['clean_domain'].str.findall(regex_free_hosting_keywords,flags=re.IGNORECASE).str.len()

    df['count_sensitive_keyword'] = df['clean_domain'].str.findall(regex_sensitive_keywords,flags=re.IGNORECASE).str.len()
    
    df['has_explicit_port'] = df['link'].apply(has_explicit_port)

    df['entropy'] = df['clean_domain'].apply(shannon_entropy)

    df[['top_level_domain', 'is_phishing']].apply(build_tld_ratio, axis=1)
    build_global_tld_ratio()
    df['tld_phishing_ratio'] = df['top_level_domain'].apply(set_tld_ratio)

    print("fine creazione colonne\n")

    return df

def build_custom_domain_columns(dominio_df):

    print("creazione colonne custom domain\n")

    dominio_df['full_domain'] = dominio_df['link'].apply(extract_full_domain)

    dominio_df["clean_domain"] = dominio_df["link"].apply(extract_domain)

    dominio_df["top_level_domain"] = dominio_df["link"].apply(extract_TLD)

    dominio_df['domain_length'] = dominio_df['clean_domain'].str.len()

    dominio_df['count_digits'] = dominio_df['clean_domain'].str.count(r'\d')

    dominio_df["is_ip"] = dominio_df["link"].apply(is_ip_address)

    dominio_df['has_at_symbol'] = dominio_df['clean_domain'].str.contains('@').astype(int)
    
    dominio_df['count_hyphens'] = dominio_df['clean_domain'].str.count('-')

    dominio_df['count_special_chars'] = dominio_df['clean_domain'].apply(lambda x: len(re.findall(r'[^a-zA-Z0-9]', x)))

    dominio_df["num_subdomains"] = dominio_df["clean_domain"].apply(count_subdomains)

    dominio_df['free_hosting_keyword'] = dominio_df['clean_domain'].str.findall(regex_free_hosting_keywords,flags=re.IGNORECASE).str.len()

    dominio_df['count_sensitive_keyword'] = dominio_df['clean_domain'].str.findall(regex_sensitive_keywords,flags=re.IGNORECASE).str.len()
    
    dominio_df['has_explicit_port'] = dominio_df['link'].apply(has_explicit_port)

    dominio_df['entropy'] = dominio_df['clean_domain'].apply(shannon_entropy)

    dominio_df['tld_phishing_ratio'] = dominio_df['top_level_domain'].apply(set_tld_ratio)

    print("Fine creazione colonne custom domain\n")

    return dominio_df

def test_custom_domain(dominio):
    # dominio = input("Inserisci dominio: ")

    dominio_df = pd.DataFrame({'link': [dominio]})
    new_df = build_custom_domain_columns(dominio_df)
    print("dominio inserito:",dominio)
    print(new_df)
    
    return new_df