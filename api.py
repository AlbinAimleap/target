import logging
from pathlib import Path
from config import Config
from datetime import datetime
from aiohttp import ClientSession
import pandas as pd
import re
from fetch import fetch
import json


logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def get_products_data(session, category):
    logger.info(f"Fetching products data for category ID: {category['category_id']}")
    params = {
        'key': '9f36aeafbe60771e321a7cc95a78140772ab3e96',
        'category': f"{category['category_id']}",
        'channel': 'WEB',
        'count': '24',
        'default_purchasability_filter': 'true',
        'include_dmc_dmr': 'true',
        'include_sponsored': 'true',
        'new_search': 'false',
        'offset': '0',
        'page': f"/c/{category['category_id']}",
        'platform': 'desktop',
        'pricing_store_id': '1896',
        'scheduled_delivery_store_id': '1896',
        'spellcheck': 'true',
        'store_ids': '1896,834,1323,1950,2122',
        'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'visitor_id': '018F0EACB087020191D886786AE7A2E7',
        'zip': '60177',
    }
    
    url = 'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2'
    response = await fetch(session, url, params)
    response.update(category)
    return response

async def get_promo(session, tcin):
    params = {
        'pricing_store_id': '1896',
        'tcin': f'{tcin}',
        'key': '9f36aeafbe60771e321a7cc95a78140772ab3e96',
        'visitor_id': Config.VISITORS_ID,
        'has_size_context': 'true',
        'channel': 'WEB',
        'page': f'/p/A-{tcin}',
    }
    url = 'https://redsky.target.com/redsky_aggregations/v1/web/pdp_personalized_v1'
    try:
        response = await fetch(session, url, params)
        if not response['data']['product']['promotions']:
            return None, None, None
        promotion = response['data']['product']['promotions'][0]
        threshold_value = promotion.get('threshold_value')
        reward_type = promotion['reward_type']
        pdp_message = promotion['pdp_message']
        return threshold_value, reward_type, pdp_message
    except Exception as e:
        logger.error(f"Error fetching promo for tcin {tcin}: {e}")
        return None, None, None
    
def find_matches_reverse(text):
    items_to_check = ['crv', 'oz', 'fz', 'count', 'ounce', 'fl',
                  'gallon', 'ct', 'lb', 'liter', 'lt', 'pound', 'kg', 'ml']

    items_to_check = [item[::-1] for item in items_to_check]
    pattern = r'(' + '|'.join(re.escape(item) for item in items_to_check) + r')\s*(\d+(?:\.\d+)?)'
    reversed_text = text[::-1]
    matches = re.findall(pattern, reversed_text, re.IGNORECASE)
    return matches

async def process_products(session, response):
    logger.info("Processing products data")
    products = []
    for pr in response['data']['search']['products']:
        product_title = pr['item']['product_description']['title']
        regular_price = pr.get('price', {}).get('reg_retail')
        sale_price = pr.get('price', {}).get('current_retail')
        
        if not regular_price:
            with open('missing_regular_price.txt', 'a') as file:
                file.write(f"{json.dumps(response['data']['search']['products'], indent=4)}\n")
            continue

        image_url = pr.get('item', {}).get('enrichment', {}).get('images', {}).get('primary_image_url')
        product_url = pr.get('item', {}).get('enrichment', {}).get('buy_url')
        
        if regular_price == sale_price:
            sale_price = ''
        
        net_weight = ''
        weight = pr.get('product_description', {}).get('bullet_descriptions', [])
        for description in weight:
            if 'Net weight:' in description:
                net_weight = description.split(':')[1].strip()
                break
            else:
                net_weight = ''  

        if net_weight == '':
            matched_items = find_matches_reverse(product_title)
            if matched_items:
                for match in matched_items:
                    try:
                        net_weight = match[1][::-1] + ' ' + match[0][::-1]
                    except:
                        pass
        tcin = product_url.split('-')[-1]
        
        threshold_value, reward_type, pdp_message = await get_promo(session, tcin)
        today = datetime.today().date()            
        formatted_today = today.strftime('%Y-%m-%d')
        products.append({
            'zipcode': Config.ZIPCODE,
            'store_name': Config.STORE_NAME,
            'store_location': Config.STORE_LOCATION,
            'store_logo': Config.STORE_LOGO,
            'url': product_url,
            'category': response['parent_category_id'],
            'sub_category': response['category_id'],
            'product_title': product_title,
            'weight': net_weight,
            'regular_price': regular_price,
            'sale_price': sale_price,
            'volume_deals_description': pdp_message or "",
            'image_url': image_url,
            'digital_coupon_description': '',
            'digital_coupon_price': '',
            'upc': tcin,
            "crawl_date": formatted_today}
        )
    
    logger.info(f"Processed {len(products)} products")
    return products

async def save_to_csv(products):
    if not products:
        logger.warning("No products to save.")
        return

    df = pd.DataFrame(products)
    cur_dir = Path(__file__).parent.resolve()
    filename = cur_dir / Path(f"products_{datetime.now().strftime('%d-%m-%Y')}.csv")
    
    try:
        df.to_csv(filename, mode='a', header=not filename.exists(), index=False)
        logger.info(f"Saved {len(products)} products to {filename}")
    except IOError as e:
        logger.error(f"Error saving products to CSV: {e}")
    except Exception as e:
        logger.error(f"Unexpected error while saving products to CSV: {e}")
