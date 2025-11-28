# transactions.py
# ----------------------------------------------------------------------------------------------------

from abc import ABC, abstractmethod
from decimal import Decimal # Import Decimal for consistent math throughout
# ----------------------------------------------------------------------------------------------------

# --- 1. Abstract Base Class (ABC). ---
class Transaction(ABC):
    """Abstract base class for all financial transactions."""
    
    def __init__(self, account_name, amount, currency, subject):
        self.account_name = account_name
        self.amount = Decimal(amount)
        self.currency = currency
        self.subject = subject

    @abstractmethod
    def execute(self, account_manager):
        """Must be implemented to perform the actual transaction."""
        pass
# ----------------------------------------------------------------------------------------------------

# --- 2. Concrete Subclass (Inherits from Transaction). ---
class DepositTransaction(Transaction):
    """Represents a simple deposit operation."""

    def execute(self, account_manager):
        account = account_manager.get_account(self.account_name)
        if account is None:
            return False, f"Account '{self.account_name}' not found."
            
        # The actual operation uses the Account object's deposit method.
        account.set_deposit(self.subject, self.amount)
        return True, "Deposit successful."
# ----------------------------------------------------------------------------------------------------
        