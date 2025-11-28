# main.py
# ----------------------------------------------------------------------------------------------------

from data import Account #data.py
from db import DatabaseManager #db.py
from manager import AccountManager #manager.py
from transaction import DepositTransaction #transaction.py
from decimal import Decimal # Import Decimal for consistent math throughout
import api #api.py
import currency #currency.py
import matplotlib.pyplot as plt # For graph
# ----------------------------------------------------------------------------------------------------

def main():
    manager = AccountManager()
    current_account = None # Tracks the account currently being viewed/used.
    
    if manager.accounts:
        # Data loaded from DB: Set current account to the first one found.
        current_account = list(manager.accounts.keys())[0]
        print(f"Loaded {len(manager.accounts)} Accounts. Base Currency: {manager.base_currency}")
    else:
        # No data found in DB: Proceed with initial setup prompts.
        print("Initial Setup(No Data Found).")
        # Initaila Base Currency.
        manager.base_currency = input("Set Base Currency(e.g., JPY/USD/...):").upper()
    
        # --- Initial Account Setup. ---
        try:
            # Get details for the first account.
            account_name = (input("Account Name(e.g., SMBC/Mizuho/...):"))
            initial_balance = (input("Initial Balance:"))
            account_currency = input("Account Currency:").upper()
            # Add account and set it as the current account.
            if manager.add_account(account_name, initial_balance, account_currency):
                current_account = account_name
                manager.save_data()
            else:
                print("Error Adding Initial Account.")
                return
        except Exception as e:
            # Catch any exceptions during initial input/setup.
            print(f"Invalid Initial Amount During Setup. Exiting.")
            return
        
    # Ensure we have a current_account before starting the main loop.
    if current_account is None:
        print("FATAL ERROR: Failed To Load or Create An Account. Exiting.")
        return
# ----------------------------------------------------------------------------------------------------
        
    # Main Loop.
    while True:
        # Always retrieve the current account object for display info.
        account_for_display = manager.get_account(current_account)
        print(f'''
              Current Account:{current_account} ({account_for_display.currency}) - Balance: {account_for_display.get_balance()} {account_for_display.currency}
              1. Dashboard           2. Transfer
              3. Deposit             4. Withdraw
              5. Account Details     6. Switch Account
              7. Add Account         8. Delete Account
              0. End''')
        choice = (input("\nchoose 0-8 for above actions:"))
        print("---------------------------------------------------")
# ----------------------------------------------------------------------------------------------------
        
        if choice == "1":
            print("Dashboard")
            
            while True:
                # Prompt for changing currency.
                print(f"Current Base Currency: {manager.base_currency}")
                change_currency = input("Enter New Base Currency To Change (or 'Enter' To Continue):").upper()
                # Check if the new currency is entered.
                if change_currency == "":
                    break
                if len(change_currency) != 3 or not change_currency.isalpha():
                    print(f"Error: '{change_currency}' Is Not Valid Currency.")
                    continue # Go back to the start of the while loop.
                manager.base_currency = change_currency
                print(f"Base Currency Updated To: {manager.base_currency}")
                break
                
            # setting total as 0.
            total_value = Decimal(0)
            base = manager.base_currency
            converter = currency.Converter()
            print(f"Base Currency: {base}")
            # print("-" * 30)
            
            for name, account_obj in manager.accounts.items():
                balance = account_obj.get_balance()
                source_curr = account_obj.currency
                converted_balance = balance
                
                try:
                    if source_curr != base:
                        # Use the Converter to get value in base currency.
                        converted_balance = converter.get_converted_amount(balance, source_curr, base)
                        if converted_balance is None:
                            print(f"⚠️ Conversion Failed For {name} ({source_curr}). Skipping.")
                            continue # Skip this account if API fails.
                        print(f"{name:<10}: {balance:<10} {source_curr} -> {converted_balance.quantize(Decimal('.01'))} {base}")
                    else:
                        print(f"{name:<10}: {balance:<10} {source_curr}")
                    total_value += converted_balance
                except Exception as e:
                    print(f"❌ Critical Error Processing Account {name}: {e}. Skipping.")
                    continue
            
            #print("-" * 30)
            # Display total, rounded to 2 decimal places.
            print(f"TOTAL VALUE: {total_value.quantize(Decimal('.01'))} {base}")
