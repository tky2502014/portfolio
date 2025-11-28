# finance_app/views.py
# ----------------------------------------------------------------------------------------------------

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .manager import AccountManager
from decimal import Decimal

# Create your views here.
# WARNING: Instantiating AccountManager globally here means it is shared across ALL requests.
# In a production web server, this is dangerous (thread safety issues).
# For this portfolio project using SQLite, it is acceptable for demonstration purposes,
# but ideally, the Manager should be instantiated inside the views.
manager = AccountManager() 

# Helper to get current account safely
def get_current_account_name():
    if manager.accounts:
        return list(manager.accounts.keys())[0]
    return None

# View to handle initial account creation
def initial_setup_view(request):
    # In a real app, this is where you'd handle the POST request 
    # from a form to call manager.add_account()
    context = {
        'message': 'Welcome! Please create your first account.',
        # Add form fields for name, balance, currency here
    }
    return render(request, 'finance_app/initial_setup.html', context)

@login_required # Requires the user to be logged in

# Main financial dashboard view.
def dashboard_view(request):
    # Handle initial setup if no accounts exist
    if not manager.accounts:
        # Redirect to a dedicated setup page (e.g., 'initial_setup')
        return redirect('initial_setup') 
    
    current_account_name = get_current_account_name()

    # Logic to fetch data for the current account
    account_for_display = manager.get_account(current_account_name)
    
    # Calculate total value in base currency (similar to your main.py logic)
    # Note: Ensure 'calculate_total_value' exists in your manager.py
    total_value_base = manager.calculate_total_value() # add this method to manager.py
    
    context = {
        'current_account_name': current_account_name,
        'balance': account_for_display.get_balance(),
        'currency': account_for_display.currency,
        'total_value': total_value_base,
        'base_currency': manager.base_currency,
        'all_accounts': manager.accounts.keys(),
        # Note: Ensure 'get_dashboard_display_data' exists in manager.py
        'dashboard_data': manager.get_dashboard_display_data(), # New helper method
    }
    return render(request, 'finance_app/dashboard.html', context)
