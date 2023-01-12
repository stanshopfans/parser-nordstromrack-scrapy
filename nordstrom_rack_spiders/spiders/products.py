import json
import random
import time

import scrapy
import pickle

with open('complete_items_mapping_len_66675.pickle', 'rb') as file:
    mapping = pickle.load(file)

tokens = [
    # original
    'b;fpfaG45E3eCbjjpuGTx7XDk7kbfz8IGAHk_dFKZrhPooOxr_jC8QWkQ5kiaKKIxSpWZse6I7Ad4oWM0pSKS64IjW0bTbWf3w2_Z5rMnH6rSqvsbdMr73qofXKvdarO855YVDNHTPKdmOKWdGeLCnotT9XkbpSCnnRzOd1kM4DU9MdHQwIDaHsAGGIjCT4Jh1L9xppDrI--DQgJtmALqfooH0SpFsjHfprZPp_voNp4sZ-GQEMuX3GiIWhisIfR0Mh463AKIrCVwMXcTD9GEoeSXyHb-rSZFxmiU4vSdXSbotGhd7M1FPSXr8k-cx1zes9asksG96stofVgjXblnbhRxs4kPPRUIH-B19UBNQPfVEfFwxqyUf_LRyHkRqLqs1qCCQlsYjPrWYlRcBP5cWOm8a4FarPtQN8ThcDcXfb9vvyJWKRy_TSkjI0dPiw-619KlIAWKoDW7sFgfanse1L-DEW3zxtFbrcyPKAhxlMhQPy4qE2RnbqmnbPA0iHbS3Z_wENuhoZzPisFm3xxWwBiSuFXDLjzIjHM6dqS6--ChULT3jh7Fi9RG-h8BT5YNfM4UpzyeVbu9FsmK4_A7qn2enUJlcS6k-DxiicnFccyBwIYk4CZRs0hPTZQ9AQ86AMZoUg_pcAqXKoRc6Rlz0a9qp8m7-d-3-DaCqxXIfRap5zSupZt2TtfDmI4Tgpuje7MPiJCf8pg6rJeCUeb3MTHN5MDOYUDS80CUz_mT7VmKLsB2m55_bmtFkXgUxStfjEYCAZY7CdLsLfKu37YLQmaGZWndQEfp6I5_pK80GZbyEofwBd2n44uFzXEIzLAmiDk2dN9-d_T0vp2v9POw=;F2CbiCsyJbTNiSgUQjIlnMraGvQLmy8_qAYqb-V3-Kc=',
    # muslim
    'b;BrPDXwV-4ayyXxhFJabeFJnorU7f9xMOFuqxCUAojXVEqg0cSktaK7WDsl_fZnjsUUYCaTL3l74IL-r9w5zd96O8qpi4MUJGp9m7_pmM5_BltbCqjh5VDdZqFTJA86CzofQojR9vq-kW9YRPiD8CU7qTLHpDjpyiu6vdf0idzMuSbql2JkqV1v766HMjxdJ2tXkoaM89ILQNw8bFUU08y_AyRadTlmZQ2KYDJIjVS_Iva_BJFE_woQ69M5Sk-v74FhC4bQ94BsupK5SRiOtpQL0jP33KfYDR0VROfFugarUS_VBL8zkQvpopo0ygyq6bsEDvvfG3tm-fT6nTk9DeJHmrAe0Z4A9xOBmsdh-JFtsVUEeeUQ5RVTyxGoamj8TjSQ_1v1CSZGexThBgIz3kfhxrWLagiLReK84Wd3IBPar-tYlMkx69Gk_ZzomOWftMI7pmLclChECygmQrSbVabJMGQMiStQCw7nl2ijMf6urfn_RjQG1YbbJ8y4J7YK03VItjJHiAZSdx9Olv3RcnTmJpeCIUi1WVo4k9fhHrFHyB1e5F7vwGqeVQGsTLfUZDchkrmYVoxckxaHhhFAIwIqAUoyeDaamGOmiVVw6paVsLt0y5Ff6yTzHsEkZBd4YpTC9AJFgfxIgUgC9NWhOVIeQJWMOKOZ1Dq0wNpZFh9ZssmcBliNy-mwppsQAuy2PzKdRKyb1qvyvenqmdZbFEs_AM3MxbuGKfOt6GDoC5PHkv0izN34U6prUnhkssth2Fw30WmlNv-nPJwJGtni56IyZVFUAbjWZ9V5-iFLhxr4ECfzBc3gKzPnot2y0sNk4QXa0fiLIUc7dubFA=;CVz9E5xSg0tn2USNfRWbY2jzhKmfJW2w0DJnEz9-PZ8=',
    # backup
    'b;aRUJloin7bJuh2E08mAtih8pGfCpe6fBbzODQBtPR9qgjY6K2E_OdqTVdxjlpHH-m2UIQy-lvqswUUS3ohR4PjgS0db-Lie9D2FDKcoyFbjiNIB-uSfRDWORwootYI0oKDfvDkMk0WIleWS51St39kxx45q24a0EMPwzZfADX6DrDEPSmrOpBS5jsn8cpFB0eCyNO9y6Ww209WYZg3QIKfMQIXDchpCuyYgHkGgjG6r5mACKxm7EpTZYpYZ_7zk8J0V1MpN4NF7lfyBsDJY3-uUuJhW84HyUGNKwseTRyGvhFnMyBHx9H1FUlcu4xS9gRHD_zGFuu0XgLPgzs-e9dtKSpk9kBC_sr4NJKobLddEy_8eoRR4nHlVKe2tXeqSlz0Smg-84hVq41xnJVIlqoOkrQRA43bN3Q1a-0xb4CG84a2j7aKWFx5EzKvIO_j9vSQZR7dWG_pph_F1y9n9iwBy0uM1_DPIGSxopjIct9wpYEdVFfQPNRZ30--vHVqK1ZJ5zIwjJOEBVZ2F1iPeDiFxvKmXtcoOys42O-qJ4Xka1OyG8b9jfwQ1xNWT4RLVsCxC-ks3dNy2igjqEhbssc8rajpYSFhk7eaSJFZYzu3EFopzvFoiF3KNlP02Ca4y3dx6zK4TcTtTUaFRV60ZZpIAyGU20pJdkq_pnr_COgJeUsXBhRKcBnrxOe9uF_ZqhEeKtL7pZYDVoTUClqqTVDBWI8x2rRCZI4FjOpesFPLbsU1oY--y7AL6xC6ZCAV8ADVXVvJGFYJOAJxPt-sXC_ueGJ03WWaL36EV278rHb2jrBvdmtYcotW8C9YF3FvtjJoNWCmCHIY7w-kw=;eGhzL1-EWmSE09ne5OX00c4dhC3tH89LkShDE4ZV11Y=',
    'b;N1HiMiZFogu6Tdy8g7NSmJucqWqkI_QoaNj8D6B8EpahC9RTChDqGBrsPBGlbKBbHioEML0MyIc3YMbGQXIUJgfk2YCx9naO7m2MQD2A2gTfdz88B3-PW8pxMBvxIl0MKmY-LdqxL0TjPmX9EflmDMuFhTcKnAsskbyysAMKItoDjDT6hy4wB5U9Ik8pTf2jjJH1mP3hx02VA4j6TWqnPGIt3KhRM-Epe0NgTT05TLEAZTjTpBPbIMVBRvAaORqfJOG8MPKAEcGsbcXUdr25XTKAxsgeRJ1VG1afYm1soo4kP05N1-ZPDi9Y5MFU-M_dwimRFdiX0kjSxxcj7enABECEj4Qlp-FNeW4WNBa96ioU7AhS7IZKuDIKjl3hWdveiJMlOpoVEANVNeRLGinw-kqiPfVve-dIJNU-o5-Y31A7fxxmeFX2osRH12fGU4JXNCJblmWHibdwfmbWtQ1avIdpJyqJFwRSCzDe8sV-YLK5NUN4BiNeQFtGFdfAHjVrtKisoAuCYptKvBo8mJzjUY2Dma2KRA8RxgwaEZijmEuv6-ajWI1akCQ-HlJTUX8RA-fZtLJyfg1-3WiHRO_zPjxHe3LUxMgJ5OP6D9QACLdYXNyPcoI2xsqYnqLk89rektYXVYrMV_OUnE1L5HcAi6LqjdzFkFnzn9Nf5xhZIoIPa9Cn7u-j7Ut8Ec1AEiizsay0WkYEkNYgieDYkjf7Nsx0Nv--s5HhTmojZ1RtTVm8EqrhrQ_NAOTSpoZ_NHxpHqPINikxjDmTeD13AU1Z60anWiIjC1rFPcczoaDIpBWUimElDzZQMn2xYG1-3KW0TL-58OGvv6chcRot;_Gpb7H074ptN2RdkDOVaR0kUz4vXGG_ObGtw2aLl5rk=',
    'b;ZN-7pGolujjLhGQF0C5DvRmsDAgMNXPwgYIc3xMSKHViItYLtTUtFzDVYSSCoulpjOvd1YDKg0tYCFXT85h9pdE0iZM9jors7lwLl6W9Q4S85qMUkXz1ASXYdZPyqGpqH-uLLBJNL8c1vo8MQTp6OYRuIH-ELvCkVdRrSuvW9A-jnno3BIhyfmxXa7-kMxBLALjWanLcfGVmDZnax6VV29a-31eUtI8mQYBwg6u36RnxbPAyjjE-36Xig_Lefkh5Ls-pLM9goYJiRA39t6EF77NIJuWTZ4IEIrwpeBq7YG3qpFUm7EdRB1eLmteFE1e_H6RtV_Td0LUSq1DvM8px0-3YbkohKd4kk-0FPDTwvT9tTh4dtlgHuwIQzRn_eyTML6Agoh-4FUwcbK93TGjeLU6p7SidmbyzlNpIGzDQ2zv5fnAchHfzN7yTy9H9s_PxCPEJ5n4unPhGVMR-tBlFkjTv13-f2yJGe7Pg_KS7Eqe222wQFYT4rh9MrPgwb3NfdjLmoQmX-jP-OaxkVBBf3A7oH9FYnrbNFmjd16m2a-r071ROWANAKsmvarWQp1O3wxqLf8y51Mt6epYey7CfVStSzD-5tw2dB_vhAArtuGMvzLRLwDDz8umPK8RNwlxjnCwyqOI1d0fGwHKwxWz1j2-6lVF9PvbG1N-Wxg_5MLnOuKB5SBp_1DSNEHDwSTMuk9_Xz32LIvAohzTyLiH72N9HwkGiPWc6ZgGYzGrf6Dt3RhT-CoBNFYkQAH62sMG6tqVWl0mvfMiUWRZCmCnBZiAJ4smjY60KAJnkXOR7rgpaFL2P7rN4gSl2LfmAWgL19xjiHmEbMK1Wneau;w34m9A9gxQZQ2ZlfZ7KSxBo04P2GT42wKyn-CwMZWFI=',
    # 'b;5lJzKflAGsk_OuPD4CDRtqMz9mgBZsOeD-IK54J03RQSFeKwSmm5-cPLjrb9-V2jOCyWz1WkCEPAAOSRUEhPJdg7z5lqBPyRtxlJJWlHqPy9gtr49PKBxPUO4V-GquJDVUqqDeVrm_YDWe_1I8gltbw4RT9yS98I2Rqovjvzn8ARL9Og3k7wJZPeyPKlE1-_oLu-Ux7crRr-3BNN7RK9QOTZab8U1gB6Vz8vljnV8xN2g-LGf7TbdfoOdsne9hxfpsa3QG43R7_HzuPRcyMFe-MjQIaM82Zc-qojCOW5gTENWoqqgUHP7huAHMVSvpinL_nRvqXZ39mmf_ieVomgv4Ycjsom61FuR243qHw0fqSemy8g84dTMLcm67KS_fgHdMf0RhnLXHOtXu_KVnm6Seiu6cS3siuVX76Wj2EVwhe0l5a7WJg6dnHq6A5ZFkrKOMBLylD6x9A-Uu0Z3Ld_jO3d6iwCcLLBl7l4MSqxqF8mcXI4J4jMU8T7Gn_cl2Zl19mt9JnxvfOxC99zjKnzB2oC5a64WSigbWVtTFzZPzW2kFNjcJz3pIHE3Hf3PBOFRMwIGAqAPqLKX6pqUxQoj2SfjjxOEamxK5CWGZmmO2foNtwFGSYldl2N67KffnQHsSwnfqW6H6QwgoTezG7nvaSmwgG1pYMJoJ8n_1a3LJsNcOG_N4SuhfAf3mUi1pQdMWXUFoLnM1DTDB1PWVwPHKQWD3PrBkz61RYTDvx45wMvQqcMSCKX7wVXe49e6sJ-SQ_FQdJjrAzGGk4CJbzIjg5rNyM7sMPz6FSC5_r2p5vuaAEKpStsEwHaczPMhSm0reKNK56HcNfu9Q0=;qQ4bg7uQyU1zy1tPKG7x5cs596KWYqaKlYlAcM9akjI=',
]