# ----------------------------------------------------------------------------------------------------
            
        elif choice == "2":
            print("Transfering")
            
            try:
                # 0. Get list of all accounts.
                available_accounts = list(manager.accounts.keys())
                # Filter out the current account.
                switch_options = [name for name in available_accounts if name != current_account]
                if not switch_options:
                    # If only the current account exists, or no accounts exist.
                    print("No Account To Switch.")
                    continue 
                print("Available Account:")
                # Iterate only over the filtered list.
                for i, name in enumerate(switch_options):
                    account_obj = manager.get_account(name)
                    print(f"{i+1}. {name} ({account_obj.currency}) - Balance: {account_obj.get_balance()} {account_obj.currency}")
                
                # 1. Setup Accounts and check validity.
                source_account = manager.get_account(current_account)
                destination_name = input("Transfer To Account Name (or 'C' To Cancel):")
                if destination_name.upper() == 'C':
                    print("Transfer Canceled.")
                    continue
                destination_account = manager.get_account(destination_name)
                
                if destination_account is None:
                    print(f"Error: Account '{destination_name}' Not Found.")
                    continue
                
                # 2. Get Amount.
                amount_str = input(f"Amount To Transfer (In {source_account.currency}):")
                transfer_amount = Decimal(amount_str) # Convert to Decimal for math.
                source_currency = source_account.currency
                destination_currency = destination_account.currency
                
                # 3. Handle Currency Conversion.
                converted_amount = transfer_amount
                if source_currency != destination_currency:
                    converter = currency.Converter()
                    # Calls the converter to get the final amount.
                    converted_amount = converter.get_converted_amount(transfer_amount, source_currency, destination_currency)
                    if converted_amount is None:
                        print("Error: Currency Conversion Failed. Transfer Canceled.")
                        continue # Conversion failed, stop transfer before withdrawal.
                
                # 4. Attempt Withdrawal from Source (after conversion confirmation).
                # The transfer amount is always in the SOURCE currency.
                if not source_account.set_withdraw(f"Transfer To {destination_name} ({destination_currency})", transfer_amount):
                    print("Error: Insufficient Funds. Transfer Cancelled.")
                    continue
                
                # 5. Perform Deposit to Destination.
                # The deposit amount is the CONVERTED amount in the destination currency.
                destination_account.set_deposit(f"Transfer From {current_account} ({source_currency})", converted_amount)
                
                # 6. Success Output.
                print(f"Transfer Success! {transfer_amount} {source_currency} Transferred.")
                print(f"Destination Received {converted_amount.quantize(Decimal('.01'))} {destination_currency}.") 
                
            except Exception as e:
                # Catch exceptions like invalid amount input (not convertible to Decimal).
                print(f"Error During Transfer: Check Input.")
                # print(f"Detailed Error: {e}") # Uncomment for debugging.
# ----------------------------------------------------------------------------------------------------
            
        elif choice == "3":
            print("Depositing")
            try:
                subject = input("Subject:")
                amount = input("Amount:") # Read as string, Decimal conversion handled in data.py.
                account_obj = manager.get_account(current_account)
                deposit = DepositTransaction(current_account, amount, account_obj.currency, subject)
                success, message = deposit.execute(manager) # manager is the AccountManager instance.
                print(message)
                print("Deposit Complete.")
            except Exception:
                print("Invalid Amount. Enter Number.")
# ----------------------------------------------------------------------------------------------------
            
        elif choice == "4":
            print("Withdrawing")
            try:
                subject = input("Subject:")
                amount = input("Amount:") # Read as string, Decimal conversion handled in data.py.
                account_obj = manager.get_account(current_account)
                # set_withdraw returns True/False based on available funds.
                if account_obj.set_withdraw(subject, amount):
                    print("Withdraw Completed.")
                else:
                    print("Insufficient Funds. Withdraw Failed.")
            except Exception:
                print("Invalid Amount. Enter Number.")
