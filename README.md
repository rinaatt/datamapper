# Test Project for check skils

This test mapper based on scrapy.

For run:

    scrapy crawl rss_feed_yandex
    
For check spider:

    scrapy check rss_feed_yandex
    
For check pipeline:

    python -m unittest datamapper/tests/pipeline.py
