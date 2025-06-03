import validators
import requests
import tldextract
import whois
from datetime import datetime

def validate_url(url):
    return validators.url(url)

def check_blacklist(url, blacklist_file='blacklist.txt'):
    with open(blacklist_file, 'r') as f:
        blacklist = f.read().splitlines()
    domain = tldextract.extract(url).registered_domain
    return domain in blacklist

def suspicious_patterns(url):
    patterns = ['@', 'http://', '-', 'tinyurl', 'bit.ly', 'free', 'login', 'verify']
    return any(p in url for p in patterns)

def get_domain_age(url):
    try:
        domain = tldextract.extract(url).registered_domain
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date:
            age_days = (datetime.now() - creation_date).days
            return age_days
    except:
        return None
    return None

def scan_url(url):
    result = {
        'url': url,
        'is_valid': validate_url(url),
        'in_blacklist': check_blacklist(url),
        'has_suspicious_patterns': suspicious_patterns(url),
        'domain_age_days': get_domain_age(url),
    }
    result['is_phishing'] = (
        not result['is_valid'] or
        result['in_blacklist'] or
        result['has_suspicious_patterns'] or
        (result['domain_age_days'] is not None and result['domain_age_days'] < 30)
    )
    return result
