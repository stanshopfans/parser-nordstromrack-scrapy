# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import Response, Request

from proxy_manager import proxies_generator
from token_manager import tokens_generator


class NordstromRackSpidersSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class NordstromRackSpidersDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message


class CustomRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):

        # if request.meta.get('dont_retry', False):
        #     return response
        # if response.status in self.retry_http_codes:
        #     reason = response_status_message(response.status)
        #     return self._retry(request, reason, spider) or response

        if spider.name == 'categories':
            if response.status == 403:
                new_proxy = next(proxies_generator)
                request.meta['proxy'] = new_proxy
                print(f'changed proxy for because 403')
                return self._retry(request, "error 403", spider)
            return response

        product_api_id = request.meta['product_api_id']

        if response.status == 403:
            new_proxy = next(spider.proxies_generator)
            request.meta['proxy'] = new_proxy
            print(f'changed proxy for {product_api_id=} because 403')
            return self._retry(request, "error 403", spider)

        # this is your check
        try:
            if response.status == 429:

                new_token = next(tokens_generator)
                new_token = bytes(new_token, 'utf-8')
                new_headers = {b'x-a8s6k1ns-e': new_token}

                request.headers.update(new_headers)
                request.meta['request_count'] += 1

                print(f'changed token for {product_api_id=}')

                custom_settings = hasattr(spider, 'custom_settings')
                if custom_settings:
                    allowed_retries = spider.custom_settings.get('RETRY_TIMES', 0)
                    current_retries = request.meta.get('retry_times', 1)

                    threshold = allowed_retries / current_retries
                    if threshold < 2:
                        new_proxy = next(proxies_generator)
                        request.meta['proxy'] = new_proxy
                        print(f'changed poxy for {product_api_id=} because there was {current_retries} fails out of {allowed_retries}')
                    if current_retries >= allowed_retries:
                        print(f"too many retries with {request} for {product_api_id=}")
                        spider.failed_urls.append({"product_api_id": product_api_id,
                                                   "reason": f'too {current_retries} retries with {request} for {product_api_id=}'})
                        return Response(url=request.url, status=9999, body=b'too many retries')

                return self._retry(request, "error 429", spider)

            return response
        except Exception as e:
            print(e)
            return Response(url=request.url, status=9999, body=e)
