import json
import time

import scrapy
from requests import PreparedRequest
from scrapy.http import Response

from schemas import NordstromRackData
from token_manager import tokens_generator
from proxy_manager import proxies_generator

class ProductsSpider(scrapy.Spider):
    # https://stackoverflow.com/questions/41404281/how-to-retry-the-request-n-times-when-an-item-gets-an-empty-field
    # https://github.com/aivarsk/scrapy-proxies
    # https://github.com/TeamHG-Memex/scrapy-rotating-proxies
    # https://stackoverflow.com/questions/13724730/how-to-get-the-scrapy-failure-urls
    name = "products"

    api_product_offer_url = "https://api.nordstrom.com/offer"
    limit_urls = 1


    handle_httpstatus_list = [429, 9999]
    failed_urls = []
    time_start = time.time()

    custom_settings = {
        'RETRY_TIMES': 20,
    }

    def start_requests(self):
        with open('category.json', 'r') as file:
            data = json.loads(file.read())

        return_dict = {}
        for product in data:
            if product['product_id'] in return_dict.keys():
                return_dict[product['product_id']]['product_categories'].append(product['product_category'])

            else:
                return_dict[product['product_id']] = {'product_categories': [product['product_category']]}

        for index, (product_api_id, values) in enumerate(return_dict.items()):

            if index == self.limit_urls:
                break

            token = next(tokens_generator)
            headers = {
                'user-agent': f'device=iPhone10,2;deviceType=iPhone;os=iOS;osVersion=16.0.3;appVersion=9.16;carrier=None;appName=rack-ios',
                'x-a8s6k1ns-e': token,
                'nord-client-id': 'APP01031',
                'nord-channel-brand': 'NORDSTROM_RACK',
                'accept': 'application/vnd.offer.v1+json',
            }
            params = {
                'apikey': 'kHeUEacPjrHY8SZXnLC8qGYSPXK0XJX5',
            }
            url = f'{self.api_product_offer_url}/{product_api_id}'
            url_schema = PreparedRequest()
            url_schema.prepare_url(url, params)
            url = url_schema.url

            request = scrapy.Request(url=url,
                                     method='GET',
                                     headers=headers,
                                     callback=self.parse)

            proxy = next(proxies_generator)
            request.meta['proxy'] = proxy
            request.meta['request_count'] = 1
            request.meta['product_api_id'] = product_api_id
            request.meta['categories'] = values['product_categories']

            # print(request.__dict__)
            print(url)
            yield request

    def parse(self, response: Response):
        # print(response.meta)
        if response.status == 200:
            data = json.loads(response.text)
            current_meta = response.meta


            data = NordstromRackData(api_data=data,
                                     product_api_id=current_meta['product_api_id'],
                                     categories=current_meta['categories'])
            yield {'product_id': response.meta['product_api_id'],
                   'retries': response.meta.get('retry_times', 0),
                   'data': data.dict()}

        else:
            print("weird error")

    def closed(self, reason):
        # will be called when the crawler process ends
        # any code
        # do something with collected data

        time_end = time.time()

        with open('logs.json', 'w+') as file:
            data = {'total_time': time_end - self.time_start,
                    'failed_urls': self.failed_urls}
            file.write(json.dumps(data, indent=4))