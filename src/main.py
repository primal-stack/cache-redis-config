import os
import yaml
from cachetools import TTLCache
from redis import Redis
from dotenv import load_dotenv

load_dotenv()

CACHE_EXPIRATION = int(os.getenv('CACHE_EXPIRATION', 300))  # default expiration in seconds

def create_redis_client():
    return Redis.from_url(os.getenv('REDIS_URL'))

def create_cache():
    return TTLCache(maxsize=100, ttl=CACHE_EXPIRATION)

def main():
    redis_client = create_redis_client()
    cache = create_cache()

    # Initialize cache with Redis data
    for key, value in redis_client.scan_iter(match='*'):
        cache[key] = value

    # Example usage
    cache['example_key'] = 'example_value'

    # Accessing cached value
    print(cache.get('example_key'))

if __name__ == '__main__':
    main()