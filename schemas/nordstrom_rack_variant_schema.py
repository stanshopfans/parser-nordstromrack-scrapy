from pydantic import BaseModel, validator, Field, root_validator
from typing import Optional, Dict, Any, List

class NordstromRackVariantData(BaseModel):
    api_data: dict = Field(exclude=True)
    remote_url: str = Field(exclude=True)
    items: Optional[List] = None

    @root_validator
    def return_items_list(cls, values):
        list_of_items = []
        for item in values['api_data']['skus']:
            is_available = item['sellingControls'][0]['availability']['isAvailable']
            is_online_purchasable = item['sellingControls'][0]['productAttributes']['isOnlinePurchasable']
            if not is_available or not is_online_purchasable:
                continue
            stock_count = item['sellingControls'][0]['availability']['quantity']

            price_section = item['sellingControls'][0]['price']
            price_type = price_section['currentPriceType'].lower()

            price = price_section[price_type]['price']['units'] + price_section[price_type]['price'][
                'nanos'] / 1_000_000_000
            price_full = price_section['compareAt']['price']['units'] + price_section['compareAt']['price'][
                'nanos'] / 1_000_000_000

            origin_color = item['productAttributes']['color']['name']
            colour_code = item['productAttributes']['color']['code']
            size = item['productAttributes']['size']['name']
            remote_url = f"{values['remote_url']}?color={origin_color}&size={size}"

            variant_images = values['api_data']['mediaExperiences']['carouselsByColor']
            variant_images = [item.get("orderedShots", [[]])
                              for item
                              in variant_images
                              if item.get('colorCode') == colour_code][0]
            variant_images = [item.get('url', None) for item in variant_images]

            remote_code = item['ids']['rmsSku']['id']
            upc = ""
            image_url = variant_images[0]
            description = f'Color: {origin_color}; Size: {size}'
            data = ['transfer']

            return_dict = dict()
            return_dict["remote_code"] = remote_code
            return_dict["upc"] = upc
            return_dict['remote_url'] = remote_url
            return_dict['image_url'] = image_url
            return_dict['description'] = description
            return_dict['origin_color'] = origin_color
            return_dict['colors'] = ''
            return_dict['size'] = size
            return_dict['price'] = str(price)
            return_dict['price_full'] = price_full
            return_dict['stock_count'] = stock_count
            return_dict['variant_images'] = variant_images
            return_dict['data'] = data
            list_of_items.append(return_dict)

        for index, product in enumerate(list_of_items):
            item_size = product['size']
            all_colours = [item['origin_color'] for item in list_of_items if item['size'] == item_size]
            list_of_items[index]['colors'] = all_colours

        values['items'] = list_of_items
        return values

