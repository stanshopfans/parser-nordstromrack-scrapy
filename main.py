import json

from scrapy import cmdline
from settings import settings
from scrapy.crawler import CrawlerProcess

from nordstrom_rack_spiders.spiders.products import ProductsSpider

process = CrawlerProcess()
process.crawl(ProductsSpider, mode=settings.mode, filename=settings.filename)
process.start()

# cmdline.execute(f"scrapy crawl products -a mode={settings.mode} -a filename={settings.filename}".split())


for i in range(5):
    print('here')
    with open('logs.json', 'r') as file:
        data = json.loads(file.read())

    if len(data['failed_urls']) > 0:
        cmdline.execute(f"scrapy crawl products -a mode={settings.mode} -a filename={settings.filename}".split())
    else:
        print('no cleanup needed')