with open('Webshare 1000 proxies.txt', 'r') as file:
    lines = file.read().split('\n')


def convert_line(line):
    auth = line.split(':')[-2:]
    auth = ":".join(auth)
    host_port = line.split(':')[0:2]
    host_port = ":".join(host_port)

    return f'http://{auth}@{host_port}'


proxies = list(map(convert_line, lines))

urls = []
i = 0
for product_id, atr in mapping.items():
    # if i == 10:
    #     break
    urls.append(product_id)
    # i += 1


class ProductsSpider(scrapy.Spider):
    # https://stackoverflow.com/questions/41404281/how-to-retry-the-request-n-times-when-an-item-gets-an-empty-field
    # https://github.com/aivarsk/scrapy-proxies
    # https://github.com/TeamHG-Memex/scrapy-rotating-proxies
    # https://stackoverflow.com/questions/13724730/how-to-get-the-scrapy-failure-urls
    name = "products"
    handle_httpstatus_list = [429, 9999]

    failed_urls = []
    time_start = time.time()

    @staticmethod
    def make_tokens_generator():
        while True:
            for token in tokens:
                yield token

    @staticmethod
    def make_proxy_generator():
        with open('Webshare 1000 proxies.txt', 'r') as file:
            lines = file.read().split('\n')

        def convert_line(line):
            auth = line.split(':')[-2:]
            auth = ":".join(auth)
            host_port = line.split(':')[0:2]
            host_port = ":".join(host_port)

            return f'http://{auth}@{host_port}'

        proxies = list(map(convert_line, lines))
        while True:
            for proxy in proxies:
                yield proxy

    proxies_generator = make_proxy_generator()
    tokens_generator = make_tokens_generator()

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     proxies_generator = self.make_proxy_generator

    custom_settings = {
        'RETRY_TIMES': 20,
    }

    def start_requests(self):

        for product_api_id in urls:
            proxy = next(self.proxies_generator)
            token = next(self.tokens_generator)
            headers = {
                'user-agent': f'device=iPhone10,2;deviceType=iPhone;os=iOS;osVersion=16.0.3;appVersion=9.16;carrier=None;appName=rack-ios',
                'x-a8s6k1ns-e': token,
                'nord-client-id': 'APP01031',
                'nord-channel-brand': 'NORDSTROM_RACK',
                #     'authorization': 'Bearer 5UZHLO4JiVmB8G2WvhHnCRkPFAJUPMBD',
                'accept': 'application/vnd.offer.v1+json',
            }
            params = {
                'apikey': 'kHeUEacPjrHY8SZXnLC8qGYSPXK0XJX5',
            }

            url = f'https://api.nordstrom.com/offer/{product_api_id}?apikey=kHeUEacPjrHY8SZXnLC8qGYSPXK0XJX5'

            request = scrapy.Request(url=url,
                                     method='GET',
                                     headers=headers,
                                     callback=self.parse)
            request.meta['proxy'] = proxy
            request.meta['request_count'] = 1
            request.meta['product_api_id'] = product_api_id
            yield request

    def parse(self, response):
        # print(response.meta)
        if response.status == 200:
            yield {'product_id': response.meta['product_api_id'],
                   'retries': response.meta.get('retry_times', 0),
                   'text': response.text[:10]}

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