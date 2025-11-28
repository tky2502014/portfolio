# portfolio_app/views.py
# ----------------------------------------------------------------------------------------------------

from django.shortcuts import render

from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage

# Create your views here.
def home_view(request):
    context = {
        'my_name': 'Your Name',
        'tagline': 'Python/Django Developer & System Engineer',
        'projects': [
            {'name': 'Personal Finance Tracker (This App)', 'link': '/finance/'},
            {'name': 'Another Project(coming soon)', 'link': '#'}
        ],
        'skills': ['Python', 'Django', 'SQLite', 'Web Development', 'Data Persistence'],
    }
    return render(request, 'portfolio_app/home.html', context)

class ContactView(FormView):
    template_name ='portfolio_app/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('portfolio_app:contact')
    
    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        
        subject = 'お問い合わせ: {}'.format(title)
        message = \
            '送信者名: {0}\nメールアドレス:{1}\n タイトル:{2}\n メッセージ:\{3}'\
                .format(name, email, title, message)
        from_email = 'admin@example.com'
        to_list = ['admin@example.com']
        message = EmailMessage(subject=subject, body=message, from_email=from_email, to=to_list)
        message.send()
        messages.success(self.request, 'お問い合わせは正常に送信されました。')
        return super().form_valid(form)