# data.py
# ----------------------------------------------------------------------------------------------------

from decimal import Decimal # Import Decimal for consistent math throughout
import copy
# ----------------------------------------------------------------------------------------------------

"""
Represents a single bank account, managing its balance, currency, and history.
Uses Decimal for high-precision financial calculations.
"""
class Account:
    def __init__(self, name, balance, currency):
        self.name = name
        # Convert initial balance to Decimal for safe arithmetic.
        self.balance = Decimal(balance)
        self.currency = currency
        self.history = [] # Stores list of transactions: [type, subject, amount, currency].
# ----------------------------------------------------------------------------------------------------
        
    # Attempts to deduct funds. Returns False if insufficient balance.
    def set_withdraw(self, subject, amount):
        amount = Decimal(amount)
        # Check for insufficient funds.
        if self.balance - amount < 0:
            return False
        self.balance -= amount
        # Record the transaction.
        self.history.append(["withdraw", subject, amount, self.currency])
        return True # withdraw complete.
# ----------------------------------------------------------------------------------------------------
    
    # Adds funds to the balance and records the transaction.
    def set_deposit(self, subject, amount):
        amount = Decimal(amount) # Ensure 'amount' is Decimal.
        self.balance += amount
        # Record the transaction.
        self.history.append(["deposit", subject, amount, self.currency])
# ----------------------------------------------------------------------------------------------------
        
    def get_historys(self):
         # Returns a copy of the list to prevent passing by reference.
        return copy.deepcopy(self.history)
# ----------------------------------------------------------------------------------------------------
    
    # Returns the current balance (Decimal).
    def get_balance(self):
        return self.balance
# ----------------------------------------------------------------------------------------------------
    
    def __repr__(self):
        return f"<Account name='{self.name}', balance={self.balance}, currency='{self.currency}'>"
# ----------------------------------------------------------------------------------------------------
