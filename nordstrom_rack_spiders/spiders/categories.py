import json
import math
from urllib.parse import urlparse

import requests
from requests.models import PreparedRequest
import scrapy
from bs4 import BeautifulSoup
from scrapy.exceptions import CloseSpider
from scrapy.http import Response

from proxy_manager import proxies_generator

class CategoriesSpider(scrapy.Spider):
    name = "categories"  # Spider name to run from CLI and middleware

    api_browse_path = 'https://api.nordstrom.com/polaris/v2/browse'
    default_products_limit = 100  # Cannot get more than 100 products per request

    limit_urls = None
    custom_settings = {
        'RETRY_TIMES': 3,
    }

    headers = {
                'apikey': '5uykMjAxVrk5MD7Aekgx33RPQ2wOqdM7',
                'nord-country-code': 'US',
                'nord-source-platform': 'IOS',
                'useseofriendlyfilters': 'true',
                'tracecontext': '127DCAE9-F26C-4EE8-B550-6EAA3EB1BEC5',
                'nord-source-channel': 'RACK',
                'nord-channel-brand': 'NORDSTROM_RACK',
                'authorization': f'Bearer aa45fa7f-d198-42b4-9ecd-1bb157cd5f05',
            }


    def start_requests(self):
        proxy = next(proxies_generator)
        response = requests.get('https://www.nordstromrack.com/navigation-sitemap.xml',
                                proxies={'http': proxy,
                                         'https': proxy})
        soup = BeautifulSoup(response.text, features='xml')
        all_urls = soup.find_all('loc')
        all_urls = [url.text for url in all_urls]
        all_urls = [url for url in all_urls if 'shop/' in url]

        print(len(all_urls))

        for url in all_urls[:self.limit_urls]:
            # url = 'https://www.nordstromrack.com/shop/Home/Kitchen & Tabletop/Water Bottles & Tumblers'
            search_path = urlparse(url).path.replace('/shop', '')[1:]
            category_path = search_path.split('/')
            category_path = [item.capitalize() for item in category_path]
            category_path = ' -> '.join(category_path)

            params = {
                'browsePath': search_path,
                'top': self.default_products_limit,  # Their API does not allow more than 50_000 per call.
                'skip': 0
            }
            url_schema = PreparedRequest()
            url_schema.prepare_url(self.api_browse_path, params)
            url = url_schema.url

            request = scrapy.Request(url=url,
                                     headers=self.headers,
                                     method='GET',
                                     callback=self.parse)
            request.meta['proxy'] = proxy
            request.meta['category_path'] = category_path
            request.meta['current_skip'] = 0
            request.meta['top'] = self.default_products_limit
            request.meta['browsePath'] = search_path
            request.meta['total_skips'] = 0
            request.meta['return_data'] = {'products': []}
            yield request

    def parse(self, response: Response):
        if response.status == 200:

            data = json.loads(response.text)
            current_meta = response.meta

            category_path = current_meta['category_path']
            search_path = current_meta['browsePath']
            current_skip = current_meta['current_skip']
            total_skips = current_meta['total_skips']
            return_data = current_meta['return_data']

            for product in data['products']:
                # print(product)
                product_data = {
                        'product_id': product['id'],
                        'product_image_url': product['mediaExperiences']['carouselsByColor'][0]['orderedShots'][0]['url'],
                        'product_category': response.meta['category_path']}
                yield product_data

            new_skip = current_skip + 1
            if not total_skips:
                total_items = data['totalProductCount']
                total_skips = math.ceil(total_items / self.default_products_limit - 1)
                if total_skips <= 0:
                    total_skips = - 1
                else:
                    print(f'will make {total_skips} additional requests for category {search_path}')

            if new_skip >= total_skips or total_skips < 0:
                pass

            else:
                params = {
                    'browsePath': search_path,
                    'top': self.default_products_limit,  # Their API does not allow more than 50_000 per call.
                    'skip': new_skip * self.default_products_limit
                }
                url_schema = PreparedRequest()
                url_schema.prepare_url(self.api_browse_path, params)
                url = url_schema.url
                request = scrapy.Request(url,
                                         method='GET',
                                         headers=self.headers,
                                         callback=self.parse)

                request.meta['proxy'] = next(proxies_generator)
                request.meta['category_path'] = category_path
                request.meta['current_skip'] = new_skip
                request.meta['browsePath'] = search_path
                request.meta['total_skips'] = total_skips
                request.meta['return_data'] = return_data

                yield request


    # def closed(self, reason):
    #     # will be called when the crawler process ends
    #     # any code
    #     # do something with collected data
    #     with open('category.json', 'r') as file:
    #         data = json.loads(file.read())
    #
    #     return_dict = {}
    #     for product in data:
    #         if product['product_id'] in return_dict.keys():
    #             return_dict[product['product_id']]['product_categories'].append(product['product_category'])
    #
    #         else:
    #             return_dict[product['product_id']] = {'product_categories': [product['product_category']]}
    #
    #
    #     with open('processed_items_mapping.json', 'w+') as file:
    #         file.write(json.dumps(return_dict, indent=4))