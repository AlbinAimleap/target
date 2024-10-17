import logging
import aiohttp
import asyncio
import concurrent.futures
from functools import partial

from get_category_links import get_categories, load_categories
from api import get_products_data, process_products, save_to_csv
from promo_validator import PromoProcessor

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



async def process_category(session, category):
    logger.info(f"Processing category: {category['name']} (ID: {category['category_id']})")
    try:
        async with asyncio.timeout(60):
            result = await get_products_data(session, category)
            products = await process_products(session, result)
            promo_validator = PromoProcessor()
            processed_products = [i for i in promo_validator.process(products) if i is not None and i["volume_deals_description"]]
            await save_to_csv(processed_products)
    except asyncio.TimeoutError:
        logger.error(f"Timeout processing category {category['name']}")
    except Exception as e:
        logger.error(f"Error processing category {category['name']}: {e}")

async def main(reload_categories=False):
    logger.info("Starting main function")
   
    async with aiohttp.ClientSession() as session:
        if reload_categories:
            await get_categories(session)
        CATEGORIES = ["grocery"]
        KEYS = ["name", "category_id", "parent_category_id"]
        categories = load_categories(CATEGORIES, KEYS)
        tasks = [process_category(session, category) for category in categories]
        await asyncio.gather(*tasks)
    
    logger.info("All categories processed and saved to CSV")

if __name__ == "__main__":
    logger.info("Script started")
    asyncio.run(main())
    logger.info("Script completed")