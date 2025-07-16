import ipaddress
import tldextract
from urllib.parse import urlparse

sensitive_keywords = ['login', 'secure', 'update', 'verify', 'account', 'bank', 'password']
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
        # extracted.subdomain può essere vuoto o contenere più sottodomini separati da '.'
        if extracted.subdomain:
            return len(extracted.subdomain.split('.'))
        else:
            return 0
    except:
        return 0

def has_explicit_port(url):
    try:
        parsed_url = urlparse(url)
        return parsed_url.port is not None
    except Exception as e:
        return False # Restituisci False in caso di errore