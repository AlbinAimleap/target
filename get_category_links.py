import json
import logging
from functools import lru_cache
from config import Config
from pathlib import Path
import secrets
import json
from fetch import fetch

def generate_random_hex(length=32):
    return secrets.token_hex(length // 2)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@lru_cache
async def get_categories(session):
    logger.info("Fetching categories")
    all_categories = []
    for category_main, idx in Config.MAIN_CATEGORIES:
        categories_list = await fetch_category_data(session, idx)
        if categories_list:
            logger.info(f"Found {len(categories_list)} categories")
            all_categories.append({"category": category_main, "links": categories_list})
    return all_categories

async def fetch_category_data(session, idx):
    try:
        visiter_id = generate_random_hex()
        url = f"https://redsky.target.com/redsky_aggregations/v1/web/taxonomy_subcategories_v1?category_id={idx}&key=9f36aeafbe60771e321a7cc95a78140772ab3e96&visitor_id={visiter_id}&channel=WEB&page=%2Fc%2F5xt1a"
        category = await fetch(session, url)
        data = category['data']['related_categories']['children']
        return [
            {
                "canonical_url": item.get('canonical_url'),
                "name": item.get('name'),
                "category_id": item.get('category_id'),
                "parent_category_id": item.get('parent_category_id'),
                "image_url": item.get('image_url'),
                "deep_link": item.get('deep_link'),
                "visibility": item.get('visibility')
            }
            for item in data
        ]
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return []
        
    with open("categories.json", "w") as f:
            json.dump(all_categories, f, indent=4)


def load_categories(categories, keys):
    filepath = Path(__file__).parent / "categories.json"
    with open(filepath, "r") as f:
        data = json.load(f)
    
    items = []
    keys_set = set(keys)
    
    if categories == ["*"] or categories == ["__all__"]:
        for item in data:
            items.extend(
                {key: link[key] for key in keys_set if key in link}
                for link in item["links"]
                if any(key in link for key in keys_set)
            )
    else:
        category_set = set(categories)
        for item in data:
            if item["category"] in category_set:
                items.extend(
                    {key: link[key] for key in keys_set if key in link}
                    for link in item["links"]
                    if any(key in link for key in keys_set)
                )
    
    return items


if __name__ == "__main__":
    get_categories()
