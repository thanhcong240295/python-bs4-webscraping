from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)

def get_domain(url: str) -> str:
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'
