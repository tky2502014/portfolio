# api.py
# ----------------------------------------------------------------------------------------------------

from decimal import Decimal # Import Decimal for consistent math throughout
from dotenv import load_dotenv # Import Loader
import os
import requests
# ----------------------------------------------------------------------------------------------------

# Load the environment variables from the .env file.
load_dotenv()

# Read the API key from the environment variable, which load_dotenv() just loaded.
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")

if not API_KEY:
    raise ValueError("API Key Not Found.")

# The base URL includes the API key, as required by this service.
BASE_URL =  f"https://v6.exchangerate-api.com/v6/{API_KEY}"

RATE_CACHE = {} # Cache to store fetched rates: {'FROM_TO': Decimal_Rate}.
# ----------------------------------------------------------------------------------------------------

"""
Fetches the latest exchange rate (1 FROM_CURRENCY = X TO_CURRENCY) from the API.
Uses caching to reduce API calls for repeated lookups.
"""
def get_exchange_rate(from_currency, to_currency):
    cache_key = f"{from_currency}_{to_currency}"
    
    if cache_key in RATE_CACHE:
        return RATE_CACHE[cache_key]
    
    # Endpoint to get all latest rates, relative to the 'from_currency'.
    endpoint = f"{BASE_URL}/latest/{from_currency}"
    
    try:
        response = requests.get(endpoint)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx).
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error Fetching Exchange Rate From API:{e}")
        return None
    
    # Extract the conversion rates dictionary.
    rates = data.get("conversion_rates")
    
    if not rates or to_currency not in rates:
        # This handles cases where the target currency code is invalid.
        print(f"Error:Rate For {to_currency} Not Found.")
        
    # Get the rate and convert it to Decimal for safe math, casting via str() first.
    rate = Decimal(str(rates[to_currency]))
    
    RATE_CACHE[cache_key] = rate # Store the rate in the cache.
    return rate
# ----------------------------------------------------------------------------------------------------

"""
 Uses the API's 'pair' endpoint for direct conversion calculation.
This is generally more reliable than fetching the rate and multiplying locally.
"""
def convert(amount, from_currency, to_currency):
    # Endpoint format: /pair/{from_code}/{to_code}/{amount}.
    endpoint = f"{BASE_URL}/pair/{from_currency}/{to_currency}/{amount}"
    
    try:
        response = requests.get(endpoint)
        response.raise_for_status() # Check for errors.
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error Converting Currency:{e}")
        return None
    
    # Check API response status
    if data.get("result") == "success":
        # Convert the resulting amount to Decimal.
        return Decimal(str(data.get("conversion_result")))
    
    # Return None if API call was successful but the conversion result field was missing.
    return None
# ----------------------------------------------------------------------------------------------------
