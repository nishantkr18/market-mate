from flask import request, jsonify
from functools import wraps
import time
from enum import Enum
from typing import Callable, Dict, Any

class UserTier(Enum):
    """Enumeration for different user tiers."""
    FREE = "Free"
    TIER_1 = "Tier-1"
    TIER_2 = "Tier-2"
    TIER_3 = "Tier-3"


# Example rate limit configuration
RATE_LIMITS: Dict[UserTier, Dict[str, int]] = {
    UserTier.FREE: {"RPM": 3, "RPD": 200, "TPM": 40000, "TPD": 1000000},
    UserTier.TIER_1: {"RPM": 500, "RPD": 10000, "TPM": 200000, "TPD": 5000000},
    UserTier.TIER_2: {"RPM": 5000, "RPD": 100000, "TPM": 2000000, "TPD": 50000000},
    UserTier.TIER_3: {"RPM": 50000, "RPD": 1000000, "TPM": 20000000, "TPD": 500000000},
}

# In-memory store for rate limit tracking (consider using a persistent store like Redis)
rate_limit_store: Dict[str, Dict[str, Dict[str, Any]]] = {}


def get_user_tier(user_id: str) -> UserTier:
    """
    Retrieve the user tier for a given user ID.

    Args:
        user_id (str): The unique identifier for the user.

    Returns:
        UserTier: The tier of the user.
    """
    # Placeholder function to get user tier
    # Replace with actual logic to fetch user tier from database
    return UserTier.FREE


def check_rate_limit(user_id: str, limit_type: str, increment_count: int) -> bool:
    """
    Check and update the rate limit for a user.

    Args:
        user_id (str): The unique identifier for the user.
        limit_type (str): The type of limit to check (e.g., "RPM", "RPD").
        increment_count (int): The number to increment the count by.

    Returns:
        bool: True if the rate limit is not exceeded, False otherwise.
    """
    current_time = time.time()
    user_limits = rate_limit_store.get(user_id, {})
    limit_info = user_limits.get(
        limit_type, {"count": 0, "timestamp": current_time})

    # Calculate time difference
    time_diff = current_time - limit_info["timestamp"]

    # Reset count if time window has passed
    if time_diff > 60 and limit_type.endswith("PM"):  # Per minute
        limit_info["count"] = 0
        limit_info["timestamp"] = current_time
    elif time_diff > 86400 and limit_type.endswith("PD"):  # Per day
        limit_info["count"] = 0
        limit_info["timestamp"] = current_time

    # Check if limit is exceeded
    if limit_info["count"] >= RATE_LIMITS[get_user_tier(user_id)][limit_type]:
        return False

    # Update count
    limit_info["count"] += increment_count
    user_limits[limit_type] = limit_info
    rate_limit_store[user_id] = user_limits
    return True


def request_rate_limit() -> Callable:
    """
    Decorator to enforce rate limiting on a Flask route.

    Returns:
        Callable: The decorated function with rate limiting applied.
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args: Any, **kwargs: Any) -> Any:
            user_id = kwargs.get("user_id")
            if not user_id:
                return jsonify({"error": "User ID is required"}), 400

            for limit_type in ["RPM", "RPD", "TPM", "TPD"]:
                increment_value = 1 if limit_type.startswith("R") else 0
                if not check_rate_limit(user_id, limit_type, increment_count=increment_value):
                    error_messages = {
                        "RPM": "You have reached the maximum number of requests per minute. Please wait a moment before trying again.",
                        "RPD": "You have reached the maximum number of requests per day. Please try again tomorrow or consider upgrading your plan.",
                        "TPM": "You have reached the maximum number of tokens processed per minute. Please wait a moment before trying again.",
                        "TPD": "You have reached the maximum number of tokens processed per day. Please try again tomorrow or consider upgrading your plan."
                    }
                    return jsonify({"error": error_messages[limit_type]}), 429

            return f(*args, **kwargs)
        return decorated_function
    return decorator
