# FreeDNS Afraid.org Domain Scraper

This project scrapes all available domains from [freedns.afraid.org](https://freedns.afraid.org/) that can be used for free subdomain registration.

<div align="center">
    <h3>See the available domains:</h3>
    <a href="domains-alphabetical.md">Domains Alphabetical</a> | <a href="domains-length.md">Domains by Length</a>
</div>

## Features

- Scrapes all ~25,000 public domains from the registry
- Handles pagination
- Extracts domain, status, owner, age, and hosts in use
- Outputs to markdown tables: alphabetical and length-sorted
- Automated via GitHub Actions every 12 hours

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

For testing with limited pages:
```bash
python scraper.py -p 10
```

The script will:
1. Scrape all 254 pages of the domain registry
2. Extract domain information from the HTML table rows
3. Save to `domains-alphabetical.md` and `domains-length.md`

## Automation (GitHub Actions)

The repository includes a GitHub Actions workflow that runs automatically every 12 hours.

To set it up:
1. Push this code to a GitHub repository
2. Ensure GitHub Actions is enabled
3. The workflow will run on schedule and commit updates to the markdown files

You can also trigger manually via the Actions tab.

## Output

- `domains-alphabetical.md`: Domains sorted alphabetically
- `domains-length.md`: Domains sorted by length (shortest first), then alphabetically
- Both files contain markdown tables with Domain, Status, Owner (linked), Age, and Hosts in Use

## Notes

- The script includes a 2-second delay between page requests to be respectful to the server
- Total runtime is approximately 8-10 minutes
- The number of pages may change over time; check the registry if scraping fails
- GitHub Actions will automatically commit changes when domains are updated
