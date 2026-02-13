#!/usr/bin/env python3
"""
FreeDNS.Afraid.org Domain Scraper

This script scrapes all available domains from freedns.afraid.org
that can be used for subdomain registration.

Usage: python scraper.py

Output: domains.txt - list of all domains, one per line
"""

import requests
from bs4 import BeautifulSoup
import time
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "https://freedns.afraid.org/domain/registry/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://freedns.afraid.org/'
}

def scrape_page(page_num):
    """Scrape a single page and return list of domains."""
    if page_num == 1:
        url = BASE_URL
    else:
        url = f"{BASE_URL}page-{page_num}.html"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')

        domains = []
        
        domain_links = soup.find_all('a', href=lambda href: href and 'edit_domain_id=' in href)
        for link in domain_links:
            domain = link.text.strip()
            if domain and '.' in domain:  # basic validation
                domains.append(domain)
        
        logger.info(f"Page {page_num}: Found {len(domains)} domains")
        return domains
        
    except requests.RequestException as e:
        logger.error(f"Error scraping page {page_num}: {e}")
        return []

def main():
    """Main scraping function."""
    all_domains = []
    total_pages = 254
    
    logger.info("Starting domain scraping...")
    
    for page in range(1, total_pages + 1):
        domains = scrape_page(page)
        all_domains.extend(domains)
        
        if page < total_pages:
            time.sleep(2)  # between requests
    
    # rm duplicates and sort
    unique_domains = sorted(list(set(all_domains)))
    
    output_file = Path("domains.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        for domain in unique_domains:
            f.write(f"{domain}\n")
    
    logger.info(f"Scraping complete. Found {len(unique_domains)} unique domains. Saved to {output_file}")

if __name__ == "__main__":
    main()
