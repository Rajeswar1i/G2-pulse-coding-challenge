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

## Sample Output
[
  {
    "title": "Great for team communication",
    "review": "Slack has transformed the way our team communicates. Channels, integrations, and notifications make collaboration seamless.",
    "date": "2024-12-15T00:00:00",
    "rating": "5",
    "author": "Jane Doe",
    "source": "g2",
    "source_url": "https://www.g2.com/products/slack/reviews"
  },
  {
    "title": "Easy to use but notifications can be overwhelming",
    "review": "Slack is intuitive, but sometimes the volume of notifications is too high. Muting channels helps, though.",
    "date": "2024-11-20T00:00:00",
    "rating": "4",
    "author": "John Smith",
    "source": "g2",
    "source_url": "https://www.g2.com/products/slack/reviews"
  },
  {
    "title": "Excellent integrations",
    "review": "The variety of app integrations makes Slack a powerful hub for all our workflows.",
    "date": "2024-10-05T00:00:00",
    "rating": "5",
    "author": "Emily Johnson",
    "source": "g2",
    "source_url": "https://www.g2.com/products/slack/reviews"
  }
]

