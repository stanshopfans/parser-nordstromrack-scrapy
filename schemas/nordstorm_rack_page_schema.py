import requests
from pydantic import BaseModel, validator, Field
from typing import Optional, Dict, Any, List
from .nordstrom_rack_variant_schema import NordstromRackVariantData

class NordstromRackData(BaseModel):
    api_data: dict = Field(exclude=True)
    product_api_id: str = Field(exclude=True)
    base_url: str = Field(default='https://www.nordstromrack.com/s', exclude=True)
    remote_url: Optional[str] = Field(exclude=True)

    brand: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

    data: Optional[Dict[str, Any]] = {'dataFacets': []}  # No dataFacets on the page

    categories: Optional[List[str]] = []  # No categories on the page

    gender: Optional[str] = None  # No gender on the page

    product_images: Optional[List[str]] = [None]

    market_id: Optional[int] = 22  # Hardcode
    remote_code: Optional[str] = None  # Same as product_api_id

    is_lost: Optional[int] = 0  # Hardcode

    variants: Optional[List] = None

    class Config:
        arbitrary_types_allowed = True


    @validator("brand", always=True, pre=True)
    def return_brand_name(cls, v, values) -> str:
        v = values["api_data"].get("productAttributes", {}).get("vendor", {}).get("labelName", None)
        return v

    @validator("remote_code", always=True, pre=True)
    def return_remote_code(cls, v, values):
        v = values['product_api_id']
        return v

    @validator("name", always=True, pre=True)
    def return_name(cls, v, values) -> str:
        v = values["api_data"].get("productAttributes", {}).get("name", None)
        return v

    @validator("description", always=True, pre=True)
    def return_description(cls, v, values):
        description = values["api_data"].get("productAttributes", {}).get("description", None)
        features = values["api_data"].get("productAttributes", {}).get('displayFeatures', {}).get("features", [""])
        features = "\n".join(features)
        v = description + '\n' + features
        return v

    @validator("product_images", always=True, pre=True)
    def return_images(cls, v, values):
        v = values["api_data"].get("mediaExperiences", {}).get("carouselsByColor", [])
        if v:
            v = v[0].get("orderedShots", [])
            v = [item.get("url", None) for item in v]

        return v

    @validator("remote_url", always=True, pre=True)
    def return_url(cls, v, values):
        v = values['api_data'].get('productAttributes', {}).get('webPathAlias', None)
        v = values['base_url'] + '/' + v + '/' + values['product_api_id']
        return v

    @validator('variants', always=True, pre=True)
    def return_variants(cls, v, values):
        v = NordstromRackVariantData(api_data=values['api_data'],
                                     remote_url=values['remote_url'])

        return v.items

    @validator('gender', always=True, pre=True)
    def return_gender(cls, v, values):
        v = values['api_data'].get('productAttributes', {}).get('gender', 'No gender').lower()
        return v


    def upload_to_us_mall(self):
        url = "https://app.usmall.ru/api/product-external"

        payload = {'json_data': self.json(),
                   'market_id': f'{self.market_id}',
                   'remote_code': f'{self.remote_code}'}

        headers = {
            'product-external-key': 'f5970c35eff4f296e2dfb9162df4102c'
        }

        response = requests.post(url,
                                 headers=headers,
                                 data=payload)

        print(response.text)