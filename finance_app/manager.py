# manager.py
# ----------------------------------------------------------------------------------------------------

from .data import Account #data.py
from .db import DatabaseManager #db.py
# ----------------------------------------------------------------------------------------------------

"""
Manages a collection of Account objects.
Acts as the interface between the main application logic and the account data.
"""
class AccountManager:
    def __init__(self):
        self.accounts = {} # Dictionary to store Account objects: {name: Account_Object}.
        self.db_manager = DatabaseManager()
        
        # Load accounts and base currency (Base currency loading is the difficult part).
        loaded_data = self.db_manager.load_all_data()
        # The 'accounts' key holds the dictionary of Account objects.
        self.accounts = loaded_data.get('accounts', {})
        # Load base_currency, default to "JPY"
        self.base_currency = loaded_data.get('base_currency', "JPY") # Load base_currency, default to "JPY".

# ----------------------------------------------------------------------------------------------------
    # This method is called by main.py when the user chooses '0. End'.
    def save_data(self):
        # This method is called by main.py when the user chooses '0. End'.
        self.db_manager.save_all_accounts(self.accounts, self.base_currency)
# ----------------------------------------------------------------------------------------------------
        
    # Close the connection when the object is destroyed.
    def __del__(self):
        if hasattr(self, 'db_manager') and self.db_manager.conn:
            self.db_manager.conn.close()
# ----------------------------------------------------------------------------------------------------
        
    # Creates a new Account object and adds it to the manager.
    def add_account(self, name, initial_balance, currency):
        if name in self.accounts:
            return False # Account already exists.
        # Use the corrected 'initial_balance' variable name.
        self.accounts[name] = Account(name, initial_balance, currency)
        return True
# ----------------------------------------------------------------------------------------------------
    
    # Retrieves an Account object by name. Returns None if not found.
    def get_account(self, name):
        return self.accounts.get(name)
# ----------------------------------------------------------------------------------------------------
    
    # Deletes an Account object by name. Returns True if successful.
    def delete_account(self, name):
        if name in self.accounts:
            # 1. Delete from the database.
            if self.db_manager.delete_account_record(name):
                # 2. Delete from the in-memory dictionary.
                del self.accounts[name]
                # 3. Save the entire state immediately to persist the deletion.
                self.save_data()
                return True
            else:
                # DB deletion failed.
                return False
        return False # Account not found.
# ----------------------------------------------------------------------------------------------------
