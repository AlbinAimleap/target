import aiohttp
import asyncio
import logging
from functools import lru_cache
from pathlib import Path
from config import Config
import random
import json
from datetime import datetime
from aiohttp import ClientSession, ClientResponseError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=4, max=60),
    retry=retry_if_exception_type(ClientResponseError)
)
async def fetch(session, url, params=None):
    try:
        async with session.get(
            url=url,
            headers=Config.HEADERS,
            params=params or {},
            proxy=Config.PROXIES.get('http') if Config.PROXIES else None
        ) as response:
            response.raise_for_status()
            logger.info(f"Successfully fetched data from URL: {url}")
            return await response.json()
    except ClientResponseError as e:
        logger.error(f"ClientResponseError occurred: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise