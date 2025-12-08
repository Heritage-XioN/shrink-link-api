import hashlib

# class for creating the url hash
class Shortener:
    @staticmethod
    def shorten_url(original_url: str) -> str:
        """Generate a short URL hash from the original URL."""
        hash_object = hashlib.sha256(original_url.encode())
        short_url = hash_object.hexdigest()[:6]  # Use first 6 characters of the hash
        return short_url
    
    @staticmethod
    def resolve_collision(original_url: str, collision_count: int) -> str:
        """
        Generates a new, unique 6-character hash by salting the original URL 
        with the collision count (or attempt number).
        
        Args:
            original_url: The URL that caused the initial collision.
            collision_count: A unique number representing the attempt count (e.g., 1, 2, 3...).
            
        Returns:
            A new 6-character hash.
        """
        # 1. Combine the original URL with the unique count (salt)
        # We convert the count to a string and append it.
        salted_data = f"{original_url}{collision_count}"
        
        # 2. Hash the salted data
        hash_object = hashlib.sha256(salted_data.encode())
        
        # 3. Truncate and return the new hash
        new_short_url = hash_object.hexdigest()[:6]
        return new_short_url
    
url_shortener = Shortener()