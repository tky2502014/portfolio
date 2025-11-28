# PortfolioProject/urls.py
# ----------------------------------------------------------------------------------------------------

"""
URL configuration for PortfolioProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Portfolio App (Root URL)
    path('', include(('portfolio_app.urls', 'portfolio_app'), namespace='portfolio_app')),
    
    # Finance App
    path('finance/', include('finance_app.urls')), 
    
    # Accounts App: Includes Signup, Login, Logout, and all Password Reset views.
    # This inclusion defines the URL names that LOGIN_URL and other redirects use.
    path('', include('accounts.urls', namespace='accounts')), 
]
