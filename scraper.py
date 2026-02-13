#!/usr/bin/env python3
"""
FreeDNS.Afraid.org Domain Scraper

This script scrapes all available domains from freedns.afraid.org
that can be used for subdomain registration.

Usage: python scraper.py [-p PAGES]

Options:
  -p PAGES, --pages PAGES  Number of pages to scrape (default: 254)

Output: domains-alphabetical.md and domains-length.md
"""

import requests
from bs4 import BeautifulSoup
import time
import logging
from pathlib import Path
import re
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "https://freedns.afraid.org/domain/registry/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://freedns.afraid.org/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
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
        
        # find domain rows with class 'trd' or 'trl'
        domain_rows = soup.find_all('tr', class_=['trd', 'trl'])
        for row in domain_rows:
            cols = row.find_all('td')
            if len(cols) >= 4:
                domain_cell = cols[0]
                status = cols[1].get_text().strip()
                owner_link = cols[2].find('a')
                if owner_link:
                    owner = owner_link.get_text().strip()
                    owner_href = owner_link.get('href')
                    owner_url = f"https://freedns.afraid.org{owner_href}" if owner_href else ""
                else:
                    owner = cols[2].get_text().strip()
                    owner_url = ""
                age = cols[3].get_text().strip()
                
                # extract domain and hosts
                full_text = domain_cell.get_text()
                lines = full_text.split('\n')
                domain = lines[0].strip()
                hosts_part = ' '.join(lines[1:]) if len(lines) > 1 else ""
                hosts_match = re.search(r'\((\d+) hosts in use\)', hosts_part)
                hosts = int(hosts_match.group(1)) if hosts_match else 0
                
                if domain and '.' in domain:
                    domains.append({
                        'domain': domain,
                        'status': status,
                        'owner': owner,
                        'owner_url': owner_url,
                        'age': age,
                        'hosts': hosts
                    })
        
        logger.info(f"Page {page_num}: Found {len(domains)} domains")
        return domains
        
    except requests.RequestException as e:
        logger.error(f"Error scraping page {page_num}: {e}")
        return []

def main(pages=254):
    """Main scraping function."""
    all_data = []
    total_pages = pages
    
    logger.info("Starting domain scraping...")
    
    for page in range(1, total_pages + 1):
        data = scrape_page(page)
        all_data.extend(data)
        
        if page < total_pages:
            time.sleep(2)  # between requests
    
    # remove duplicates based on domain
    unique_data = {item['domain']: item for item in all_data}.values()
    
    logger.info(f"Collected {len(all_data)} entries, unique: {len(unique_data)}")
    
    # sort alphabetically
    sorted_alpha = sorted(unique_data, key=lambda x: x['domain'])
    
    # sort by length then alphabetically
    sorted_length = sorted(unique_data, key=lambda x: (len(x['domain']), x['domain']))
    
    # write to md files
    write_md("domains-alphabetical.md", sorted_alpha)
    write_md("domains-length.md", sorted_length)
    
    logger.info(f"Scraping complete. Found {len(unique_data)} unique domains.")

def write_md(filename, data):
    """Write data to markdown table."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# FreeDNS Afraid.org Domains\n\n")
        f.write(f"Total domains: {len(data)}\n\n")
        f.write("| Domain | Status | Owner | Age | Hosts in Use |\n")
        f.write("|--------|--------|-------|-----|--------------|\n")
        for item in data:
            owner_link = f"[{item['owner']}]({item['owner_url']})" if item['owner_url'] else item['owner']
            f.write(f"| {item['domain']} | {item['status']} | {owner_link} | {item['age']} | {item['hosts']} |\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape domains from freedns.afraid.org')
    parser.add_argument('-p', '--pages', type=int, default=254, help='Number of pages to scrape (default: 254)')
    args = parser.parse_args()
    main(args.pages)
