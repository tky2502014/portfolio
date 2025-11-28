# accounts/views.py
# ----------------------------------------------------------------------------------------------------

from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 

# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    
    # FIX: Use the namespaced URL pattern: 'accounts:signup_success'
    success_url = reverse_lazy('accounts:signup_success')
    
    def form_valid(self, form):
        user = form.save()
        self.object = user
        return super().form_valid(form)
    
class SignUpSuccessView(TemplateView):
    template_name = "accounts/signup_success.html"

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/mypage.html"
    # LoginRequiredMixin automatically redirects unauthenticated users to the login page
    