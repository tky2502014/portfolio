# db.py
# ----------------------------------------------------------------------------------------------------

from .data import Account # data.py
from decimal import Decimal # Import Decimal for consistent math throughout
import sqlite3
import json
# ----------------------------------------------------------------------------------------------------

class DatabaseManager:
    def __init__(self, db_name='accounts.db'):
        # 1. Connect to the database file.
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # 2. Ensure the table exists.
        self._create_table()

# ----------------------------------------------------------------------------------------------------
    def _create_table(self):
        # Use an 'IF NOT EXISTS' clause.
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                name TEXT PRIMARY KEY,
                balance TEXT,         -- Stored as string for Decimal precision
                currency TEXT,
                history TEXT          -- Stored as JSON string
            )
        ''')
        
        # Create the SETTINGS table (for global values like base_currency),
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        self.conn.commit()

# ----------------------------------------------------------------------------------------------------
    def save_all_accounts(self, accounts_dict, base_currency):
        # 1. Clear existing data to simplify saving (simulates overwriting).
        self.cursor.execute("DELETE FROM accounts")
        
        # 2. Iterate through accounts_dict to prepare data for insertion.
        for name, account_obj in accounts_dict.items():
            # Serialize the complex fields.
            balance_str = str(account_obj.balance)
            serializable_history = []
            for item in account_obj.history:
                # item is [type, subject, amount (Decimal), currency].
                transaction_type, subject, amount, currency_code = item
                
                # Convert the Decimal amount to a string for JSON serialization.
                serializable_history.append([
                    transaction_type, 
                    subject, 
                    str(amount), # <-- The fix is here!
                    currency_code
                ])
            history_json = json.dumps(serializable_history)
            
            # Use '?' placeholders to prevent SQL injection.
            self.cursor.execute('''
                INSERT INTO accounts (name, balance, currency, history)
                VALUES (?, ?, ?, ?)
            ''', (name, balance_str, account_obj.currency, history_json))
        
        # 3. Commit the changes.
        self.cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", 
                            ('base_currency', base_currency))
        
        self.conn.commit()

# ----------------------------------------------------------------------------------------------------
    def load_all_data(self):
        accounts = {}
        # 1. Fetch all rows.
        self.cursor.execute("SELECT name, balance, currency, history FROM accounts")
        rows = self.cursor.fetchall()
        
        # 2. Deserialize data and re-create Account objects.
        for name, balance_str, currency_code, history_json in rows:
            history_list_str = json.loads(history_json)
            
            history_list_decimal = []
            for item in history_list_str:
                transaction_type, subject, amount_str, currency_code_hist = item
                history_list_decimal.append([
                    transaction_type, 
                    subject, 
                    Decimal(amount_str), # Convert back to Decimal here.
                    currency_code_hist
                ])
                
            account = Account(name, balance_str, currency_code)
            account.history = history_list_decimal
        
            accounts[name] = account
        
         #Load SETTINGS (Base Currency). ---
        base_currency = "JPY" # Default value if no setting is found.
        self.cursor.execute("SELECT value FROM settings WHERE key = 'base_currency'")
        setting_row = self.cursor.fetchone()
        
        if setting_row:
            base_currency = setting_row[0] # The first (and only) column from the row.

        # Return all loaded data as a single dictionary.
        return {
            'accounts': accounts,
            'base_currency': base_currency
        }
# ----------------------------------------------------------------------------------------------------

    # Deletes a specific account record from the database.
    def delete_account_record(self, name):
        try:
            self.cursor.execute("DELETE FROM accounts WHERE name = ?", (name,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error during deletion: {e}")
            return False
# ----------------------------------------------------------------------------------------------------
        