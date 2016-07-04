# customs-news-crawler
Collection of Scrapy spiders used to crawl the customs sites of some european nations.

## Requirements
- Python 2.7 or Python >= 3.5
- Scrapy >= 1.0

## Installation via pip
```python
pip install Scrapy
```

## Usage
```bash
$ cd spiders/
$ scrapy runspider albania.py -o albania-results.csv
```

Change the .py file name to run the relative spider.
Make sure the output file has the `.csv` extension if you want the data in that format (you can also use `.json` if you prefere JSON data).

If you need to perform a heavy number of requests please consider incorporating these spiders inside a full fledged Scrapy project and add proper User-Agent / Throttling / ... configuration.

## License
BSD3, see the attached `LICENSE` file for more information.