from flask import request, jsonify
from functools import wraps
import time
from enum import Enum


class UserTier(Enum):
    FREE = "Free"
    TIER_1 = "Tier-1"
    TIER_2 = "Tier-2"
    TIER_3 = "Tier-3"


# Example rate limit configuration
RATE_LIMITS = {
    UserTier.FREE: {"RPM": 3, "RPD": 200, "TPM": 40000, "TPD": 1000000},
    UserTier.TIER_1: {"RPM": 500, "RPD": 10000, "TPM": 200000, "TPD": 5000000},
    UserTier.TIER_2: {"RPM": 5000, "RPD": 100000, "TPM": 2000000, "TPD": 50000000},
    UserTier.TIER_3: {"RPM": 50000, "RPD": 1000000, "TPM": 20000000, "TPD": 500000000},
}

# In-memory store for rate limit tracking (consider using a persistent store like Redis)
rate_limit_store = {}


def get_user_tier(user_id):
    # Placeholder function to get user tier
    # Replace with actual logic to fetch user tier from database
    return UserTier.FREE


def check_rate_limit(user_id, limit_type, increment_count: int):
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


def request_rate_limit():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = kwargs.get("user_id")
            if not user_id:
                return jsonify({"error": "User ID is required"}), 400

            for limit_type in ["RPM", "RPD", "TPM", "TPD"]:
                if limit_type.startswith("R"):
                    increment_value = 1
                else:
                    increment_value = 0
                if not check_rate_limit(user_id, limit_type, increment_count=increment_value):
                    return jsonify({"error": f"Rate limit exceeded for {limit_type}. Please try again later."}), 429

            return f(*args, **kwargs)
        return decorated_function
    return decorator
