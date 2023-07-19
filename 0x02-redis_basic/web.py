import requests
import redis
import time
# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def get_page(url: str) -> str:
    # Check if the URL content is cached
    cached_content = redis_client.get(f"content:{url}")
    if cached_content:
        return cached_content.decode('utf-8')

    # Fetch the content from the URL
    response = requests.get(url)
    content = response.text

    # Cache the content with a 10-second expiration time
    redis_client.setex(f"content:{url}", 10, content)

    # Track the access count of the URL
    access_count = redis_client.incr(f"count:{url}")

    print(f"Accessed {url} {access_count} time(s)")

    return content


# Test the function
if __name__ == "__main__":
    url = "http://slowwly.robertomurray" \
          ".co.uk/delay/5000/url/https://www.example.com"
    content = get_page(url)
    print(content)
