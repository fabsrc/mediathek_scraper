# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'mediathek_scraper',
    version      = '0.7',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = mediathek_scraper.settings']},
)
