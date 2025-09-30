# Pulse Coding Assignment - Product Reviews Scraper

## Overview
This project scrapes product reviews from **G2**, **Capterra**, and **TrustRadius** for a specific company and time period.

## Requirements
- Python 3.9+
- Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
```bash
python scraper.py --company "Company Name" --start 2023-01-01 --end 2024-12-31 --source g2 --output out.json
```

### Parameters
- `--company`: Company name (required)
- `--start`: Start date (YYYY-MM-DD or natural language parsable)
- `--end`: End date (YYYY-MM-DD)
- `--source`: Source site (`g2`, `capterra`, `trustradius`)
- `--output`: Output JSON filename (default: `reviews.json`)
- `--headless`: Optional flag to run browser headless (default: headless)

## Output
A JSON array of reviews, each containing:
- `title`
- `review` (body text)
- `date` (ISO 8601 string)
- `rating` (if available)
- `author` (if available)
- `source` (g2/capterra/trustradius)
- `source_url` (direct URL to review if available)

## Notes
- Uses Selenium (headless Chrome) to handle JS-heavy review pages.
- Performs web search to find the company's review page dynamically.
- Handles pagination by scrolling.
- Respect site scraping policies; for educational purposes only.

## Bonus Source
- **TrustRadius** integrated as the third source for SaaS reviews.
