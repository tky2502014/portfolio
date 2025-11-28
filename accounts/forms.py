# accounts/forms.py
# ----------------------------------------------------------------------------------------------------

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for creating a new user, based on the standard Django UserCreationForm.
    It links to the CustomUser model.
    """
    class Meta:
        model = CustomUser
        # UserCreationForm implicitly handles password1 and password2
        fields = ('username', 'email')
