import hashlib

class Shortener:
    @staticmethod
    def shorten_url(original_url: str) -> str:
        """Generate a short URL hash from the original URL."""
        hash_object = hashlib.sha256(original_url.encode())
        short_url = hash_object.hexdigest()[:6]  # Use first 6 characters of the hash
        return short_url
    
url_shortener = Shortener()