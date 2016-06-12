# Mediathek Scraper

*Scrapes videos from mediatheks of ARD, ZDF, arte and 3sat*

## Installation

This scraper requires [Scrapy](http://scrapy.org/)

```bash
pip install scrapy
```

## Usage

Specify the mediathek to crawl: `ard`, `zdf`, `3sat`, `arte`

```bash
scrapy crawl ard
```

The output is stored in `items.jsonl`
