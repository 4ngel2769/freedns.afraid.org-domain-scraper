# FreeDNS Afraid.org Domain Scraper

This project scrapes all available domains from [freedns.afraid.org](https://freedns.afraid.org/) that can be used for free subdomain registration.

## Features

- Scrapes all ~25,000 public domains from the registry
- Handles pagination

## Requirements

- Python 3.9+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the scraper:
```bash
python scraper.py
```

The script will:
1. Scrape all 254 pages of the domain registry
2. Extract domain names from the HTML tables
3. Save unique domains to `domains.txt`

## Automation (Every 12 Hours)

### Linux/Mac (using cron)

Add to crontab:
```bash
0 */12 * * * cd /path/to/project && python scraper.py
```

### Windows Task Scheduler

1. Open Task Scheduler
2. Create a new task
3. Set trigger to "Daily" with repeat every 12 hours
4. Set action to "Start a program"
5. Program: `python.exe`
6. Arguments: `scraper.py` (full path)
7. Start in: Full path to this directory

## Output

- `domains.txt`: List of all scraped domains, one per line
- Console logs: Progress and any errors

## Notes

- The script includes a 2-second delay between page requests to be respectful to the server
- Total runtime is approximately 8-10 minutes with current 254 pages
- The number of pages may change over time; check the registry if scraping fails

## Legal

- This scraper only accesses publicly available information
- No authentication is required
- Be respectful with request frequency
- Check freedns.afraid.org for any terms of service updates
