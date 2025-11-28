# currency.py
# ----------------------------------------------------------------------------------------------------

from decimal import Decimal # Import Decimal for consistent math throughout
import api #api.py
# ----------------------------------------------------------------------------------------------------

# Orchestrates currency conversion, primarily by calling methods in the api module.
class Converter:
    # Determines the conversion route (direct conversion or rate multiplication).
    def get_converted_amount(self, amount, from_currency, to_currency):
        amount = Decimal(amount) # Ensure input amount is Decimal.
        
        if from_currency == to_currency:
            return amount # No conversion needed.
        
        # 1. Attempt direct conversion via API endpoint (more accurate/easier).
        converted_amount = api.convert(amount, from_currency, to_currency)
        
        if converted_amount is not None:
            return converted_amount
        else:
            print("Falling Back To Manual Rate Calculation...")
            
        # 2. Fallback: Get rate and calculate manually.
        rate = api.get_exchange_rate(from_currency, to_currency)
        
        if rate is not None:
            return amount * rate
        else:
            print(f"Failed To Get Rate For {from_currency} To {to_currency}. Transfer Cannot Be Completed.")
            return None # Critical failure.
# ----------------------------------------------------------------------------------------------------
        