# ----------------------------------------------------------------------------------------------------
            
        elif choice == "5":
            print("Account Details")
            account_obj = manager.get_account(current_account)
            print(f"Current Balance:{account_obj.get_balance()}{account_obj.currency}")
            history = account_obj.get_historys()
            if not history:
                print("No History Found.")
            else:
                print("--- History ---")
                
                # 1. Calculate the starting balance before any transactions in the history list.
                # This is done by taking the current balance and subtracting the net amount of all transactions.
                current_total_balance = account_obj.get_balance()
                net_transaction_sum = sum(
                    amount if type == "deposit" else -amount
                    for type, _, amount, _ in history
                )
                initial_balance = current_total_balance - net_transaction_sum
                # Initialize plot data arrays. START with the calculated initial balance.
                running_balance = initial_balance
                balances = [running_balance] # Set the first point to the actual initial balance.
                transaction_labels = ["Initial"] 
                running_balance = initial_balance 
                
                # Unpack the enumerate result into 'i' (the index) and 'record' (the history item).
                for i, record in enumerate(history):
                    # Now, unpack the 'record' (which is the list/tuple of 4 elements).
                    transaction_type, subject, amount, curr = record
                    
                    # Calculate new balance.
                    if transaction_type == "deposit":
                        running_balance += amount
                    elif transaction_type == "withdraw":
                        running_balance -= amount
                        
                    balances.append(running_balance)
                    
                    # Create a descriptive label for the X-axis.
                    label = f"{i+1}: {transaction_type.capitalize()} ({subject})"
                    transaction_labels.append(label)
                    
                    # Using string formatting for alignment (f-string justification: :<8).
                    print(f"{transaction_type:<10} | Subject:{subject:<15} | Amount:{amount} {curr}")
                    
                # Convert Decimal balances to float for Matplotlib.
                plot_balances = [float(b) for b in balances]
                
                plt.figure(figsize=(10, 6)) # Set graph size.
                plt.plot(transaction_labels, plot_balances, marker='o', linestyle='-', color='skyblue')
                
                plt.title(f'Balance History for {current_account} ({account_obj.currency})')
                plt.xlabel('Transaction Number and Subject')
                plt.ylabel(f'Balance ({account_obj.currency})')
                
                # Rotate X-axis labels for better visibility if many transactions exist.
                plt.xticks(rotation=45, ha='right')
                plt.grid(True)
                plt.tight_layout() # Adjust layout to prevent labels from being cut off.
                
                plt.show() # Display the graph.
# ----------------------------------------------------------------------------------------------------
                
        elif choice == "6":
            print("Switching Account")
            
            # Get list of all accounts.
            available_accounts = list(manager.accounts.keys())
            # Filter out the current account.
            switch_options = [name for name in available_accounts if name != current_account]
            if not switch_options:
                # If only the current account exists, or no accounts exist.
                print("No Account To Switch.")
                continue 
            print("Available Account:")
            # Iterate only over the filtered list.
            for i, name in enumerate(switch_options):
                account_obj = manager.get_account(name)
                print(f"{i+1}. {name} ({account_obj.currency}) - Balance: {account_obj.get_balance()} {account_obj.currency}")
                
            new_account_name = input("Enter Account To Switch To (or 'C' To Cancel):")
            if new_account_name.upper() == 'C':
                print("Switching Canceled.")
                continue
            
            # Change the current_account variable if the name is valid.
            if new_account_name in manager.accounts:
                # global current_account # This line is only needed if 'current_account' was not initialized in main.
                current_account = new_account_name
                print(f"Account Switched to {current_account}.")
            else:
                print(f"Error. Account '{new_account_name}' Not Found.")
# ----------------------------------------------------------------------------------------------------
            
        elif choice == "7":
            print("Adding Account")
            name = input("New Account Name (or 'C' To Cancel):")
            if name.upper() == 'C':
                print("Adding Canceled.")
                continue 
            try:
                balance = input("Initial Balance:")
                currency_code = input("Currency:").upper()
                if manager.add_account(name, balance, currency_code):
                    print(f"Account '{name}' Created.")
                else:
                    print("Account Already Exists.")
            except Exception:
                print("Invalid Amount. Enter Number.")
# ----------------------------------------------------------------------------------------------------

        elif choice == "8":
            print("Deleting Account")
            
            # 1. Ask for confirmation.
            conformation = input(f"Delete Current Account '{current_account}'? ('C' To Confirm):").upper()
            if conformation != "C":
                print("Account Deletion Cancelled.")
                continue
            
            # 2. Check if this is the only remaining account.
            if len(manager.accounts) <= 1:
                print("Deletion Failed: Cannot Delete Last Remaining Account.")
                print("Create Another Account First.")
                continue
            
            # 3. Call manager to delete.
            if manager.delete_account(current_account):
                print(f"Account '{current_account}' Successfully Deleted.")
                
                # 4. CRITICAL: Switch to a new current account.
                # Get the remaining account keys and set the first one as current.
                remaining_accounts = list(manager.accounts.keys())
                if remaining_accounts:
                    current_account = remaining_accounts[0]
                    print(f"Switched Current Account To: {current_account}")
                else:
                    print("No Account Remaining. Exiting Program.")
                    break
            else:
                # This case should be prevented by step 2, but is a safe fallback.
                print(f"Error: Account '{current_account}' Cound Not Be Deleted.")
            
# ----------------------------------------------------------------------------------------------------
            
        elif choice == "0":
            print("Saving Data.")
            manager.save_data() # <-- ADDED DATABASE SAVE CALL.
            print("Ending")
            break
# ----------------------------------------------------------------------------------------------------
            
        else:
            print("Invalid Input.  Choose 0-6.")
# ----------------------------------------------------------------------------------------------------
        
if __name__ == "__main__":
    main()
# ----------------------------------------------------------------------------------------------------
    