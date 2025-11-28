# accounts/urls.py
# ----------------------------------------------------------------------------------------------------

from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('signup/',
         views.SignUpView.as_view(),
         name='signup'),
         
    path('signup_success/',
         views.SignUpSuccessView.as_view(),
         name='signup_success'),
    
    path('login/',
         auth_views.LoginView.as_view(template_name='accounts/login.html'),
         name='login'),
    
    path('logout/',
         auth_views.LogoutView.as_view(template_name='accounts/logout.html'),
         name='logout'),
    
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
    
    # --- Password Change (Missing Views added here) ---
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='accounts/password_change_form.html',success_url=reverse_lazy('accounts:password_change_done')),
         name='password_change'),
         
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
    
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html",success_url=reverse_lazy('accounts:password_reset_done')),
         name='password_reset'),
         
     # --- Password Reset Paths ---
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
         name='password_reset_done'),
         
    # CRITICAL: Added trailing slash to match expected path for link clicking
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
         name='password_reset_confirm'),
         
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
         name='password_reset_complete'),
]