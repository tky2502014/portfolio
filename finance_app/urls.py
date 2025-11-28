# finance_app/urls.py
# ----------------------------------------------------------------------------------------------------

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    # paths for 'deposit', 'withdraw', 'transfer', etc. here
    path('setup/', views.initial_setup_view, name='initial_setup'),
]

